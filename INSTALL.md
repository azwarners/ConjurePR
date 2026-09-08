# ConjurePR Installation

ConjurePR is currently under active development. This guide covers the development installation for the CLI-first architecture.

## Requirements

You need:

- Linux;
- Python 3.11 or newer;
- Git;
- GitHub CLI (`gh`) for draft pull-request creation;
- Redless installed and callable through its supported public interface;
- access to the GitHub repositories you intend to use.

Sidecaravan is expected to become the canonical home of reusable Git and other machine-oriented tools used by ConjurePR and Redless. Until those interfaces are implemented, development may use small internal Git adapters.

## Install ConjurePR

```bash
git clone https://github.com/azwarners/ConjurePR.git
cd ConjurePR
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

For development work, keep the virtual environment active when invoking the current package entry point.

## Verify the package

Run the test suite:

```bash
pytest
```

The repository currently contains implementation from the earlier API-first Phase 1 and Phase 2 design. During the architecture transition, some current commands may still reflect that older interface until Phase 3 is implemented.

## Redless

ConjurePR's target architecture delegates software-engineering execution to Redless rather than calling an LLM directly.

Redless should be independently installed and usable before testing the future Phase 4 integration. ConjurePR will invoke Redless through a stable external/public interface and will not import Redless internals.

## GitHub authentication

Use a narrowly scoped GitHub credential with access only to repositories ConjurePR is allowed to operate on.

Recommended repository permissions are limited to what is required to push worker branches and create pull requests. Protect the configured base branch with GitHub repository rules so the ConjurePR credential cannot bypass normal review policy.

ConjurePR must never place credentials in repository remotes, logs, artifacts, prompts, Redless task text, or pull-request bodies.

## Repository policy

The target configuration registers repositories explicitly instead of accepting arbitrary local paths or clone URLs.

Conceptual example:

```toml
[repositories.example_project]
url = "https://github.com/example/example-project.git"
base_branch = "main"

[repositories.example_project.verification]
commands = [
  ["pytest", "-q"]
]
```

Each ConjurePR job will operate in a fresh disposable clone and a `conjurepr/*` worker branch.

## Target CLI

The primary interface will be a CLI command in `PATH`:

```bash
conjurepr run \
  --repository example_project \
  --issue-file issue.md
```

Machine callers such as Apmatia will be able to request structured output:

```bash
conjurepr run \
  --repository example_project \
  --issue-file issue.md \
  --json
```

A permanent ConjurePR HTTP server is no longer part of the target architecture.

## Production deployment

A dedicated service account, systemd unit, or detached-job mechanism may be useful later for unattended execution, but none is required to define the core application architecture.

The first complete release should work simply as a local CLI application installed in `PATH` and callable by a person, shell script, Apmatia agent, or another program.
