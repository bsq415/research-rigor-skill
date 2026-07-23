#!/usr/bin/env python3
"""Create or verify a portable SHA-256 manifest for a deliberate artifact package."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
from typing import Iterable


SCHEMA_VERSION = 1
DEFAULT_EXCLUDES = (
    "*.tmp",
    "*.lock",
    "__pycache__/*",
    "**/__pycache__/*",
    "*.pyc",
)


def _excluded(relative: str, patterns: Iterable[str]) -> bool:
    path = PurePosixPath(relative)
    return any(fnmatch.fnmatch(relative, pattern) or path.match(pattern) for pattern in patterns)


def _sha256_stable(path: Path) -> tuple[str, int]:
    before = path.stat()
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise RuntimeError(f"file changed while hashing: {path}")
    return digest.hexdigest(), after.st_size


def _iter_files(
    root: Path,
    patterns: tuple[str, ...],
    manifest_path: Path | None,
) -> list[tuple[str, Path]]:
    result: list[tuple[str, Path]] = []
    manifest_resolved = manifest_path.resolve() if manifest_path is not None else None
    for path in root.rglob("*"):
        if path.is_symlink():
            raise RuntimeError(f"portable package contains a symlink: {path}")
        if not path.is_file():
            continue
        if manifest_resolved is not None and path.resolve() == manifest_resolved:
            continue
        relative = path.relative_to(root).as_posix()
        if not relative or relative.startswith("../") or _excluded(relative, patterns):
            continue
        result.append((relative, path))
    return sorted(result)


def create_manifest(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    manifest = args.manifest.resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"artifact root is not a directory: {root}")
    if manifest.exists() and not args.replace:
        raise FileExistsError(f"manifest already exists: {manifest}; use --replace explicitly")

    patterns = tuple(dict.fromkeys((*DEFAULT_EXCLUDES, *args.exclude)))
    records = []
    for relative, path in _iter_files(root, patterns, manifest):
        digest, size = _sha256_stable(path)
        records.append({"path": relative, "bytes": size, "sha256": digest})
    if not records:
        raise RuntimeError("refusing to seal an empty artifact package")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "algorithm": "sha256",
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "root_label": root.name,
        "excludes": list(patterns),
        "files": records,
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    temporary = manifest.with_name(f".{manifest.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temporary, manifest)
    print(f"Sealed {len(records)} file(s) in {manifest}")
    return 0


def _canonical_record_path(raw: object) -> str:
    if not isinstance(raw, str) or not raw:
        raise ValueError("manifest path is empty or non-string")
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != raw:
        raise ValueError(f"manifest path is not canonical and relative: {raw!r}")
    return raw


def verify_manifest(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    manifest = args.manifest.resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"artifact root is not a directory: {root}")
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("manifest must contain an object")
    if payload.get("schema_version") != SCHEMA_VERSION or payload.get("algorithm") != "sha256":
        raise ValueError("unsupported manifest schema or algorithm")
    raw_records = payload.get("files")
    if not isinstance(raw_records, list) or not raw_records:
        raise ValueError("manifest files must be a nonempty list")

    expected: set[str] = set()
    errors: list[str] = []
    for raw in raw_records:
        if not isinstance(raw, dict) or set(raw) != {"path", "bytes", "sha256"}:
            errors.append("record schema mismatch")
            continue
        try:
            relative = _canonical_record_path(raw["path"])
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if relative in expected:
            errors.append(f"duplicate manifest path: {relative}")
            continue
        expected.add(relative)
        path = root / Path(relative)
        if not path.is_file() or path.is_symlink():
            errors.append(f"missing or nonportable file: {relative}")
            continue
        digest, size = _sha256_stable(path)
        if type(raw["bytes"]) is not int or raw["bytes"] != size:
            errors.append(f"byte count mismatch: {relative}")
        if not isinstance(raw["sha256"], str) or raw["sha256"].lower() != digest:
            errors.append(f"SHA-256 mismatch: {relative}")

    if args.strict:
        recorded_excludes = payload.get("excludes", [])
        if not isinstance(recorded_excludes, list) or not all(
            isinstance(item, str) for item in recorded_excludes
        ):
            errors.append("manifest excludes must be a list of strings")
            recorded_excludes = []
        patterns = tuple(dict.fromkeys((*recorded_excludes, *args.exclude)))
        observed = {
            relative for relative, _ in _iter_files(root, patterns, manifest)
        }
        missing = sorted(expected - observed)
        extra = sorted(observed - expected)
        errors.extend(f"strict manifest missing file: {item}" for item in missing)
        errors.extend(f"strict manifest has unrecorded file: {item}" for item in extra)

    if errors:
        for message in errors:
            print(f"ERROR: {message}")
        return 1
    print(f"Verified {len(expected)} file(s) against {manifest}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("create", "verify"):
        child = subparsers.add_parser(name)
        child.add_argument("root", type=Path)
        child.add_argument("manifest", type=Path)
        child.add_argument("--exclude", action="append", default=[])
    subparsers.choices["create"].add_argument("--replace", action="store_true")
    subparsers.choices["verify"].add_argument("--strict", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "create":
            return create_manifest(args)
        return verify_manifest(args)
    except (
        FileExistsError,
        FileNotFoundError,
        json.JSONDecodeError,
        OSError,
        RuntimeError,
        ValueError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
