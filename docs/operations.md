# Operations

## Update via Browser (MVP)
1. Start the service on the remote Windows Server.
2. Open `http://<server-ip>:3000/admin` in a browser.
3. Click **Update** to run `git pull --rebase` in the repo folder.

If `ADMIN_TOKEN` is set, append `?token=...` to the URL or send `x-admin-token` header.

## Environment Variables
- `PORT`: HTTP port, default `3000`
- `ADMIN_TOKEN`: optional admin token for `/admin`
- `REPO_DIR`: repo path for `git pull`, defaults to service working directory

## Service Management (Windows)
Use NSSM or Task Scheduler to keep the service running:
- `python src/server.py`
- On update, restart the service from the manager if needed.
