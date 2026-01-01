# Architecture

## Scope
A minimal HTTP API service that exposes a single health-style endpoint and a manual update page.

## Components
- Flask app: handles routing and JSON responses
- Update handler: runs a fixed `git pull --rebase` command

## Conventions
- JSON-only responses
- HTTP status codes reflect success or failure
- Paths are versioned with `/api` to keep room for future versions
