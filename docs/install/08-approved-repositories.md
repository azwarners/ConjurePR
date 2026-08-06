# Register approved repositories

ConjurePR should accept repository identifiers, not arbitrary local paths or user-supplied URLs.

Example configuration entries:

```toml
[repositories.example_project]
url = "https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY.git"
base_branch = "main"

[repositories.another_project]
url = "https://github.com/YOUR_GITHUB_USERNAME/ANOTHER_REPOSITORY.git"
base_branch = "main"
```

A job request should use:

```json
{
  "repository": "example_project",
  "issue": "Add a --version option."
}
```

Reject:

- local repository paths;
- `file://` URLs;
- arbitrary SSH hosts;
- unregistered repositories.

This prevents API callers from instructing ConjurePR to clone and execute code from an arbitrary source.

The repository registry and command profiles are production policy. Store the
configuration root-owned and readable but not writable by `conjurepr`.

Previous: [Install ConjurePR](07-install-conjurepr.md)  
Next: [Create a GitHub fine-grained token](09-github-token.md)  
Index: [Installation path](00-index.md)
