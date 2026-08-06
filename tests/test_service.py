from pathlib import Path

import pytest

from conjurepr.models import JobRequest, JobStatus
from conjurepr.service import IdempotencyConflict, JobService


def test_submit_is_durable_and_idempotent(tmp_path: Path) -> None:
    service = JobService(tmp_path)
    request = JobRequest(repository="demo", title="Fix it", issue="Fix the bug.")

    first, created = service.submit(request, "same-request")
    duplicate, duplicate_created = service.submit(request, "same-request")

    assert created is True
    assert duplicate_created is False
    assert first.job_id == duplicate.job_id == "cpr-0001"
    assert service.queue.pending() == ["cpr-0001"]
    assert (tmp_path / "cpr-0001" / "request.json").exists()
    assert (tmp_path / "cpr-0001" / "issue.md").read_text() == "Fix the bug."
    assert [event.event for event in service.journal("cpr-0001")] == ["job_created", "job_queued"]


def test_idempotency_key_cannot_be_reused_for_different_request(tmp_path: Path) -> None:
    service = JobService(tmp_path)
    service.submit(JobRequest(repository="demo", issue="First"), "same-request")

    with pytest.raises(IdempotencyConflict):
        service.submit(JobRequest(repository="demo", issue="Different"), "same-request")


def test_jobs_list_in_creation_order_and_queued_job_can_be_cancelled(tmp_path: Path) -> None:
    service = JobService(tmp_path)
    service.submit(JobRequest(repository="one", issue="One"))
    service.submit(JobRequest(repository="two", issue="Two"))

    assert [job.job_id for job in service.list_jobs()] == ["cpr-0001", "cpr-0002"]
    cancelled = service.cancel("cpr-0001")

    assert cancelled.status == JobStatus.CANCELLED
    assert cancelled.cancellation_requested is True
    assert service.queue.pending() == ["cpr-0002"]
    assert service.journal("cpr-0001")[-1].event == "job_cancelled"
