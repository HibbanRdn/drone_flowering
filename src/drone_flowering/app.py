from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from . import __version__
from .config import ConfigLoader
from .frame_source import VideoFileFrameSource
from .inference import DummyInferenceEngine
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
    config = ConfigLoader.load(config_path)
    run_started_at = datetime.now().astimezone()
    run_id = run_started_at.strftime("%Y%m%d-%H%M%S-%f")

    frame_source = VideoFileFrameSource(config.input_video, config.sampling_every_n_frames)
    video_metadata = frame_source.video_metadata()
    inference = DummyInferenceEngine(config.dummy_label, config.dummy_confidence)
    telemetry_provider = MockTelemetryProvider(config.mock_telemetry)
    writer = JsonlCsvResultWriter(config.output_root / run_id)

    detections_written = 0
    frames_processed = 0

    try:
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

            for detection in inference.detect(frame_record.frame, frame_record.frame_index):
                detections_written += 1
                writer.write_detection(
                    {
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
                )
    finally:
        writer.close()

    return PipelineResult(run_id, writer.run_dir, frames_processed, detections_written)
