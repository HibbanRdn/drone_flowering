from __future__ import annotations

from pathlib import Path

import cv2

from .config import OverlayConfig
from .frame_source import FrameRecord


class OpenCvOverlayRenderer:
    def __init__(
        self,
        run_dir: Path,
        config: OverlayConfig,
        fps: float,
        width_px: int,
        height_px: int,
    ) -> None:
        self.config = config
        self.count = 0
        self.warnings: list[str] = []
        self.video_path = run_dir / "overlay.mp4"
        self.video = None
        self.frames_dir = run_dir / "frames"
        self.frames_dir_created = False

        if not config.enabled:
            return

        if config.output_frames:
            self.frames_dir.mkdir()
            self.frames_dir_created = True
        if config.output_video:
            if width_px < 1 or height_px < 1:
                self.warnings.append("Overlay video dilewati: ukuran frame tidak valid")
                return
            self.video = cv2.VideoWriter(
                str(self.video_path),
                cv2.VideoWriter_fourcc(*"mp4v"),
                fps if fps > 0 else 5.0,
                (width_px, height_px),
            )
            if not self.video.isOpened():
                self.video = None
                self.warnings.append("Overlay video tidak dapat dibuat")

    def render(
        self,
        frame: object,
        frame_record: FrameRecord,
        detections: list[dict[str, object]],
        timestamp_iso: str,
        telemetry: dict[str, object],
    ) -> None:
        if not self.config.enabled:
            return
        if self.config.max_frames is not None and self.count >= self.config.max_frames:
            return
        if frame is None or not hasattr(frame, "copy"):
            self.warnings.append(
                f"Overlay frame dilewati: frame invalid pada index {frame_record.frame_index}"
            )
            return

        image = frame.copy()
        for detection in detections:
            x1, y1, x2, y2 = [int(v) for v in detection["bbox_xyxy"]]
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = (
                f"{detection['label']} {float(detection['confidence']):.2f} "
                f"frame={frame_record.frame_index} "
                f"t={frame_record.timestamp_ms}ms "
                f"gimbal={telemetry.get('gimbal_pitch_deg', '')}"
            )
            cv2.putText(
                image,
                label,
                (x1, max(15, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )
        cv2.putText(
            image,
            timestamp_iso,
            (8, 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

        self.count += 1
        if self.video is not None:
            self.video.write(image)
        if self.config.output_frames:
            cv2.imwrite(str(self.frames_dir / f"frame_{self.count:06d}.jpg"), image)

    def close(self) -> None:
        if self.video is not None:
            self.video.release()

    @property
    def frames_written(self) -> int:
        return self.count

    @property
    def overlay_video_output(self) -> str | None:
        if self.config.enabled and self.video_path.exists():
            return str(self.video_path)
        return None

    @property
    def overlay_frames_output(self) -> str | None:
        if self.config.enabled and self.frames_dir_created:
            return str(self.frames_dir)
        return None
