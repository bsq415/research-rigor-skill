#!/usr/bin/env python3
"""Audit structural research-gate integrity; do not treat this as scientific review."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import re
import sys
from typing import Any


GATE_IDS = tuple(f"G{index}" for index in range(12))
STATUSES = {
    "not_started",
    "in_progress",
    "passed",
    "failed",
    "blocked",
    "paused",
    "deferred",
    "killed",
}
REQUIRED_FILES = (
    "research_state.json",
    "00_CONSTRAINTS.md",
    "01_PROBLEM_CARD.md",
    "02_LITERATURE_LOG.csv",
    "02_SEARCH_LOG.csv",
    "02_NEAREST_NEIGHBOR_MATRIX.csv",
    "03_CLAIM_EVIDENCE_MATRIX.csv",
    "03_THEOREM_CONTRACT.csv",
    "04_EXPERIMENT_PROTOCOL.md",
    "04_COVERAGE_MODEL.csv",
    "05_RUN_LEDGER.csv",
    "06_RESULT_FACTS.csv",
    "07_PAPER_CLAIM_MAP.csv",
    "07_ONE_PAGE_PAPER.md",
    "08_REVIEW_REMEDIATION.csv",
    "09_SUBMISSION_CHECKLIST.md",
    "10_AI_REVIEW_LEDGER.csv",
    "11_ARCHIVE_RECORD.md",
    "DECISION_LOG.md",
    "BLOCKERS.md",
)
REQUIRED_HEADERS = {
    "02_LITERATURE_LOG.csv": {
        "paper_id",
        "full_text_verified",
        "forensic",
        "anchors",
        "audit_status",
    },
    "02_SEARCH_LOG.csv": {
        "query_id",
        "searched_at",
        "source",
        "query",
        "retrieved_ids",
    },
    "02_NEAREST_NEIGHBOR_MATRIX.csv": {
        "paper_id",
        "research_question",
        "unit_or_shift",
        "candidate_exact_delta",
        "strongest_already_done_argument",
        "anchors",
        "forensic_status",
    },
    "03_CLAIM_EVIDENCE_MATRIX.csv": {
        "claim_id",
        "exact_text",
        "falsifier",
        "strongest_baseline",
        "non_claims",
        "status",
    },
    "03_THEOREM_CONTRACT.csv": {
        "theorem_id",
        "exact_statement",
        "assumptions",
        "boundary_cases",
        "counterexamples",
        "proof_obligations",
        "allowed_wording",
        "forbidden_wording",
        "status",
    },
    "04_COVERAGE_MODEL.csv": {
        "step",
        "planned_count",
        "expected_valid_rate",
        "pilot_valid_rate",
        "minimum_required",
        "action_if_below",
    },
    "05_RUN_LEDGER.csv": {
        "run_id",
        "planned_cell",
        "source_commit",
        "config_hash",
        "status",
        "artifact_hash",
    },
    "06_RESULT_FACTS.csv": {
        "fact_id",
        "claim_id",
        "estimate",
        "denominator",
        "status",
        "source_hash",
    },
    "07_PAPER_CLAIM_MAP.csv": {
        "section",
        "claim_id",
        "fact_ids",
        "limitations",
        "non_claims",
        "status",
    },
    "08_REVIEW_REMEDIATION.csv": {
        "comment_id",
        "reviewer_request",
        "type",
        "action",
        "regression_checks",
        "status",
    },
    "10_AI_REVIEW_LEDGER.csv": {
        "review_id",
        "round",
        "service",
        "manuscript_sha256",
        "coverage_limit",
        "privacy_terms_checked",
        "privacy_terms_status",
        "terms_snapshot_path",
        "terms_snapshot_sha256",
        "upload_authorized_by",
        "raw_review_sha256",
        "status",
    },
}
TRUE_VALUES = {"1", "true", "yes", "y", "verified", "passed"}
PLACEHOLDER_RE = re.compile(r"__[A-Z0-9_]+__")


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


def _read_csv(path: Path, audit: Audit) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = set(reader.fieldnames or [])
            missing = REQUIRED_HEADERS.get(path.name, set()) - headers
            if missing:
                audit.error(f"{path.name} is missing columns: {sorted(missing)}")
            return [dict(row) for row in reader]
    except (OSError, csv.Error) as exc:
        audit.error(f"cannot read {path.name}: {exc}")
        return []


def _truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in TRUE_VALUES


def _gate_map(state: dict[str, Any], audit: Audit) -> dict[str, dict[str, Any]]:
    gates = state.get("gates")
    if not isinstance(gates, list):
        audit.error("research_state.json gates must be a list")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for raw in gates:
        if not isinstance(raw, dict) or not isinstance(raw.get("id"), str):
            audit.error("every gate must be an object with a string id")
            continue
        gate_id = raw["id"]
        if gate_id in result:
            audit.error(f"duplicate gate id: {gate_id}")
            continue
        result[gate_id] = raw
    if tuple(result) != GATE_IDS:
        audit.error(f"gate ids/order must be exactly {list(GATE_IDS)}")
    return result


def _evidence_exists(
    item: str, control: Path, project: Path
) -> bool:
    if "://" in item:
        return True
    candidate = Path(item)
    if candidate.is_absolute() or ".." in candidate.parts:
        return False
    return (control / candidate).exists() or (project / candidate).exists()


def audit_project(raw_root: Path) -> tuple[Audit, Path]:
    audit = Audit()
    control, project = _control_root(raw_root)

    for name in REQUIRED_FILES:
        if not (control / name).is_file():
            audit.error(f"missing required control artifact: {name}")

    state_path = control / "research_state.json"
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        audit.error(f"cannot parse research_state.json: {exc}")
        return audit, control
    if not isinstance(state, dict):
        audit.error("research_state.json must contain an object")
        return audit, control

    if state.get("schema_version") != 1:
        audit.error("research_state.json schema_version must be 1")
    title = state.get("project_title")
    if not isinstance(title, str) or not title.strip() or PLACEHOLDER_RE.search(title):
        audit.error("project_title is empty or still contains a template token")

    privacy = state.get("privacy")
    if not isinstance(privacy, dict):
        audit.error("privacy must be an object")
        privacy = {}
    if privacy.get("classification") not in {"private", "internal", "public"}:
        audit.error("privacy.classification must be private, internal, or public")
    if not isinstance(privacy.get("export_policy"), str) or not privacy.get("export_policy", "").strip():
        audit.error("privacy.export_policy must be explicit")

    gates = _gate_map(state, audit)
    seen_unpassed = False
    for gate_id in GATE_IDS:
        gate = gates.get(gate_id)
        if gate is None:
            continue
        status = gate.get("status")
        if status not in STATUSES:
            audit.error(f"{gate_id} has invalid status: {status!r}")
            status = "not_started"
        if status != "passed":
            seen_unpassed = True
        elif seen_unpassed:
            audit.error(f"{gate_id} is passed while an earlier gate is not passed")

        evidence = gate.get("evidence")
        blockers = gate.get("blockers")
        if not isinstance(evidence, list) or not all(isinstance(item, str) for item in evidence):
            audit.error(f"{gate_id}.evidence must be a list of strings")
            evidence = []
        if not isinstance(blockers, list) or not all(isinstance(item, str) for item in blockers):
            audit.error(f"{gate_id}.blockers must be a list of strings")
            blockers = []
        if status == "passed" and not evidence:
            audit.error(f"{gate_id} is passed without evidence")
        if status == "passed" and blockers:
            audit.error(f"{gate_id} is passed with unresolved blockers")
        for item in evidence:
            if not _evidence_exists(item, control, project):
                audit.error(
                    f"{gate_id} evidence is missing, nonportable, or escapes the project: {item!r}"
                )

    current_stage = state.get("current_stage")
    if current_stage not in gates:
        audit.error("current_stage must name an existing gate")
    elif state.get("stage_status") != gates[current_stage].get("status"):
        audit.error("stage_status must match the current gate status")

    frozen = state.get("frozen")
    if not isinstance(frozen, dict):
        audit.error("frozen must be an object")
        frozen = {}
    passed = {gate_id for gate_id, gate in gates.items() if gate.get("status") == "passed"}
    if frozen.get("claims") is True and "G3" not in passed:
        audit.error("claims cannot be frozen before G3 passes")
    if frozen.get("protocol") is True and not {"G4", "G6"} <= passed:
        audit.error("protocol cannot be frozen before G4 and G6 pass")
    if frozen.get("test_touched") is True and (
        frozen.get("protocol") is not True or "G6" not in passed
    ):
        audit.error("locked test cannot be touched before pilot and protocol freeze")
    if frozen.get("submission_ready") is True:
        if not set(GATE_IDS) <= passed:
            audit.error("submission_ready requires every gate to pass")
        if privacy.get("release_scan_passed") is not True:
            audit.error("submission_ready requires privacy.release_scan_passed")
        if privacy.get("semantic_review_passed") is not True:
            audit.error("submission_ready requires privacy.semantic_review_passed")

    csv_rows: dict[str, list[dict[str, str]]] = {}
    for name in REQUIRED_HEADERS:
        path = control / name
        if path.is_file():
            csv_rows[name] = _read_csv(path, audit)

    literature = csv_rows.get("02_LITERATURE_LOG.csv", [])
    paper_ids = [row.get("paper_id", "").strip() for row in literature if row.get("paper_id", "").strip()]
    if len(paper_ids) != len(set(paper_ids)):
        audit.error("02_LITERATURE_LOG.csv contains duplicate nonempty paper_id values")
    verified = [row for row in literature if _truthy(row.get("full_text_verified"))]
    forensic = [row for row in verified if _truthy(row.get("forensic"))]
    independently_audited = [
        row for row in verified if row.get("audit_status", "").strip().lower() == "passed"
    ]
    policy = state.get("literature_policy") if isinstance(state.get("literature_policy"), dict) else {}
    deep_min = int(policy.get("verified_deep_read_min", 0) or 0)
    forensic_min = int(policy.get("forensic_neighbor_min", 0) or 0)
    audit_fraction = float(policy.get("independent_audit_fraction", 0.0) or 0.0)
    if "G2" in passed:
        if len(verified) < deep_min:
            audit.error(f"G2 passed with {len(verified)} verified deep reads; requires {deep_min}")
        if len(forensic) < forensic_min:
            audit.error(f"G2 passed with {len(forensic)} forensic neighbors; requires {forensic_min}")
        required_audits = math.ceil(len(verified) * audit_fraction)
        if len(independently_audited) < required_audits:
            audit.error(
                f"G2 passed with {len(independently_audited)} independent audits; "
                f"requires {required_audits}"
            )
        if any(not row.get("anchors", "").strip() for row in verified):
            audit.error("G2 passed but at least one verified deep read lacks source anchors")
    audit.details["literature"] = {
        "rows": len(literature),
        "verified_deep_reads": len(verified),
        "forensic_neighbors": len(forensic),
        "independent_audits": len(independently_audited),
    }
    if "G2" in passed:
        searches = csv_rows.get("02_SEARCH_LOG.csv", [])
        neighbors = csv_rows.get("02_NEAREST_NEIGHBOR_MATRIX.csv", [])
        if not searches:
            audit.error("G2 passed without a search log")
        if len(neighbors) < forensic_min:
            audit.error(
                f"G2 passed with {len(neighbors)} nearest-neighbor rows; requires {forensic_min}"
            )

    claims = csv_rows.get("03_CLAIM_EVIDENCE_MATRIX.csv", [])
    frozen_claims = [row for row in claims if row.get("status", "").strip().lower() == "frozen"]
    if "G3" in passed:
        if not frozen_claims:
            audit.error("G3 passed without a frozen claim")
        if len(frozen_claims) > 3:
            audit.error("G3 has more than three frozen headline claims")
        for row in frozen_claims:
            for field in ("exact_text", "falsifier", "strongest_baseline", "non_claims"):
                if not row.get(field, "").strip():
                    audit.error(f"frozen claim {row.get('claim_id')!r} lacks {field}")

    coverage = csv_rows.get("04_COVERAGE_MODEL.csv", [])
    if "G4" in passed and not coverage:
        audit.error("G4 passed without a coverage model")

    runs = csv_rows.get("05_RUN_LEDGER.csv", [])
    if "G7" in passed:
        terminal = {"sealed", "complete", "failed", "invalid", "not_run"}
        if not runs:
            audit.error("G7 passed without run-ledger rows")
        if any(row.get("status", "").strip().lower() not in terminal for row in runs):
            audit.error("G7 passed while a run is partial, running, or unclassified")
        sealed = [row for row in runs if row.get("status", "").strip().lower() in {"sealed", "complete"}]
        if not sealed:
            audit.error("G7 passed without a sealed or complete run")
        for row in sealed:
            for field in ("source_commit", "config_hash", "artifact_hash"):
                if not row.get(field, "").strip():
                    audit.error(f"sealed run {row.get('run_id')!r} lacks {field}")

    facts = csv_rows.get("06_RESULT_FACTS.csv", [])
    green_facts = [row for row in facts if row.get("status", "").strip().lower() == "green"]
    if "G8" in passed:
        if not green_facts:
            audit.error("G8 passed without a green result fact")
        for row in green_facts:
            for field in ("fact_id", "claim_id", "denominator", "source_hash"):
                if not row.get(field, "").strip():
                    audit.error(f"green fact {row.get('fact_id')!r} lacks {field}")

    paper_map = csv_rows.get("07_PAPER_CLAIM_MAP.csv", [])
    if "G9" in passed:
        if not paper_map:
            audit.error("G9 passed without paper-claim-map rows")
        if any(not row.get("fact_ids", "").strip() for row in paper_map):
            audit.error("G9 passed but a paper claim lacks fact_ids")

    remediation = csv_rows.get("08_REVIEW_REMEDIATION.csv", [])
    if "G10" in passed and not remediation:
        audit.error("G10 passed without reviewer-red-team or remediation rows")

    ai_reviews = csv_rows.get("10_AI_REVIEW_LEDGER.csv", [])
    for row in ai_reviews:
        review_id = row.get("review_id", "").strip()
        if not review_id:
            audit.error("AI review ledger contains a row without review_id")
            continue
        if not _truthy(row.get("privacy_terms_checked")):
            audit.error(f"AI review {review_id!r} lacks a recorded privacy-terms check")
        terms_status = row.get("privacy_terms_status", "").strip().lower()
        if terms_status not in {"clear", "unclear", "absent", "prohibited"}:
            audit.error(
                f"AI review {review_id!r} has invalid privacy_terms_status: {terms_status!r}"
            )
        review_status = row.get("status", "").strip().lower()
        external_states = {"submitted", "received", "processed", "closed"}
        if review_status in external_states:
            if terms_status != "clear":
                audit.error(
                    f"AI review {review_id!r} was externally processed without clear terms"
                )
            if not row.get("upload_authorized_by", "").strip():
                audit.error(f"AI review {review_id!r} lacks human upload authorization")
            if not row.get("manuscript_sha256", "").strip():
                audit.error(f"AI review {review_id!r} lacks the reviewed manuscript hash")
            if not row.get("terms_snapshot_path", "").strip() or not row.get(
                "terms_snapshot_sha256", ""
            ).strip():
                audit.error(f"AI review {review_id!r} lacks a terms snapshot and hash")
        if review_status in {"received", "processed", "closed"}:
            if not row.get("raw_review_sha256", "").strip():
                audit.error(f"AI review {review_id!r} lacks the raw review hash")

    checklist = control / "09_SUBMISSION_CHECKLIST.md"
    if "G11" in passed and checklist.is_file():
        unchecked = checklist.read_text(encoding="utf-8").count("- [ ]")
        if unchecked:
            audit.error(f"G11 passed with {unchecked} unchecked submission item(s)")

    for path in control.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".csv"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            audit.warn(f"could not inspect template tokens in {path.relative_to(control)}")
            continue
        if PLACEHOLDER_RE.search(text):
            audit.error(f"unresolved scaffold token in {path.relative_to(control).as_posix()}")

    audit.details["gate_statuses"] = {
        gate_id: gates.get(gate_id, {}).get("status") for gate_id in GATE_IDS
    }
    audit.details["control_root"] = control.name
    return audit, control


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_directory", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        audit, control = audit_project(args.project_directory)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    payload = {
        "control_root": str(control),
        "ok": not audit.errors,
        "errors": audit.errors,
        "warnings": audit.warnings,
        "details": audit.details,
        "note": "Structural audit only; scientific validity still requires evidence review.",
    }
    if args.as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for message in audit.errors:
            print(f"ERROR: {message}")
        for message in audit.warnings:
            print(f"WARNING: {message}")
        if not audit.errors:
            print("Structural research audit passed.")
        print("NOTE: This does not certify novelty or scientific validity.")
    return 1 if audit.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
