# Per-job clone layout

Every job should receive a fresh clone:

```text
/srv/conjurepr/jobs/cpr-0001/
├── repo/
├── artifacts/
├── prompts/
├── responses/
├── commands/
├── request.json
├── state.json
├── journal.jsonl
└── worker.log
```

Conceptual clone:

```bash
git clone \
  --origin origin \
  https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY.git \
  /srv/conjurepr/jobs/cpr-0001/repo
```

Worker branch:

```bash
git -C /srv/conjurepr/jobs/cpr-0001/repo \
  switch --create conjurepr/cpr-0001-example origin/main
```

ConjurePR must verify:

- clone destination remains inside the job directory;
- base branch exists;
- worker branch starts with `conjurepr/`;
- modifications happen only on the worker branch;
- clone remotes contain no embedded token.

Previous: [Create the configuration file](12-configuration.md)  
Next: [Command execution rules](14-command-execution.md)  
Index: [Installation path](00-index.md)

