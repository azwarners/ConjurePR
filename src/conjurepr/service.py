"""Durable job intake and management for Phase 2."""

from datetime import datetime, timezone
import threading
from pathlib import Path

from .artifacts import ArtifactStore
from .job_runner import JobQueue
from .journal import Journal
from .models import ArtifactInfo, JobDetail, JobRequest, JobStatus, JobSummary, JournalEvent


class JobNotFound(Exception):
    pass


class IdempotencyConflict(Exception):
    pass


class JobService:
    def __init__(self, jobs_root: Path):
        self.store = ArtifactStore(jobs_root)
        self.queue = JobQueue()
        self._lock = threading.RLock()
        self._next_id = self._find_next_id()
        self._restore_queue()

    def _find_next_id(self) -> int:
        values = []
        for directory in self.store.jobs_root.glob("cpr-*"):
            try:
                values.append(int(directory.name.removeprefix("cpr-")))
            except ValueError:
                continue
        return max(values, default=0) + 1

    def _restore_queue(self) -> None:
        for directory in sorted(self.store.jobs_root.glob("cpr-*")):
            state_path = directory / "state.json"
            if not state_path.exists():
                continue
            state = self.store.read_json(state_path)
            if state.get("status") == JobStatus.QUEUED:
                self.queue.put(directory.name)

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)

    def _state(self, job_id: str) -> dict:
        try:
            return self.store.read_json(self.store.job_dir(job_id) / "state.json")
        except (FileNotFoundError, ValueError) as error:
            raise JobNotFound(job_id) from error

    def _summary(self, state: dict) -> JobSummary:
        return JobSummary.model_validate(state)

    def _detail(self, state: dict) -> JobDetail:
        state = dict(state)
        state["artifact_count"] = len(self.store.list_artifacts(state["job_id"]))
        return JobDetail.model_validate(state)

    def submit(self, request: JobRequest, idempotency_key: str | None = None) -> tuple[JobSummary, bool]:
        with self._lock:
            if idempotency_key:
                existing = self._find_idempotent(idempotency_key)
                if existing:
                    if existing["request"] != request.model_dump(mode="json"):
                        raise IdempotencyConflict(idempotency_key)
                    return self._summary(existing["state"]), False

            job_id = f"cpr-{self._next_id:04d}"
            self._next_id += 1
            directory = self.store.create_job(job_id)
            now = self._now()
            request_data = request.model_dump(mode="json")
            state = {
                "job_id": job_id,
                "repository": request.repository,
                "title": request.title,
                "status": JobStatus.QUEUED,
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
                "issue": request.issue,
                "acceptance_criteria": request.acceptance_criteria,
                "out_of_scope": request.out_of_scope,
                "idempotency_key": idempotency_key,
                "cancellation_requested": False,
            }
            self.store.write_json(directory / "request.json", {**request_data, "idempotency_key": idempotency_key})
            (directory / "issue.md").write_text(request.issue, encoding="utf-8")
            self.store.write_json(directory / "state.json", state)
            journal = Journal(directory / "journal.jsonl", job_id)
            journal.append("job_created", repository=request.repository)
            journal.append("job_queued")
            self.queue.put(job_id)
            return self._summary(state), True

    def _find_idempotent(self, key: str) -> dict | None:
        for directory in self.store.jobs_root.glob("cpr-*"):
            request_path = directory / "request.json"
            state_path = directory / "state.json"
            if not request_path.exists() or not state_path.exists():
                continue
            request = self.store.read_json(request_path)
            if request.get("idempotency_key") == key:
                return {"request": {k: v for k, v in request.items() if k != "idempotency_key"}, "state": self.store.read_json(state_path)}
        return None

    def list_jobs(self) -> list[JobSummary]:
        with self._lock:
            states = []
            for directory in self.store.jobs_root.glob("cpr-*"):
                if (directory / "state.json").exists():
                    states.append(self._summary(self.store.read_json(directory / "state.json")))
            return sorted(states, key=lambda item: item.created_at)

    def get_job(self, job_id: str) -> JobDetail:
        return self._detail(self._state(job_id))

    def journal(self, job_id: str) -> list[JournalEvent]:
        self._state(job_id)
        records = Journal(self.store.job_dir(job_id) / "journal.jsonl", job_id).read()
        return [JournalEvent.model_validate(record) for record in records]

    def artifacts(self, job_id: str) -> list[ArtifactInfo]:
        self._state(job_id)
        return [ArtifactInfo(name=name, size=size) for name, size in self.store.list_artifacts(job_id)]

    def artifact(self, job_id: str, name: str) -> str:
        self._state(job_id)
        return self.store.read_artifact(job_id, name)

    def cancel(self, job_id: str) -> JobDetail:
        with self._lock:
            state = self._state(job_id)
            if state["status"] == JobStatus.QUEUED:
                state["status"] = JobStatus.CANCELLED
                state["cancellation_requested"] = True
                state["updated_at"] = self._now().isoformat()
                self.store.write_json(self.store.job_dir(job_id) / "state.json", state)
                Journal(self.store.job_dir(job_id) / "journal.jsonl", job_id).append("job_cancelled")
                self.queue.discard(job_id)
            return self._detail(state)
