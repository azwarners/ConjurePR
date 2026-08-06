# Create the configuration file

Create:

```bash
sudo -u conjurepr \
  vi /srv/conjurepr/config/config.toml
```

Example:

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

Replace the example values.

After editing, make the production policy file root-owned and read-only to
the service account:

```bash
sudo chown root:conjurepr /srv/conjurepr/config/config.toml
sudo chmod 0640 /srv/conjurepr/config/config.toml
sudo chown root:conjurepr /srv/conjurepr/config
sudo chmod 0750 /srv/conjurepr/config
```

The administrator must perform future policy edits. The `conjurepr` account
must be able to read this file but must not be able to replace the file or
modify repository allowlists, command profiles, branch restrictions, or
security settings.

Previous: [Store the GitHub token](11-store-token.md)  
Next: [Per-job clone layout](13-job-layout.md)  
Index: [Installation path](00-index.md)
