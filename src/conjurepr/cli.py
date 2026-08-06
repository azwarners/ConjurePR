"""HTTP-only command-line client and service entry point."""

import argparse
import json
import logging
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .config import load_config


def _api_url(value: str | None) -> str:
    return (value or os.environ.get("CONJUREPR_API_URL") or "http://127.0.0.1:8765").rstrip("/")


def _health(api_url: str) -> int:
    return _print_request(api_url, "/api/health")


def _print_request(api_url: str, path: str, method: str = "GET", payload: dict | None = None, headers: dict[str, str] | None = None) -> int:
    body = json.dumps(payload).encode() if payload is not None else None
    request_headers = {"Content-Type": "application/json"} if body is not None else {}
    request_headers.update(headers or {})
    request = Request(f"{api_url}{path}", data=body, headers=request_headers, method=method)
    try:
        with urlopen(request, timeout=10) as response:
            response_payload = json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        print(f"ConjurePR server returned HTTP {error.code}: {detail}")
        return 1
    except URLError as error:
        print(f"Could not reach ConjurePR server: {error.reason}")
        return 1

    print(json.dumps(response_payload, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="conjurepr")
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve = subparsers.add_parser("serve", help="start the local API service")
    serve.add_argument("--config", help="path to a TOML configuration file")

    health = subparsers.add_parser("health", help="check the API service")
    health.add_argument("--api-url", help="API base URL")

    submit = subparsers.add_parser("submit", help="submit a job through the API")
    submit.add_argument("--api-url", help="API base URL")
    submit.add_argument("--repository", required=True)
    submit.add_argument("--issue-file", required=True)
    submit.add_argument("--title")
    submit.add_argument("--acceptance-criterion", action="append", default=[])
    submit.add_argument("--out-of-scope", action="append", default=[])
    submit.add_argument("--idempotency-key")

    for name, help_text in (
        ("jobs", "list jobs"),
        ("show", "show one job"),
        ("journal", "show a job journal"),
        ("artifacts", "list job artifacts"),
        ("cancel", "cancel a queued job"),
    ):
        command = subparsers.add_parser(name, help=help_text)
        command.add_argument("job_id", nargs="?" if name == "jobs" else None)
        command.add_argument("--api-url", help="API base URL")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "health":
        return _health(_api_url(args.api_url))

    if args.command == "submit":
        try:
            issue = open(args.issue_file, encoding="utf-8").read()
        except OSError as error:
            print(f"Could not read issue file: {error}")
            return 1
        payload = {
            "repository": args.repository,
            "title": args.title,
            "issue": issue,
            "acceptance_criteria": args.acceptance_criterion,
            "out_of_scope": args.out_of_scope,
        }
        headers = {"Idempotency-Key": args.idempotency_key} if args.idempotency_key else None
        return _print_request(_api_url(args.api_url), "/api/jobs", "POST", payload, headers)

    api_url = _api_url(args.api_url)
    if args.command == "jobs":
        return _print_request(api_url, "/api/jobs")
    if args.command == "show":
        return _print_request(api_url, f"/api/jobs/{args.job_id}")
    if args.command == "journal":
        return _print_request(api_url, f"/api/jobs/{args.job_id}/journal")
    if args.command == "artifacts":
        return _print_request(api_url, f"/api/jobs/{args.job_id}/artifacts")
    if args.command == "cancel":
        return _print_request(api_url, f"/api/jobs/{args.job_id}/cancel", "POST")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    config = load_config(args.config)
    from .api import create_app
    import uvicorn

    uvicorn.run(create_app(config), host=config.server.host, port=config.server.port)
    return 0
