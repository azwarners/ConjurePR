"""HTTP API for ConjurePR Phase 2."""

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse

from . import __version__
from .config import Config
from .models import HealthResponse
from .models import JobRequest
from .service import IdempotencyConflict, JobNotFound, JobService


def create_app(config: Config | None = None, service: JobService | None = None) -> FastAPI:
    """Build the API application without starting a server."""

    app = FastAPI(title="ConjurePR", version=__version__)
    app.state.job_service = service or JobService((config or Config()).paths.jobs)

    @app.get("/api/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok", service="conjurepr", version=__version__)

    @app.post("/api/jobs")
    def submit_job(request: JobRequest, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
        try:
            job, created = app.state.job_service.submit(request, idempotency_key)
        except IdempotencyConflict as error:
            raise HTTPException(status_code=409, detail=f"Idempotency key already belongs to a different request: {error}") from error
        return JSONResponse(status_code=202 if created else 200, content=job.model_dump(mode="json"))

    @app.get("/api/jobs")
    def list_jobs():
        return [job.model_dump(mode="json") for job in app.state.job_service.list_jobs()]

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: str):
        try:
            return app.state.job_service.get_job(job_id).model_dump(mode="json")
        except JobNotFound as error:
            raise HTTPException(status_code=404, detail="job not found") from error

    @app.get("/api/jobs/{job_id}/journal")
    def get_journal(job_id: str):
        try:
            return [event.model_dump(mode="json") for event in app.state.job_service.journal(job_id)]
        except JobNotFound as error:
            raise HTTPException(status_code=404, detail="job not found") from error

    @app.get("/api/jobs/{job_id}/artifacts")
    def list_artifacts(job_id: str):
        try:
            return [artifact.model_dump(mode="json") for artifact in app.state.job_service.artifacts(job_id)]
        except JobNotFound as error:
            raise HTTPException(status_code=404, detail="job not found") from error

    @app.get("/api/jobs/{job_id}/artifacts/{name}")
    def get_artifact(job_id: str, name: str):
        try:
            return PlainTextResponse(app.state.job_service.artifact(job_id, name))
        except (JobNotFound, ValueError, FileNotFoundError) as error:
            raise HTTPException(status_code=404, detail="artifact not found") from error

    @app.post("/api/jobs/{job_id}/cancel")
    def cancel_job(job_id: str):
        try:
            return app.state.job_service.cancel(job_id).model_dump(mode="json")
        except JobNotFound as error:
            raise HTTPException(status_code=404, detail="job not found") from error

    return app
