# Installation philosophy

ConjurePR performs autonomous code changes and test execution.

It should not run with broad access to the operator's account.

The recommended deployment follows these principles:

- run ConjurePR as a dedicated Linux user;
- deny access to the operator's home and normal repositories;
- accept only registered remote repositories;
- create a fresh clone for every job;
- create only `conjurepr/*` branches;
- push only worker branches;
- create draft pull requests;
- protect `main` with GitHub rules;
- never merge automatically;
- keep the API bound to localhost.

The intended relationship is:

```text
Operator account
├── /home/operator/
└── /path/to/operator/repos/
    ├── project-a/
    ├── project-b/
    └── project-c/

ConjurePR service account
└── /srv/conjurepr/
    ├── config/
    ├── credentials/
    ├── jobs/
    ├── cache/
    ├── logs/
    └── state/
```

ConjurePR should not be able to read `/path/to/operator/repos`.

Previous: [Installation path](00-index.md)  
Next: [Optional TriageTTY companion](02-triagetty.md)  
Index: [Installation path](00-index.md)

