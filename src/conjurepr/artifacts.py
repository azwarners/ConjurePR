"""Durable, path-safe storage for Phase 2 job files."""

import json
import os
from pathlib import Path
from typing import Any


class ArtifactStore:
    def __init__(self, jobs_root: Path):
        self.jobs_root = jobs_root.expanduser().resolve()
        self.jobs_root.mkdir(parents=True, exist_ok=True)

    def job_dir(self, job_id: str) -> Path:
        if not job_id.startswith("cpr-") or "/" in job_id or "\\" in job_id:
            raise ValueError("invalid job ID")
        directory = (self.jobs_root / job_id).resolve()
        if directory.parent != self.jobs_root:
            raise ValueError("job directory escapes jobs root")
        return directory

    def create_job(self, job_id: str) -> Path:
        directory = self.job_dir(job_id)
        directory.mkdir(mode=0o700)
        (directory / "artifacts").mkdir(mode=0o700)
        (directory / "prompts").mkdir(mode=0o700)
        (directory / "responses").mkdir(mode=0o700)
        (directory / "commands").mkdir(mode=0o700)
        return directory

    @staticmethod
    def write_json(path: Path, value: Any) -> None:
        temporary = path.with_name(f".{path.name}.tmp")
        temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, path)

    @staticmethod
    def read_json(path: Path) -> Any:
        return json.loads(path.read_text(encoding="utf-8"))

    def write_text(self, job_id: str, name: str, content: str) -> Path:
        if Path(name).name != name or not name.endswith((".md", ".txt", ".json")):
            raise ValueError("invalid artifact name")
        path = self.job_dir(job_id) / "artifacts" / name
        path.write_text(content, encoding="utf-8")
        return path

    def list_artifacts(self, job_id: str) -> list[tuple[str, int]]:
        directory = self.job_dir(job_id)
        return sorted(
            (path.name, path.stat().st_size)
            for path in directory.iterdir()
            if path.is_file() and path.name not in {"worker.log"}
        )

    def read_artifact(self, job_id: str, name: str) -> str:
        if Path(name).name != name:
            raise ValueError("invalid artifact name")
        path = self.job_dir(job_id) / name
        if not path.is_file():
            path = self.job_dir(job_id) / "artifacts" / name
        return path.read_text(encoding="utf-8")
