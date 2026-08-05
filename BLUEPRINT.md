# ConjurePR Blueprint

## 1. Product purpose

ConjurePR is a small, API-first autonomous coding service that transforms a well-defined software issue into a reviewable draft pull request.

The user connects:

* one OpenAI-compatible LLM;
* one existing local Git repository;
* one small bug report or feature request;
* one or more validation commands.

ConjurePR then:

1. evaluates whether the issue is suitable;
2. inspects the relevant repository content;
3. produces a short implementation plan;
4. creates a dedicated Git branch;
5. modifies the code;
6. runs configured tests and checks;
7. attempts a limited number of repairs;
8. reviews the resulting diff;
9. commits the changes;
10. pushes the branch;
11. opens a draft pull request for human review.

ConjurePR never merges the pull request.

## 2. Permanent product boundary

ConjurePR performs **small, iterative development tasks** against existing codebases.

Supported work includes:

* focused bug fixes;
* small new features;
* validation improvements;
* narrowly scoped refactoring required by an issue;
* new or updated tests;
* small configuration changes;
* minor documentation directly associated with a code change.

ConjurePR is permanently not responsible for:

* greenfield application construction;
* broad architectural design;
* deep architectural reviews;
* open-ended codebase improvement;
* large migrations;
* sweeping refactors;
* full documentation rewrites;
* product planning;
* issue decomposition;
* project management;
* deployment;
* release management;
* autonomous merging;
* generalized agent behavior;
* multi-agent collaboration.

ConjurePR must not evolve into a general-purpose autonomous software engineer.

Its responsibility remains:

> Convert one bounded software issue into one draft pull request.

## 3. Guiding principles

### KISS

Prefer a fixed, understandable workflow over dynamic planning machinery.

### Single responsibility

ConjurePR produces pull requests. Broader planning and orchestration belong to Nick, Apmatia, OpenIPE, or other tools.

### API first

Every client uses the local HTTP API.

The CLI must never bypass the API and directly invoke workflow internals.

### Human approval

A successful run ends with a draft pull request awaiting review.

PR creation does not mean the work is accepted.

### Bounded autonomy

ConjurePR may operate unattended, but only inside strict limits.

### Evidence over assertion

Tests pass only when an actual command exits successfully. Files changed only when the Git diff proves it. The model’s claims are never treated as verification.

## 4. High-level architecture

```text
CLI
  │
  │ HTTP
  ▼
ConjurePR API
  │
  ▼
Application service
  │
  ▼
Single-job queue and runner
  │
  ▼
Fixed PR workflow
  ├── LLM client
  ├── repository tools
  ├── Git tools
  ├── command runner
  └── artifact storage
```

The first release supports:

* one local user;
* localhost access only;
* one configured LLM;
* one active job at a time;
* multiple queued jobs;
* existing local Git repositories;
* GitHub pull requests through the `gh` CLI;
* file-based job state and artifacts.

Do not introduce a database, message broker, distributed workers, or graphical client.

## 5. Runtime model

Start the service with:

```bash
conjurepr serve
```

Default address:

```text
http://127.0.0.1:8765
```

Submit work through the CLI:

```bash
conjurepr submit \
  --repo /data/projects/triagetty \
  --issue issue.md \
  --test-command "pytest -q"
```

The CLI sends an HTTP request and exits after the job is accepted.

The server continues running the job independently.

The user can return later:

```bash
conjurepr jobs
conjurepr show <job-id>
conjurepr watch <job-id>
conjurepr diff <job-id>
conjurepr open-pr <job-id>
```

## 6. Core workflow

ConjurePR uses a fixed prompt-driven workflow:

```text
Issue submitted
    ↓
Scope evaluation
    ↓
Repository analysis
    ↓
Short implementation plan
    ↓
Create worker branch
    ↓
Implement change
    ↓
Run tests and checks
    ↓
Limited repair loop
    ↓
Review final diff
    ↓
Optional final correction
    ↓
Commit
    ↓
Push branch
    ↓
Create draft pull request
```

Ordinary Python controls this sequence.

The LLM reasons within individual stages. It does not invent new stages, delegate work, browse freely, redesign the project, or expand the objective.

## 7. Scope evaluation

The first stage determines whether the submitted issue fits ConjurePR.

Possible results:

```text
accepted
needs_clarification
too_large
unsupported
```

Accept tasks such as:

```text
Add a --version command-line option.

Fix the crash when the preferences file is missing.

Allow project lists to be filtered by status.

Persist the selected terminal font size.

Add tests for duplicate project-name validation.
```

Reject or pause tasks such as:

```text
Build an Android client.

Redesign the application architecture.

Modernize the entire repository.

Improve the documentation.

Create a new application from scratch.

Make Apmatia better.
```

A rejected issue must include a clear explanation and, where practical, advice for reducing it into smaller issues.

A scope rejection is a successful use of ConjurePR’s guardrails, not an application failure.

## 8. Enforced limits

Use configurable limits rather than relying entirely on model judgment.

Example configuration:

```toml
[scope]
maximum_changed_files = 12
maximum_diff_lines = 800
maximum_model_calls = 20
maximum_repair_attempts = 3
maximum_review_corrections = 1
maximum_runtime_minutes = 240
maximum_command_seconds = 1200
```

When a job exceeds a limit, stop and report that the issue should be divided into smaller work.

Do not allow ConjurePR to quietly turn one issue into a multi-day development campaign.

## 9. Project structure

```text
ConjurePR/
├── pyproject.toml
├── README.md
├── BLUEPRINT.md
├── config.example.toml
├── src/
│   └── conjurepr/
│       ├── __init__.py
│       ├── api.py
│       ├── cli.py
│       ├── config.py
│       ├── models.py
│       ├── service.py
│       ├── job_runner.py
│       ├── workflow.py
│       ├── scope.py
│       ├── llm_client.py
│       ├── workspace.py
│       ├── git_tools.py
│       ├── command_runner.py
│       ├── artifacts.py
│       ├── journal.py
│       └── prompts/
│           ├── evaluate_scope.md
│           ├── analyze.md
│           ├── plan.md
│           ├── implement.md
│           ├── repair.md
│           ├── review.md
│           └── finalize.md
└── tests/
    ├── test_api.py
    ├── test_cli.py
    ├── test_scope.py
    ├── test_service.py
    ├── test_workflow.py
    ├── test_workspace.py
    ├── test_git_tools.py
    └── test_artifacts.py
```

Keep modules small and explicit.

Do not create plugin systems or deep class hierarchies.

## 10. Module responsibilities

### `api.py`

Defines HTTP routes, validates input, calls the service layer, and converts application errors into HTTP responses.

It contains no workflow logic.

### `cli.py`

Parses commands, sends HTTP requests, and displays responses.

It never imports `workflow.py`, `git_tools.py`, `workspace.py`, or `llm_client.py`.

### `service.py`

Creates jobs, lists jobs, retrieves status, queues work, handles cancellation, and exposes artifacts.

### `job_runner.py`

Runs one queued job at a time and records terminal success or failure.

### `workflow.py`

Controls the fixed stage sequence and all limits.

### `scope.py`

Evaluates task suitability and enforces configured size constraints.

### `llm_client.py`

Calls one OpenAI-compatible endpoint and stores every prompt and response.

### `workspace.py`

Safely inspects and modifies repository files while preventing access outside the repository root.

### `git_tools.py`

Creates branches, shows diffs, stages explicit files, commits, pushes, and invokes GitHub CLI.

### `command_runner.py`

Runs configured commands with timeouts and captures stdout, stderr, exit code, and duration.

### `artifacts.py`

Creates and manages each job’s artifact directory.

### `journal.py`

Appends structured job events for monitoring and later Apmatia integration.

## 11. Configuration

Use a local TOML file:

```toml
[server]
host = "127.0.0.1"
port = 8765

[llm]
base_url = "http://localhost:8080/v1"
model = "qwen3-coder-next"
api_key = ""
temperature = 0.2
max_tokens = 8192
timeout_seconds = 600

[worker]
runs_directory = "./runs"
maximum_repair_attempts = 3
maximum_review_corrections = 1
maximum_runtime_minutes = 240
maximum_command_seconds = 1200

[scope]
maximum_changed_files = 12
maximum_diff_lines = 800
maximum_model_calls = 20

[git]
default_base_branch = "main"
remote = "origin"
create_draft_pull_requests = true
```

Allow secrets to be supplied through environment variables.

Never commit real credentials.

## 12. API

Initial endpoints:

```text
GET    /api/health

POST   /api/jobs
GET    /api/jobs
GET    /api/jobs/{job_id}

GET    /api/jobs/{job_id}/journal
GET    /api/jobs/{job_id}/artifacts
GET    /api/jobs/{job_id}/artifacts/{name}
GET    /api/jobs/{job_id}/diff
GET    /api/jobs/{job_id}/log

POST   /api/jobs/{job_id}/cancel
```

Job submission:

```json
{
  "repository_path": "/data/projects/triagetty",
  "title": "Add configurable terminal font size",
  "issue": "Add a preference that controls terminal font size and persists between launches.",
  "acceptance_criteria": [
    "The font size can be changed through preferences.",
    "The selected value persists.",
    "Existing tests pass."
  ],
  "out_of_scope": [
    "Redesigning the preferences interface."
  ],
  "test_commands": [
    ["pytest", "-q"]
  ],
  "base_branch": "main"
}
```

Response:

```json
{
  "job_id": "cpr-0001",
  "status": "queued"
}
```

The API must respond immediately after accepting the job.

## 13. Job states

```text
queued
evaluating_scope
needs_clarification
rejected
analyzing
planning
preparing_branch
implementing
testing
repairing
reviewing
committing
pushing
creating_pull_request
completed
failed
cancelled
```

A job in `needs_clarification` must stop until a later API capability is added or the issue is resubmitted more clearly.

The first release may simply return the clarification questions and require a new submission.

## 14. Job artifacts

Each run receives:

```text
runs/
└── cpr-0001/
    ├── request.json
    ├── issue.md
    ├── scope-evaluation.md
    ├── repository-summary.md
    ├── analysis.md
    ├── plan.md
    ├── implementation-log.md
    ├── test-output.txt
    ├── review.md
    ├── final-summary.md
    ├── pull-request-title.txt
    ├── pull-request-body.md
    ├── state.json
    ├── journal.jsonl
    ├── worker.log
    ├── prompts/
    └── responses/
```

Artifacts are the durable handoff between workflow stages.

Do not use an ever-growing chat transcript as the primary state.

## 15. Git workflow

For the first implementation, require a clean repository and use a dedicated branch.

```bash
git switch main
git pull --ff-only
git switch -c conjurepr/cpr-0001-terminal-font-size
```

ConjurePR must:

* never commit on the base branch;
* never push directly to the base branch;
* never force-push;
* never merge;
* never discard uncommitted user work;
* never automatically stash changes;
* stage only files intentionally changed by the job.

The first prototype may require a disposable or dedicated clone.

Git worktrees can be considered later only if they simplify running multiple ConjurePR service instances. They are not required for the first milestone.

## 16. Repository analysis

Inspect only enough information to solve the submitted issue.

Likely inputs include:

* top-level directory tree;
* README;
* contributor or agent instructions;
* package configuration;
* relevant source files;
* relevant tests;
* text-search results.

The analysis artifact should identify:

* current behavior;
* likely relevant files;
* intended change;
* risks;
* ambiguities;
* expected tests.

This stage must not perform a broad architectural review.

## 17. Planning

Produce a short, issue-sized plan.

A valid plan should normally contain only a few steps:

```text
1. Update the preferences model to store terminal font size.
2. Apply the setting when initializing the terminal widget.
3. Add persistence and validation tests.
4. Run the configured test suite.
```

Do not generate a project roadmap, architecture document, or extensive speculative design.

## 18. Implementation

Process the plan in controlled steps.

For each step:

1. inspect relevant files;
2. provide selected content to the model;
3. request a unified diff;
4. validate all affected paths;
5. apply the patch;
6. record changed files;
7. inspect the resulting diff.

Prefer unified diffs.

Allow whole-file replacement only for small files where doing so is clearly safer.

The model must not receive unrestricted shell access.

## 19. Testing and repair

Run the exact configured commands.

Example:

```text
pytest -q
python -m compileall src
```

Capture:

* command arguments;
* stdout;
* stderr;
* exit code;
* duration;
* timeout status.

When a command fails, provide the model with:

* the issue;
* plan;
* current diff;
* exact command output;
* remaining repair attempts.

Permit at most the configured number of repairs.

When repairs are exhausted, preserve the branch and artifacts and mark the job failed. Do not create a deceptively successful PR.

A later option may permit a clearly marked draft PR containing known failures, but this is not required initially.

## 20. Diff review

After tests pass, ask the model to review only the completed diff.

The review should check for:

* unmet acceptance criteria;
* unrelated changes;
* obvious regressions;
* missing tests;
* excessive complexity;
* accidental generated files;
* unsupported scope expansion.

Allow one final correction cycle.

Rerun tests after any correction.

The review stage is not an invitation to redesign surrounding code.

## 21. Finalization and draft PR

When the work passes validation and review:

1. identify intentionally changed files;
2. generate a concise commit message;
3. stage only those files;
4. commit;
5. push the branch;
6. generate a PR title and body;
7. create a draft pull request;
8. save the PR URL.

Verify GitHub CLI authentication:

```bash
gh auth status
```

Push:

```bash
git push -u origin <branch>
```

Create the PR:

```bash
gh pr create \
  --draft \
  --base main \
  --head <branch> \
  --title "<generated title>" \
  --body-file <generated body file>
```

A successful ConjurePR job ends with a draft PR URL.

## 22. Pull-request format

```markdown
## Requested change

Concise restatement of the submitted issue.

## What changed

Summary of the implementation.

## Acceptance criteria

- [x] Criterion verified
- [x] Criterion verified
- [ ] Criterion not verified, with explanation

## Files changed

Brief description of important files.

## Testing

- `pytest -q` — passed
- `python -m compileall src` — passed

## Notes for review

Specific areas that deserve human attention.

## Limitations

Anything uncertain, incomplete, or manually untested.

## ConjurePR job

- Job ID: `cpr-0001`
- Model: `qwen3-coder-next`
- Duration: ...
- Model calls: ...
```

Never fabricate test or acceptance results.

## 23. CLI

Initial commands:

```text
conjurepr serve
conjurepr health
conjurepr submit
conjurepr jobs
conjurepr show
conjurepr watch
conjurepr diff
conjurepr journal
conjurepr artifacts
conjurepr log
conjurepr cancel
```

Example:

```bash
conjurepr submit \
  --repo /data/projects/triagetty \
  --title "Add configurable terminal font size" \
  --issue-file issue.md \
  --test-command "pytest -q"
```

The CLI must communicate exclusively through HTTP.

Closing the CLI must not stop the job.

## 24. Cancellation and failure behavior

Queued jobs cancel immediately.

Running jobs set a cancellation flag checked between major operations.

Preserve all artifacts after cancellation or failure.

Failures must be visible through:

* job status;
* journal;
* log;
* final error artifact.

Do not automatically delete branches or modified files after failure.

## 25. Testing strategy

Automated tests must use a mocked LLM.

The ordinary test suite must not require a running model or GitHub account.

Test:

* API health;
* job submission;
* queue behavior;
* CLI HTTP calls;
* scope acceptance and rejection;
* state transitions;
* path safety;
* artifact generation;
* repair limits;
* cancellation;
* Git branch creation;
* explicit staging;
* preservation of the base branch.

Use temporary Git repositories for integration tests.

GitHub PR creation may initially be tested through mocked `gh` command responses.

## 26. Implementation milestones

### Milestone 1: API-first skeleton

Deliver:

* Python package;
* configuration;
* FastAPI service;
* health endpoint;
* CLI HTTP client;
* logging;
* tests.

Success:

```bash
conjurepr serve
conjurepr health
```

### Milestone 2: Job submission and artifacts

Deliver:

* job model;
* queue;
* state files;
* journal;
* artifact directories;
* status endpoints.

Success:

A submitted job is visible through the API and CLI after the submitting command exits.

### Milestone 3: Scope, analysis, and planning

Deliver:

* scope evaluation;
* LLM connection;
* repository inspection;
* analysis and planning prompts;
* persisted prompts and responses.

Success:

ConjurePR accepts a small issue, rejects an oversized one, and produces a focused plan without changing code.

### Milestone 4: Branch and implementation

Deliver:

* clean-repository validation;
* worker branch creation;
* safe file operations;
* patch application;
* diff endpoint.

Success:

A small code change appears only on a ConjurePR branch.

### Milestone 5: Testing and repair

Deliver:

* configured command execution;
* output capture;
* repair prompt;
* bounded repair cycle.

Success:

ConjurePR detects a failing test and attempts a limited correction.

### Milestone 6: Review and commit

Deliver:

* final diff review;
* one optional correction;
* explicit staging;
* commit;
* summary and PR text.

Success:

A complete run leaves a tested, committed branch ready to push.

### Milestone 7: Draft pull request

Deliver:

* `gh` authentication validation;
* branch push;
* draft PR creation;
* PR URL in job status.

Success:

One small issue becomes one reviewable draft pull request.

## 27. First demonstration

Use a disposable clone of TriageTTY or a tiny test repository.

Choose a deliberately small issue, such as:

* improve one error message;
* add a `--version` option;
* correct one preference behavior;
* add validation for one invalid input;
* add one missing test.

The first demonstration succeeds when:

1. the service accepts the issue through its API;
2. the CLI exits;
3. ConjurePR continues working;
4. the scope gate accepts the issue;
5. a dedicated branch is created;
6. the code changes;
7. tests run;
8. the diff is reviewed;
9. the change is committed;
10. the branch is pushed;
11. a draft PR appears on GitHub;
12. `main` remains untouched;
13. Nick decides whether to merge.

## 28. Explicitly deferred

Do not implement:

* Flet or another GUI;
* web dashboard;
* external database;
* authentication;
* public network exposure;
* multiple active workers within one service;
* model switching per job;
* multiple-model review;
* agent personas;
* free-form tool loops;
* web research;
* architecture analysis;
* issue decomposition;
* greenfield generation;
* autonomous merge;
* deployment;
* release creation;
* notifications;
* scheduling;
* Apmatia integration;
* OpenIPE integration;
* GitLab, Gitea, or Forgejo support.

Multiple independent ConjurePR instances may eventually be run against separate repositories. That does not require turning one instance into a distributed orchestration system.

## 29. Coding guidance

Prefer:

* plain Python;
* FastAPI;
* explicit state;
* simple prompt templates;
* direct Git commands;
* file-based artifacts;
* short functions;
* clear logs;
* conservative error handling;
* behavior Nick can understand by reading the code.

Avoid:

* premature abstractions;
* generalized agent frameworks;
* dynamic free-form loops;
* deep inheritance;
* speculative plugins;
* broad application frameworks;
* unrequested architecture;
* direct CLI-to-core access;
* scope expansion.

## 30. Definition of done

ConjurePR’s first release is complete when Nick can:

1. start the local service;
2. configure one OpenAI-compatible model;
3. submit a small issue through the CLI;
4. close the terminal client;
5. return later;
6. inspect the workflow status and artifacts;
7. find a tested commit on a separate branch;
8. open a generated draft pull request;
9. review its summary, checks, and changed files;
10. merge or reject it himself.

The permanent product promise is:

> **Give ConjurePR one small, well-defined software issue. It will return one tested draft pull request for human review.**
