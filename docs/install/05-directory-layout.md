# Create the directory layout

```bash
sudo install -d -o conjurepr -g conjurepr -m 0700 \
  /srv/conjurepr/config \
  /srv/conjurepr/credentials \
  /srv/conjurepr/jobs \
  /srv/conjurepr/cache \
  /srv/conjurepr/logs \
  /srv/conjurepr/state
```

Verify:

```bash
sudo find /srv/conjurepr \
  -maxdepth 1 \
  -printf '%M %u:%g %p\n'
```

Expected owner:

```text
conjurepr:conjurepr
```

Expected access:

```text
0700
```

The initial directory ownership may be `conjurepr:conjurepr`, but the
production policy configuration will be changed to root-owned and read-only
after it is created. Job, cache, log, and state directories remain writable
only by the service account.

Previous: [Create the service account](04-service-account.md)  
Next: [Verify separation from operator repositories](06-repository-separation.md)  
Index: [Installation path](00-index.md)
