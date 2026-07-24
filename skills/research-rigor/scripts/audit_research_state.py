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
SCHEMA_VERSIONS = {1, 2}
EXECUTION_MODES = {"guided", "full-cycle"}
EXECUTION_STATUSES = {"ready", "running", "waiting_human", "blocked", "complete"}
BASE_REQUIRED_FILES = (
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
V2_REQUIRED_FILES = (
    "00_AUTONOMY_CONTRACT.md",
    "01_IDEA_CANDIDATES.csv",
    "04_EXPERIMENT_MATRIX.csv",
    "04_PROTOCOL_AMENDMENTS.csv",
    "07_MANUSCRIPT_AUDIT.csv",
    "RESEARCH_CYCLE_LOG.csv",
)
REQUIRED_HEADERS = {
    "01_IDEA_CANDIDATES.csv": {
        "candidate_id",
        "research_question",
        "decision_value",
        "technical_delta",
        "strongest_already_done_argument",
        "evidence_feasibility",
        "falsifier",
        "kill_criteria",
        "status",
        "decision_owner",
        "decision_evidence",
    },
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
    "04_EXPERIMENT_MATRIX.csv": {
        "cell_id",
        "claim_id",
        "role",
        "method",
        "metric",
        "valid_denominator",
        "pass_threshold",
        "kill_or_redesign_threshold",
        "planned_status",
        "artifact_path",
    },
    "04_PROTOCOL_AMENDMENTS.csv": {
        "amendment_id",
        "trigger_type",
        "trigger_evidence",
        "old_protocol_version",
        "changed_fields",
        "scientific_impact",
        "invalidated_artifacts",
        "new_protocol_version",
        "authorization_basis",
        "fresh_validation_required",
        "fresh_validation_evidence",
        "status",
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
    "07_MANUSCRIPT_AUDIT.csv": {
        "finding_id",
        "location",
        "audit_type",
        "severity",
        "claim_or_text",
        "evidence_ids",
        "issue",
        "required_action",
        "status",
        "resolution_evidence",
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
    "RESEARCH_CYCLE_LOG.csv": {
        "cycle_id",
        "recorded_at",
        "task_id",
        "gate",
        "event",
        "from_status",
        "to_status",
        "summary",
        "evidence",
        "next_action",
        "acceptance_condition",
        "requires_human",
    },
}
TRUE_VALUES = {"1", "true", "yes", "y", "verified", "passed"}
PLACEHOLDER_RE = re.compile(r"__[A-Z0-9_]+__")
CHECKBOX_RE = re.compile(r"^\s*-\s+\[([ xX])\]", re.MULTILINE)


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


def _checkbox_counts(path: Path, audit: Audit) -> tuple[int, int]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        audit.error(f"cannot read {path.name}: {exc}")
        return 0, 0
    matches = CHECKBOX_RE.findall(text)
    unchecked = sum(value == " " for value in matches)
    return len(matches), unchecked


def _nonempty_ids(
    rows: list[dict[str, str]], field: str, artifact: str, audit: Audit
) -> list[str]:
    values = [row.get(field, "").strip() for row in rows]
    if any(not value for value in values):
        audit.error(f"{artifact} contains a row without {field}")
    nonempty = [value for value in values if value]
    if len(nonempty) != len(set(nonempty)):
        audit.error(f"{artifact} contains duplicate nonempty {field} values")
    return nonempty


def _split_refs(value: Any) -> list[str]:
    return [
        item
        for item in re.split(r"[\s,;|]+", str(value or "").strip())
        if item
    ]


def _policy_int(value: Any, field: str, audit: Audit) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        audit.error(f"literature_policy.{field} must be a non-negative integer")
        return 0
    if parsed < 0:
        audit.error(f"literature_policy.{field} must be a non-negative integer")
        return 0
    return parsed


def _policy_fraction(value: Any, field: str, audit: Audit) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        audit.error(f"literature_policy.{field} must be between 0 and 1")
        return 0.0
    if not 0 <= parsed <= 1:
        audit.error(f"literature_policy.{field} must be between 0 and 1")
        return 0.0
    return parsed


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

    state_path = control / "research_state.json"
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        audit.error(f"cannot parse research_state.json: {exc}")
        return audit, control
    if not isinstance(state, dict):
        audit.error("research_state.json must contain an object")
        return audit, control

    schema_version = state.get("schema_version")
    if schema_version not in SCHEMA_VERSIONS:
        audit.error(
            f"research_state.json schema_version must be one of {sorted(SCHEMA_VERSIONS)}"
        )
        schema_version = 1
    if schema_version == 1:
        audit.warn(
            "schema_version 1 is legacy; run init_research_project.py --merge and "
            "migrate the execution state before using full-cycle mode"
        )
    required_files = BASE_REQUIRED_FILES + (V2_REQUIRED_FILES if schema_version == 2 else ())
    for name in required_files:
        if not (control / name).is_file():
            audit.error(f"missing required control artifact: {name}")

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
    if schema_version == 2 and gates:
        expected_stage = next(
            (
                gate_id
                for gate_id in GATE_IDS
                if gates.get(gate_id, {}).get("status") != "passed"
            ),
            "G11",
        )
        if current_stage != expected_stage:
            audit.error(
                f"current_stage must be the earliest unpassed gate ({expected_stage})"
            )

    if schema_version == 2:
        execution = state.get("execution")
        if not isinstance(execution, dict):
            audit.error("schema_version 2 requires an execution object")
            execution = {}
        if execution.get("mode") not in EXECUTION_MODES:
            audit.error(
                f"execution.mode must be one of {sorted(EXECUTION_MODES)}"
            )
        if execution.get("status") not in EXECUTION_STATUSES:
            audit.error(
                f"execution.status must be one of {sorted(EXECUTION_STATUSES)}"
            )
        if execution.get("current_gate") != current_stage:
            audit.error("execution.current_gate must match current_stage")
        if not isinstance(execution.get("active_task"), str):
            audit.error("execution.active_task must be a string")
        for field in ("next_action", "acceptance_condition"):
            if not isinstance(execution.get(field), str) or not execution.get(field, "").strip():
                audit.error(f"execution.{field} must be a nonempty string")
        if not isinstance(execution.get("requires_human"), bool):
            audit.error("execution.requires_human must be a boolean")
        if execution.get("status") == "waiting_human" and execution.get(
            "requires_human"
        ) is not True:
            audit.error("waiting_human execution status requires requires_human=true")
        if execution.get("status") in {"ready", "running"} and execution.get(
            "requires_human"
        ) is True:
            audit.error(
                f"{execution.get('status')} execution status requires requires_human=false"
            )
        if execution.get("status") == "blocked" and current_stage in gates:
            if gates[current_stage].get("status") != "blocked":
                audit.error("blocked execution status requires the current gate to be blocked")
        if execution.get("status") == "complete" and current_stage in gates:
            all_passed = all(
                gates.get(gate_id, {}).get("status") == "passed"
                for gate_id in GATE_IDS
            )
            terminal_direction = gates[current_stage].get("status") in {
                "deferred",
                "killed",
            }
            if not all_passed and not terminal_direction:
                audit.error(
                    "complete execution status requires all gates passed or a "
                    "deferred/killed current direction"
                )

    frozen = state.get("frozen")
    if not isinstance(frozen, dict):
        audit.error("frozen must be an object")
        frozen = {}
    passed = {gate_id for gate_id, gate in gates.items() if gate.get("status") == "passed"}
    if frozen.get("claims") is True and "G3" not in passed:
        audit.error("claims cannot be frozen before G3 passes")
    if "G3" in passed and frozen.get("claims") is not True:
        audit.error("G3 passed but frozen.claims is not true")
    if frozen.get("protocol") is True and not {"G4", "G6"} <= passed:
        audit.error("protocol cannot be frozen before G4 and G6 pass")
    if "G6" in passed and frozen.get("protocol") is not True:
        audit.error("G6 passed but frozen.protocol is not true")
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
    if "G11" in passed and frozen.get("submission_ready") is not True:
        audit.error("G11 passed but frozen.submission_ready is not true")

    csv_rows: dict[str, list[dict[str, str]]] = {}
    for name in REQUIRED_HEADERS:
        path = control / name
        if path.is_file():
            csv_rows[name] = _read_csv(path, audit)

    if "G0" in passed:
        contract_files = ["00_CONSTRAINTS.md"]
        if schema_version == 2:
            contract_files.append("00_AUTONOMY_CONTRACT.md")
        for name in contract_files:
            path = control / name
            if not path.is_file():
                continue
            total, unchecked = _checkbox_counts(path, audit)
            if total == 0:
                audit.error(f"G0 passed but {name} has no acceptance checkboxes")
            if unchecked:
                audit.error(f"G0 passed with {unchecked} unchecked item(s) in {name}")

    candidates = csv_rows.get("01_IDEA_CANDIDATES.csv", [])
    if candidates:
        _nonempty_ids(candidates, "candidate_id", "01_IDEA_CANDIDATES.csv", audit)
        allowed_candidate_statuses = {
            "proposed",
            "screening",
            "viable",
            "selected",
            "rejected",
            "deferred",
            "killed",
        }
        for row in candidates:
            status = row.get("status", "").strip().lower()
            if status not in allowed_candidate_statuses:
                audit.error(
                    f"idea candidate {row.get('candidate_id')!r} has invalid status: {status!r}"
                )
    if schema_version == 2 and "G1" in passed:
        viable_candidates = [
            row
            for row in candidates
            if row.get("status", "").strip().lower() in {"viable", "selected"}
        ]
        if not viable_candidates:
            audit.error("G1 passed without a viable or selected idea candidate")
        for row in viable_candidates:
            for field in (
                "research_question",
                "decision_value",
                "technical_delta",
                "evidence_feasibility",
                "falsifier",
                "kill_criteria",
            ):
                if not row.get(field, "").strip():
                    audit.error(
                        f"viable idea candidate {row.get('candidate_id')!r} lacks {field}"
                    )
    if schema_version == 2 and "G2" in passed:
        selected_candidates = [
            row
            for row in candidates
            if row.get("status", "").strip().lower() == "selected"
        ]
        if len(selected_candidates) != 1:
            audit.error(
                f"G2 requires exactly one selected idea candidate; found {len(selected_candidates)}"
            )
        for row in selected_candidates:
            for field in (
                "strongest_already_done_argument",
                "decision_owner",
                "decision_evidence",
            ):
                if not row.get(field, "").strip():
                    audit.error(
                        f"selected idea candidate {row.get('candidate_id')!r} lacks {field}"
                    )
            decision_evidence = row.get("decision_evidence", "").strip()
            if decision_evidence and not _evidence_exists(
                decision_evidence, control, project
            ):
                audit.error(
                    f"selected idea candidate {row.get('candidate_id')!r} has "
                    "missing or nonportable decision_evidence"
                )

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
    deep_min = _policy_int(
        policy.get("verified_deep_read_min", 0), "verified_deep_read_min", audit
    )
    forensic_min = _policy_int(
        policy.get("forensic_neighbor_min", 0), "forensic_neighbor_min", audit
    )
    audit_fraction = _policy_fraction(
        policy.get("independent_audit_fraction", 0.0),
        "independent_audit_fraction",
        audit,
    )
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
        neighbor_ids = {
            row.get("paper_id", "").strip()
            for row in neighbors
            if row.get("paper_id", "").strip()
        }
        unknown_neighbor_ids = sorted(neighbor_ids - set(paper_ids))
        if unknown_neighbor_ids:
            audit.error(
                "nearest-neighbor rows are missing from the literature ledger: "
                f"{unknown_neighbor_ids}"
            )

    claims = csv_rows.get("03_CLAIM_EVIDENCE_MATRIX.csv", [])
    if claims:
        _nonempty_ids(claims, "claim_id", "03_CLAIM_EVIDENCE_MATRIX.csv", audit)
    claim_ids = {
        row.get("claim_id", "").strip()
        for row in claims
        if row.get("claim_id", "").strip()
    }
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

    experiment_matrix = csv_rows.get("04_EXPERIMENT_MATRIX.csv", [])
    if experiment_matrix:
        _nonempty_ids(
            experiment_matrix, "cell_id", "04_EXPERIMENT_MATRIX.csv", audit
        )
    if schema_version == 2 and "G4" in passed:
        if not experiment_matrix:
            audit.error("G4 passed without experiment-matrix rows")
        for row in experiment_matrix:
            for field in (
                "claim_id",
                "role",
                "method",
                "metric",
                "valid_denominator",
                "pass_threshold",
                "kill_or_redesign_threshold",
                "planned_status",
            ):
                if not row.get(field, "").strip():
                    audit.error(
                        f"experiment cell {row.get('cell_id')!r} lacks {field}"
                    )
            if row.get("claim_id", "").strip() not in claim_ids:
                audit.error(
                    f"experiment cell {row.get('cell_id')!r} references an unknown claim_id"
                )
        covered_claims = {
            row.get("claim_id", "").strip()
            for row in experiment_matrix
            if row.get("claim_id", "").strip()
        }
        uncovered_claims = sorted(
            row.get("claim_id", "").strip()
            for row in frozen_claims
            if row.get("claim_id", "").strip() not in covered_claims
        )
        if uncovered_claims:
            audit.error(
                f"frozen claims lack experiment-matrix coverage: {uncovered_claims}"
            )

    amendments = csv_rows.get("04_PROTOCOL_AMENDMENTS.csv", [])
    if amendments:
        _nonempty_ids(
            amendments, "amendment_id", "04_PROTOCOL_AMENDMENTS.csv", audit
        )
    amendment_statuses = {"proposed", "approved", "applied", "rejected", "superseded"}
    for row in amendments:
        amendment_id = row.get("amendment_id", "").strip()
        status = row.get("status", "").strip().lower()
        if status not in amendment_statuses:
            audit.error(
                f"protocol amendment {amendment_id!r} has invalid status: {status!r}"
            )
        if status in {"approved", "applied"}:
            for field in (
                "trigger_type",
                "trigger_evidence",
                "old_protocol_version",
                "changed_fields",
                "scientific_impact",
                "invalidated_artifacts",
                "new_protocol_version",
                "authorization_basis",
                "fresh_validation_required",
            ):
                if not row.get(field, "").strip():
                    audit.error(f"protocol amendment {amendment_id!r} lacks {field}")
        if status == "applied" and _truthy(row.get("fresh_validation_required")):
            fresh_evidence = row.get("fresh_validation_evidence", "").strip()
            if not fresh_evidence:
                audit.error(
                    f"applied protocol amendment {amendment_id!r} requires fresh validation evidence"
                )
            else:
                for item in fresh_evidence.split(";"):
                    if not _evidence_exists(item.strip(), control, project):
                        audit.error(
                            f"protocol amendment {amendment_id!r} fresh validation "
                            f"evidence is missing or nonportable: {item!r}"
                        )

    runs = csv_rows.get("05_RUN_LEDGER.csv", [])
    if runs:
        _nonempty_ids(runs, "run_id", "05_RUN_LEDGER.csv", audit)
    run_ids = {
        row.get("run_id", "").strip()
        for row in runs
        if row.get("run_id", "").strip()
    }
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
            planned_cell = row.get("planned_cell", "").strip()
            matrix_ids = {
                item.get("cell_id", "").strip()
                for item in experiment_matrix
                if item.get("cell_id", "").strip()
            }
            if schema_version == 2 and planned_cell not in matrix_ids:
                audit.error(
                    f"sealed run {row.get('run_id')!r} references an unknown planned_cell"
                )

    facts = csv_rows.get("06_RESULT_FACTS.csv", [])
    if facts:
        _nonempty_ids(facts, "fact_id", "06_RESULT_FACTS.csv", audit)
    fact_by_id = {
        row.get("fact_id", "").strip(): row
        for row in facts
        if row.get("fact_id", "").strip()
    }
    green_facts = [row for row in facts if row.get("status", "").strip().lower() == "green"]
    if "G8" in passed:
        if not green_facts:
            audit.error("G8 passed without a green result fact")
        for row in green_facts:
            for field in ("fact_id", "claim_id", "denominator", "source_hash"):
                if not row.get(field, "").strip():
                    audit.error(f"green fact {row.get('fact_id')!r} lacks {field}")
            if row.get("claim_id", "").strip() not in claim_ids:
                audit.error(
                    f"green fact {row.get('fact_id')!r} references an unknown claim_id"
                )
            if row.get("run_id", "").strip() not in run_ids:
                audit.error(
                    f"green fact {row.get('fact_id')!r} references an unknown run_id"
                )

    paper_map = csv_rows.get("07_PAPER_CLAIM_MAP.csv", [])
    if "G9" in passed:
        if not paper_map:
            audit.error("G9 passed without paper-claim-map rows")
        if any(not row.get("fact_ids", "").strip() for row in paper_map):
            audit.error("G9 passed but a paper claim lacks fact_ids")
        for row in paper_map:
            paper_claim = row.get("claim_id", "").strip()
            if paper_claim not in claim_ids:
                audit.error(
                    f"paper section {row.get('section')!r} references an unknown claim_id"
                )
            for fact_id in _split_refs(row.get("fact_ids")):
                fact = fact_by_id.get(fact_id)
                if fact is None:
                    audit.error(
                        f"paper section {row.get('section')!r} references unknown fact_id {fact_id!r}"
                    )
                elif fact.get("status", "").strip().lower() != "green":
                    audit.error(
                        f"paper section {row.get('section')!r} references unsealed "
                        f"fact_id {fact_id!r}"
                    )

    manuscript_audit = csv_rows.get("07_MANUSCRIPT_AUDIT.csv", [])
    if manuscript_audit:
        _nonempty_ids(
            manuscript_audit, "finding_id", "07_MANUSCRIPT_AUDIT.csv", audit
        )
    allowed_severities = {"info", "minor", "major", "fatal"}
    allowed_finding_statuses = {
        "open",
        "resolved",
        "accepted_limitation",
        "deferred_new_study",
        "not_applicable",
    }
    for row in manuscript_audit:
        finding_id = row.get("finding_id", "").strip()
        severity = row.get("severity", "").strip().lower()
        status = row.get("status", "").strip().lower()
        if severity not in allowed_severities:
            audit.error(
                f"manuscript finding {finding_id!r} has invalid severity: {severity!r}"
            )
        if status not in allowed_finding_statuses:
            audit.error(
                f"manuscript finding {finding_id!r} has invalid status: {status!r}"
            )
        if status in {"resolved", "accepted_limitation", "deferred_new_study"}:
            if not row.get("resolution_evidence", "").strip():
                audit.error(
                    f"manuscript finding {finding_id!r} lacks resolution_evidence"
                )
    if schema_version == 2 and "G9" in passed:
        if not manuscript_audit:
            audit.error("G9 passed without manuscript-audit rows")
        unresolved_major = [
            row
            for row in manuscript_audit
            if row.get("severity", "").strip().lower() in {"fatal", "major"}
            and row.get("status", "").strip().lower() == "open"
        ]
        if unresolved_major:
            ids = [row.get("finding_id", "").strip() for row in unresolved_major]
            audit.error(f"G9 passed with unresolved fatal or major findings: {ids}")

    remediation = csv_rows.get("08_REVIEW_REMEDIATION.csv", [])
    if remediation:
        _nonempty_ids(
            remediation, "comment_id", "08_REVIEW_REMEDIATION.csv", audit
        )
    if "G10" in passed and not remediation:
        audit.error("G10 passed without reviewer-red-team or remediation rows")

    ai_reviews = csv_rows.get("10_AI_REVIEW_LEDGER.csv", [])
    if ai_reviews:
        _nonempty_ids(ai_reviews, "review_id", "10_AI_REVIEW_LEDGER.csv", audit)
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
            for field in ("manuscript_path", "terms_snapshot_path"):
                evidence_path = row.get(field, "").strip()
                if evidence_path and not _evidence_exists(
                    evidence_path, control, project
                ):
                    audit.error(
                        f"AI review {review_id!r} has missing or nonportable {field}"
                    )
        if review_status in {"received", "processed", "closed"}:
            if not row.get("raw_review_sha256", "").strip():
                audit.error(f"AI review {review_id!r} lacks the raw review hash")
            raw_review_path = row.get("raw_review_path", "").strip()
            if not raw_review_path or not _evidence_exists(
                raw_review_path, control, project
            ):
                audit.error(
                    f"AI review {review_id!r} lacks a portable raw review artifact"
                )

    checklist = control / "09_SUBMISSION_CHECKLIST.md"
    if "G11" in passed and checklist.is_file():
        unchecked = checklist.read_text(encoding="utf-8").count("- [ ]")
        if unchecked:
            audit.error(f"G11 passed with {unchecked} unchecked submission item(s)")

    cycle_log = csv_rows.get("RESEARCH_CYCLE_LOG.csv", [])
    if cycle_log:
        _nonempty_ids(cycle_log, "cycle_id", "RESEARCH_CYCLE_LOG.csv", audit)
        for row in cycle_log:
            cycle_id = row.get("cycle_id", "").strip()
            if row.get("gate", "").strip() not in GATE_IDS:
                audit.error(
                    f"research cycle {cycle_id!r} has invalid gate: {row.get('gate')!r}"
                )
            if not row.get("task_id", "").strip():
                audit.error(f"research cycle {cycle_id!r} lacks task_id")
            if not row.get("summary", "").strip():
                audit.error(f"research cycle {cycle_id!r} lacks summary")
            if not row.get("next_action", "").strip():
                audit.error(f"research cycle {cycle_id!r} lacks next_action")
            if not row.get("acceptance_condition", "").strip():
                audit.error(
                    f"research cycle {cycle_id!r} lacks acceptance_condition"
                )
            if str(row.get("requires_human", "")).strip().lower() not in {
                "true",
                "false",
            }:
                audit.error(
                    f"research cycle {cycle_id!r} requires_human must be true or false"
                )

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
