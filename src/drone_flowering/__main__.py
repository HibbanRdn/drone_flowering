from __future__ import annotations

import argparse
import sys

from .app import run_pipeline
from .config import ConfigError


def main(argv: list[str] | None = None) -> int:
    # MEMPARSE ARGUMEN CLI, MEMANGGIL RUN_PIPELINE(), LALU MENAMPILKAN HASIL RUN KE TERMINAL
    parser = argparse.ArgumentParser(description="Jalankan offline prototype drone flowering.")
    parser.add_argument("--config", default="configs/offline.json", help="Path config JSON.")
    args = parser.parse_args(argv)

    try:
        result = run_pipeline(args.config)
    except (ConfigError, FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"run_id: {result.run_id}")
    print(f"run_dir: {result.run_dir}")
    print(f"frames_processed: {result.frames_processed}")
    print(f"detections_written: {result.detections_written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
