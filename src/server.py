import json
import os
import subprocess
import time
from http import HTTPStatus
from urllib.parse import parse_qs, urlparse

from flask import Flask, jsonify, request, Response

app = Flask(__name__)

PORT = int(os.getenv("PORT", "3000"))
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")
REPO_DIR = os.getenv("REPO_DIR", os.getcwd())


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

    html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Remote Control</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2rem; }
      button { padding: 0.6rem 1rem; font-size: 1rem; }
      pre { background: #f4f4f4; padding: 1rem; }
    </style>
  </head>
  <body>
    <h1>Remote Control</h1>
    <p>Click to pull the latest code. Restart the service if needed.</p>
    <button id="update">Update</button>
    <pre id="output"></pre>
    <script>
      const btn = document.getElementById("update");
      const out = document.getElementById("output");
      btn.addEventListener("click", async () => {
        out.textContent = "Running update...";
        const params = new URLSearchParams(window.location.search);
        const token = params.get("token");
        const url = token ? `/admin/update?token=${encodeURIComponent(token)}` : "/admin/update";
        const resp = await fetch(url, { method: "POST" });
        const json = await resp.json();
        out.textContent = JSON.stringify(json, null, 2);
      });
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


@app.errorhandler(404)
def not_found(_):
    return (
        jsonify({"ok": False, "error": "NotFound", "message": "Route not found"}),
        404,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
