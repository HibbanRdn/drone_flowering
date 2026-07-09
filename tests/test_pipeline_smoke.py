from __future__ import annotations

import json
import shutil
import sys
import csv
import os
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from drone_plot_gap.app import run_pipeline
from drone_plot_gap.schema import SCHEMA_VERSION


def main() -> None:
    # SMOKE TEST: MEMBUAT VIDEO SINTETIS, MENJALANKAN PIPELINE, MEMVERIFIKASI SEMUA OUTPUT DAN FIELD WAJIB
    import cv2
    import numpy as np

    workdir = Path(".tmp_smoke")
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir()

    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
        cli_result = subprocess.run(
            [sys.executable, "-m", "drone_plot_gap", "--help"],
            cwd=Path("."),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        assert cli_result.returncode == 0
        assert "--config" in cli_result.stdout

        video_path = workdir / "input.avi"
        writer = cv2.VideoWriter(
            str(video_path),
            cv2.VideoWriter_fourcc(*"MJPG"),
            5.0,
            (64, 48),
        )
        for i in range(12):
            writer.write(np.full((48, 64, 3), i * 10, dtype=np.uint8))
        writer.release()

        config_path = workdir / "offline.json"
        config_path.write_text(
            json.dumps(
                {
                    "input": {"video_path": str(video_path)},
                    "output": {"root_dir": str(workdir / "outputs" / "runs")},
                    "experiment": {
                        "mission_id": "MISSING_PLANT_TEST_001",
                        "block_id": "PINEAPPLE_BLOCK_001",
                        "crop_type": "pineapple",
                        "target_case": "missing_plant",
                        "flight_pattern": "top_view_grid",
                        "camera_view": "nadir",
                        "altitude_m": 35.0,
                        "gimbal_pitch_deg": -90.0,
                        "speed_mps": 2.0,
                    },
                    "sampling": {"every_n_frames": 5},
                    "dummy_inference": {
                        "label": "empty_plot_candidate",
                        "confidence": 0.72,
                    },
                    "mock_telemetry": {
                        "lat": -5.123456,
                        "lng": 105.123456,
                        "altitude_m": 35.0,
                        "heading_deg": 92.5,
                        "gimbal_pitch_deg": -90.0,
                        "speed_mps": 4.2,
                    },
                }
            ),
            encoding="utf-8",
        )

        result = run_pipeline(config_path)
        assert result.run_dir.exists()
        assert result.frames_processed == 3
        assert result.detections_written == 3

        jsonl_path = result.run_dir / "detections.jsonl"
        csv_path = result.run_dir / "detections.csv"
        metadata_path = result.run_dir / "run_metadata.json"
        manifest_path = result.run_dir / "run_manifest.json"
        summary_path = result.run_dir / "run_summary.json"
        assert jsonl_path.exists()
        assert csv_path.exists()
        assert metadata_path.exists()
        assert manifest_path.exists()
        assert summary_path.exists()

        records = [
            json.loads(line)
            for line in jsonl_path.read_text(encoding="utf-8").splitlines()
        ]
        assert records
        assert {record["run_id"] for record in records} == {result.run_id}
        record = records[0]
        required = {
            "schema_version",
            "run_id",
            "source_video",
            "frame_index",
            "timestamp_ms",
            "timestamp_iso",
            "detection_id",
            "label",
            "confidence",
            "bbox_xyxy",
            "bbox_format",
            "telemetry",
        }
        telemetry_required = (
            "lat",
            "lng",
            "altitude_m",
            "heading_deg",
            "gimbal_pitch_deg",
            "speed_mps",
        )
        for record in records:
            assert required <= record.keys()
            assert record["schema_version"] == SCHEMA_VERSION
            assert record["schema_version"] == "drone-plot-gap-detection.v1"
            assert record["run_id"] == result.run_id
            assert record["label"] == "empty_plot_candidate"
            assert record["model_name"] == "dummy_plot_gap_baseline"
            assert record["bbox_format"] == "xyxy"
            for key in telemetry_required:
                assert key in record["telemetry"]

        with csv_path.open(newline="", encoding="utf-8") as csv_file:
            rows = list(csv.DictReader(csv_file))
        assert rows
        assert {row["run_id"] for row in rows} == {result.run_id}
        assert {row["label"] for row in rows} == {"empty_plot_candidate"}
        for column in (
            "telemetry_lat",
            "telemetry_lng",
            "telemetry_altitude_m",
            "telemetry_heading_deg",
            "telemetry_gimbal_pitch_deg",
            "telemetry_speed_mps",
        ):
            assert column in rows[0]

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        assert manifest["experiment"]["mission_id"] == "MISSING_PLANT_TEST_001"
        assert manifest["experiment"]["target_case"] == "missing_plant"
        assert manifest["experiment"]["camera_view"] == "nadir"
        assert manifest["summary"]["frames_processed"] == 3
        assert manifest["summary"]["detections_written"] == 3
        assert manifest["summary"]["overlay_enabled"] is False
        assert summary["mission_id"] == "MISSING_PLANT_TEST_001"
        assert summary["block_id"] == "PINEAPPLE_BLOCK_001"
        assert summary["target_case"] == "missing_plant"
        assert summary["frames_processed"] == 3
        assert summary["detections_written"] == 3
        assert summary["labels_count"] == {"empty_plot_candidate": 3}
        assert summary["confidence_min"] == 0.72
        assert summary["confidence_max"] == 0.72
        assert summary["confidence_avg"] == 0.72
        assert summary["overlay_enabled"] is False

        no_experiment_config_path = workdir / "offline_no_experiment.json"
        no_experiment_config = json.loads(config_path.read_text(encoding="utf-8"))
        no_experiment_config.pop("experiment")
        no_experiment_config_path.write_text(
            json.dumps(no_experiment_config), encoding="utf-8"
        )

        second_result = run_pipeline(no_experiment_config_path)
        assert second_result.run_dir.exists()
        assert second_result.run_dir != result.run_dir
        assert not (second_result.run_dir / "overlay.mp4").exists()
        assert not (second_result.run_dir / "frames").exists()
        second_manifest = json.loads(
            (second_result.run_dir / "run_manifest.json").read_text(encoding="utf-8")
        )
        assert second_manifest["experiment"] == {}

        overlay_config_path = workdir / "offline_overlay.json"
        overlay_config = json.loads(config_path.read_text(encoding="utf-8"))
        overlay_config["overlay"] = {
            "enabled": True,
            "output_video": False,
            "output_frames": True,
            "max_frames": 2,
        }
        overlay_config_path.write_text(json.dumps(overlay_config), encoding="utf-8")

        overlay_result = run_pipeline(overlay_config_path)
        frame_files = sorted((overlay_result.run_dir / "frames").glob("*.jpg"))
        assert len(frame_files) == 2
        assert all(path.stat().st_size > 0 for path in frame_files)
        assert (overlay_result.run_dir / "detections.jsonl").exists()
        assert (overlay_result.run_dir / "detections.csv").exists()
        overlay_manifest = json.loads(
            (overlay_result.run_dir / "run_manifest.json").read_text(encoding="utf-8")
        )
        assert overlay_manifest["summary"]["overlay_enabled"] is True
        assert overlay_manifest["summary"]["overlay_frames_written"] == 2
        assert overlay_manifest["outputs"]["overlay_frames_dir"].endswith("frames")
        assert "overlay_video" not in overlay_manifest["outputs"]
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
    print("smoke test ok")
