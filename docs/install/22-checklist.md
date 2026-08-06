# Installation checklist

- [ ] ConjurePR runs as the `conjurepr` user.
- [ ] The account has no privileged supplementary groups.
- [ ] `/srv/conjurepr` is private.
- [ ] The account cannot read operator repositories.
- [ ] Application code under `/opt/conjurepr` is not writable by the service account.
- [ ] Only registered repositories are accepted.
- [ ] Every job uses a fresh clone.
- [ ] The GitHub token is repository-limited.
- [ ] The token has an expiration date.
- [ ] `main` is protected.
- [ ] ConjurePR is not a bypass actor.
- [ ] Direct pushes and force pushes to `main` are blocked.
- [ ] Draft PRs are mandatory.
- [ ] Automatic merging is disabled.
- [ ] Workflow-file changes are disabled by default.
- [ ] Commands use argument arrays.
- [ ] `shell=True` is never used.
- [ ] Test commands are configured and bounded.
- [ ] Paths and symlinks are validated.
- [ ] Diff and file limits are enforced.
- [ ] Model and command calls have finite timeouts.
- [ ] Cancellation terminates subprocess groups.
- [ ] Interrupted jobs are marked honestly.
- [ ] The API listens only on localhost.
- [ ] Logs and artifacts contain no credentials.

Previous: [Verify isolation](21-verify-isolation.md)  
Next: [Remaining limitations](23-limitations.md)  
Index: [Installation path](00-index.md)

