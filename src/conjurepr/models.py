"""HTTP request and response models for the Phase 2 API."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class JobStatus(StrEnum):
    QUEUED = "queued"
    CANCELLED = "cancelled"
    FAILED = "failed"
    COMPLETED = "completed"
    INTERRUPTED = "interrupted"


class JobRequest(BaseModel):
    repository: str
    title: str | None = None
    issue: str
    acceptance_criteria: list[str] = Field(default_factory=list)
    out_of_scope: list[str] = Field(default_factory=list)


class JobSummary(BaseModel):
    job_id: str
    repository: str
    title: str | None = None
    status: JobStatus
    created_at: datetime
    updated_at: datetime


class JobDetail(JobSummary):
    issue: str
    acceptance_criteria: list[str]
    out_of_scope: list[str]
    idempotency_key: str | None = None
    cancellation_requested: bool = False
    artifact_count: int = 0


class ArtifactInfo(BaseModel):
    name: str
    size: int


class JournalEvent(BaseModel):
    timestamp: datetime
    job_id: str
    event: str
    details: dict[str, object] = Field(default_factory=dict)


class JobSubmissionResponse(JobSummary):
    pass
