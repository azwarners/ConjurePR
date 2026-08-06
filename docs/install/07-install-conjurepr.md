# Install ConjurePR

Choose an installation directory outside the writable service home:

```bash
sudo install -d -m 0755 /opt/conjurepr
sudo chown "$USER":"$USER" /opt/conjurepr
```

Clone:

```bash
git clone https://github.com/azwarners/ConjurePR.git /opt/conjurepr/source
cd /opt/conjurepr/source
```

Create a virtual environment:

```bash
python3 -m venv /opt/conjurepr/venv
source /opt/conjurepr/venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

Return ownership to root after installation:

```bash
sudo chown -R root:root /opt/conjurepr
sudo chmod -R go-w /opt/conjurepr
```

The service account should be able to execute the installed application but not modify its source or virtual environment.

Previous: [Verify separation from operator repositories](06-repository-separation.md)  
Next: [Register approved repositories](08-approved-repositories.md)  
Index: [Installation path](00-index.md)

