# API Design

## Base URL
- Local: `http://localhost:3000`

## Response Envelope
All responses are JSON.

Success:
```json
{
  "ok": true,
  "message": "...",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

Error:
```json
{
  "ok": false,
  "error": "NotFound",
  "message": "Route not found"
}
```

## Status Codes
- 200: success
- 404: route not found
