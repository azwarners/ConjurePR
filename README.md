# ConjurePR

**ConjurePR is an API-first service for bounded pull-request automation.** It accepts a specific repository task, records and tracks a job, and provides API and CLI interfaces for observing its execution. Its design aims to turn a well-scoped implementation request into a reviewable draft pull request without inventing another general-purpose coding-agent engine.

## Implemented interfaces and features

The repository contains a Python package with a `conjurepr` command and a FastAPI service. The command-line interface currently exposes:

- `serve` — start the service.
- `health` — check the API.
- `submit` — submit an issue description and target repository as a job, with optional title, acceptance criteria, exclusions, and idempotency key.
- `jobs` and `show` — list jobs and inspect one job.
- `journal` and `artifacts` — retrieve recorded job events and artifacts.
- `cancel` — request cancellation of a queued job.

The API provides `/api/health` and `/api/jobs` endpoints with job-specific detail, journal, and artifact routes. These interfaces are implemented; successful creation and testing of a draft GitHub PR depend on the configured execution backend, credentials, and operational environment. Do not treat submitting a job as proof that a pull request was produced.

## Install and quick start

Prerequisites: Python 3.11 or newer. Clone and install in a virtual environment:

```sh
git clone https://github.com/azwarners/ConjurePR.git
cd ConjurePR
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
```

Explore the commands and run the automated tests:

```sh
conjurepr --help
python -m pytest
```

Start the local API service in one terminal:

```sh
conjurepr serve
```

In another terminal:

```sh
conjurepr health
```

The CLI's default API URL is `http://127.0.0.1:8765`; override it with `CONJUREPR_API_URL` or the supported `--api-url` flag.

To submit a bounded task, save the issue description to a file and run:

```sh
conjurepr submit \
  --repository OWNER/REPOSITORY \
  --issue-file issue.md \
  --title "Implement a bounded change" \
  --acceptance-criterion "The relevant tests pass"
conjurepr jobs
```

Replace `OWNER/REPOSITORY` with an accessible repository and review the configuration and execution permissions before submitting work that may modify code. Use `conjurepr show JOB_ID`, `conjurepr journal JOB_ID`, and `conjurepr artifacts JOB_ID` to inspect the resulting job.

## Architecture and scope

ConjurePR's job and API boundary is separate from the coding-agent runtime: [Redless](https://github.com/azwarners/Redless) focuses on reusable coding labor, while [DesignDiviner](https://github.com/azwarners/DesignDiviner) describes a higher-level, evidence-grounded architecture-planning workflow. [Ysparr](https://github.com/azwarners/Ysparr) handles OpenAI-compatible model transport, and [Apmatia](https://github.com/azwarners/Apmatia) may expose cooperating tools to conversational agents. Those neighboring projects are not mandatory components of the basic CLI and API smoke test.

## Status and cautions

This README documents the shipped package, CLI surface, and API entry points. A job's actual execution, test validation, and PR outcome must be checked through its recorded status and artifacts. Keep human review and repository protections in place for code changes; do not assume automated execution implies an approved or merged PR.
