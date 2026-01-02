# PRD (Simple Mode)

## Background
- Remote Windows server can access vendor system via VPN.
- Local environment is primary dev and control center.
- Need fast iteration and simple remote updates.

## Users
- Operator: runs and maintains the remote service.
- Integrator: calls the public API from outside.

## Goals
- Provide a minimal public API to query trace codes.
- Keep updates simple and fast.
- Keep runtime stable on the remote server.

## Non-goals
- Full security/compliance in MVP.
- Complex platform automation.

## Core Features
- `/api/ping` health check.
- Trace lookup endpoint (TBD).
- Admin update + restart page.

## Success Metrics
- External requests return expected data within SLA.
- Update + restart works without manual file copy.
