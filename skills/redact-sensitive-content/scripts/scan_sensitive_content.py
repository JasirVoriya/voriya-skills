#!/usr/bin/env python3
"""Scan Markdown content for obvious sensitive information patterns."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    hint: str


RULES = [
    Rule(
        name="email",
        pattern=re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        hint="Replace with a placeholder such as someone@example.com.",
    ),
    Rule(
        name="cn-mobile",
        pattern=re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)"),
        hint="Mask the middle digits, for example 138****5678.",
    ),
    Rule(
        name="private-ip",
        pattern=re.compile(
            r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})\b"
        ),
        hint="Replace with a generalized internal address such as 10.x.x.x.",
    ),
    Rule(
        name="internal-host",
        pattern=re.compile(r"\b[\w.-]+\.(?:internal|local|corp|lan)\b", re.IGNORECASE),
        hint="Replace with a neutral hostname such as internal.example.com.",
    ),
    Rule(
        name="filesystem-path",
        pattern=re.compile(r"(?:/Users/[\w.-]+/[\S]+|/home/[\w.-]+/[\S]+)"),
        hint="Replace with a generic path such as /path/to/project.",
    ),
    Rule(
        name="aws-access-key",
        pattern=re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
        hint="Never publish real cloud credentials.",
    ),
    Rule(
        name="github-token",
        pattern=re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
        hint="Replace with ***REDACTED***.",
    ),
    Rule(
        name="generic-api-key",
        pattern=re.compile(r"\b(?:sk|rk|pk)_[A-Za-z0-9_-]{16,}\b"),
        hint="Replace with a placeholder such as YOUR_API_KEY.",
    ),
    Rule(
        name="jwt-token",
        pattern=re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9._-]+\.[A-Za-z0-9._-]+\b"),
        hint="JWTs are credentials and must be removed or masked.",
    ),
    Rule(
        name="password-assignment",
        pattern=re.compile(r"(?i)\b(?:password|passwd|pwd|secret|token|apikey|api_key)\b\s*[:=]\s*['\"]?[^\s'\"`]{6,}"),
        hint="Do not publish assigned credentials; replace the value with a placeholder.",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan Markdown files for obvious sensitive information patterns."
    )
    parser.add_argument("paths", nargs="+", help="Markdown file or directory paths to scan.")
    return parser.parse_args()


def iter_markdown_files(raw_paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw_path in raw_paths:
        path = Path(raw_path).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"error: path does not exist: {path}")
        if path.is_dir():
            files.extend(sorted(candidate for candidate in path.rglob("*.md") if candidate.is_file()))
        elif path.is_file():
            if path.suffix.lower() != ".md":
                raise SystemExit(f"error: only Markdown files are supported: {path}")
            files.append(path)
    if not files:
        raise SystemExit("error: no Markdown files found")
    return files


def scan_file(path: Path) -> list[str]:
    findings: list[str] = []
    text = path.read_text(encoding="utf-8")
    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule in RULES:
            match = rule.pattern.search(line)
            if not match:
                continue
            snippet = match.group(0)
            if len(snippet) > 80:
                snippet = snippet[:77] + "..."
            findings.append(f"{path}:{line_number}: [{rule.name}] {snippet}\n  hint: {rule.hint}")
    return findings


def main() -> None:
    args = parse_args()
    files = iter_markdown_files(args.paths)
    findings: list[str] = []
    for path in files:
        findings.extend(scan_file(path))

    if findings:
        print("Potential sensitive content detected:\n")
        print("\n".join(findings))
        raise SystemExit(2)

    print("No obvious sensitive content detected.")


if __name__ == "__main__":
    main()
