from __future__ import annotations

SCHEMA_VERSION = "drone-flowering-detection.v1"

CSV_COLUMNS = [
    "schema_version",
    "run_id",
    "source_video",
    "frame_index",
    "timestamp_ms",
    "timestamp_iso",
    "detection_id",
    "label",
    "confidence",
    "bbox_x_min",
    "bbox_y_min",
    "bbox_x_max",
    "bbox_y_max",
    "bbox_format",
    "telemetry_lat",
    "telemetry_lng",
    "telemetry_altitude_m",
    "telemetry_heading_deg",
    "telemetry_gimbal_pitch_deg",
    "telemetry_speed_mps",
    "telemetry_source",
]


def flatten_detection(record: dict[str, object]) -> dict[str, object]:
    bbox = record["bbox_xyxy"]
    telemetry = record["telemetry"]
    return {
        "schema_version": record["schema_version"],
        "run_id": record["run_id"],
        "source_video": record["source_video"],
        "frame_index": record["frame_index"],
        "timestamp_ms": record["timestamp_ms"],
        "timestamp_iso": record["timestamp_iso"],
        "detection_id": record["detection_id"],
        "label": record["label"],
        "confidence": record["confidence"],
        "bbox_x_min": bbox[0],
        "bbox_y_min": bbox[1],
        "bbox_x_max": bbox[2],
        "bbox_y_max": bbox[3],
        "bbox_format": record["bbox_format"],
        "telemetry_lat": telemetry["lat"],
        "telemetry_lng": telemetry["lng"],
        "telemetry_altitude_m": telemetry["altitude_m"],
        "telemetry_heading_deg": telemetry["heading_deg"],
        "telemetry_gimbal_pitch_deg": telemetry["gimbal_pitch_deg"],
        "telemetry_speed_mps": telemetry["speed_mps"],
        "telemetry_source": telemetry.get("source", ""),
    }
