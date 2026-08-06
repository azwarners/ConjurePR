import io
import json
from pathlib import Path
from unittest.mock import patch

from conjurepr.cli import main


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


def test_health_command_uses_http_api(capsys) -> None:
    response = FakeResponse(json.dumps({"status": "ok"}).encode())

    with patch("conjurepr.cli.urlopen", return_value=response) as open_url:
        result = main(["health", "--api-url", "http://127.0.0.1:8765"])

    assert result == 0
    assert "\"status\": \"ok\"" in capsys.readouterr().out
    open_url.assert_called_once()
    assert open_url.call_args.args[0].full_url == "http://127.0.0.1:8765/api/health"


def test_submit_command_reads_issue_and_uses_http_api(tmp_path: Path, capsys) -> None:
    issue_file = tmp_path / "issue.md"
    issue_file.write_text("Fix the bug.")
    response = FakeResponse(json.dumps({"job_id": "cpr-0001", "status": "queued"}).encode())

    with patch("conjurepr.cli.urlopen", return_value=response) as open_url:
        result = main([
            "submit",
            "--api-url",
            "http://127.0.0.1:8765",
            "--repository",
            "demo",
            "--issue-file",
            str(issue_file),
            "--idempotency-key",
            "key-1",
        ])

    assert result == 0
    assert "cpr-0001" in capsys.readouterr().out
    request = open_url.call_args.args[0]
    assert request.full_url == "http://127.0.0.1:8765/api/jobs"
    assert request.get_header("Idempotency-key") == "key-1"
    assert json.loads(request.data) == {
        "repository": "demo",
        "title": None,
        "issue": "Fix the bug.",
        "acceptance_criteria": [],
        "out_of_scope": [],
    }
