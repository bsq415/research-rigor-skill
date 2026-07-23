#!/usr/bin/env python3
"""Scan a release tree for likely identity, secret, path, and project-content leaks."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
from typing import Iterable


TEXT_EXTENSIONS = {
    "",
    ".bib",
    ".cfg",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".rst",
    ".sh",
    ".tex",
    ".toml",
    ".ts",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
BASE_PATTERNS = {
    "email": re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    "windows_user_path": re.compile(r"(?i)\b[A-Z]:\\Users\\[^\\\s\"'<>]+"),
    "unix_home_path": re.compile(r"(?<!\w)/(?:home|Users)/[^/\s\"'<>]+"),
    "orcid": re.compile(r"\b\d{4}-\d{4}-\d{4}-[\dX]{4}\b", re.IGNORECASE),
    "ipv4": re.compile(
        r"(?<!\d)(?:25[0-5]|2[0-4]\d|1?\d?\d)"
        r"(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}(?!\d)"
    ),
    "private_key_header": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws_access_key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "api_token": re.compile(r"\b(?:sk|rk|pk)-[A-Za-z0-9_-]{20,}\b"),
}
GENERIC_PATTERNS = {
    "windows_absolute_path": re.compile(r"(?i)\b[A-Z]:\\(?:[^\\\r\n\"'<>]+\\)*[^\\\r\n\"'<>]*"),
    "repository_url": re.compile(r"https?://(?:www\.)?(?:github|gitlab)\.com/[^\s)>\"]+"),
    "doi": re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE),
    "arxiv_id": re.compile(r"\barXiv:\s*\d{4}\.\d{4,5}(?:v\d+)?\b", re.IGNORECASE),
    "cloud_instance_id": re.compile(r"\bi-[0-9a-f]{8,17}\b", re.IGNORECASE),
}


def _load_deny_terms(args: argparse.Namespace) -> list[str]:
    terms = [item for item in args.deny_term if item]
    if args.denylist is not None:
        for line in args.denylist.read_text(encoding="utf-8-sig").splitlines():
            value = line.strip()
            if value and not value.startswith("#"):
                terms.append(value)
    return list(dict.fromkeys(terms))


def _candidate_files(root: Path) -> Iterable[tuple[Path, str]]:
    if root.is_file():
        yield root, root.name
        return
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if any(part in {".git", "__pycache__"} for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        yield path, path.relative_to(root).as_posix()


def scan(args: argparse.Namespace) -> dict:
    root = args.release_path.resolve()
    if not root.exists():
        raise FileNotFoundError(f"release path does not exist: {root}")

    patterns = dict(BASE_PATTERNS)
    if args.generic_release:
        patterns.update(GENERIC_PATTERNS)
    deny_terms = _load_deny_terms(args)
    for index, term in enumerate(deny_terms, start=1):
        patterns[f"deny_term_{index}"] = re.compile(re.escape(term), re.IGNORECASE)
    for index, term in enumerate(dict.fromkeys(args.deny_case_term), start=1):
        if term:
            patterns[f"deny_case_term_{index}"] = re.compile(re.escape(term))

    findings: list[dict[str, object]] = []
    scanned_files = 0
    for path, relative in _candidate_files(root):
        size = path.stat().st_size
        if size > args.max_bytes:
            findings.append(
                {
                    "file": relative,
                    "line": None,
                    "column": None,
                    "category": "unscanned_large_text",
                }
            )
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            findings.append(
                {
                    "file": relative,
                    "line": None,
                    "column": None,
                    "category": "unscanned_non_utf8_text",
                }
            )
            continue
        scanned_files += 1
        for line_number, line in enumerate(text.splitlines(), start=1):
            for category, pattern in patterns.items():
                for match in pattern.finditer(line):
                    findings.append(
                        {
                            "file": relative,
                            "line": line_number,
                            "column": match.start() + 1,
                            "category": category,
                        }
                    )

    categories = Counter(str(item["category"]) for item in findings)
    return {
        "ok": not findings,
        "release_label": root.name,
        "generic_release": args.generic_release,
        "scanned_files": scanned_files,
        "finding_count": len(findings),
        "categories": dict(sorted(categories.items())),
        "findings": findings,
        "note": (
            "Matched values are intentionally omitted. "
            "A clean scan does not prove anonymity; perform semantic review."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("release_path", type=Path)
    parser.add_argument("--generic-release", action="store_true")
    parser.add_argument("--deny-term", action="append", default=[])
    parser.add_argument(
        "--deny-case-term",
        action="append",
        default=[],
        help="case-sensitive fixed term, useful for acronyms that are ordinary words",
    )
    parser.add_argument("--denylist", type=Path)
    parser.add_argument("--max-bytes", type=int, default=10_000_000)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.max_bytes < 1:
        parser.error("--max-bytes must be positive")
    try:
        result = scan(args)
    except (FileNotFoundError, OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for finding in result["findings"]:
            location = finding["file"]
            if finding["line"] is not None:
                location += f":{finding['line']}:{finding['column']}"
            print(f"{location} [{finding['category']}]")
        if result["ok"]:
            print(f"Release scan passed across {result['scanned_files']} text file(s).")
        else:
            print(
                f"Release scan found {result['finding_count']} issue(s) "
                f"across {result['scanned_files']} scanned text file(s)."
            )
        print(result["note"])
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
