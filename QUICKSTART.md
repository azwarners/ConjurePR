# ConjurePR Quick Start

> **Purpose:** Get ConjurePR running quickly for evaluation.
>
> This setup prioritizes simplicity over isolation. ConjurePR runs with the permissions of your normal user account. Use it only with trusted repositories, small issues, and a narrowly scoped GitHub token.

This prototype also assumes a trusted single-user host. Binding the API to
`127.0.0.1` limits network exposure but does not authenticate other local
users or processes.
>
> For unattended or long-term use, follow [INSTALL.md](INSTALL.md).

## 1. What this quick start does

This guide runs ConjurePR as your normal user and stores its files under your home directory.

ConjurePR still:

- clones repositories into its own job directories;
- does not operate on your normal working checkout;
- creates `conjurepr/*` branches;
- opens draft pull requests;
- never merges automatically.

This guide does **not** provide the stronger isolation of a dedicated Linux service account.

## 2. Requirements

You need:

- Linux;
- Python 3.11 or newer;
- Git;
- GitHub CLI;
- access to an OpenAI-compatible LLM endpoint;
- a GitHub repository you are willing to use for testing.

Check the tools:

```bash
python3 --version
git --version
gh --version
```

## 3. Clone ConjurePR

```bash
git clone https://github.com/azwarners/ConjurePR.git
cd ConjurePR
```

## 4. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## 5. Create local directories

```bash
mkdir -p \
  ~/.config/conjurepr \
  ~/.local/share/conjurepr/jobs \
  ~/.local/share/conjurepr/cache \
  ~/.local/share/conjurepr/logs \
  ~/.local/share/conjurepr/state \
  ~/.local/share/conjurepr/credentials
```

Restrict access:

```bash
chmod 700 \
  ~/.config/conjurepr \
  ~/.local/share/conjurepr \
  ~/.local/share/conjurepr/credentials
```

## 6. Create a GitHub fine-grained token

Create a fine-grained personal access token limited to only the repositories ConjurePR may use.

Recommended repository permissions:

- **Contents: Read and write**
- **Pull requests: Read and write**

Avoid unrelated permissions such as:

- Administration
- Actions
- Secrets
- Variables
- Repository hooks
- Workflows

Use an expiration date.

## 7. Store the GitHub token

Create a token file:

```bash
install -m 0600 /dev/null \
  ~/.local/share/conjurepr/credentials/github-token
```

Edit it:

```bash
vi ~/.local/share/conjurepr/credentials/github-token
```

Place only the token in the file.

Do not commit this file.

## 8. Protect the base branch

The token permission needed to push feature branches may also permit broader repository writes.

Protect `main` using GitHub branch protection or a repository ruleset.

Recommended rules:

- require pull requests before merge;
- block direct pushes to `main`;
- block force pushes;
- block deletion;
- do not allow ConjurePR to bypass the rule.

Token permissions and branch protection are separate layers. Use both.

## 9. Create the configuration file

Create:

```bash
vi ~/.config/conjurepr/config.toml
```

Example:

```toml
[server]
host = "127.0.0.1"
port = 8765

[paths]
jobs = "~/.local/share/conjurepr/jobs"
cache = "~/.local/share/conjurepr/cache"
logs = "~/.local/share/conjurepr/logs"
state = "~/.local/share/conjurepr/state"

[llm]
base_url = "http://127.0.0.1:8080/v1"
model = "YOUR_MODEL_NAME"
api_key = ""
temperature = 0.2
max_tokens = 8192
timeout_seconds = 600

[github]
token_file = "~/.local/share/conjurepr/credentials/github-token"
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
test = [["pytest", "-q"]]
validate = [["python", "-m", "compileall", "src"]]

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

Replace:

- `YOUR_MODEL_NAME`
- `YOUR_GITHUB_USERNAME`
- `YOUR_REPOSITORY`

with real values.

## 10. Start ConjurePR

```bash
conjurepr serve \
  --config ~/.config/conjurepr/config.toml
```

Leave this terminal running.

In another terminal:

```bash
source .venv/bin/activate
conjurepr health
```

## 11. Prepare a small issue

Create:

```bash
vi issue.md
```

Example:

```markdown
Add a `--version` option to the command-line interface.

Acceptance criteria:

- `example-app --version` prints the installed version.
- The command exits successfully.
- Existing tests pass.
- Add a focused test where practical.

Out of scope:

- Redesigning the CLI.
- Changing packaging.
- Updating unrelated documentation.
```

## 12. Submit the job

```bash
conjurepr submit \
  --repository example_project \
  --issue-file issue.md
```

The CLI should return a job ID and exit.

ConjurePR continues working through the local API service.

## 13. Monitor the job

```bash
conjurepr jobs
conjurepr show <job-id>
conjurepr watch <job-id>
conjurepr journal <job-id>
conjurepr diff <job-id>
conjurepr artifacts <job-id>
```

A successful job should end with:

- a fresh clone in ConjurePR's job directory;
- a `conjurepr/*` branch;
- test results;
- a commit;
- a pushed branch;
- a draft pull request URL.

## 14. Review the result

On GitHub:

1. read the pull-request summary;
2. inspect the reported tests;
3. open **Files changed**;
4. review every changed file;
5. check for unrelated edits;
6. test the branch locally if needed;
7. merge only when satisfied.

ConjurePR must never merge automatically.

## 15. Quick-start safety rules

While using this simplified setup:

- do not run ConjurePR with `sudo`;
- use only trusted repositories;
- use small, explicit issues;
- keep the API bound to `127.0.0.1`;
- use a fine-grained token limited to selected repositories;
- protect `main`;
- do not allow arbitrary shell commands;
- do not leave it running unattended until you understand its behavior;
- do not point it at sensitive repositories during early testing.

## 16. Move to the recommended deployment

Once you are satisfied with the prototype, follow [INSTALL.md](INSTALL.md).

The recommended deployment uses:

- a dedicated `conjurepr` Linux account;
- a private service directory;
- systemd;
- tighter filesystem restrictions;
- resource controls;
- no access to the operator's normal repositories.
