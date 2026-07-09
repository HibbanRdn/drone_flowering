from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from . import __version__
from .config import ConfigLoader
from .frame_source import VideoFileFrameSource
from .inference import DummyInferenceEngine
from .overlay import OpenCvOverlayRenderer
from .schema import SCHEMA_VERSION
from .telemetry import MockTelemetryProvider
from .writer import JsonlCsvResultWriter


@dataclass(frozen=True)
class PipelineResult:
    run_id: str
    run_dir: Path
    frames_processed: int
    detections_written: int


def run_pipeline(config_path: str | Path) -> PipelineResult:
    # MEMBACA CONFIG, INISIALISASI SEMUA MODUL, MENJALANKAN LOOP FRAME, DAN MENULIS SEMUA OUTPUT
    config = ConfigLoader.load(config_path)
    run_started_at = datetime.now().astimezone()
    run_id = run_started_at.strftime("%Y%m%d-%H%M%S-%f")

    frame_source = VideoFileFrameSource(config.input_video, config.sampling_every_n_frames)
    video_metadata = frame_source.video_metadata()
    inference = DummyInferenceEngine(config.dummy_label, config.dummy_confidence)
    telemetry_provider = MockTelemetryProvider(config.mock_telemetry)
    writer = JsonlCsvResultWriter(config.output_root / run_id)
    overlay = None

    detections_written = 0
    frames_processed = 0
    labels_count: dict[str, int] = {}
    confidences: list[float] = []
    timestamps_ms: list[float] = []
    telemetry_summary: dict[str, object] = {}
    warnings: list[str] = []

    try:
        overlay = OpenCvOverlayRenderer(
            writer.run_dir,
            config.overlay,
            max(
                1.0,
                float(video_metadata.get("fps") or 0.0)
                / config.sampling_every_n_frames,
            ),
            int(video_metadata.get("width_px") or 0),
            int(video_metadata.get("height_px") or 0),
        )
        writer.write_run_metadata(
            {
                "schema_version": SCHEMA_VERSION,
                "run_id": run_id,
                "created_at_iso": run_started_at.isoformat(timespec="milliseconds"),
                "config_path": str(config.config_path),
                "app_version": __version__,
                "input_video": video_metadata,
                "config_snapshot": config.raw,
            }
        )

        for sample_index, frame_record in enumerate(frame_source.frames()):
            frames_processed += 1
            timestamp_iso = (
                run_started_at + timedelta(milliseconds=frame_record.timestamp_ms)
            ).isoformat(timespec="milliseconds")
            telemetry = telemetry_provider.get(frame_record.timestamp_ms)

            detection_records = []
            for detection in inference.detect(frame_record.frame, frame_record.frame_index):
                detections_written += 1
                record = {
                    "schema_version": SCHEMA_VERSION,
                    "run_id": run_id,
                    "source_video": str(config.input_video),
                    "frame_index": frame_record.frame_index,
                    "timestamp_ms": frame_record.timestamp_ms,
                    "timestamp_iso": timestamp_iso,
                    "sample_index": sample_index,
                    "detection_id": f"{run_id}-{detections_written:06d}",
                    **detection,
                    "telemetry": telemetry,
                }
                detection_records.append(record)
                writer.write_detection(record)
                label = str(record["label"])
                labels_count[label] = labels_count.get(label, 0) + 1
                confidences.append(float(record["confidence"]))
                timestamps_ms.append(float(record["timestamp_ms"]))
                telemetry_summary = {
                    "altitude_m": telemetry["altitude_m"],
                    "gimbal_pitch_deg": telemetry["gimbal_pitch_deg"],
                    "speed_mps": telemetry["speed_mps"],
                }
            overlay.render(
                frame_record.frame,
                frame_record,
                detection_records,
                timestamp_iso,
                telemetry,
            )

        if frames_processed == 0:
            warnings.append("Tidak ada frame yang diproses")

        overlay.close()
        finished_at = datetime.now().astimezone()
        warnings.extend(overlay.warnings)
        outputs = {
            "detections_jsonl": str(writer.run_dir / "detections.jsonl"),
            "detections_csv": str(writer.run_dir / "detections.csv"),
        }
        if overlay.overlay_video_output:
            outputs["overlay_video"] = overlay.overlay_video_output
        if overlay.overlay_frames_output:
            outputs["overlay_frames_dir"] = overlay.overlay_frames_output

        duration_seconds = round((finished_at - run_started_at).total_seconds(), 3)
        summary = {
            "run_id": run_id,
            "mission_id": config.experiment.get("mission_id"),
            "block_id": config.experiment.get("block_id"),
            "target_case": config.experiment.get("target_case"),
            "source_video": str(config.input_video),
            "frames_processed": frames_processed,
            "detections_written": detections_written,
            "labels_count": labels_count,
            "confidence_min": min(confidences) if confidences else None,
            "confidence_max": max(confidences) if confidences else None,
            "confidence_avg": round(sum(confidences) / len(confidences), 6)
            if confidences
            else None,
            "timestamp_ms_min": min(timestamps_ms) if timestamps_ms else None,
            "timestamp_ms_max": max(timestamps_ms) if timestamps_ms else None,
            "telemetry": telemetry_summary,
            "overlay_enabled": config.overlay.enabled,
            "output_files": outputs,
        }
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "created_at": run_started_at.isoformat(timespec="milliseconds"),
            "source_video": str(config.input_video),
            "config_path": str(config.config_path),
            "config_snapshot": config.raw,
            "experiment": config.experiment,
            "outputs": outputs,
            "summary": {
                "frames_processed": frames_processed,
                "detections_written": detections_written,
                "overlay_enabled": config.overlay.enabled,
                "overlay_frames_written": overlay.frames_written,
                "started_at": run_started_at.isoformat(timespec="milliseconds"),
                "finished_at": finished_at.isoformat(timespec="milliseconds"),
                "duration_seconds": duration_seconds,
            },
            "warnings": warnings,
        }
        writer.write_json("run_manifest.json", manifest)
        writer.write_json("run_summary.json", summary)
    finally:
        if overlay is not None:
            overlay.close()
        writer.close()

    return PipelineResult(run_id, writer.run_dir, frames_processed, detections_written)
