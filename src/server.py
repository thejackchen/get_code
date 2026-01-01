import os
import subprocess
import time
import threading
from http import HTTPStatus

from flask import Flask, jsonify, request, Response

app = Flask(__name__)

PORT = int(os.getenv("PORT", "3000"))
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")
REPO_DIR = os.getenv("REPO_DIR", os.getcwd())
RESTART_SCRIPT = os.getenv("RESTART_SCRIPT", os.path.join(REPO_DIR, "start.bat"))
RESTART_DELAY = int(os.getenv("RESTART_DELAY", "2"))
START_TIME = time.time()


def is_admin_authorized(req) -> bool:
    if not ADMIN_TOKEN:
        return True
    token = req.args.get("token") or req.headers.get("x-admin-token")
    return token == ADMIN_TOKEN


def run_update():
    command = ["git", "pull", "--rebase"]
    proc = subprocess.run(
        command,
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    output = "\n".join([proc.stdout, proc.stderr]).strip()
    if proc.returncode != 0:
        return {
            "ok": False,
            "error": "UpdateFailed",
            "message": f"Exit code {proc.returncode}",
            "output": output,
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    return {
        "ok": True,
        "message": "Update completed",
        "output": output,
    }, HTTPStatus.OK


def schedule_restart():
    if os.name == "nt":
        cmd = f'timeout /t {RESTART_DELAY} >nul & start "" "{RESTART_SCRIPT}"'
        subprocess.Popen(["cmd", "/c", cmd], cwd=REPO_DIR)
    else:
        subprocess.Popen([RESTART_SCRIPT], cwd=REPO_DIR)

    def _exit_soon():
        time.sleep(1)
        os._exit(0)

    threading.Thread(target=_exit_soon, daemon=True).start()


def get_version_info():
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=3,
        )
        version = proc.stdout.strip() if proc.returncode == 0 else "unknown"
    except Exception:
        version = "unknown"

    uptime_seconds = int(time.time() - START_TIME)
    return {
        "version": version,
        "uptime_seconds": uptime_seconds,
    }


@app.get("/api/ping")
def ping():
    return jsonify(
        {
            "ok": True,
            "message": "pong",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
    )


@app.get("/admin")
def admin_page():
    if not is_admin_authorized(request):
        return jsonify({"ok": False, "error": "Unauthorized", "message": "Invalid token"}), 401

    status = get_version_info()
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Remote Control</title>
    <style>
      body {{ font-family: Arial, sans-serif; margin: 2rem; }}
      button {{ padding: 0.6rem 1rem; font-size: 1rem; }}
      .info {{ margin-bottom: 1rem; }}
      pre {{ background: #f4f4f4; padding: 1rem; }}
    </style>
  </head>
  <body>
    <h1>Remote Control</h1>
    <div class="info">
      <div><strong>Version:</strong> {status["version"]}</div>
      <div><strong>Uptime:</strong> {status["uptime_seconds"]}s</div>
    </div>
    <p>Click once to update and restart.</p>
    <button id="oneclick">Update + Restart</button>
    <pre id="output"></pre>
    <script>
      const btn = document.getElementById("oneclick");
      const out = document.getElementById("output");
      const params = new URLSearchParams(window.location.search);
      const token = params.get("token");
      const withToken = (path) => token ? `${path}?token=${encodeURIComponent(token)}` : path;
      const run = async (label, path) => {
        out.textContent = label;
        const resp = await fetch(withToken(path), { method: "POST" });
        const json = await resp.json();
        out.textContent = JSON.stringify(json, null, 2);
      };
      btn.addEventListener("click", () => run("Updating and restarting...", "/admin/oneclick"));
    </script>
  </body>
</html>"""
    return Response(html, mimetype="text/html")


@app.post("/admin/update")
def admin_update():
    if not is_admin_authorized(request):
        return jsonify({"ok": False, "error": "Unauthorized", "message": "Invalid token"}), 401

    payload, status = run_update()
    return jsonify(payload), status


@app.post("/admin/restart")
def admin_restart():
    if not is_admin_authorized(request):
        return jsonify({"ok": False, "error": "Unauthorized", "message": "Invalid token"}), 401

    schedule_restart()
    return jsonify({"ok": True, "message": "Restart scheduled"}), 202


@app.post("/admin/update-and-restart")
def admin_update_and_restart():
    if not is_admin_authorized(request):
        return jsonify({"ok": False, "error": "Unauthorized", "message": "Invalid token"}), 401

    payload, status = run_update()
    if status != HTTPStatus.OK:
        return jsonify(payload), status

    schedule_restart()
    payload["message"] = "Update completed. Restart scheduled."
    return jsonify(payload), 202


@app.post("/admin/oneclick")
def admin_oneclick():
    return admin_update_and_restart()


@app.errorhandler(404)
def not_found(_):
    return (
        jsonify({"ok": False, "error": "NotFound", "message": "Route not found"}),
        404,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
