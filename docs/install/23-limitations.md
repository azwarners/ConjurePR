# Remaining limitations

This deployment significantly reduces risk, but it is not a complete sandbox.

Code running as `conjurepr` may still:

- access files owned by `conjurepr`;
- read the GitHub token;
- use available network access;
- consume host resources;
- contact accessible local services;
- interfere with other jobs owned by the same account.

Future hardening may include:

- separate controller and executor users;
- short-lived GitHub App tokens;
- per-job namespaces;
- no-network test sandboxes;
- transient systemd units;
- rootless containers;
- egress filtering;
- stronger cross-job isolation.

Network egress isolation is intentionally not part of the prototype. The
service may contact the configured LLM, GitHub, and other locally reachable
services. Treat this as a known limitation until egress filtering or a
no-network execution sandbox is implemented.

Previous: [Installation checklist](22-checklist.md)  
Next: [Permanent deployment principle](24-principle.md)  
Index: [Installation path](00-index.md)
