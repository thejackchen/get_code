# Design Notes

## Context and Goal
We need a minimal, reliable MVP service on a remote Windows Server that can:
- Accept requests from outside the LAN.
- Query a vendor system that is only reachable through VPN from the remote machine.
- Provide a simple one-click update/restart workflow for fast iteration.

## Background (Why This Approach)
- The vendor system is not exposed to the public internet.
- Only the remote machine can reach the vendor via VPN.
- PDA scanning happens inside the local network; we need a bridge to the vendor data.
- MVP must be quick to deploy and easy to update without manual file copying.

## Preconditions and Constraints
- Remote OS: Windows Server 2012 R2 (stable target).
- Python 3.8.x available on the server.
- Git installed on the server.
- Public access is via router NAT/port forwarding to the server.
- Port chosen must not be blocked by the ISP.

## High-Level Design
- **Remote API Service** (Flask): exposes simple HTTP endpoints to external callers.
- **Vendor Adapter** (planned): internal module to call the vendor system via VPN.
- **Admin UI**: browser-accessible update page with one-click update + restart.
- **Startup**: Windows Task Scheduler starts the service on boot.

## Data Flow (MVP)
1. External client sends request to remote API.
2. Remote API validates input and calls vendor adapter.
3. Vendor adapter queries vendor system through VPN.
4. API returns normalized response to external client.

## Update/Restart Flow (MVP)
1. Admin clicks **Update + Restart**.
2. Service runs `git pull` to fetch latest code.
3. Service spawns a new Python process and exits the old one.
4. New process serves requests (PID/Start Time change confirms restart).

## Operational Notes
- Use a non-standard public port (e.g., `35678`) to avoid ISP blocks.
- NAT forwards public `:35678` -> server `10.50.45.22:35678`.
- Windows firewall allows inbound TCP `35678`.
- Admin page shows version, uptime, PID, and start time for verification.

## Security (Deferred for MVP)
- Authentication and IP allowlist for admin endpoints.
- Rate limiting and audit logging.
- Caching and retry strategies for vendor calls.

## Next Steps
- Implement vendor adapter (protocol, fields, error handling).
- Add request validation and response normalization.
- Add authentication to `/admin` and business endpoints.
