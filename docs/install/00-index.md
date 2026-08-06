# Installation path

This is the complete ordered installation path. Read the modules in order; each module contains one installation step or concept.

1. [Installation philosophy](01-philosophy.md) — deployment principles and account/workspace separation.
2. [Optional TriageTTY companion](02-triagetty.md) — interactive help for following this guide.
3. [Requirements](03-requirements.md) — host, software, access, and repository prerequisites.
4. [Create the service account](04-service-account.md) — create and verify the locked system account.
5. [Create the directory layout](05-directory-layout.md) — create the private service directories.
6. [Verify separation from operator repositories](06-repository-separation.md) — check path access and ACLs.
7. [Install ConjurePR](07-install-conjurepr.md) — install the source and virtual environment.
8. [Register approved repositories](08-approved-repositories.md) — configure the repository allowlist.
9. [Create a GitHub fine-grained token](09-github-token.md) — limit the token to approved repositories.
10. [Protect the base branch](10-base-branch.md) — protect `main` with GitHub rules.
11. [Store the GitHub token](11-store-token.md) — create the credential file securely.
12. [Create the configuration file](12-configuration.md) — configure paths, LLM, GitHub, worker, and scope limits.
13. [Per-job clone layout](13-job-layout.md) — define fresh clone and artifact handling.
14. [Command execution rules](14-command-execution.md) — bound commands and subprocess behavior.
15. [Treat repository content as untrusted](15-untrusted-content.md) — keep repository data from changing policy.
16. [Path and patch safety](16-patch-safety.md) — validate paths, symlinks, patches, and limits.
17. [Create the systemd service](17-systemd-service.md) — install the service unit and hardening settings.
18. [Start the service](18-start-service.md) — enable, start, inspect, and incrementally adjust it.
19. [Verify the API](19-verify-api.md) — confirm health and localhost-only binding.
20. [Submit a test job](20-test-job.md) — submit and monitor a bounded example issue.
21. [Verify isolation](21-verify-isolation.md) — confirm clone, branch, credential, and host separation.
22. [Installation checklist](22-checklist.md) — confirm the complete deployment.
23. [Remaining limitations](23-limitations.md) — understand what this deployment does not isolate.
24. [Permanent deployment principle](24-principle.md) — the invariant for production deployment.

Previous: [Public entry point](../../INSTALL.md)  
Next: [Installation philosophy](01-philosophy.md)  
Index: this page
