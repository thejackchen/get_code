# Design Mode (Improved Architecture)

## Goals
- Keep local-first control and build workflows.
- Minimize remote responsibilities and keep runtime stable.
- Enable fast iteration with safe, atomic-ish updates.
- Keep tech replaceable; focus on roles, boundaries, and lifecycle.

## Constraints and Assumptions
- Remote runtime is a Windows Server VM with VPN access to vendor systems.
- Local environment is the primary dev/build/control center.
- External access requires port forwarding/NAT; some ports may be blocked.
- Early stage values speed over full security/compliance.

## Design Principles
- Control plane stays local; remote is runtime-only.
- Deploy artifacts, not raw source, when possible.
- Updates must be observable and reversible.
- Keep a single, deterministic service entrypoint.
- Make rollback and recovery boring and fast.

## Proposed Architecture

### 1) Control Plane (Local)
- Source of truth: git repo.
- Build produces a versioned artifact (zip or folder) with a version file.
- Release metadata: version, build time, changelog, checksum.
- A simple “release push” script publishes artifacts.

### 2) Build Plane (Local or CI)
- Standard build step packages the service into an artifact.
- Artifacts are immutable; new version = new artifact.
- Output can be stored in GitHub Releases, a private file share, or S3.

### 3) Runtime Plane (Remote)
- A single runtime service that:
  - serves business APIs
  - provides minimal admin endpoints
  - reports version and health
- A lightweight updater that:
  - pulls the latest artifact
  - swaps active version atomically
  - restarts service reliably

## Runtime Layout (Remote)
```
D:\get_code
  \current -> D:\get_code\releases\20250102-001
  \releases
     \20250101-001
     \20250102-001
  \state
     version.json
  \logs
  start.bat
  update.bat
```

- `current` is a pointer (directory or symlink) to active release.
- `update.bat` fetches artifact, verifies checksum, updates `current`.
- `start.bat` always launches from `current`.

## Update Strategy (Improved)
- Update is staged:
  1) Download new artifact to `releases/`.
  2) Verify checksum.
  3) Switch `current` to new version.
  4) Restart service.
  5) If health check fails, rollback `current` to previous version.

This keeps updates atomic-ish and rollback simple.

## Restart Strategy (Reliable)
- Use one stable command to restart service.
- Prefer “spawn new process, then exit old” for minimal downtime.
- Task Scheduler is still used for boot-time start.

## Observability
- `/api/ping` returns version, uptime, and timestamp.
- `/admin/status` returns version and build metadata.
- Logs written to `logs/` with timestamps.

## Security (Deferred but Planned)
- Admin endpoints protected by token + IP allowlist.
- Rate limiting for public endpoints.
- Separate admin port from public API port.

## Recommended Phased Path

### Phase 0 (Now)
- Keep current service + one-click restart.
- Add version/uptime/health endpoint.

### Phase 1 (Stability)
- Introduce artifact packaging.
- Add update script with checksum verification.
- Keep a previous release for rollback.

### Phase 2 (Control Plane)
- Add local “release push” tool.
- Store release metadata and allow controlled deploys.

### Phase 3 (Security/Compliance)
- Admin auth, allowlist, logging, and audit trail.

## Why This Is Better
- Removes tight coupling to manual git pulls on the remote.
- Enables predictable rollbacks.
- Reduces human error during updates.
- Keeps remote minimal and local in control.
