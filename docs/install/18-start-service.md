# Start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now conjurepr.service
sudo systemctl status conjurepr.service
```

Follow logs:

```bash
sudo journalctl -u conjurepr.service -f
```

Check hardening:

```bash
systemd-analyze security conjurepr.service
```

Apply restrictions incrementally if development tools need adjustments. Document every relaxation.

Previous: [Create the systemd service](17-systemd-service.md)  
Next: [Verify the API](19-verify-api.md)  
Index: [Installation path](00-index.md)

