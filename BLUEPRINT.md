# ConjurePR Blueprint

> **Implementation directive for Codex**
>
> Read this entire blueprint before changing code.
>
> Implement **Phase 2 only**.
>
> Stop and report when Phase 2 is complete.
>
> Do not begin Phase 3 without explicit approval.

---

## 1. Product definition

ConjurePR is an API-first autonomous coding service that transforms one small, well-defined software issue into one tested draft pull request for human review.

Its permanent product promise is:

> **One bounded software issue in. One tested draft pull request out.**

ConjurePR is intentionally narrow. It must not become a general-purpose autonomous software engineer.

It does not perform:

- greenfield project construction;
- broad architectural design or review;
- issue decomposition;
- open-ended codebase improvement;
- large migrations or sweeping refactors;
- generalized multi-agent collaboration;
- free-form autonomous tool use;
- deployment, release management, or autonomous merge.

Broader planning and orchestration belong to the user, Apmatia, OpenIPE, or other systems. ConjurePR executes one small issue and returns one draft pull request.

## 2. Core principles

### Single responsibility

ConjurePR exists to produce bounded pull requests.

### KISS

Prefer ordinary Python, explicit state, fixed stages, small modules, simple artifacts, and direct behavior.

### API first

Every client uses the HTTP API. The CLI is only the first client and must not import workflow, Git, repository, command, or model internals.

### Human approval

A successful job ends with a draft pull request. ConjurePR never merges automatically.

### Bounded autonomy

The service may work unattended, but only within configured limits.

### Evidence over assertion

The model's claims are never proof. Tests pass only when configured commands return success. Changed files are determined by Git. Pull-request creation must be confirmed by GitHub.

### Disposable remote clones

ConjurePR must never require access to the operator's working checkout. Every job begins by cloning an approved remote repository into ConjurePR-owned storage.

## 3. Supported work

Supported:

- focused bug fixes;
- small new features;
- narrowly scoped validation improvements;
- focused tests;
- minor configuration changes;
- small refactors required by a specific issue;
- small documentation changes directly associated with code changes.

Good issues:

```text
Add a --version option.
Fix the crash when the preferences file is missing.
Persist the selected terminal font size.
Add duplicate project-name validation.
Add tests for status filtering.
```

Unsupported:

```text
Build an Android client.
Redesign the architecture.
Create a new application.
Modernize the entire repository.
Rewrite all documentation.
Improve the project generally.
Refactor everything.
```


## 4. High-level architecture

```text
CLI
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
Fixed pull-request workflow
  ├── scope evaluator
  ├── LLM client
  ├── repository clone manager
  ├── workspace tools
  ├── patch validator
  ├── Git tools
  ├── command runner
  ├── artifact store
  └── journal
```

The first release supports:

- one local user;
- localhost access only;
- one configured OpenAI-compatible LLM;
- one active job at a time;
- multiple queued jobs;
- registered remote repositories;
- one fresh clone per job;
- file-based state and artifacts;
- GitHub integration;
- draft pull requests only.

The prototype assumes a trusted, single-user host. Binding the API to
localhost limits network exposure, but is not authentication: another local
user or process may still be able to reach it.

Do not introduce an external database, Redis, Celery, RabbitMQ, distributed workers, a GUI, public networking, user authentication, multi-user tenancy, or generalized plugins.

Network egress isolation is intentionally deferred. The prototype may reach
the configured LLM, GitHub, and other services available to its service
account. Future hardening may add egress filtering, no-network test sandboxes,
or per-job namespaces.

## 5. Runtime model

Start the service:

```bash
conjurepr serve
```

Default API:

```text
http://127.0.0.1:8765
```

Submit:

```bash
conjurepr submit   --repository example_project   --issue-file issue.md
```

The CLI sends an HTTP request and exits after acceptance. The server continues independently.

Monitoring commands:

```bash
conjurepr jobs
conjurepr show <job-id>
conjurepr watch <job-id>
conjurepr diff <job-id>
conjurepr journal <job-id>
conjurepr artifacts <job-id>
conjurepr cancel <job-id>
```

The CLI must never silently fall back to direct core access.

## 6. Fixed workflow

```text
Issue submitted
    ↓
Scope evaluation
    ↓
Prepare job directory
    ↓
Clone registered repository
    ↓
Create worker branch
    ↓
Repository analysis
    ↓
Short implementation plan
    ↓
Implement change
    ↓
Run configured tests and checks
    ↓
Limited repair loop
    ↓
Review final diff
    ↓
Optional final correction
    ↓
Commit
    ↓
Push worker branch
    ↓
Create draft pull request
    ↓
Complete
```

Ordinary Python controls the sequence. The LLM reasons inside stages. It cannot add stages, delegate work, browse freely, redesign the project, expand scope, grant itself tools, choose arbitrary commands, or change policy.


## 7. Scope evaluation

Possible results:

```text
accepted
needs_clarification
too_large
unsupported
```

The result includes:

- decision;
- concise explanation;
- likely affected area;
- ambiguities;
- issue-reduction advice when rejected.

A rejection is correct guardrail behavior, not application failure.

Enforce configured limits:

```toml
[scope]
maximum_changed_files = 12
maximum_diff_lines = 800

[worker]
maximum_runtime_minutes = 240
maximum_model_calls = 20
maximum_repair_attempts = 3
maximum_review_corrections = 1
maximum_command_seconds = 1200
```

When a limit is exceeded, stop, preserve artifacts, identify the limit, and recommend dividing the issue.

## 8. Registered repositories

ConjurePR accepts repository identifiers, not local paths or arbitrary URLs.

Example request:

```json
{
  "repository": "example_project",
  "title": "Add a version option",
  "issue": "Add a --version option.",
  "acceptance_criteria": [
    "The command prints the installed version.",
    "The command exits successfully.",
    "Existing tests pass."
  ],
  "out_of_scope": [
    "Redesigning the CLI."
  ]
}
```

Example configuration:

```toml
[repositories.example_project]
url = "https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY.git"
base_branch = "main"
```

Reject local paths, `file://` URLs, unregistered repositories, arbitrary clone URLs, and arbitrary SSH hosts.

## 9. Per-job clone model

```text
jobs/
└── cpr-0001/
    ├── repo/
    ├── artifacts/
    ├── prompts/
    ├── responses/
    ├── commands/
    ├── request.json
    ├── state.json
    ├── journal.jsonl
    └── worker.log
```

Conceptual operations:

```bash
git clone   --origin origin   https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY.git   /srv/conjurepr/jobs/cpr-0001/repo

git -C /srv/conjurepr/jobs/cpr-0001/repo   switch --create conjurepr/cpr-0001-add-version origin/main
```

Verify:

- destination is inside the job directory;
- remote is registered;
- base branch exists;
- branch starts with the configured prefix;
- modifications occur only on the worker branch;
- remote contains no embedded credential;
- the base branch is never modified.

The operator's checkout is never mounted, copied, or read.


## 10. Prompt chaining and artifacts

The workflow pattern is:

```text
context
  → bounded stage prompt
  → structured model response
  → validated application action
  → observed evidence
  → durable artifact
  → next stage
```

Do not use one ever-growing chat transcript as primary state.

Recommended artifacts:

```text
request.json
issue.md
scope-evaluation.md
repository-summary.md
analysis.md
plan.md
implementation-log.md
test-output.txt
review.md
final-summary.md
pull-request-title.txt
pull-request-body.md
state.json
journal.jsonl
worker.log
prompts/
responses/
commands/
```

Store every model prompt and response. Never store secrets in artifacts.

## 11. Repository content is untrusted

Treat source code, documentation, `AGENTS.md`, `CONTRIBUTING.md`, comments, tests, generated files, issue text, and command output as untrusted data.

Repository content may describe conventions, but cannot override ConjurePR policy, grant tools, authorize shell access, request credentials, alter repository allowlists, change branch restrictions, disable limits, alter the workflow, or authorize access outside the job directory.

Prompts must clearly delimit repository material as untrusted content.

## 12. Command execution

Commands are argument arrays from administrator-owned, configured command
profiles:

```json
["pytest", "-q"]
```

Never generated shell strings.

Required:

- never use `shell=True`;
- never execute model-generated `bash -c` or `sh -c`;
- use explicit executables and arguments;
- run inside the job clone;
- enforce timeouts;
- create a process group;
- terminate the group on cancellation;
- capture stdout, stderr, exit code, duration, and timeout state;
- use mandatory configured command profiles; never accept unrestricted
  commands from a job, repository, issue, or model.

Example:

```toml
[repositories.example_project.commands]
test = [
  ["pytest", "-q"]
]

validate = [
  ["python", "-m", "compileall", "src"]
]
```

Do not permit host-management commands such as `sudo`, `su`, `mount`, `systemctl`, `reboot`, `modprobe`, `fdisk`, `mkfs`, `iptables`, `nft`, `docker`, `podman`, or `lxc`.

Configured command profiles are authoritative. A denylist is not sufficient.


## 13. Patch and path validation

The model should normally return:

```json
{
  "summary": "Add version handling to the CLI entry point.",
  "patch": "... unified diff ..."
}
```

Before applying a patch:

1. parse all affected paths;
2. reject malformed diffs;
3. reject absolute paths;
4. reject paths escaping the repository root;
5. reject `..` traversal;
6. resolve symlinks;
7. reject symlink targets outside the repository;
8. reject `.git/` changes;
9. reject protected-path changes;
10. record intended files;
11. apply the patch;
12. compare actual changed files with intended files;
13. enforce file-count and diff-size limits;
14. run `git diff --check`.

Protect `.github/workflows/` by default.

## 14. Job states

```text
queued
evaluating_scope
needs_clarification
rejected
preparing
cloning
creating_branch
analyzing
planning
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
interrupted
```

Persist state after every meaningful transition.

## 15. Crash recovery

Full automatic resume is not required initially.

On startup:

1. find jobs left active;
2. mark them `interrupted`;
3. preserve clone and artifacts;
4. journal the interruption;
5. expose it through the API;
6. require resubmission or a later explicit restart feature.

Truthful interruption is preferred to uncertain resumption.

## 16. Cancellation

Provide:

```text
POST /api/jobs/{job_id}/cancel
```

Queued jobs cancel immediately. Active jobs set a cancellation flag. The workflow checks between operations. Running process groups are terminated. Model calls have finite timeouts. Late responses are discarded. Artifacts remain. Branches and clones are not automatically deleted.

## 17. Idempotency and concurrency

Support an optional `Idempotency-Key`. Repeated submission with the same key returns the original job.

The first version allows one globally active job. Additional jobs remain queued. Only one job per repository may enter execution at a time.

Do not build a distributed coordinator.


## 18. Git workflow

ConjurePR must:

- create a dedicated worker branch;
- stage only intended files;
- never automatically use `git add .`;
- never commit on the base branch;
- never push to the base branch;
- never force-push;
- never merge;
- never delete the branch automatically;
- never use the operator's checkout.

Suggested branch:

```text
conjurepr/cpr-0001-short-description
```

Before commit:

```bash
git status --short
git diff --check
git diff --stat
```

Stage explicit paths only. Use one concise commit in the first release.

## 19. GitHub credential model

Use a narrowly scoped GitHub credential:

- selected repositories only;
- Contents: Read and write;
- Pull requests: Read and write.

The token cannot independently express “worker branches allowed, main denied.” Protection therefore uses:

```text
Fine-grained token
  limits repositories and permission categories

GitHub branch rule
  protects main

ConjurePR application policy
  allows only conjurepr/* branches and draft PRs
```

Never merge, mark a PR ready automatically, force-push, push to `main`, alter branch rules, write secrets into remotes, or log tokens.

Deployment details belong in `INSTALL.md`, `QUICKSTART.md`, and
`docs/install/` until a separate security document exists.

## 20. Draft pull-request creation

A successful job:

1. commits validated changes;
2. pushes the worker branch;
3. generates a PR title and body;
4. creates a draft PR;
5. records the URL;
6. stops.

For GitHub authentication, read the token from the protected token file only
in the controller, pass it to GitHub CLI and Git subprocesses through a
short-lived environment or credential-helper setup, and never place it in a
remote URL, command-line argument, prompt, response, log, artifact, or PR
body. Clone and push remotes must remain ordinary credential-free GitHub URLs.
Use the same protected authentication flow for `gh auth status` and
`gh pr create`.

Conceptual commands:

```bash
git push -u origin <worker-branch>

gh pr create   --draft   --base main   --head <worker-branch>   --title "<generated title>"   --body-file <generated-body-file>
```

## 21. Pull-request format

```markdown
## Requested change

Concise restatement of the submitted issue.

## What changed

Summary of the implementation.

## Acceptance criteria

- [x] Criterion verified
- [ ] Criterion not verified, with explanation

## Files changed

Brief description of important files.

## Testing

- `pytest -q` — passed

## Notes for review

Areas deserving human attention.

## Limitations

Anything uncertain, incomplete, or manually untested.

## ConjurePR job

- Job ID: `cpr-0001`
- Model: `MODEL_NAME`
- Duration: ...
- Model calls: ...
```

Never fabricate results.


## 22. Initial API

Use FastAPI and JSON.

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
GET    /api/jobs/{job_id}/pull-request

POST   /api/jobs/{job_id}/cancel
```

Job submission returns immediately.

## 23. CLI

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
conjurepr pr
conjurepr cancel
```

The CLI communicates only over HTTP, supports a configurable API URL, reports server errors clearly, and never imports core execution modules.

## 24. Configuration

Use TOML.

```toml
[server]
host = "127.0.0.1"
port = 8765

[paths]
jobs = "/srv/conjurepr/jobs"
cache = "/srv/conjurepr/cache"
logs = "/srv/conjurepr/logs"
state = "/srv/conjurepr/state"

[llm]
base_url = "http://127.0.0.1:8080/v1"
model = "YOUR_MODEL_NAME"
api_key = ""
temperature = 0.2
max_tokens = 8192
timeout_seconds = 600

[github]
token_file = "/srv/conjurepr/credentials/github-token"
branch_prefix = "conjurepr/"
draft_pull_requests = true
allow_merge = false
allow_force_push = false
allow_base_branch_push = false
allow_workflow_file_changes = false

[repositories.example_project]
url = "https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY.git"
base_branch = "main"

[repositories.example_project.commands]
test = [
  ["pytest", "-q"]
]

validate = [
  ["python", "-m", "compileall", "src"]
]

[worker]
maximum_active_jobs = 1
maximum_runtime_minutes = 240
maximum_model_calls = 20
maximum_repair_attempts = 3
maximum_review_corrections = 1
maximum_command_seconds = 1200

[scope]
maximum_changed_files = 12
maximum_diff_lines = 800
```

In production, policy configuration and its containing directory must be
owned by root and readable but not writable by the `conjurepr` service
account. The service account may write job state and artifacts, but must not
be able to replace or change repository allowlists, command profiles, branch
restrictions, or security settings.

Environment variables may override secrets. Never commit credentials.


## 25. Suggested project structure

```text
ConjurePR/
├── pyproject.toml
├── README.md
├── BLUEPRINT.md
├── QUICKSTART.md
├── INSTALL.md
├── docs/
│   └── install/
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
│       ├── repositories.py
│       ├── clone_manager.py
│       ├── workspace.py
│       ├── patching.py
│       ├── git_tools.py
│       ├── github.py
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
```

Keep modules small. Do not create deep inheritance or speculative provider systems.

## 26. Module responsibilities

- `api.py`: routes, request validation, response models, error mapping. No workflow logic.
- `cli.py`: parse commands, make HTTP requests, display results. No core imports.
- `service.py`: create, list, retrieve, queue, cancel, and expose jobs and artifacts.
- `job_runner.py`: run one job, enforce repository concurrency, invoke workflow.
- `workflow.py`: fixed stages, transitions, limits, cancellation, completion.
- `scope.py`: evaluate scope and parse accepted, clarification, oversized, or unsupported results.
- `repositories.py`: load registered repositories and command profiles.
- `clone_manager.py`: create job clone, validate remote, create worker branch.
- `workspace.py`: list, read, search, validate paths, reject escapes.
- `patching.py`: parse, validate, and apply diffs; enforce limits.
- `llm_client.py`: call one OpenAI-compatible endpoint, save prompts and responses.
- `git_tools.py`: status, diff, changed files, explicit staging, commit, push.
- `github.py`: verify authentication, create draft PR, retrieve URL, never merge.
- `command_runner.py`: argument-array execution, timeout, process groups, cancellation.
- `artifacts.py`: create and manage job artifacts.
- `journal.py`: append ordered structured events.

## 27. Journal events

Suggested events:

```text
job_created
job_queued
job_started
scope_started
scope_completed
clone_started
clone_completed
branch_created
stage_started
stage_completed
llm_request_started
llm_request_completed
patch_requested
patch_applied
file_modified
command_started
command_completed
repair_started
review_completed
commit_created
branch_pushed
pull_request_created
job_completed
job_failed
job_cancelled
job_interrupted
```


## 28. Testing strategy

The normal test suite must not require a real LLM, GitHub account, token, or network.

Mock LLM and GitHub interactions. Use temporary Git repositories.

Test:

- API health;
- CLI HTTP behavior;
- server-unavailable errors;
- job submission and idempotency;
- queue behavior;
- repository registration;
- rejection of local paths and arbitrary URLs;
- clone destination validation;
- branch creation and base-branch preservation;
- scope acceptance and rejection;
- path traversal and symlink escapes;
- protected paths;
- patch parsing and limits;
- argument-array commands;
- timeout and process-group cancellation;
- interrupted-state recovery;
- explicit Git staging;
- draft PR behavior;
- absence of merge behavior.

## 29. Implementation phases

### Phase 1: API-first skeleton

Deliver:

- Python package structure;
- `pyproject.toml`;
- configuration loading;
- FastAPI application;
- `GET /api/health`;
- CLI HTTP client;
- `conjurepr serve`;
- `conjurepr health`;
- logging foundation;
- basic request and response models;
- tests for the health endpoint and CLI health command.

Success:

```bash
conjurepr serve
```

starts the API, and:

```bash
conjurepr health
```

reaches it over HTTP.

The CLI must not import execution internals.

**Stop after Phase 1.**

Do not implement jobs, cloning, model calls, Git operations, command execution, or later milestones.

### Phase 2: Job submission and durable artifacts

Add job models, submission/list/detail endpoints, idempotency, run directories, state, journal, one-job queue, and cancellation state.

### Phase 3: Registered repositories and scope evaluation

Add repository configuration, rejection of local paths and arbitrary URLs, LLM connection, scope prompt, structured scope results, and model-call limits.

### Phase 4: Fresh clone and branch preparation

Add job clone directories, approved remote cloning, remote and base validation, and worker-branch creation.

### Phase 5: Analysis and planning

Add repository inspection, focused search and reads, repository summary, analysis, plan, and prompt/response storage.

### Phase 6: Patch implementation

Add structured model output, unified-diff validation, path and symlink safety, protected paths, patch application, limits, `git diff --check`, and diff endpoint.

### Phase 7: Testing and repair

Add configured command profiles, argument-array execution, timeouts, process-group cancellation, output capture, and bounded repair.

### Phase 8: Review and commit

Add final diff review, acceptance evaluation, one correction, retesting, explicit staging, commit, summary, and PR text.

### Phase 9: Push and draft pull request

Add GitHub authentication, worker-branch push, draft PR creation, PR URL storage, PR endpoint, and CLI `pr`.

### Phase 10: Reliability hardening

Add interruption handling, cleanup policies, credential redaction, repository concurrency enforcement, richer diagnostics, and end-to-end mocked tests.


## 30. First real demonstration

Use a disposable test repository or a deliberately small issue.

The full demonstration succeeds when:

1. the service starts;
2. the CLI submits through HTTP and exits;
3. scope accepts the issue;
4. the repository is cloned into ConjurePR-owned storage;
5. a worker branch is created;
6. analysis and plan artifacts are produced;
7. a patch is safely applied;
8. tests run;
9. bounded repairs occur if needed;
10. the final diff is reviewed;
11. the change is committed;
12. the branch is pushed;
13. a draft PR appears;
14. the base branch remains untouched;
15. the operator decides whether to merge.

## 31. Explicitly deferred

Do not implement:

- graphical interfaces or dashboards;
- external databases;
- public API exposure;
- authentication or multi-user support;
- multiple simultaneous workers;
- dynamic free-form agent loops;
- personas or multi-agent collaboration;
- architecture review or issue decomposition;
- project planning or greenfield generation;
- internet research;
- arbitrary command execution;
- autonomous merge, deployment, or releases;
- GitLab, Gitea, or Forgejo;
- model switching or multiple-model review;
- distributed orchestration;
- scheduling or notifications;
- Apmatia or OpenIPE integration.

## 32. Coding guidance

Prefer plain Python, FastAPI, explicit models, small functions, visible state, file artifacts, direct Git commands, clear logs, structured model responses, conservative failures, and readable code.

Avoid premature abstractions, generalized plugins, provider frameworks, deep inheritance, magical dependency injection, hidden workflow behavior, direct CLI-to-core access, arbitrary shells, broad refactors, and speculative features.

The code should be understandable to a Linux administrator reading it later.

## 33. Definition of done

The first complete release allows a user to:

1. start the service;
2. configure one model;
3. register one repository;
4. submit one small issue through the CLI;
5. close the CLI;
6. return later;
7. inspect status, journal, prompts, responses, tests, logs, and diff;
8. find a tested commit on a `conjurepr/*` branch;
9. open the generated draft PR;
10. review and merge or reject it manually.

Permanent promise:

> **Give ConjurePR one small, well-defined software issue. It will return one tested draft pull request for human review.**

---

# Final instruction to Codex

Read this complete blueprint.

Implement **Phase 2 only**.

Do not implement cloning, LLM calls, Git operations, command execution, or
later workflow behavior yet. Phase 2 adds only durable job intake and
management state.

Keep the implementation minimal, API-first, tested, and readable.

When Phase 2 is complete:

1. run the tests;
2. summarize what was implemented;
3. list files changed;
4. report deviations or unresolved questions;
5. stop.

Do not begin Phase 3 without explicit approval.
