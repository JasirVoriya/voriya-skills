# Capability map template

Fill this table from browser discovery and API inspection.

| capability | ui path | method | endpoint | request contract | response contract | auth requirement | validation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| example-capability | Dashboard -> Action | POST | /api/example | JSON fields | 200 + JSON object | bearer token + csrf | smoke test id |

## Notes

- Keep endpoints and schemas synchronized with production behavior.
- Mark capabilities with no stable API as `unsupported-via-api`.
- Record auth artifacts needed by each endpoint (headers, cookies, query).
