# Path and patch safety

Before applying a patch:

1. parse affected paths;
2. reject absolute paths;
3. reject traversal outside the repository;
4. resolve destinations against the repository root;
5. reject symlinks escaping the repository;
6. reject changes to `.git/`;
7. reject changes exceeding file or diff limits;
8. record intended files;
9. apply the patch;
10. compare actual changed files with intended files;
11. run `git diff --check`.

Protect `.github/workflows/` by default.

Workflow-file changes should require a deliberate future policy.

Previous: [Treat repository content as untrusted](15-untrusted-content.md)  
Next: [Create the systemd service](17-systemd-service.md)  
Index: [Installation path](00-index.md)

