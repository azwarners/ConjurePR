# Store the GitHub token

Create:

```bash
sudo install \
  -o conjurepr \
  -g conjurepr \
  -m 0600 \
  /dev/null \
  /srv/conjurepr/credentials/github-token
```

Edit:

```bash
sudo -u conjurepr \
  vi /srv/conjurepr/credentials/github-token
```

Place only the token in the file.

Verify permissions without printing it:

```bash
sudo stat \
  -c '%A %U:%G %n' \
  /srv/conjurepr/credentials/github-token
```

Expected:

```text
-rw------- conjurepr:conjurepr
```

Do not place the token in:

- repositories;
- configuration files;
- clone URLs;
- command-line arguments;
- prompts;
- responses;
- logs;
- artifacts;
- PR descriptions.

For clone, push, and GitHub CLI operations, ConjurePR should read this file
only in the controller and pass the token to child processes through a
short-lived protected environment or credential-helper setup. Git remotes
must use ordinary credential-free HTTPS URLs; never embed the token in a
remote, command-line argument, prompt, response, log, artifact, or PR body.
Use the same protected flow for `gh auth status` and `gh pr create`.

## Credential caveat

Code executing as the `conjurepr` user may be able to read files owned by that account, including this token.

The dedicated account protects the rest of the host. The fine-grained token and branch rules reduce the GitHub blast radius.

A later hardening phase may separate the credential-owning controller from untrusted job execution.

Previous: [Protect the base branch](10-base-branch.md)  
Next: [Create the configuration file](12-configuration.md)  
Index: [Installation path](00-index.md)
