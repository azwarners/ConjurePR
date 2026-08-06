# Protect the base branch

For every approved repository, create a GitHub rule targeting `main`.

Recommended rules:

- require a pull request before merging;
- block direct pushes;
- block force pushes;
- block deletion;
- optionally require status checks;
- optionally require an approving review;
- do not list ConjurePR as a bypass actor.

Use three layers:

```text
Fine-grained token
  limits repositories and permission categories

GitHub branch rule
  protects main

ConjurePR application policy
  allows only conjurepr/* branches and draft PR creation
```

Previous: [Create a GitHub fine-grained token](09-github-token.md)  
Next: [Store the GitHub token](11-store-token.md)  
Index: [Installation path](00-index.md)

