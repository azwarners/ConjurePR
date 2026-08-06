# Permanent deployment principle

> ConjurePR must never require access to the operator's working checkout.

It receives an approved remote repository, clones it into an application-owned disposable workspace, performs one bounded issue, pushes one worker branch, and opens one draft pull request for human review.

Previous: [Remaining limitations](23-limitations.md)  
Next: [Public entry point](../../INSTALL.md)  
Index: [Installation path](00-index.md)
