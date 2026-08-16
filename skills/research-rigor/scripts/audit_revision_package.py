#!/usr/bin/env python3
"""Audit reviewer coverage, resubmission documents, and final-size figure records.

This is a structural and provenance audit. It does not judge scientific
correctness, citation relevance, response quality, or venue compliance.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
import sys
from typing import Any


REVIEW_FILE = "08_REVIEW_REMEDIATION.csv"
FIGURE_FILE = "07_FIGURE_AUDIT.csv"
RESPONSE_FILE = "08_RESPONSE_LETTER.md"
HIGHLIGHTS_FILE = "08_RESUBMISSION_HIGHLIGHTS.md"
COVER_FILE = "08_COVER_LETTER.md"

REVIEW_HEADERS = {
    "comment_id",
    "source",
    "source_record",
    "reviewer_request",
    "reviewer_intent",
    "type",
    "severity",
    "assessment",
    "scientific_validity",
    "action",
    "evidence_needed",
    "evidence_ids",
    "changed_locations",
    "change_evidence",
    "response_anchor",
    "regression_checks",
    "citation_checks",
    "unresolved_limitation",
    "status",
    "response_text",
}
FIGURE_HEADERS = {
    "figure_id",
    "claim_id",
    "content_type",
    "source_data",
    "generation_artifact",
    "final_asset",
    "final_render_evidence",
    "format",
    "vector_or_raster",
    "target_width",
    "effective_dpi",
    "required_min_dpi",
    "font_embedded_or_na",
    "legible_at_final_size",
    "line_and_marker_check",
    "color_independent",
    "crop_checked",
    "axis_integrity",
    "uncertainty_or_na",
    "caption_check",
    "final_render_checked",
    "status",
    "notes",
}

REVIEW_TYPES = {
    "evidence",
    "analysis",
    "clarification",
    "presentation",
    "citation",
    "policy",
    "out-of-scope",
}
SEVERITIES = {"info", "minor", "major", "fatal"}
ASSESSMENTS = {"valid", "partially_valid", "disputed", "not_applicable"}
REVIEW_STATUSES = {
    "open",
    "planned",
    "in_progress",
    "resolved",
    "accepted_limitation",
    "deferred_new_study",
    "out_of_scope",
}
TERMINAL_REVIEW_STATUSES = {
    "resolved",
    "accepted_limitation",
    "deferred_new_study",
    "out_of_scope",
}

FIGURE_TYPES = {
    "plot",
    "line_art",
    "diagram",
    "photo",
    "heatmap",
    "mixed",
    "table",
    "not_applicable",
}
FIGURE_KINDS = {"vector", "raster", "mixed", "not_applicable"}
FIGURE_STATUSES = {
    "planned",
    "in_progress",
    "passed",
    "failed",
    "waived",
    "not_applicable",
}
AXIS_STATES = {
    "zero_based",
    "full_range",
    "justified_truncation",
    "log_scale",
    "not_applicable",
}
VECTOR_FORMATS = {"pdf", "eps", "svg"}
RASTER_FORMATS = {"png", "tif", "tiff", "jpg", "jpeg"}
TRUE_VALUES = {"1", "true", "yes", "y", "verified", "passed"}
NA_VALUES = {"n/a", "na", "not_applicable", "not applicable"}
TEMPLATE_MARKER_RE = re.compile(
    r"\b(?:TBD|TODO|FIXME)\b|^\s*-\s*\[\s\]", re.IGNORECASE | re.MULTILINE
)


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.details: dict[str, Any] = {}

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def _control_root(raw: Path) -> tuple[Path, Path]:
    root = raw.resolve()
    if (root / "research_state.json").is_file():
        return root, root.parent
    control = root / ".research"
    if (control / "research_state.json").is_file():
        return control, root
    raise FileNotFoundError(
        f"could not find research_state.json in {root} or {control}"
    )


def _read_csv(path: Path, required: set[str], audit: Audit) -> list[dict[str, str]]:
    if not path.is_file():
        audit.error(f"missing required revision artifact: {path.name}")
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = set(reader.fieldnames or [])
            missing = required - headers
            if missing:
                audit.error(f"{path.name} is missing columns: {sorted(missing)}")
            return [dict(row) for row in reader]
    except (OSError, csv.Error) as exc:
        audit.error(f"cannot read {path.name}: {exc}")
        return []


def _truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in TRUE_VALUES


def _na(value: Any) -> bool:
    return str(value or "").strip().lower() in NA_VALUES


def _split_types(value: str) -> set[str]:
    return {
        item.strip().lower()
        for item in re.split(r"[|;]", value or "")
        if item.strip()
    }


def _unique_ids(
    rows: list[dict[str, str]], field: str, artifact: str, audit: Audit
) -> list[str]:
    values = [row.get(field, "").strip() for row in rows]
    if any(not value for value in values):
        audit.error(f"{artifact} contains a row without {field}")
    present = [value for value in values if value]
    if len(present) != len(set(present)):
        audit.error(f"{artifact} contains duplicate nonempty {field} values")
    return present


def _path_refs(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"[|;]", value or "") if item.strip()]


def _portable_existing(value: str, control: Path, project: Path) -> bool:
    refs = _path_refs(value)
    if not refs:
        return False
    for item in refs:
        if "://" in item:
            continue
        candidate = Path(item)
        if candidate.is_absolute() or ".." in candidate.parts:
            return False
        if not (control / candidate).exists() and not (project / candidate).exists():
            return False
    return True


def _require_fields(
    row: dict[str, str], fields: tuple[str, ...], label: str, audit: Audit
) -> None:
    for field in fields:
        if not row.get(field, "").strip():
            audit.error(f"{label} lacks {field}")


def _audit_review_rows(
    rows: list[dict[str, str]],
    response_text: str,
    control: Path,
    project: Path,
    strict: bool,
    expected_comments: int | None,
    audit: Audit,
) -> None:
    ids = _unique_ids(rows, "comment_id", REVIEW_FILE, audit)
    anchors: list[str] = []

    for row in rows:
        comment_id = row.get("comment_id", "").strip()
        label = f"review comment {comment_id!r}"
        _require_fields(
            row,
            (
                "source",
                "source_record",
                "reviewer_request",
                "reviewer_intent",
                "type",
                "severity",
                "assessment",
                "scientific_validity",
                "action",
                "response_anchor",
                "status",
            ),
            label,
            audit,
        )

        if row.get("source_record", "").strip() and not _portable_existing(
            row["source_record"], control, project
        ):
            audit.error(f"{label} has missing, absolute, or nonportable source_record")

        types = _split_types(row.get("type", ""))
        if not types or not types <= REVIEW_TYPES:
            audit.error(f"{label} has invalid type values: {sorted(types)}")

        severity = row.get("severity", "").strip().lower()
        if severity not in SEVERITIES:
            audit.error(f"{label} has invalid severity: {severity!r}")
        assessment = row.get("assessment", "").strip().lower()
        if assessment not in ASSESSMENTS:
            audit.error(f"{label} has invalid assessment: {assessment!r}")
        status = row.get("status", "").strip().lower()
        if status not in REVIEW_STATUSES:
            audit.error(f"{label} has invalid status: {status!r}")

        anchor = row.get("response_anchor", "").strip()
        if anchor:
            anchors.append(anchor)
            if response_text and anchor not in response_text:
                audit.error(f"{label} response_anchor is absent from {RESPONSE_FILE}")

        terminal = status in TERMINAL_REVIEW_STATUSES
        if strict and not terminal:
            audit.error(f"{label} is not terminal in strict mode: {status!r}")
        if terminal:
            _require_fields(row, ("response_text", "regression_checks"), label, audit)

        if types & {"evidence", "analysis"}:
            if not row.get("evidence_needed", "").strip():
                audit.error(f"{label} requests evidence or analysis but lacks evidence_needed")
            if status == "resolved" and not row.get("evidence_ids", "").strip():
                audit.error(f"resolved {label} lacks evidence_ids")

        if "citation" in types and terminal:
            if not row.get("citation_checks", "").strip():
                audit.error(f"terminal citation {label} lacks citation_checks")

        if status == "resolved":
            _require_fields(
                row, ("changed_locations", "change_evidence"), label, audit
            )
        elif status in {
            "accepted_limitation",
            "deferred_new_study",
            "out_of_scope",
        }:
            _require_fields(
                row, ("unresolved_limitation", "change_evidence"), label, audit
            )

        change_evidence = row.get("change_evidence", "").strip()
        if terminal and change_evidence and not _portable_existing(
            change_evidence, control, project
        ):
            audit.error(f"{label} has missing, absolute, or nonportable change_evidence")

    if len(anchors) != len(set(anchors)):
        audit.error(f"{REVIEW_FILE} contains duplicate nonempty response_anchor values")

    if expected_comments is not None:
        counted = sum(
            1
            for row in rows
            if row.get("source", "").strip().lower() != "self_initiated"
        )
        if counted != expected_comments:
            audit.error(
                f"expected {expected_comments} actionable comments, found {counted} "
                "non-self-initiated remediation rows"
            )

    audit.details["review_comment_ids"] = ids


def _number(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _audit_figure_rows(
    rows: list[dict[str, str]],
    control: Path,
    project: Path,
    strict: bool,
    audit: Audit,
) -> None:
    ids = _unique_ids(rows, "figure_id", FIGURE_FILE, audit)
    if strict and not rows:
        audit.error(
            f"strict mode requires figure audit rows or an explicit not_applicable row in {FIGURE_FILE}"
        )

    for row in rows:
        figure_id = row.get("figure_id", "").strip()
        label = f"figure audit {figure_id!r}"
        content_type = row.get("content_type", "").strip().lower()
        kind = row.get("vector_or_raster", "").strip().lower()
        status = row.get("status", "").strip().lower()

        if content_type not in FIGURE_TYPES:
            audit.error(f"{label} has invalid content_type: {content_type!r}")
        if kind not in FIGURE_KINDS:
            audit.error(f"{label} has invalid vector_or_raster: {kind!r}")
        if status not in FIGURE_STATUSES:
            audit.error(f"{label} has invalid status: {status!r}")

        if strict and status in {"planned", "in_progress", "failed"}:
            audit.error(f"{label} is not submission-ready in strict mode: {status!r}")

        if status in {"waived", "not_applicable"}:
            if not row.get("notes", "").strip():
                audit.error(f"{label} requires an explanatory note")
            if status == "not_applicable" and (
                content_type != "not_applicable" or kind != "not_applicable"
            ):
                audit.error(
                    f"{label} marked not_applicable must use not_applicable content and kind"
                )
            continue
        if status != "passed":
            continue
        if content_type == "not_applicable" or kind == "not_applicable":
            audit.error(f"passed {label} cannot use not_applicable content or kind")

        _require_fields(
            row,
            (
                "claim_id",
                "source_data",
                "generation_artifact",
                "final_asset",
                "final_render_evidence",
                "format",
                "target_width",
                "axis_integrity",
                "uncertainty_or_na",
            ),
            label,
            audit,
        )
        for field in (
            "source_data",
            "generation_artifact",
            "final_asset",
            "final_render_evidence",
        ):
            value = row.get(field, "").strip()
            if value and not _portable_existing(value, control, project):
                audit.error(f"{label} has missing, absolute, or nonportable {field}")

        fmt = row.get("format", "").strip().lower().lstrip(".")
        if kind == "vector" and fmt not in VECTOR_FORMATS:
            audit.error(f"{label} declares vector content with incompatible format {fmt!r}")
        if kind == "raster" and fmt not in RASTER_FORMATS:
            audit.error(f"{label} declares raster content with incompatible format {fmt!r}")
        if kind == "mixed" and fmt not in VECTOR_FORMATS:
            audit.error(f"{label} mixed content requires a vector container format")
        if fmt in {"jpg", "jpeg"} and content_type in {"plot", "line_art", "diagram"}:
            audit.error(f"{label} uses lossy JPEG for text or line-oriented content")

        if kind in {"raster", "mixed"}:
            actual = _number(row.get("effective_dpi", ""))
            required = _number(row.get("required_min_dpi", ""))
            if actual is None or required is None or actual <= 0 or required <= 0:
                audit.error(f"{label} requires positive numeric effective and minimum DPI")
            elif actual < required:
                audit.error(
                    f"{label} effective DPI {actual:g} is below its recorded minimum {required:g}"
                )
        elif kind == "vector":
            if not _na(row.get("effective_dpi")) or not _na(
                row.get("required_min_dpi")
            ):
                audit.error(f"{label} should record DPI fields as not_applicable for vector output")

        if kind in {"vector", "mixed"} and not _truthy(
            row.get("font_embedded_or_na")
        ):
            audit.error(f"{label} lacks a passed embedded-font check")
        if kind == "raster" and not (
            _truthy(row.get("font_embedded_or_na"))
            or _na(row.get("font_embedded_or_na"))
        ):
            audit.error(f"{label} has invalid font_embedded_or_na value")

        for field in (
            "legible_at_final_size",
            "crop_checked",
            "caption_check",
            "final_render_checked",
        ):
            if not _truthy(row.get(field)):
                audit.error(f"passed {label} lacks a passed {field}")
        for field in ("line_and_marker_check", "color_independent"):
            if not (_truthy(row.get(field)) or _na(row.get(field))):
                audit.error(f"passed {label} lacks a passed or not_applicable {field}")

        axis = row.get("axis_integrity", "").strip().lower()
        if axis not in AXIS_STATES:
            audit.error(f"{label} has invalid axis_integrity: {axis!r}")
        if axis == "justified_truncation" and not row.get("notes", "").strip():
            audit.error(f"{label} uses a truncated axis without a recorded justification")

    audit.details["figure_ids"] = ids


def _read_document(
    path: Path, strict: bool, audit: Audit, minimum_chars: int = 120
) -> str:
    if not path.is_file():
        audit.error(f"missing required revision artifact: {path.name}")
        return ""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        audit.error(f"cannot read {path.name}: {exc}")
        return ""
    if len(text.strip()) < minimum_chars:
        audit.error(f"{path.name} is unexpectedly short")
    markers = TEMPLATE_MARKER_RE.findall(text)
    if markers:
        message = f"{path.name} contains {len(markers)} unfinished template marker(s)"
        if strict:
            audit.error(message)
        else:
            audit.warn(message)
    if strict and re.search(r"(?im)^status:\s*draft\s*$", text):
        audit.error(f"{path.name} is still marked draft")
    return text


def audit_revision_package(
    raw_root: Path, strict: bool, expected_comments: int | None
) -> tuple[Audit, Path]:
    audit = Audit()
    control, project = _control_root(raw_root)

    response_text = _read_document(control / RESPONSE_FILE, strict, audit)
    highlights_text = _read_document(control / HIGHLIGHTS_FILE, strict, audit)
    _read_document(control / COVER_FILE, strict, audit)

    review_rows = _read_csv(control / REVIEW_FILE, REVIEW_HEADERS, audit)
    figure_rows = _read_csv(control / FIGURE_FILE, FIGURE_HEADERS, audit)

    if strict and not review_rows:
        audit.error(f"strict mode requires at least one row in {REVIEW_FILE}")
    _audit_review_rows(
        review_rows,
        response_text,
        control,
        project,
        strict,
        expected_comments,
        audit,
    )
    _audit_figure_rows(figure_rows, control, project, strict, audit)

    if highlights_text:
        bullets = [
            line
            for line in highlights_text.splitlines()
            if re.match(r"^\s*-\s+(?!\[[ xX]\])\S", line)
        ]
        if strict and not bullets:
            audit.error(f"{HIGHLIGHTS_FILE} contains no submission-ready highlight bullets")
        audit.details["highlight_count"] = len(bullets)

    audit.details["review_row_count"] = len(review_rows)
    audit.details["figure_row_count"] = len(figure_rows)
    audit.details["control_root"] = control.name
    audit.details["strict"] = strict
    return audit, control


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_directory", type=Path)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail on unfinished templates, unresolved comments, and non-ready figures",
    )
    parser.add_argument(
        "--expected-comments",
        type=int,
        help="expected actionable rows, excluding source=self_initiated",
    )
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.expected_comments is not None and args.expected_comments < 0:
        parser.error("--expected-comments must be non-negative")
    try:
        audit, control = audit_revision_package(
            args.project_directory, args.strict, args.expected_comments
        )
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    payload = {
        "ok": not audit.errors,
        "control_root": str(control),
        "errors": audit.errors,
        "warnings": audit.warnings,
        "details": audit.details,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Revision package audit: {'PASS' if not audit.errors else 'FAIL'}")
        print(f"Control root: {control}")
        for warning in audit.warnings:
            print(f"WARNING: {warning}")
        for error in audit.errors:
            print(f"ERROR: {error}")
        print(
            "Structural checks only; scientific validity and venue compliance "
            "still require qualified human review."
        )
    return 0 if not audit.errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
