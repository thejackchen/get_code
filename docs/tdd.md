# TDD (Simple Mode)

## Architecture Overview
- Local: source control and updates.
- Remote: single runtime service with VPN access.

## Components
- API service (Flask): public endpoints and admin update UI.
- Vendor adapter (planned): wraps vendor API calls.

## Runtime
- Single process on Windows Server.
- Task Scheduler for boot start.
- Update + restart triggers a process respawn.

## Interfaces
- `GET /api/ping`: health check.
- `POST /admin/oneclick`: update + restart.
- `POST /api/trace/lookup`: planned.

## Deployment
- Git pull + restart (current).
- Keep minimal dependencies to reduce failure surface.

## Observability
- Version, PID, uptime exposed in admin page.
