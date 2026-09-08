# ConjurePR

**One bounded software issue in. One tested draft pull request out.**

ConjurePR is a small CLI-first pull-request orchestrator. It prepares a disposable repository workspace, delegates software-engineering work to [Redless](https://github.com/azwarners/Redless), verifies the resulting repository state, and creates a draft pull request for human review.

ConjurePR is intentionally not a general-purpose coding agent. It does not implement its own agent loop, model client, code-editing tools, repository-analysis tools, or repair loop.

## Architecture

```text
User / Apmatia / another application
              |
              v
          ConjurePR
              |
              +-- prepare disposable clone and worker branch
              +-- enforce ConjurePR job policy
              +-- invoke Redless
              +-- verify resulting Git state and configured checks
              +-- commit and push approved changes
              +-- create one draft pull request
                         |
                         v
                       GitHub

Redless
   |
   +-- performs the software-engineering task
   +-- may use Sidecaravan for reusable agent tools
```

The project boundaries are deliberate:

- **Sidecaravan** owns reusable machine-oriented capabilities such as Git, filesystem, search, repository-analysis, and other general tools.
- **Redless** performs reusable digital labor and owns the agentic execution loop.
- **Ysparr** handles reusable OpenAI-compatible model request/response transport.
- **ConjurePR** owns the policy and orchestration required to turn one bounded issue into one draft pull request.
- **Apmatia** may expose ConjurePR, Redless, Sidecaravan, and other applications to conversational agents and users.

## Why a CLI?

ConjurePR is intended to work equally well for a person at a shell prompt, an Apmatia agent, a script, or another local application. Its primary interface is therefore a command in `PATH`, with machine-readable output available for callers.

A permanent HTTP service is not part of the target architecture. Long-running or detached execution can be added later without requiring a continuously running server.

## Intended workflow

```text
Issue
  -> validate bounded request
  -> create disposable clone
  -> create conjurepr/* worker branch
  -> invoke Redless with the issue and workspace
  -> wait for Redless result
  -> inspect Git state
  -> enforce scope and protected-path policy
  -> run configured verification
  -> stage explicit files
  -> commit
  -> push worker branch
  -> create draft pull request
  -> stop
```

Redless decides **how to perform the work**. ConjurePR decides **whether the resulting work qualifies for a pull request**.

## Permanent safety rules

ConjurePR must never:

- modify the operator's normal working checkout;
- commit directly to the configured base branch;
- force-push;
- merge a pull request;
- silently expand the requested scope;
- trust an agent's claim when Git, command results, or GitHub can provide direct evidence;
- expose reusable agent tools that belong in Sidecaravan.

Repository content and issue text are untrusted input. ConjurePR policy remains authoritative.

## Current status

The repository currently contains the original API-first Phase 1 and durable-job Phase 2 implementation. That code predates the CLI-first Redless architecture and will be adapted rather than discarded where its state, artifact, journal, and job concepts remain useful.

The next implementation milestone is the architecture transition described in [BLUEPRINT.md](BLUEPRINT.md).

## Development installation

```bash
git clone https://github.com/azwarners/ConjurePR.git
cd ConjurePR
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

See [INSTALL.md](INSTALL.md) for the current development setup and dependency expectations.

## License

See [LICENSE](LICENSE).
