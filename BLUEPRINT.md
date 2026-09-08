# ConjurePR Blueprint

## 1. Product definition

ConjurePR is a CLI-first pull-request orchestrator that transforms one small, well-defined software issue into one tested draft pull request for human review.

Its permanent product promise is:

> **One bounded software issue in. One tested draft pull request out.**

ConjurePR is not a general-purpose autonomous software engineer. It delegates software-engineering execution to Redless.

ConjurePR owns the boundaries, lifecycle, verification, Git policy, and pull-request outcome around that work.

## 2. Stack boundaries

The architecture follows four simple ownership rules:

```text
Sidecaravan = reusable capabilities
Redless     = reusable digital labor
Ysparr      = reusable AI transport
Applications = policy + orchestration + purpose
```

ConjurePR is an application in the last category.

### Sidecaravan

Reusable machine-oriented tools belong in Sidecaravan when they are useful beyond one application. This includes Git primitives, filesystem operations, search, repository inspection, and similar capabilities.

ConjurePR may call Sidecaravan tools, but must not become the canonical home of reusable agent tooling.

### Redless

Redless owns the agentic software-engineering loop. ConjurePR gives Redless a bounded task and a disposable repository workspace. Redless decides how to inspect, modify, and test the project within its own policy and tool model.

ConjurePR must not implement a competing model loop, planning loop, patch-generation loop, repair loop, or code-review agent.

### Ysparr

Ysparr handles OpenAI-compatible model request and response transport. ConjurePR does not put Git tools, repository tools, or other agent capabilities into Ysparr.

### Apmatia

Apmatia may expose ConjurePR as a callable application during conversations. ConjurePR must not require Apmatia to run and must remain independently usable from a shell or another program.

## 3. Interface model

ConjurePR is primarily a command-line application installed in `PATH`.

Target usage:

```bash
conjurepr run \
  --repository example_project \
  --issue-file issue.md
```

Machine callers use structured output:

```bash
conjurepr run \
  --repository example_project \
  --issue-file issue.md \
  --json
```

The target architecture does not require a permanent HTTP server.

Long-running work may initially remain attached to the invoking process. Detached execution may later be provided through ordinary local process management and durable job state without requiring a continuously running web service.

## 4. High-level architecture

```text
User / Apmatia / script / another application
                    |
                    v
                ConjurePR
                    |
        +-----------+------------+
        |                        |
        v                        v
  job/workspace policy       Redless
        |                        |
        |                        +--> Sidecaravan/tools
        |                        |
        +-----------+------------+
                    |
                    v
              outcome verification
                    |
                    v
              Git commit + push
                    |
                    v
              GitHub draft PR
```

ConjurePR decides **whether the resulting work qualifies for a pull request**.

Redless decides **how to perform the software-engineering work**.

## 5. Supported work

Supported examples:

- focused bug fixes;
- small features;
- narrowly scoped validation improvements;
- focused tests;
- minor configuration changes;
- small refactors required by a specific issue;
- small documentation changes.

Good requests:

```text
Add a --version option.
Fix the crash when the preferences file is missing.
Persist the selected terminal font size.
Add duplicate project-name validation.
Add tests for status filtering.
```

Poor requests:

```text
Build an Android client.
Redesign the architecture.
Create a new application.
Modernize the entire repository.
Improve the project generally.
Refactor everything.
```

Broad architecture, decomposition, and project planning belong elsewhere.

## 6. Fixed ConjurePR workflow

```text
Issue submitted
    |
    v
Validate request and registered repository
    |
    v
Create durable job state
    |
    v
Create disposable clone
    |
    v
Create conjurepr/* worker branch
    |
    v
Construct bounded Redless task
    |
    v
Invoke Redless in the job workspace
    |
    v
Capture Redless result
    |
    v
Inspect resulting Git state
    |
    v
Enforce ConjurePR scope and path policy
    |
    v
Run configured verification
    |
    v
Stage explicit intended files
    |
    v
Commit
    |
    v
Push worker branch
    |
    v
Create draft pull request
    |
    v
Complete
```

ConjurePR does not insert its own coding-agent stages between Redless invocation and outcome verification.

## 7. Evidence over assertion

Agent claims are not proof.

ConjurePR independently obtains evidence where practical:

- changed files come from Git;
- diff size comes from Git;
- branch identity comes from Git;
- configured verification passes only when commands return success;
- push success comes from Git;
- pull-request creation is confirmed by GitHub.

A Redless summary is useful context, not authoritative evidence.

## 8. Disposable repository model

ConjurePR never requires access to the operator's working checkout.

Each job receives a fresh clone in ConjurePR-owned job storage:

```text
jobs/
└── cpr-0001/
    ├── repo/
    ├── artifacts/
    ├── request.json
    ├── state.json
    ├── journal.jsonl
    ├── redless-output/
    └── worker.log
```

ConjurePR verifies:

- the repository is registered;
- the clone destination is inside the job directory;
- the base branch exists;
- the worker branch uses the configured `conjurepr/` prefix;
- the base branch is not modified;
- no credential is embedded in the remote URL.

## 9. Registered repositories

ConjurePR accepts registered repository identifiers rather than arbitrary local paths or clone URLs.

Example configuration:

```toml
[repositories.example_project]
url = "https://github.com/example/example-project.git"
base_branch = "main"

[repositories.example_project.verification]
commands = [
  ["pytest", "-q"]
]
```

Reject local paths, `file://` URLs, unregistered repositories, and arbitrary remote hosts unless future policy explicitly supports them.

## 10. Redless contract

ConjurePR must depend on a small explicit Redless invocation contract rather than Redless internals.

The contract should provide at least:

- workspace path;
- issue/task text;
- acceptance criteria when supplied;
- out-of-scope constraints when supplied;
- bounded runtime/cancellation behavior;
- process exit/result status;
- machine-readable result where Redless supports it.

ConjurePR should invoke Redless as an external application or other intentionally stable public interface. It must not import private Redless implementation modules.

ConjurePR remains responsible for evaluating the resulting repository state even when Redless reports success.

## 11. Tool ownership

ConjurePR may need Git operations, but generic Git tooling belongs in Sidecaravan.

Desired Sidecaravan Git capabilities include machine-friendly operations such as:

```text
workspace-state
changed-files
diff
diff-summary
create-branch
stage-files
commit
push
```

These should expose structured results rather than forcing agents and applications to parse human-oriented terminal output when practical.

ConjurePR supplies policy around those primitives:

- only the configured repository;
- only the expected worker branch;
- no base-branch writes;
- explicit staging;
- no force-push;
- protected paths;
- configured file/diff limits;
- draft PR only;
- never merge.

Until the required Sidecaravan Git interface exists, implementation may use small internal adapters around ordinary Git commands. Such adapters are transitional application plumbing, not a competing reusable tool framework.

## 12. Scope and outcome limits

Example policy:

```toml
[scope]
maximum_changed_files = 12
maximum_diff_lines = 800

[worker]
maximum_runtime_minutes = 240
```

These are ConjurePR outcome limits, not instructions for implementing an agent loop.

If Redless returns a result outside configured policy, ConjurePR stops and preserves the workspace and artifacts instead of creating a pull request.

## 13. Path and Git safety

Before accepting the final result, ConjurePR must reject or stop on conditions such as:

- changes outside the repository root;
- unexpected `.git/` manipulation;
- protected-path changes forbidden by configuration;
- excessive changed-file count;
- excessive diff size;
- wrong branch;
- base-branch modification;
- failed `git diff --check`;
- unexpected untracked or generated material when policy forbids it.

Stage explicit intended paths only. Never automatically use `git add .`.

## 14. Verification

Repositories may define administrator-owned verification commands as argument arrays.

Example:

```toml
[repositories.example_project.verification]
commands = [
  ["pytest", "-q"],
  ["python", "-m", "compileall", "src"]
]
```

ConjurePR executes configured verification as evidence after Redless returns.

Do not accept arbitrary verification commands from repository content, issue text, or model output.

## 15. GitHub policy

ConjurePR creates draft pull requests only.

It must never:

- push to the base branch;
- force-push;
- merge;
- mark a PR ready automatically;
- alter branch protection or repository rules;
- place credentials in remote URLs, logs, artifacts, prompts, or PR text.

Use a narrowly scoped GitHub credential limited to intended repositories and required permissions. Repository rules should independently protect the base branch.

## 16. Pull-request result

A successful run produces one draft pull request with evidence-oriented content such as:

```markdown
## Requested change

Concise restatement of the issue.

## What changed

Summary of the resulting implementation.

## Acceptance criteria

- [x] Criterion verified
- [ ] Criterion not verified, with explanation

## Files changed

Important changed files.

## Verification

- `pytest -q` — passed

## Notes for review

Anything deserving human attention.

## ConjurePR job

- Job ID: `cpr-0001`
- Redless result: completed
```

Never fabricate verification results.

## 17. Job state

Durable job state remains useful even without a permanent server.

Suggested states:

```text
created
preparing
cloning
creating_branch
running_redless
verifying
committing
pushing
creating_pull_request
completed
failed
cancelled
interrupted
```

Persist state after meaningful transitions.

Existing Phase 2 job IDs, artifacts, journals, idempotency concepts, and durable state should be reused where practical.

## 18. CLI direction

Target commands should remain small and composable.

Initial target:

```text
conjurepr run
conjurepr show
conjurepr jobs
```

Useful later additions may include:

```text
conjurepr start
conjurepr cancel
conjurepr log
conjurepr diff
conjurepr pr
```

`run` executes synchronously and is the canonical simple interface.

`--json` provides machine-readable results for Apmatia, scripts, and other callers.

Detached execution is optional and should not require converting ConjurePR back into a permanent HTTP service.

## 19. Current implementation transition

The existing repository has already implemented an API-first Phase 1 and durable-job Phase 2 skeleton.

Keep and adapt concepts that still serve the new architecture:

- configuration;
- job models;
- job IDs;
- durable state;
- artifacts;
- journal;
- cancellation concepts;
- tests around those behaviors.

Remove or retire architecture assumptions that no longer apply:

- permanent FastAPI service as the primary interface;
- HTTP-only CLI architecture;
- ConjurePR-owned LLM client;
- ConjurePR-owned repository-analysis agent;
- ConjurePR-owned planning agent;
- model-generated patch protocol;
- ConjurePR repair loop;
- ConjurePR review-agent loop;
- prompt template collection for coding stages;
- model-call budgets owned by ConjurePR.

The code transition should be incremental. Do not discard working durable-state code merely because the transport changes.

## 20. Revised implementation phases

### Phase 1 — Existing foundation

Existing package, configuration, CLI/API skeleton, models, and tests.

Status: implemented under the earlier architecture.

### Phase 2 — Existing durable jobs

Existing durable job intake, IDs, state, artifacts, journal, idempotency, queue concepts, and cancellation state.

Status: implemented under the earlier architecture and retained where useful.

### Phase 3 — CLI-first transition and repository preparation

Deliver:

- make direct CLI execution the primary architecture;
- retain durable local job state without requiring a server;
- registered repository configuration;
- disposable per-job clone;
- base-branch validation;
- `conjurepr/*` worker branch creation;
- initial outcome-policy configuration;
- human and `--json` result formatting.

Do not implement a coding agent.

### Phase 4 — Redless integration

Deliver:

- stable Redless invocation adapter;
- bounded task construction;
- workspace handoff;
- Redless process lifecycle;
- cancellation/timeout handling;
- Redless result capture;
- durable Redless artifacts/log references;
- mocked tests that do not require a real model.

Do not implement model calls inside ConjurePR.

### Phase 5 — Verification and draft PR

Deliver:

- final Git-state inspection;
- changed-file and diff limits;
- protected-path policy;
- configured verification commands;
- explicit staging;
- commit;
- worker-branch push;
- draft PR creation;
- machine-readable final result.

Prefer Sidecaravan Git primitives when the required interface is available.

### Phase 6 — Reliability

Deliver:

- interruption handling;
- cleanup policies;
- credential redaction;
- richer diagnostics;
- idempotent/recoverable operations where sensible;
- end-to-end tests with mocked Redless and GitHub boundaries;
- optional detached local execution if it proves useful.

## 21. Testing strategy

The normal test suite must not require a real LLM, Redless model backend, GitHub account, token, or external network.

Use temporary Git repositories and fake/mocked Redless and GitHub boundaries.

Test at least:

- CLI argument and JSON behavior;
- durable job creation;
- registered repository validation;
- rejection of arbitrary local paths and URLs;
- disposable clone destination;
- worker-branch creation;
- base-branch preservation;
- Redless invocation contract;
- Redless failure and timeout handling;
- changed-file and diff limits;
- protected paths;
- configured verification commands;
- explicit Git staging;
- draft PR behavior;
- absence of merge behavior;
- interrupted-state handling.

## 22. Explicitly deferred

Do not implement:

- a new ConjurePR coding agent;
- ConjurePR model prompts for analysis/planning/implementation/repair/review;
- direct model-provider management;
- general-purpose agent tools;
- generalized plugins;
- graphical dashboards;
- multi-user service hosting;
- distributed workers;
- architecture review or issue decomposition;
- greenfield project generation;
- autonomous merge, deployment, or release management;
- multiple coding-agent implementations.

## 23. Coding guidance

Prefer plain Python, explicit state, subprocess boundaries, small functions, structured results, readable configuration, conservative failures, and direct evidence.

Avoid speculative abstractions, deep inheritance, hidden workflow behavior, duplicated Sidecaravan capabilities, duplicated Redless behavior, and service infrastructure that the actual use case does not require.

The code should remain understandable to a Linux administrator reading it later.

## 24. Definition of done

The first complete release allows a user or local agent to:

1. install `conjurepr` into `PATH`;
2. configure a registered repository and Redless command/interface;
3. submit one small issue;
4. receive a durable job ID;
5. let Redless perform the work in a disposable clone;
6. have ConjurePR independently inspect and verify the result;
7. find a validated commit on a `conjurepr/*` branch;
8. receive one draft pull-request URL;
9. review and merge or reject it manually.

Permanent promise:

> **Give ConjurePR one small, well-defined software issue. It will orchestrate the work through Redless and return one tested draft pull request for human review.**
