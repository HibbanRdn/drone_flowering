from __future__ import annotations


class MockTelemetryProvider:
    def __init__(self, config: dict[str, float]) -> None:
        self.config = config

    def get(self, timestamp_ms: float) -> dict[str, float | str]:
        seconds = timestamp_ms / 1000.0
        return {
            "lat": self.config["lat"] + self.config["lat_step_per_s"] * seconds,
            "lng": self.config["lng"] + self.config["lng_step_per_s"] * seconds,
            "altitude_m": self.config["altitude_m"],
            "heading_deg": (
                self.config["heading_deg"]
                + self.config["heading_step_deg_per_s"] * seconds
            )
            % 360.0,
            "gimbal_pitch_deg": self.config["gimbal_pitch_deg"],
            "speed_mps": self.config["speed_mps"],
            "source": "mock",
        }
