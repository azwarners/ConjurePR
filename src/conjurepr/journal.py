"""Append-only structured job journal."""

from datetime import datetime, timezone
import json
from pathlib import Path


class Journal:
    def __init__(self, path: Path, job_id: str):
        self.path = path
        self.job_id = job_id

    def append(self, event: str, **details: object) -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "job_id": self.job_id,
            "event": event,
            "details": details,
        }
        with self.path.open("a", encoding="utf-8") as journal:
            journal.write(json.dumps(record, sort_keys=True) + "\n")

    def read(self) -> list[dict[str, object]]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line]
