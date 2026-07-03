from __future__ import annotations


class DummyInferenceEngine:
    def __init__(self, label: str, confidence: float) -> None:
        self.label = label
        self.confidence = confidence

    def detect(self, frame: object, frame_index: int) -> list[dict[str, object]]:
        height, width = frame.shape[:2]
        x1, y1 = int(width * 0.4), int(height * 0.4)
        x2, y2 = int(width * 0.6), int(height * 0.6)
        return [
            {
                "label": self.label,
                "confidence": self.confidence,
                "bbox_xyxy": [x1, y1, x2, y2],
                "bbox_format": "xyxy",
                "model_name": "dummy_inference",
                "model_version": "0.1.0",
            }
        ]
