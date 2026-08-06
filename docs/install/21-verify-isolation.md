# Verify isolation

Confirm ConjurePR:

- created a fresh clone in `/srv/conjurepr/jobs`;
- created a `conjurepr/*` branch;
- modified only the clone;
- cannot read operator repositories;
- cannot push directly to `main`;
- cannot force-push;
- created only a draft PR;
- preserved job artifacts;
- did not expose the token in logs or remotes.

Check repository access:

```bash
sudo -u conjurepr test -r /path/to/operator/repos \
  && echo "WARNING" \
  || echo "OK"
```

Check clone remote:

```bash
sudo -u conjurepr \
  git -C /srv/conjurepr/jobs/<job-id>/repo remote -v
```

The token must not appear.

Previous: [Submit a test job](20-test-job.md)  
Next: [Installation checklist](22-checklist.md)  
Index: [Installation path](00-index.md)

