"""Phase 2 in-memory queue boundary.

Execution is intentionally deferred. The queue preserves submission order and
will be consumed by the workflow runner in a later phase.
"""

from collections import deque


class JobQueue:
    def __init__(self) -> None:
        self._pending: deque[str] = deque()

    def put(self, job_id: str) -> None:
        self._pending.append(job_id)

    def discard(self, job_id: str) -> None:
        self._pending = deque(item for item in self._pending if item != job_id)

    def pending(self) -> list[str]:
        return list(self._pending)
