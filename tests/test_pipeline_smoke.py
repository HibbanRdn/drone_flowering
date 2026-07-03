from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from drone_flowering.app import run_pipeline


def main() -> None:
    import cv2
    import numpy as np

    workdir = Path(".tmp_smoke")
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir()

    try:
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
                    "sampling": {"every_n_frames": 5},
                    "dummy_inference": {
                        "label": "flowering_candidate",
                        "confidence": 0.72,
                    },
                    "mock_telemetry": {
                        "lat": -5.123456,
                        "lng": 105.123456,
                        "altitude_m": 35.0,
                        "heading_deg": 92.5,
                        "gimbal_pitch_deg": -60.0,
                        "speed_mps": 4.2,
                    },
                }
            ),
            encoding="utf-8",
        )

        result = run_pipeline(config_path)
        assert result.frames_processed == 3
        assert result.detections_written == 3

        jsonl_path = result.run_dir / "detections.jsonl"
        csv_path = result.run_dir / "detections.csv"
        assert jsonl_path.exists()
        assert csv_path.exists()

        record = json.loads(jsonl_path.read_text(encoding="utf-8").splitlines()[0])
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
        assert required <= record.keys()
        for key in (
            "lat",
            "lng",
            "altitude_m",
            "heading_deg",
            "gimbal_pitch_deg",
            "speed_mps",
        ):
            assert key in record["telemetry"]
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
    print("smoke test ok")
