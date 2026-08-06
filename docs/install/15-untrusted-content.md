# Treat repository content as untrusted

Issue text, source files, documentation, tests, comments, generated files, and command output are untrusted data.

Repository content may describe coding conventions, but it cannot:

- override ConjurePR policy;
- grant tools or shell access;
- request secrets;
- alter repository allowlists;
- change branch restrictions;
- disable scope limits;
- alter the fixed workflow;
- authorize access outside the job directory.

Previous: [Command execution rules](14-command-execution.md)  
Next: [Path and patch safety](16-patch-safety.md)  
Index: [Installation path](00-index.md)

