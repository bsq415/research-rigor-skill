#!/usr/bin/env python3
"""Create a private-by-default research control layer without overwriting files."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD_ROOT = SKILL_ROOT / "assets" / "project-scaffold"


def _relative_control_dir(raw: str) -> Path:
    value = Path(raw)
    if value.is_absolute() or ".." in value.parts or not value.parts:
        raise ValueError("--control-dir must be a relative path inside the project")
    return value


def _render(source: Path, replacements: dict[str, str]) -> str:
    text = source.read_text(encoding="utf-8")
    for token, value in replacements.items():
        text = text.replace(token, value)
    return text


def initialize(args: argparse.Namespace) -> int:
    if not SCAFFOLD_ROOT.is_dir():
        raise FileNotFoundError(f"missing bundled scaffold: {SCAFFOLD_ROOT}")

    project = args.project_directory.resolve()
    project.mkdir(parents=True, exist_ok=True)
    control = project / _relative_control_dir(args.control_dir)

    if control.exists() and not control.is_dir():
        raise FileExistsError(f"control path exists and is not a directory: {control}")
    if control.exists() and not args.merge:
        raise FileExistsError(
            f"research control layer already exists: {control}; "
            "use --merge to add only missing templates"
        )

    created_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    title = args.title.strip() if args.title else project.name
    if not title:
        raise ValueError("project title cannot be empty")
    replacements = {
        "__PROJECT_TITLE__": title,
        "__CREATED_UTC__": created_utc,
        "__DEEP_READ_MIN__": str(args.deep_read_min),
        "__FORENSIC_NEIGHBOR_MIN__": str(args.forensic_neighbor_min),
        "__INDEPENDENT_AUDIT_FRACTION__": str(args.independent_audit_fraction),
        "__PRIVACY_CLASSIFICATION__": args.classification,
        "__EXPORT_POLICY__": args.export_policy,
        "__EXECUTION_MODE__": args.mode,
    }

    control.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    skipped: list[str] = []
    for source in sorted(path for path in SCAFFOLD_ROOT.rglob("*") if path.is_file()):
        relative = source.relative_to(SCAFFOLD_ROOT)
        destination = control / relative
        if destination.exists():
            if args.merge:
                skipped.append(relative.as_posix())
                continue
            raise FileExistsError(f"refusing to overwrite: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(_render(source, replacements), encoding="utf-8", newline="\n")
        created.append(relative.as_posix())

    state_path = control / "research_state.json"
    if state_path.is_file():
        json.loads(state_path.read_text(encoding="utf-8"))

    print(f"Research control layer: {control}")
    print(f"Created {len(created)} file(s); skipped {len(skipped)} existing file(s).")
    for relative in created:
        print(f"  created {relative}")
    if skipped:
        print("Existing files were preserved:")
        for relative in skipped:
            print(f"  kept {relative}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_directory", type=Path)
    parser.add_argument("--title", help="human-readable project title; defaults to directory name")
    parser.add_argument("--control-dir", default=".research")
    parser.add_argument("--deep-read-min", type=int, default=300)
    parser.add_argument("--forensic-neighbor-min", type=int, default=30)
    parser.add_argument("--independent-audit-fraction", type=float, default=0.1)
    parser.add_argument(
        "--mode",
        choices=("guided", "full-cycle"),
        default="guided",
        help="guided waits for requested units; full-cycle continues through authorized gates",
    )
    parser.add_argument(
        "--classification",
        choices=("private", "internal", "public"),
        default="private",
    )
    parser.add_argument("--export-policy", default="sanitized-only")
    parser.add_argument(
        "--merge",
        action="store_true",
        help="add missing scaffold files while preserving every existing file",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.deep_read_min < 0:
        parser.error("--deep-read-min must be non-negative")
    if args.forensic_neighbor_min < 0:
        parser.error("--forensic-neighbor-min must be non-negative")
    if not 0 <= args.independent_audit_fraction <= 1:
        parser.error("--independent-audit-fraction must be between 0 and 1")
    try:
        return initialize(args)
    except (FileExistsError, FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
