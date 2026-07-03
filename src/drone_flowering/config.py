from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ConfigError(ValueError):
    """Error config yang aman ditampilkan ke user."""


@dataclass(frozen=True)
class OverlayConfig:
    enabled: bool
    output_video: bool
    output_frames: bool
    max_frames: int | None


@dataclass(frozen=True)
class PipelineConfig:
    config_path: Path
    input_video: Path
    output_root: Path
    sampling_every_n_frames: int
    dummy_label: str
    dummy_confidence: float
    mock_telemetry: dict[str, float]
    overlay: OverlayConfig
    experiment: dict[str, Any]
    raw: dict[str, Any]


class ConfigLoader:
    @staticmethod
    def load(path: str | Path) -> PipelineConfig:
        config_path = Path(path)
        if not config_path.exists():
            raise ConfigError(f"Config tidak ditemukan: {config_path}")

        try:
            raw = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ConfigError(f"Config JSON invalid: {exc}") from exc

        video_path = _relative_path(raw, "input.video_path")
        output_root = _relative_path(raw, "output.root_dir")
        every_n_frames = int(_value(raw, "sampling.every_n_frames"))
        if every_n_frames < 1:
            raise ConfigError("sampling.every_n_frames harus >= 1")

        confidence = float(_value(raw, "dummy_inference.confidence"))
        if not 0.0 <= confidence <= 1.0:
            raise ConfigError("dummy_inference.confidence harus di antara 0.0 dan 1.0")

        experiment = _experiment_config(raw)
        telemetry = {
            "lat": float(_value(raw, "mock_telemetry.lat")),
            "lng": float(_value(raw, "mock_telemetry.lng")),
            "altitude_m": _mock_or_experiment_float(raw, experiment, "altitude_m"),
            "heading_deg": float(_value(raw, "mock_telemetry.heading_deg")),
            "gimbal_pitch_deg": _mock_or_experiment_float(
                raw, experiment, "gimbal_pitch_deg"
            ),
            "speed_mps": _mock_or_experiment_float(raw, experiment, "speed_mps"),
        }
        for key in ("lat_step_per_s", "lng_step_per_s", "heading_step_deg_per_s"):
            telemetry[key] = float(raw.get("mock_telemetry", {}).get(key, 0.0))

        overlay = _overlay_config(raw)

        if not video_path.exists():
            raise FileNotFoundError(f"Video input tidak ditemukan: {video_path}")

        return PipelineConfig(
            config_path=config_path,
            input_video=video_path,
            output_root=output_root,
            sampling_every_n_frames=every_n_frames,
            dummy_label=str(_value(raw, "dummy_inference.label")),
            dummy_confidence=confidence,
            mock_telemetry=telemetry,
            overlay=overlay,
            experiment=experiment,
            raw=raw,
        )


def _value(raw: dict[str, Any], dotted_key: str) -> Any:
    current: Any = raw
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            raise ConfigError(f"Field config wajib hilang: {dotted_key}")
        current = current[part]
    return current


def _relative_path(raw: dict[str, Any], dotted_key: str) -> Path:
    path = Path(str(_value(raw, dotted_key)))
    if path.is_absolute():
        raise ConfigError(f"{dotted_key} harus path relatif, bukan path absolut")
    return path


def _overlay_config(raw: dict[str, Any]) -> OverlayConfig:
    overlay = raw.get("overlay", {})
    if not isinstance(overlay, dict):
        raise ConfigError("overlay harus object JSON")

    enabled = _bool(overlay, "enabled", False)
    output_video = _bool(overlay, "output_video", True)
    output_frames = _bool(overlay, "output_frames", False)
    max_frames_raw = overlay.get("max_frames")
    max_frames = int(max_frames_raw) if max_frames_raw is not None else None

    if max_frames is not None and max_frames < 1:
        raise ConfigError("overlay.max_frames harus >= 1 jika diisi")
    if enabled and not output_video and not output_frames:
        raise ConfigError("overlay enabled, tetapi output_video dan output_frames false")

    return OverlayConfig(enabled, output_video, output_frames, max_frames)


def _experiment_config(raw: dict[str, Any]) -> dict[str, Any]:
    experiment = raw.get("experiment", {})
    if not isinstance(experiment, dict):
        raise ConfigError("experiment harus object JSON")
    return experiment


def _mock_or_experiment_float(
    raw: dict[str, Any], experiment: dict[str, Any], key: str
) -> float:
    mock = raw.get("mock_telemetry", {})
    if isinstance(mock, dict) and key in mock:
        return float(mock[key])
    if key in experiment:
        return float(experiment[key])
    return float(_value(raw, f"mock_telemetry.{key}"))


def _bool(raw: dict[str, Any], key: str, default: bool) -> bool:
    value = raw.get(key, default)
    if not isinstance(value, bool):
        raise ConfigError(f"overlay.{key} harus boolean")
    return value
