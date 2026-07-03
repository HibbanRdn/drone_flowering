from __future__ import annotations

import csv
import json
from pathlib import Path

from .schema import CSV_COLUMNS, flatten_detection


class JsonlCsvResultWriter:
    def __init__(self, run_dir: Path) -> None:
        self.run_dir = run_dir
        self.run_dir.mkdir(parents=True, exist_ok=False)
        self._jsonl = (run_dir / "detections.jsonl").open("w", encoding="utf-8")
        self._csv_file = (run_dir / "detections.csv").open("w", newline="", encoding="utf-8")
        self._csv = csv.DictWriter(self._csv_file, fieldnames=CSV_COLUMNS)
        self._csv.writeheader()

    def write_run_metadata(self, metadata: dict[str, object]) -> None:
        (self.run_dir / "run_metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def write_json(self, filename: str, data: dict[str, object]) -> None:
        (self.run_dir / filename).write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def write_detection(self, record: dict[str, object]) -> None:
        self._jsonl.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._csv.writerow(flatten_detection(record))

    def close(self) -> None:
        self._jsonl.close()
        self._csv_file.close()
