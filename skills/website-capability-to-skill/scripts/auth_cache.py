#!/usr/bin/env python3
"""
Manage per-site auth cache files under ~/.<site>-auth.yaml.

This utility is intentionally generic so generated API-first skills can reuse it.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import yaml


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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
    normalized = normalize_url(raw_url)
    return urlparse(normalized).netloc.lower()


def host_slug(host: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", host.lower()).strip("-")
    return slug or "site"


def auth_path_for_url(raw_url: str) -> Path:
    host = extract_host(raw_url)
    return Path.home() / f".{host_slug(host)}-auth.yaml"


def parse_iso8601(value: str) -> datetime:
    normalized = value.strip().replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = dict(base)
    for key, patch_value in patch.items():
        base_value = result.get(key)
        if isinstance(base_value, dict) and isinstance(patch_value, dict):
            result[key] = deep_merge(base_value, patch_value)
        else:
            result[key] = patch_value
    return result


def load_doc(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        raise ValueError(f"Auth file must be a YAML mapping: {path}")
    return loaded


def write_doc(path: Path, payload: dict[str, Any]) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=False)
    os.replace(temp, path)
    os.chmod(path, 0o600)


def value_at_dot_path(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def auth_payload_present(doc: dict[str, Any]) -> bool:
    auth = doc.get("auth", {})
    if not isinstance(auth, dict):
        return False
    candidates = [
        auth.get("token"),
        auth.get("headers"),
        auth.get("cookies"),
        auth.get("query"),
    ]
    for item in candidates:
        if isinstance(item, dict) and item:
            return True
        if isinstance(item, str) and item.strip():
            return True
    return False


def build_probe_headers(doc: dict[str, Any]) -> dict[str, str]:
    auth = doc.get("auth", {})
    headers = dict(auth.get("headers", {}) or {})
    token = auth.get("token")
    cookies = auth.get("cookies", {}) or {}
    if token and "Authorization" not in headers:
        headers["Authorization"] = f"Bearer {token}"
    if cookies and "Cookie" not in headers:
        headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())
    return {str(k): str(v) for k, v in headers.items()}


def probe_validation_endpoint(doc: dict[str, Any], timeout_seconds: int) -> tuple[bool, str]:
    validation = doc.get("validation", {})
    if not isinstance(validation, dict) or not validation.get("url"):
        return False, "validation.url is missing"
    url = str(validation["url"])
    method = str(validation.get("method", "GET")).upper()
    expected = validation.get("expect_status", [])
    if expected and not isinstance(expected, list):
        return False, "validation.expect_status must be a list"
    expected_set = {int(v) for v in expected} if expected else set()
    headers = build_probe_headers(doc)
    request = Request(url=url, method=method, headers=headers)
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            status = int(response.status)
            if expected_set and status not in expected_set:
                return False, f"probe status {status} not in expected {sorted(expected_set)}"
            if not expected_set and status >= 400:
                return False, f"probe status {status} indicates failure"
            return True, f"probe status {status}"
    except HTTPError as err:
        return False, f"probe failed with HTTP {err.code}"
    except URLError as err:
        return False, f"probe network error: {err.reason}"
    except Exception as err:  # pragma: no cover
        return False, f"probe exception: {err}"


def command_path(args: argparse.Namespace) -> int:
    print(auth_path_for_url(args.url))
    return 0


def command_read(args: argparse.Namespace) -> int:
    path = auth_path_for_url(args.url)
    doc = load_doc(path)
    if not doc:
        print(f"Auth cache not found: {path}", file=sys.stderr)
        return 1
    output = doc.get("auth", {}) if args.auth_only else doc
    if args.json:
        print(json.dumps(output, indent=2, sort_keys=False))
    else:
        print(yaml.safe_dump(output, sort_keys=False, allow_unicode=False).rstrip())
    return 0


def command_write(args: argparse.Namespace) -> int:
    path = auth_path_for_url(args.url)
    existing = load_doc(path)
    try:
        incoming_auth = json.loads(args.auth_json)
    except json.JSONDecodeError as err:
        print(f"Invalid --auth-json payload: {err}", file=sys.stderr)
        return 1
    if not isinstance(incoming_auth, dict):
        print("--auth-json must be a JSON object.", file=sys.stderr)
        return 1

    normalized_url = normalize_url(args.url)
    host = extract_host(args.url)
    created_at = value_at_dot_path(existing, "meta.created_at") if existing else None
    auth_section = incoming_auth
    if args.merge and existing:
        current_auth = existing.get("auth", {})
        if not isinstance(current_auth, dict):
            current_auth = {}
        auth_section = deep_merge(current_auth, incoming_auth)

    ttl_hours = args.ttl_hours
    expires_at = None
    if ttl_hours is not None:
        expires_at = (datetime.now(timezone.utc) + timedelta(hours=ttl_hours)).replace(
            microsecond=0
        ).isoformat()

    updated_doc = {
        "version": 1,
        "site": {
            "url": normalized_url,
            "host": host,
        },
        "auth": auth_section,
        "meta": {
            "created_at": created_at or now_utc_iso(),
            "updated_at": now_utc_iso(),
            "source": args.source,
            "expires_at": expires_at,
        },
        "validation": {
            "url": args.validation_url or value_at_dot_path(existing, "validation.url"),
            "method": (args.validation_method or value_at_dot_path(existing, "validation.method") or "GET").upper(),
            "expect_status": args.expect_status or value_at_dot_path(existing, "validation.expect_status") or [200],
        },
    }
    write_doc(path, updated_doc)
    print(path)
    return 0


def command_is_valid(args: argparse.Namespace) -> int:
    path = auth_path_for_url(args.url)
    doc = load_doc(path)
    reasons: list[str] = []
    if not doc:
        reasons.append(f"auth cache not found: {path}")
    else:
        if not auth_payload_present(doc):
            reasons.append("auth payload is empty")
        expires_at = value_at_dot_path(doc, "meta.expires_at")
        if expires_at:
            try:
                expiry = parse_iso8601(str(expires_at))
                if datetime.now(timezone.utc) >= expiry.astimezone(timezone.utc):
                    reasons.append(f"auth expired at {expires_at}")
            except ValueError:
                reasons.append(f"invalid meta.expires_at format: {expires_at}")
        for dotted in args.required_key:
            value = value_at_dot_path(doc, dotted)
            if value in (None, "", {}, []):
                reasons.append(f"missing required key: {dotted}")
        if args.http_check and not reasons:
            ok, message = probe_validation_endpoint(doc, args.timeout_seconds)
            if not ok:
                reasons.append(message)
            else:
                print(message)

    if reasons:
        for reason in reasons:
            print(reason, file=sys.stderr)
        return 1
    print("valid")
    return 0


def command_invalidate(args: argparse.Namespace) -> int:
    path = auth_path_for_url(args.url)
    if not path.exists():
        print(f"Auth cache not found: {path}", file=sys.stderr)
        return 1
    if args.backup:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup_path = path.with_suffix(path.suffix + f".{timestamp}.bak")
        path.replace(backup_path)
        print(backup_path)
        return 0
    path.unlink()
    print(path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage ~/.<site>-auth.yaml cache files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_path = subparsers.add_parser("path", help="Print auth cache file path for URL.")
    parser_path.add_argument("--url", required=True, help="Target website URL.")
    parser_path.set_defaults(func=command_path)

    parser_read = subparsers.add_parser("read", help="Read auth cache file.")
    parser_read.add_argument("--url", required=True, help="Target website URL.")
    parser_read.add_argument("--json", action="store_true", help="Print as JSON.")
    parser_read.add_argument("--auth-only", action="store_true", help="Print only auth section.")
    parser_read.set_defaults(func=command_read)

    parser_write = subparsers.add_parser("write", help="Write auth cache file.")
    parser_write.add_argument("--url", required=True, help="Target website URL.")
    parser_write.add_argument(
        "--auth-json",
        required=True,
        help="Auth payload as JSON object, for example: '{\"headers\": {...}}'.",
    )
    parser_write.add_argument(
        "--source",
        default="browser-recovery",
        help="Source label for the auth payload.",
    )
    parser_write.add_argument(
        "--ttl-hours",
        type=float,
        help="Optional TTL in hours from now.",
    )
    parser_write.add_argument(
        "--merge",
        action="store_true",
        help="Merge with existing auth payload instead of replacing it.",
    )
    parser_write.add_argument(
        "--validation-url",
        help="Optional API endpoint to probe during validity checks.",
    )
    parser_write.add_argument(
        "--validation-method",
        help="Validation endpoint HTTP method.",
    )
    parser_write.add_argument(
        "--expect-status",
        nargs="+",
        type=int,
        help="Expected probe HTTP status code(s).",
    )
    parser_write.set_defaults(func=command_write)

    parser_valid = subparsers.add_parser("is-valid", help="Check auth cache validity.")
    parser_valid.add_argument("--url", required=True, help="Target website URL.")
    parser_valid.add_argument(
        "--required-key",
        action="append",
        default=[],
        help="Dot path required in auth file, for example auth.headers.Authorization.",
    )
    parser_valid.add_argument(
        "--http-check",
        action="store_true",
        help="Call validation.url with current auth headers/cookies.",
    )
    parser_valid.add_argument(
        "--timeout-seconds",
        type=int,
        default=15,
        help="Timeout for --http-check probe call.",
    )
    parser_valid.set_defaults(func=command_is_valid)

    parser_invalidate = subparsers.add_parser(
        "invalidate", help="Delete or backup auth cache file."
    )
    parser_invalidate.add_argument("--url", required=True, help="Target website URL.")
    parser_invalidate.add_argument(
        "--backup",
        action="store_true",
        help="Rename cache file to timestamped .bak instead of deleting.",
    )
    parser_invalidate.set_defaults(func=command_invalidate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except ValueError as err:
        print(str(err), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
