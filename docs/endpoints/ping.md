# GET /api/ping

## Description
Simple liveness check for the service.

## Request
No parameters.

## Response 200
```json
{
  "ok": true,
  "message": "pong",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Response 404
```json
{
  "ok": false,
  "error": "NotFound",
  "message": "Route not found"
}
```
