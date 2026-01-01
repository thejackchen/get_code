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
- `RESTART_TASK_NAME`: Windows Task Scheduler task name for restart-only task

## Service Management (Windows)
Use NSSM or Task Scheduler to keep the service running:
- `python src/server.py`
- On update, restart the service from the manager if needed.

## Recommended Reliable Restart (Windows)
Create a separate restart task that kills the listener on port 35678 and starts `start.bat`.

`D:\\get_code\\restart.bat`:
```bat
@echo off
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :35678 ^| findstr LISTENING') do set PID=%%a
if defined PID taskkill /F /PID %PID%
timeout /t 2 >nul
D:\get_code\start.bat
```

Create the restart task (one-time):
```bat
schtasks /create /tn "get_code_restart" /tr "D:\get_code\restart.bat" /sc ONCE /st 00:00 /f
```

Then set environment variable:
```
RESTART_TASK_NAME=get_code_restart
```
