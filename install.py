#!/usr/bin/env python3
"""Install the canonical Rigorous Research Assistant skill for Codex or Claude Code."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys


SKILL_NAME = "research-rigor"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Rigorous Research Assistant without overwriting an existing skill."
    )
    parser.add_argument("--host", choices=("codex", "claude-code"), required=True)
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument(
        "--project-dir",
        type=Path,
        help="Project root for a Claude Code project-scoped installation.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print source and destination without copying files.",
    )
    return parser.parse_args()


def destination(args: argparse.Namespace) -> Path:
    if args.host == "codex":
        if args.scope != "user":
            raise ValueError("Codex installation currently supports --scope user only.")
        codex_root = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        return codex_root / "skills" / SKILL_NAME

    if args.scope == "user":
        return Path.home() / ".claude" / "skills" / SKILL_NAME

    if args.project_dir is None:
        raise ValueError("--project-dir is required for Claude Code project scope.")
    project_root = args.project_dir.expanduser().resolve()
    if not project_root.is_dir():
        raise ValueError(f"Project directory does not exist: {project_root}")
    return project_root / ".claude" / "skills" / SKILL_NAME


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    source = repo_root / "skills" / SKILL_NAME

    if not (source / "SKILL.md").is_file():
        print(f"ERROR: canonical skill is missing: {source}", file=sys.stderr)
        return 2

    try:
        target = destination(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Source:      {source}")
    print(f"Destination: {target}")

    if target.exists():
        print(
            "ERROR: destination already exists; move or remove it deliberately before installing.",
            file=sys.stderr,
        )
        return 3

    if args.dry_run:
        print("Dry run only; no files copied.")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)

    invocation = "$research-rigor" if args.host == "codex" else "/research-rigor"
    print(f"Installed Rigorous Research Assistant. Invoke it with {invocation}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
