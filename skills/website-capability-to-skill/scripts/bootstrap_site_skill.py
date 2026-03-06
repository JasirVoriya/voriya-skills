#!/usr/bin/env python3
"""
Bootstrap a site-specific API-first skill from a target URL.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

MAX_SKILL_NAME_LENGTH = 64


def normalize_url(raw_url: str) -> str:
    value = raw_url.strip()
    if "://" not in value:
        value = f"https://{value}"
    parsed = urlparse(value)
    host = (parsed.netloc or parsed.path).strip()
    if not host:
        raise ValueError(f"Cannot parse host from URL: {raw_url}")
    if "@" in host:
        host = host.split("@", 1)[1]
    if ":" in host:
        host = host.split(":", 1)[0]
    path = parsed.path if parsed.netloc else ""
    normalized = f"{parsed.scheme or 'https'}://{host}{path}"
    if parsed.query:
        normalized = f"{normalized}?{parsed.query}"
    return normalized


def extract_host(raw_url: str) -> str:
    return urlparse(normalize_url(raw_url)).netloc.lower()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "site"


def default_skill_name(host: str) -> str:
    name = f"{slugify(host)}-api-operator"
    if len(name) <= MAX_SKILL_NAME_LENGTH:
        return name
    trimmed = name[:MAX_SKILL_NAME_LENGTH].rstrip("-")
    return trimmed or "site-api-operator"


def normalize_skill_name(skill_name: str) -> str:
    normalized = slugify(skill_name)
    if len(normalized) > MAX_SKILL_NAME_LENGTH:
        normalized = normalized[:MAX_SKILL_NAME_LENGTH].rstrip("-")
    if not normalized:
        raise ValueError("Skill name is empty after normalization.")
    return normalized


def title_case(slug: str) -> str:
    return " ".join(word.capitalize() for word in slug.split("-") if word)


def make_short_description(host: str) -> str:
    candidates = [
        f"Operate {host} via API with auth cache",
        f"API operator for {host} with auth cache",
        f"API workflow for {host}",
        "API workflow with auth cache",
    ]
    for candidate in candidates:
        if 25 <= len(candidate) <= 64:
            return candidate
    fallback = candidates[-1]
    if len(fallback) > 64:
        fallback = fallback[:64].rstrip()
    if len(fallback) < 25:
        fallback = "API skill with auth cache flow"
    return fallback


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def skill_md_template(skill_name: str, host: str, target_url: str) -> str:
    host_slug = slugify(host)
    title = title_case(skill_name)
    return f"""---
name: {skill_name}
description: API-first integration skill for {host}. Use when tasks target {host} website capabilities and must run through API calls. Use browser only for discovery and auth recovery. Store auth cache at ~/.{host_slug}-auth.yaml and refresh from browser data when auth fails.
---

# {title}

## Overview

Operate `{host}` via direct HTTP API calls. Use browser only to learn flows and
recover auth data.

## API-first rules

1. Execute business actions with API calls only.
2. Use browser only for discovery and auth recovery.
3. Read auth cache before API calls.
4. If auth fails, recover from browser artifacts and rewrite auth cache.

## Target context

- Target URL: `{target_url}`
- Target host: `{host}`
- Auth cache file: `~/.{host_slug}-auth.yaml` (auto-generated from host)

## Capability map

Maintain `references/capability-map.md` with endpoint mappings and keep it
updated when APIs change.

## Auth lifecycle

1. Resolve auth file path:
   `python3 scripts/auth_cache.py path --url "{target_url}"`
2. Read and validate auth before API calls:
   - `python3 scripts/auth_cache.py read --url "{target_url}"`
   - `python3 scripts/auth_cache.py is-valid --url "{target_url}"`
3. If API returns auth errors (`401`, `403`, token expired, session invalid):
   - Open website with browser tooling.
   - Complete login flow if needed.
   - Extract required auth artifacts from network/cookies/storage.
   - Save refreshed auth:
     `python3 scripts/auth_cache.py write --url "{target_url}" --auth-json '<json>' --source browser-recovery --ttl-hours 8`
4. Retry API once with refreshed auth.
5. If retry still fails, return blocked status and evidence.

## Validation

1. Verify each mapped capability through API without browser actions.
2. Mark unsupported capabilities explicitly in capability map.
3. Keep examples and endpoint contracts current.
"""


def readme_template(skill_name: str, host: str, target_url: str) -> str:
    host_slug = slugify(host)
    return f"""# {skill_name}

Generated API-first skill scaffold for `{host}`.

## Target context

- Target URL: `{target_url}`
- Target host: `{host}`
- Auth cache: `~/.{host_slug}-auth.yaml`

## Generated files

```text
{skill_name}/
  SKILL.md
  README.md
  agents/openai.yaml
  scripts/auth_cache.py
  references/capability-map.md
```

## Quick start

1. Update endpoint mappings in `references/capability-map.md`.
2. Read existing auth cache:
   `python3 scripts/auth_cache.py read --url "{target_url}"`
3. Validate auth before API calls:
   `python3 scripts/auth_cache.py is-valid --url "{target_url}"`
"""


def openai_yaml_template(display_name: str, short_description: str) -> str:
    return (
        "interface:\n"
        f"  display_name: {yaml_quote(display_name)}\n"
        f"  short_description: {yaml_quote(short_description)}\n"
    )


FALLBACK_CAPABILITY_MAP = """# Capability map

Fill this file with capability-to-endpoint mappings discovered from the target
website.

| capability | ui path | method | endpoint | request contract | response contract | auth requirement | validation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| example-capability | Dashboard -> Action | POST | /api/example | JSON body fields | 200 + JSON schema | bearer token + csrf | integration test id |
"""


def create_skill(args: argparse.Namespace) -> Path:
    target_url = normalize_url(args.url)
    host = extract_host(target_url)
    skill_name = normalize_skill_name(args.skill_name) if args.skill_name else default_skill_name(host)
    skill_dir = Path(args.output_root).resolve() / skill_name
    if skill_dir.exists():
        raise ValueError(f"Skill directory already exists: {skill_dir}")

    display_name = title_case(skill_name)
    short_description = make_short_description(host)

    (skill_dir / "agents").mkdir(parents=True, exist_ok=False)
    (skill_dir / "scripts").mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(parents=True, exist_ok=True)

    (skill_dir / "SKILL.md").write_text(
        skill_md_template(skill_name, host, target_url),
        encoding="utf-8",
    )
    (skill_dir / "README.md").write_text(
        readme_template(skill_name, host, target_url),
        encoding="utf-8",
    )
    (skill_dir / "agents" / "openai.yaml").write_text(
        openai_yaml_template(display_name, short_description),
        encoding="utf-8",
    )

    source_auth_cache = Path(__file__).resolve().with_name("auth_cache.py")
    destination_auth_cache = skill_dir / "scripts" / "auth_cache.py"
    if not source_auth_cache.exists():
        raise ValueError(f"Missing source auth cache script: {source_auth_cache}")
    shutil.copy2(source_auth_cache, destination_auth_cache)
    destination_auth_cache.chmod(0o755)

    source_capability_map = (
        Path(__file__).resolve().parents[1] / "references" / "capability-map-template.md"
    )
    destination_capability_map = skill_dir / "references" / "capability-map.md"
    if source_capability_map.exists():
        shutil.copy2(source_capability_map, destination_capability_map)
    else:
        destination_capability_map.write_text(FALLBACK_CAPABILITY_MAP, encoding="utf-8")

    return skill_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a site-specific API-first skill scaffold.")
    parser.add_argument("--url", required=True, help="Target website URL.")
    parser.add_argument(
        "--output-root",
        required=True,
        help="Root directory where the generated skill directory will be created.",
    )
    parser.add_argument(
        "--skill-name",
        help="Optional custom skill name (hyphen-case; defaults to <host>-api-operator).",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        skill_dir = create_skill(args)
    except ValueError as err:
        print(str(err), file=sys.stderr)
        return 1
    print(skill_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
