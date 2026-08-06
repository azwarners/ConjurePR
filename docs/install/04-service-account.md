# Create the service account

Create a locked system account:

```bash
sudo useradd \
  --system \
  --create-home \
  --home-dir /srv/conjurepr \
  --shell /usr/sbin/nologin \
  conjurepr
```

Verify:

```bash
getent passwd conjurepr
id conjurepr
```

The account should not belong to privilege-bearing groups such as:

```text
sudo
wheel
docker
podman
libvirt
lxd
disk
adm
systemd-journal
```

Do not add the account to the operator's groups.

Previous: [Requirements](03-requirements.md)  
Next: [Create the directory layout](05-directory-layout.md)  
Index: [Installation path](00-index.md)

