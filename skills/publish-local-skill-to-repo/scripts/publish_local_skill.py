#!/usr/bin/env python3
"""Publish a local skill folder into a target skills git repository."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
SKILL_NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,63})$")
IGNORE_PATTERNS = shutil.ignore_patterns(".git", ".DS_Store", "__pycache__", "*.pyc")


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=str(cwd), check=True)


def check_output(cmd: list[str], cwd: Path) -> str:
    return subprocess.check_output(cmd, cwd=str(cwd), text=True).strip()


def is_valid_repo_root(path: Path) -> bool:
    return path.is_dir() and (path / ".git").exists() and (path / "skills").exists()


def discover_repo_root_from_cwd() -> Path:
    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if is_valid_repo_root(candidate):
            return candidate
    raise ValueError(
        "Cannot infer repo root from current working directory. "
        "Pass --repo-root <path-to-target-repo>."
    )


def validate_repo_root(repo_root: Path) -> None:
    if not repo_root.exists() or not repo_root.is_dir():
        raise ValueError(f"Repository root does not exist: {repo_root}")
    if not (repo_root / ".git").exists():
        raise ValueError(f"Not a git repository: {repo_root}")
    if not (repo_root / "skills").exists():
        raise ValueError(f"Missing skills directory under repo root: {repo_root / 'skills'}")


def validate_source_skill(source_skill_dir: Path) -> None:
    if not source_skill_dir.exists() or not source_skill_dir.is_dir():
        raise ValueError(f"Source skill directory does not exist: {source_skill_dir}")
    if not (source_skill_dir / "SKILL.md").exists():
        raise ValueError(f"Source skill is missing SKILL.md: {source_skill_dir}")


def normalize_skill_name(raw_name: str) -> str:
    value = raw_name.strip().lower()
    value = re.sub(r"[^a-z0-9-]+", "-", value).strip("-")
    if len(value) > MAX_SKILL_NAME_LENGTH:
        value = value[:MAX_SKILL_NAME_LENGTH].rstrip("-")
    if not value or not SKILL_NAME_RE.match(value):
        raise ValueError(
            "Invalid skill name. Use lowercase letters, digits, and hyphens only."
        )
    return value


def publish_skill(source_skill_dir: Path, destination_skill_dir: Path) -> None:
    if destination_skill_dir.exists():
        shutil.rmtree(destination_skill_dir)
    destination_skill_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_skill_dir, destination_skill_dir, ignore=IGNORE_PATTERNS)


def commit_and_push(
    repo_root: Path,
    destination_skill_dir: Path,
    commit_message: str,
    no_push: bool,
    remote: str,
) -> bool:
    relative_skill_path = destination_skill_dir.relative_to(repo_root)
    run(["git", "add", str(relative_skill_path)], repo_root)

    staged_diff = subprocess.run(
        ["git", "diff", "--cached", "--quiet", "--", str(relative_skill_path)],
        cwd=str(repo_root),
        check=False,
    )
    if staged_diff.returncode == 0:
        return False

    run(["git", "commit", "-m", commit_message], repo_root)

    if no_push:
        return True

    current_branch = check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_root)
    if current_branch == "HEAD":
        raise ValueError("Detached HEAD. Checkout a branch before pushing.")
    run(["git", "push", remote, current_branch], repo_root)
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Publish a local skill into a target skills repository and push changes."
    )
    parser.add_argument(
        "--source-skill-dir",
        required=True,
        help="Path to the local skill directory to publish.",
    )
    parser.add_argument(
        "--target-skill-name",
        help="Optional target skill name. Defaults to source directory name.",
    )
    parser.add_argument(
        "--repo-root",
        help="Optional target repository root. Defaults to auto-detect from current working directory.",
    )
    parser.add_argument(
        "--commit-message",
        help="Optional commit message. Defaults to feat(skills): publish <skill-name>.",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Commit changes but do not push to remote.",
    )
    parser.add_argument(
        "--remote",
        default="origin",
        help="Remote name for push. Defaults to origin.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and print the publish plan without writing changes.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        source_skill_dir = Path(args.source_skill_dir).expanduser().resolve()
        repo_root = (
            Path(args.repo_root).expanduser().resolve()
            if args.repo_root
            else discover_repo_root_from_cwd()
        )

        validate_repo_root(repo_root)
        validate_source_skill(source_skill_dir)

        target_skill_name = normalize_skill_name(
            args.target_skill_name if args.target_skill_name else source_skill_dir.name
        )
        destination_skill_dir = (repo_root / "skills" / target_skill_name).resolve()

        if source_skill_dir == destination_skill_dir:
            raise ValueError(
                "Source and destination skill paths are identical. "
                "Use a source directory outside this repository path."
            )

        commit_message = (
            args.commit_message
            if args.commit_message
            else f"feat(skills): publish {target_skill_name}"
        )

        if args.dry_run:
            print(f"repo_root={repo_root}")
            print(f"source_skill_dir={source_skill_dir}")
            print(f"destination_skill_dir={destination_skill_dir}")
            print(f"commit_message={commit_message}")
            print(f"remote={args.remote}")
            print(f"push={'no' if args.no_push else 'yes'}")
            return 0

        publish_skill(source_skill_dir, destination_skill_dir)
        changed = commit_and_push(
            repo_root=repo_root,
            destination_skill_dir=destination_skill_dir,
            commit_message=commit_message,
            no_push=args.no_push,
            remote=args.remote,
        )

        print(f"published_skill_path={destination_skill_dir}")
        if not changed:
            print("No file changes detected after publish. Nothing committed.")
        elif args.no_push:
            print("Committed locally without pushing (per --no-push).")
        else:
            print("Committed and pushed successfully.")
        return 0

    except (ValueError, subprocess.CalledProcessError) as err:
        print(str(err), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
