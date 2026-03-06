# Generated skill template

Use this structure for each site-specific skill generated from a URL.

## Required frontmatter

```yaml
---
name: <domain>-api-operator
description: API-first integration skill for <domain>. Use when tasks target this website and must be executed through API calls. Use browser only for discovery and auth recovery. Store auth cache at ~/.<domain>-auth.yaml and refresh it from browser data when auth fails.
---
```

## Required body sections

1. `Overview`
2. `API-first rules`
3. `Target context` (URL, host, auth cache file name)
4. `Capability map` (link to `references/capability-map.md`)
5. `Auth lifecycle` (load cache -> call API -> browser recovery on auth fail -> save cache -> retry)
6. `Validation`

## Required auth behavior

1. Generate auth file name from the target host.
2. Use `~/.<host-slug>-auth.yaml` as the auth file location.
3. Read auth cache before API calls.
4. If auth is invalid, recover auth via browser tooling.
5. Overwrite auth cache after successful recovery.
6. Keep auth file permission at `0600`.

## Minimum generated files

- `SKILL.md`
- `README.md`
- `agents/openai.yaml`
- `scripts/auth_cache.py`
- `references/capability-map.md`
