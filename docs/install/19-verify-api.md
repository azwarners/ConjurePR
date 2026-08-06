# Verify the API

```bash
conjurepr health
```

The API should listen only on:

```text
127.0.0.1:8765
```

Verify:

```bash
ss -ltnp | grep 8765
```

Do not expose the prototype publicly.

This localhost-only design assumes a trusted single-user host. It limits
network exposure but does not authenticate other local users or processes.

Previous: [Start the service](18-start-service.md)  
Next: [Submit a test job](20-test-job.md)  
Index: [Installation path](00-index.md)
