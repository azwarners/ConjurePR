# Create a GitHub fine-grained token

Create a fine-grained personal access token limited to only the repositories ConjurePR may use.

Recommended repository permissions:

- **Contents: Read and write**
- **Pull requests: Read and write**

Avoid unrelated permissions such as:

- Administration
- Actions
- Codespaces
- Deployments
- Environments
- Pages
- Repository hooks
- Secrets
- Variables
- Workflows

Use an expiration date and rotate the token periodically.

## Important limitation

The permission required to push a worker branch can also authorize other Git content changes in the selected repository.

A fine-grained token cannot by itself express:

```text
allow conjurepr/* branches
deny main
```

Protect `main` separately with GitHub branch protection or a repository ruleset.

Previous: [Register approved repositories](08-approved-repositories.md)  
Next: [Protect the base branch](10-base-branch.md)  
Index: [Installation path](00-index.md)

