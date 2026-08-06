from pathlib import Path

from conjurepr.models import JobRequest
from conjurepr.api import create_app
from conjurepr.service import JobService


def test_health_endpoint(tmp_path: Path) -> None:
    app = create_app(service=JobService(tmp_path))
    health_route = next(route for route in app.routes if route.path == "/api/health")

    assert health_route.endpoint().model_dump() == {
        "status": "ok",
        "service": "conjurepr",
        "version": "0.1.0",
    }


def test_job_submission_route_uses_durable_service(tmp_path: Path) -> None:
    app = create_app(service=JobService(tmp_path))
    submit_route = next(route for route in app.routes if route.path == "/api/jobs")

    response = submit_route.endpoint(JobRequest(repository="demo", issue="Fix it."), "key-1")

    assert response.status_code == 202
    assert response.body is not None
    assert b'"status":"queued"' in response.body
    assert (tmp_path / "cpr-0001" / "state.json").exists()
