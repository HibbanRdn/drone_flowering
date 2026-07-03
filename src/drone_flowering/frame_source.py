from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

try:
    import cv2
except ModuleNotFoundError:  # pragma: no cover - depends on local environment
    cv2 = None


@dataclass(frozen=True)
class FrameRecord:
    frame: object
    frame_index: int
    timestamp_ms: float


class VideoFileFrameSource:
    def __init__(self, video_path: Path, every_n_frames: int) -> None:
        self.video_path = video_path
        self.every_n_frames = every_n_frames

    def video_metadata(self) -> dict[str, object]:
        cap = self._open()
        try:
            fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
            return {
                "source_video": str(self.video_path),
                "fps": fps,
                "width_px": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0),
                "height_px": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0),
                "frame_count": frame_count,
                "duration_ms": (frame_count / fps * 1000.0) if fps > 0 else None,
            }
        finally:
            cap.release()

    def frames(self) -> Iterator[FrameRecord]:
        cap = self._open()
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
        frame_index = 0
        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                if frame_index % self.every_n_frames == 0:
                    timestamp_ms = frame_index / fps * 1000.0 if fps > 0 else 0.0
                    yield FrameRecord(frame, frame_index, round(timestamp_ms, 3))
                frame_index += 1
        finally:
            cap.release()

    def _open(self):
        if cv2 is None:
            raise RuntimeError("OpenCV belum terpasang. Jalankan `pip install -e .`.")
        cap = cv2.VideoCapture(str(self.video_path))
        if not cap.isOpened():
            raise RuntimeError(f"Video tidak dapat dibuka: {self.video_path}")
        return cap
