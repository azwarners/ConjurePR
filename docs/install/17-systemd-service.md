# Create the systemd service

Create:

```bash
sudo vi /etc/systemd/system/conjurepr.service
```

Example:

```ini
[Unit]
Description=ConjurePR autonomous pull-request service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=conjurepr
Group=conjurepr

WorkingDirectory=/srv/conjurepr
ExecStart=/opt/conjurepr/venv/bin/conjurepr serve \
  --config /srv/conjurepr/config/config.toml

Restart=on-failure
RestartSec=5

NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=strict
ProtectHome=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
RestrictSUIDSGID=yes
LockPersonality=yes
CapabilityBoundingSet=
AmbientCapabilities=

ReadWritePaths=/srv/conjurepr
UMask=0077

CPUQuota=400%
MemoryHigh=32G
MemoryMax=48G
TasksMax=512
LimitNOFILE=4096

[Install]
WantedBy=multi-user.target
```

The resource values are examples. Adjust them for the host and project workloads.

Previous: [Path and patch safety](16-patch-safety.md)  
Next: [Start the service](18-start-service.md)  
Index: [Installation path](00-index.md)

