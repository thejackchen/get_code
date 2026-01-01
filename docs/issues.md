# Issues Log

## Summary
This file records the problems encountered during setup and the resolutions.

## Issues
1) **Git push authentication failure**
- Symptom: `fatal: could not read Username for 'https://github.com'`.
- Cause: GitHub no longer accepts account passwords for HTTPS push.
- Fix: Use a Personal Access Token (PAT) or credential manager.

2) **Win7 incompatible Node.js installers**
- Symptom: Node installer blocked on Windows 7.
- Cause: Newer Node.js versions do not support Windows 7.
- Fix: Moved runtime to Python 3.8.10 on Windows Server 2012 R2.

3) **Git not found on server**
- Symptom: `git` command not found.
- Cause: Git not installed or not on PATH.
- Fix: Install Git for Windows and reopen PowerShell.

4) **Commands pasted on one line**
- Symptom: `findstr`/`curl`/`git` failures or mixed command errors.
- Cause: Multiple commands pasted into a single line in PowerShell.
- Fix: Execute commands one at a time, or use single-line commands with `;`.

5) **PowerShell `curl` confusion**
- Symptom: `curl` errors and timeouts in PowerShell.
- Cause: PowerShell `curl` is an alias to `Invoke-WebRequest`.
- Fix: Use `Invoke-WebRequest ... -UseBasicParsing` or browser test.

6) **Admin update not taking effect**
- Symptom: Admin page stayed on old version after update.
- Cause: Code pulled but process not restarted.
- Fix: Restart the service after update.

7) **Template syntax error**
- Symptom: `SyntaxError: f-string: expecting '}'` when starting server.
- Cause: f-string collided with `{}` in HTML/JS.
- Fix: Replaced f-string with placeholder replacement.

8) **Restart task name parsing**
- Symptom: `schtasks` errors with `"python auto"` (task name split).
- Cause: Quotes/spacing mishandled in scripts.
- Fix: Removed task-based restart flow.

9) **restart.bat corruption**
- Symptom: `@@echo off`, `tokens=5` parse errors.
- Cause: File written with bad escaping in PowerShell.
- Fix: Stop using complex batch parsing.

10) **Service not coming back after one-click**
- Symptom: After update, service stopped and did not restart.
- Cause: Restart flow depended on task scripts that failed.
- Fix: New approach spawns a new Python process and then exits the old one.

## Current Stable Approach
- Update: `git pull`
- Restart: One-click uses in-process restart (spawns new process and exits old).
- Startup: Windows Task Scheduler still used to start the service at boot.
