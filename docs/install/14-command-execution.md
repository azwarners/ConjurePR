# Command execution rules

Commands must use argument arrays:

```json
["pytest", "-q"]
```

Never generated shell strings:

```text
pytest -q && curl ...
```

Required rules:

- never use `shell=True`;
- never execute model-generated `bash -c` or `sh -c`;
- use explicit executables and arguments;
- set the working directory inside the job clone;
- enforce timeouts;
- create a process group;
- terminate the process group on cancellation;
- capture stdout, stderr, exit code, duration, and timeout state;
- use mandatory, administrator-owned configured validation profiles; never
  accept unrestricted commands from a job, repository, issue, or model.

Do not permit host-management tools such as:

```text
sudo
su
mount
umount
systemctl
service
reboot
shutdown
modprobe
fdisk
parted
mkfs
iptables
nft
docker
podman
lxc
```

Configured command profiles are authoritative. A denylist alone is not a
security boundary.

Previous: [Per-job clone layout](13-job-layout.md)  
Next: [Treat repository content as untrusted](15-untrusted-content.md)  
Index: [Installation path](00-index.md)
