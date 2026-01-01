# Operations

## Update via Browser (MVP)
1. Start the service on the remote Windows Server.
2. Open `http://<server-ip>:<port>/admin` in a browser.
3. Click **Update + Restart** to pull code and restart the service.

If `ADMIN_TOKEN` is set, append `?token=...` to the URL or send `x-admin-token` header.

## Environment Variables
- `PORT`: HTTP port, default `3000`
- `ADMIN_TOKEN`: optional admin token for `/admin`
- `REPO_DIR`: repo path for `git pull`, defaults to service working directory
- `RESTART_SCRIPT`: restart script path, defaults to `start.bat` in `REPO_DIR`
- `RESTART_DELAY`: delay seconds before restart, default `2`
- `TASK_NAME`: Windows Task Scheduler task name, recommended for reliable restarts

## Service Management (Windows)
Use NSSM or Task Scheduler to keep the service running:
- `python src/server.py`
- On update, restart the service from the manager if needed.
