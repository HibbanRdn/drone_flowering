from __future__ import annotations


class DummyInferenceEngine:
    def __init__(self, label: str, confidence: float) -> None:
        # MENYIMPAN LABEL DAN CONFIDENCE DARI CONFIG UNTUK DIGUNAKAN DI SETIAP DETECTION
        self.label = label
        self.confidence = confidence

    def detect(self, frame: object, frame_index: int) -> list[dict[str, object]]:
        # MEMBUAT DUMMY CANDIDATE PLOT KOSONG DI TENGAH FRAME (BUKAN AI ASLI)
        height, width = frame.shape[:2]
        x1, y1 = int(width * 0.4), int(height * 0.4)
        x2, y2 = int(width * 0.6), int(height * 0.6)
        return [
            {
                "label": self.label,
                "confidence": self.confidence,
                "bbox_xyxy": [x1, y1, x2, y2],
                "bbox_format": "xyxy",
                "model_name": "dummy_plot_gap_baseline",
                "model_version": "0.1.0",
            }
        ]
