# Submit a test job

Create a small issue:

```bash
vi issue.md
```

Example:

```markdown
Add a `--version` option.

Acceptance criteria:

- The option prints the installed version.
- It exits successfully.
- Existing tests pass.
- Add a focused test where practical.

Out of scope:

- Redesigning the CLI.
- Changing package structure.
- Updating unrelated documentation.
```

Submit:

```bash
conjurepr submit \
  --repository example_project \
  --issue-file issue.md
```

Monitor:

```bash
conjurepr jobs
conjurepr show <job-id>
conjurepr watch <job-id>
conjurepr journal <job-id>
conjurepr diff <job-id>
conjurepr artifacts <job-id>
```

Previous: [Verify the API](19-verify-api.md)  
Next: [Verify isolation](21-verify-isolation.md)  
Index: [Installation path](00-index.md)

