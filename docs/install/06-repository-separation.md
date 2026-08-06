# Verify separation from operator repositories

ConjurePR should not be able to read the operator's repository directory.

Example:

```bash
sudo -u conjurepr test -r /path/to/operator/repos \
  && echo "WARNING: conjurepr can read operator repositories" \
  || echo "OK: operator repositories are not readable"
```

Inspect path permissions and ACLs:

```bash
namei -l /path/to/operator/repos
getfacl -p /path/to/operator/repos
```

Do not solve an access failure by granting ConjurePR membership in the operator's groups.

The prototype assumes a trusted single-user host. `127.0.0.1` prevents remote
network access but does not authenticate local users or processes.

Previous: [Create the directory layout](05-directory-layout.md)  
Next: [Install ConjurePR](07-install-conjurepr.md)  
Index: [Installation path](00-index.md)
