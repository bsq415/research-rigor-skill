#!/usr/bin/env python3
"""Inspect and safely advance a persistent, evidence-gated research cycle."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any
from uuid import uuid4

from audit_research_state import GATE_IDS, audit_project


CHECKPOINT_STATUSES = {
    "planned",
    "in_progress",
    "completed",
    "failed",
    "blocked",
    "paused",
}
TRANSITION_STATUSES = {
    "in_progress",
    "passed",
    "failed",
    "blocked",
    "paused",
    "deferred",
    "killed",
}
TERMINAL_PROJECT_STATUSES = {"deferred", "killed"}
CYCLE_FIELDS = (
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
)
GATE_GUIDANCE = {
    "G0": (
        "references/stage-gates.md#G0",
        ["00_CONSTRAINTS.md", "00_AUTONOMY_CONTRACT.md", "research_state.json"],
    ),
    "G1": (
        "references/idea-and-literature.md",
        ["01_PROBLEM_CARD.md", "01_IDEA_CANDIDATES.csv"],
    ),
    "G2": (
        "references/idea-and-literature.md",
        [
            "01_IDEA_CANDIDATES.csv",
            "02_SEARCH_LOG.csv",
            "02_LITERATURE_LOG.csv",
            "02_NEAREST_NEIGHBOR_MATRIX.csv",
        ],
    ),
    "G3": (
        "references/experiment-and-evidence.md",
        ["03_CLAIM_EVIDENCE_MATRIX.csv", "03_THEOREM_CONTRACT.csv"],
    ),
    "G4": (
        "references/experiment-and-evidence.md",
        [
            "04_EXPERIMENT_PROTOCOL.md",
            "04_EXPERIMENT_MATRIX.csv",
            "04_COVERAGE_MODEL.csv",
            "04_PROTOCOL_AMENDMENTS.csv",
        ],
    ),
    "G5": (
        "references/experiment-and-evidence.md",
        ["05_RUN_LEDGER.csv", "DECISION_LOG.md"],
    ),
    "G6": (
        "references/experiment-and-evidence.md",
        ["05_RUN_LEDGER.csv", "04_PROTOCOL_AMENDMENTS.csv"],
    ),
    "G7": (
        "references/experiment-and-evidence.md",
        ["05_RUN_LEDGER.csv", "04_PROTOCOL_AMENDMENTS.csv"],
    ),
    "G8": (
        "references/experiment-and-evidence.md",
        ["06_RESULT_FACTS.csv", "05_RUN_LEDGER.csv"],
    ),
    "G9": (
        "references/paper-review-submission.md",
        [
            "07_ONE_PAGE_PAPER.md",
            "07_PAPER_CLAIM_MAP.csv",
            "07_MANUSCRIPT_AUDIT.csv",
        ],
    ),
    "G10": (
        "references/paper-review-submission.md",
        ["08_REVIEW_REMEDIATION.csv", "10_AI_REVIEW_LEDGER.csv"],
    ),
    "G11": (
        "references/paper-review-submission.md",
        ["09_SUBMISSION_CHECKLIST.md", "11_ARCHIVE_RECORD.md"],
    ),
}


class CycleError(RuntimeError):
    """A safe research-cycle mutation could not be completed."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _control_root(raw: Path) -> tuple[Path, Path]:
    root = raw.resolve()
    if (root / "research_state.json").is_file():
        return root, root.parent
    control = root / ".research"
    if (control / "research_state.json").is_file():
        return control, root
    raise CycleError(f"could not find research_state.json in {root} or {control}")


def _load_state(control: Path) -> dict[str, Any]:
    try:
        state = json.loads((control / "research_state.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CycleError(f"cannot parse research_state.json: {exc}") from exc
    if not isinstance(state, dict):
        raise CycleError("research_state.json must contain an object")
    if state.get("schema_version") != 2:
        raise CycleError(
            "research_cycle.py requires schema_version 2; merge the current "
            "scaffold and migrate the state deliberately"
        )
    return state


def _gate_map(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    gates = state.get("gates")
    if not isinstance(gates, list):
        raise CycleError("research_state.json gates must be a list")
    result = {
        gate.get("id"): gate
        for gate in gates
        if isinstance(gate, dict) and isinstance(gate.get("id"), str)
    }
    if tuple(result) != GATE_IDS:
        raise CycleError(f"gate ids/order must be exactly {list(GATE_IDS)}")
    return result


def _assert_clean_structure(project: Path) -> None:
    audit, _ = audit_project(project)
    if audit.errors:
        preview = "\n".join(f"- {message}" for message in audit.errors[:12])
        remainder = len(audit.errors) - min(len(audit.errors), 12)
        suffix = f"\n- ... and {remainder} more" if remainder else ""
        raise CycleError(
            "structural audit failed before mutation; repair the control layer first:\n"
            f"{preview}{suffix}"
        )


def _validate_text(value: str, field: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise CycleError(f"{field} cannot be empty")
    if "\r" in cleaned or "\n" in cleaned:
        raise CycleError(f"{field} must be a single line")
    return cleaned


def _verified_evidence(
    raw_items: list[str], control: Path, project: Path
) -> list[str]:
    verified: list[str] = []
    for raw in raw_items:
        item = raw.strip()
        if not item:
            continue
        if "\r" in item or "\n" in item:
            raise CycleError("evidence paths must be single-line values")
        if "://" in item:
            verified.append(item)
            continue
        candidate = Path(item)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise CycleError(
                f"evidence must be a portable path inside the project: {item!r}"
            )
        if not (control / candidate).exists() and not (project / candidate).exists():
            raise CycleError(f"evidence does not exist: {item!r}")
        verified.append(candidate.as_posix())
    return list(dict.fromkeys(verified))


def _atomic_write(path: Path, text: str) -> None:
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)


def _append_cycle(log_path: Path, row: dict[str, str]) -> None:
    exists = log_path.is_file()
    with log_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CYCLE_FIELDS)
        if not exists or log_path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(row)


def _execution_status(
    outcome: str, requires_human: bool, final_gate_passed: bool = False
) -> str:
    if final_gate_passed or outcome in TERMINAL_PROJECT_STATUSES:
        return "complete"
    if outcome == "blocked":
        return "blocked"
    if requires_human or outcome in {"paused", "failed"}:
        return "waiting_human"
    if outcome in {"planned", "in_progress"}:
        return "running"
    return "ready"


def _mutate_transaction(
    project: Path,
    control: Path,
    state: dict[str, Any],
    row: dict[str, str],
) -> None:
    state_path = control / "research_state.json"
    log_path = control / "RESEARCH_CYCLE_LOG.csv"
    original_state = state_path.read_text(encoding="utf-8")
    original_log = log_path.read_text(encoding="utf-8") if log_path.exists() else None
    _atomic_write(
        state_path,
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
    )
    try:
        _append_cycle(log_path, row)
        audit, _ = audit_project(project)
        if audit.errors:
            preview = "\n".join(f"- {message}" for message in audit.errors[:12])
            remainder = len(audit.errors) - min(len(audit.errors), 12)
            suffix = f"\n- ... and {remainder} more" if remainder else ""
            raise CycleError(
                "proposed transition failed structural validation and was rolled back:\n"
                f"{preview}{suffix}"
            )
    except Exception:
        _atomic_write(state_path, original_state)
        if original_log is None:
            if log_path.exists():
                log_path.unlink()
        else:
            _atomic_write(log_path, original_log)
        raise


def _cycle_row(
    *,
    cycle_id: str,
    recorded_at: str,
    task_id: str,
    gate: str,
    event: str,
    from_status: str,
    to_status: str,
    summary: str,
    evidence: list[str],
    next_action: str,
    acceptance_condition: str,
    requires_human: bool,
) -> dict[str, str]:
    return {
        "cycle_id": cycle_id,
        "recorded_at": recorded_at,
        "task_id": task_id,
        "gate": gate,
        "event": event,
        "from_status": from_status,
        "to_status": to_status,
        "summary": summary,
        "evidence": ";".join(evidence),
        "next_action": next_action,
        "acceptance_condition": acceptance_condition,
        "requires_human": str(requires_human).lower(),
    }


def _common_inputs(
    args: argparse.Namespace, control: Path, project: Path
) -> tuple[str, str, str, str, list[str], bool]:
    task_id = _validate_text(args.task_id, "task_id")
    summary = _validate_text(args.summary, "summary")
    next_action = _validate_text(args.next_action, "next_action")
    acceptance = _validate_text(args.acceptance_condition, "acceptance_condition")
    evidence = _verified_evidence(args.evidence or [], control, project)
    requires_human = bool(args.requires_human)
    return task_id, summary, next_action, acceptance, evidence, requires_human


def command_status(args: argparse.Namespace) -> int:
    control, project = _control_root(args.project_directory)
    state = _load_state(control)
    gates = _gate_map(state)
    audit, _ = audit_project(project)
    current = state["current_stage"]
    execution = state["execution"]
    guidance, artifacts = GATE_GUIDANCE[current]
    payload = {
        "project": state.get("project_title"),
        "control_root": str(control),
        "mode": execution.get("mode"),
        "execution_status": execution.get("status"),
        "current_gate": current,
        "gate_status": gates[current].get("status"),
        "active_task": execution.get("active_task"),
        "next_action": execution.get("next_action"),
        "acceptance_condition": execution.get("acceptance_condition"),
        "requires_human": execution.get("requires_human"),
        "blockers": gates[current].get("blockers", []),
        "protocol": guidance,
        "authoritative_artifacts": artifacts,
        "structural_audit_ok": not audit.errors,
        "audit_errors": audit.errors,
        "audit_warnings": audit.warnings,
        "resume_command": (
            f'python "{Path(__file__).resolve()}" status "{project}"'
        ),
        "note": "Structural status only; evidence review determines scientific validity.",
    }
    if args.as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        fields = (
            ("Project", payload["project"]),
            ("Mode", payload["mode"]),
            ("Execution", payload["execution_status"]),
            ("Stage", f"{current} ({payload['gate_status']})"),
            ("Active task", payload["active_task"] or "none"),
            ("Requires human", str(payload["requires_human"]).lower()),
            ("Protocol", payload["protocol"]),
            ("Artifacts", ", ".join(payload["authoritative_artifacts"])),
            ("Next action", payload["next_action"]),
            ("Acceptance", payload["acceptance_condition"]),
            (
                "Structural audit",
                "passed" if payload["structural_audit_ok"] else "failed",
            ),
            ("Resume", payload["resume_command"]),
        )
        for label, value in fields:
            print(f"{label}: {value}")
        if payload["blockers"]:
            print(f"Blockers: {'; '.join(payload['blockers'])}")
        for message in audit.errors:
            print(f"ERROR: {message}")
        for message in audit.warnings:
            print(f"WARNING: {message}")
        print("NOTE: Structural status is not a scientific-validity judgment.")
    return 1 if audit.errors else 0


def command_checkpoint(args: argparse.Namespace) -> int:
    control, project = _control_root(args.project_directory)
    _assert_clean_structure(project)
    state = _load_state(control)
    gates = _gate_map(state)
    current = state["current_stage"]
    if args.gate != current:
        raise CycleError(
            f"checkpoint gate must match current_stage {current}; got {args.gate}"
        )
    gate = gates[current]
    if gate.get("status") in {"passed", "failed", "deferred", "killed"}:
        raise CycleError(
            f"cannot checkpoint terminal gate status {gate.get('status')!r}; "
            "use an explicit transition to reopen or advance"
        )
    (
        task_id,
        summary,
        next_action,
        acceptance,
        evidence,
        requires_human,
    ) = _common_inputs(args, control, project)
    now = _utc_now()
    cycle_id = f"cycle-{uuid4().hex}"
    from_status = str(gate.get("status"))
    if args.status == "blocked":
        to_status = "blocked"
        blockers = list(args.blocker or [])
        if not blockers:
            raise CycleError("a blocked checkpoint requires --blocker")
        gate["blockers"] = list(dict.fromkeys(blockers))
    elif args.status == "paused":
        to_status = "paused"
        gate["blockers"] = list(dict.fromkeys(args.blocker or []))
        requires_human = True
    else:
        to_status = "in_progress"
        gate["blockers"] = []
    gate["status"] = to_status
    gate["evidence"] = list(
        dict.fromkeys([*gate.get("evidence", []), *evidence])
    )
    state["stage_status"] = to_status
    state["updated_utc"] = now
    execution = state["execution"]
    execution.update(
        {
            "status": _execution_status(args.status, requires_human),
            "current_gate": current,
            "active_task": (
                task_id
                if args.status in {"planned", "in_progress", "blocked", "paused"}
                else ""
            ),
            "last_checkpoint_id": cycle_id,
            "last_checkpoint_utc": now,
            "next_action": next_action,
            "acceptance_condition": acceptance,
            "requires_human": requires_human,
        }
    )
    row = _cycle_row(
        cycle_id=cycle_id,
        recorded_at=now,
        task_id=task_id,
        gate=current,
        event=f"checkpoint:{args.status}",
        from_status=from_status,
        to_status=to_status,
        summary=summary,
        evidence=evidence,
        next_action=next_action,
        acceptance_condition=acceptance,
        requires_human=requires_human,
    )
    _mutate_transaction(project, control, state, row)
    print(f"Checkpoint recorded: {cycle_id}")
    print(f"Stage: {current} ({to_status})")
    print(f"Next action: {next_action}")
    print(f"Acceptance condition: {acceptance}")
    return 0


def command_transition(args: argparse.Namespace) -> int:
    control, project = _control_root(args.project_directory)
    _assert_clean_structure(project)
    state = _load_state(control)
    gates = _gate_map(state)
    current = state["current_stage"]
    target_index = GATE_IDS.index(args.gate)
    current_index = GATE_IDS.index(current)
    reopening = target_index < current_index
    if reopening:
        if args.status != "in_progress" or not args.reopen_dependent_gates:
            raise CycleError(
                "an earlier gate can be reopened only with --status in_progress "
                "and --reopen-dependent-gates"
            )
    elif args.gate != current:
        raise CycleError(f"transition gate must match current_stage {current}")

    (
        task_id,
        summary,
        next_action,
        acceptance,
        evidence,
        requires_human,
    ) = _common_inputs(args, control, project)
    gate = gates[args.gate]
    from_status = str(gate.get("status"))
    blockers = list(dict.fromkeys(args.blocker or []))
    if args.status == "passed":
        if not evidence:
            raise CycleError("a passed transition requires at least one --evidence path")
        if blockers:
            raise CycleError("a passed transition cannot include unresolved blockers")
        prior = GATE_IDS[:target_index]
        unpassed = [gate_id for gate_id in prior if gates[gate_id].get("status") != "passed"]
        if unpassed:
            raise CycleError(f"cannot pass {args.gate}; earlier gates are unpassed: {unpassed}")
    if args.status == "blocked" and not blockers:
        raise CycleError("a blocked transition requires --blocker")
    if args.status in {"paused", "failed"}:
        requires_human = True

    if reopening:
        for gate_id in GATE_IDS[target_index + 1 :]:
            gates[gate_id]["status"] = "not_started"
            gates[gate_id]["blockers"] = []
        current = args.gate
        frozen = state["frozen"]
        if target_index <= GATE_IDS.index("G3"):
            frozen["claims"] = False
        if target_index <= GATE_IDS.index("G6"):
            frozen["protocol"] = False
        frozen["submission_ready"] = False
    gate["status"] = args.status
    gate["evidence"] = list(
        dict.fromkeys([*gate.get("evidence", []), *evidence])
    )
    gate["blockers"] = [] if args.status in {"passed", "in_progress"} else blockers

    if args.status == "passed":
        frozen = state["frozen"]
        if args.gate == "G3":
            frozen["claims"] = True
        elif args.gate == "G6":
            frozen["protocol"] = True
        elif args.gate == "G11":
            frozen["submission_ready"] = True

    final_gate_passed = args.gate == "G11" and args.status == "passed"
    if args.status == "passed" and not final_gate_passed:
        next_gate = GATE_IDS[target_index + 1]
        state["current_stage"] = next_gate
        state["stage_status"] = gates[next_gate]["status"]
    else:
        state["current_stage"] = args.gate
        state["stage_status"] = args.status

    now = _utc_now()
    cycle_id = f"cycle-{uuid4().hex}"
    state["updated_utc"] = now
    execution = state["execution"]
    execution.update(
        {
            "status": _execution_status(
                args.status, requires_human, final_gate_passed=final_gate_passed
            ),
            "current_gate": state["current_stage"],
            "active_task": "" if args.status == "passed" else task_id,
            "last_checkpoint_id": cycle_id,
            "last_checkpoint_utc": now,
            "next_action": next_action,
            "acceptance_condition": acceptance,
            "requires_human": (
                False
                if final_gate_passed or args.status in TERMINAL_PROJECT_STATUSES
                else requires_human
            ),
        }
    )
    row = _cycle_row(
        cycle_id=cycle_id,
        recorded_at=now,
        task_id=task_id,
        gate=args.gate,
        event="reopen" if reopening else "transition",
        from_status=from_status,
        to_status=args.status,
        summary=summary,
        evidence=evidence,
        next_action=next_action,
        acceptance_condition=acceptance,
        requires_human=execution["requires_human"],
    )
    _mutate_transaction(project, control, state, row)
    print(f"Transition recorded: {cycle_id}")
    print(f"Gate decision: {args.gate} -> {args.status}")
    print(
        f"Current stage: {state['current_stage']} "
        f"({state['stage_status']})"
    )
    print(f"Next action: {next_action}")
    print(f"Acceptance condition: {acceptance}")
    return 0


def _add_common_mutation_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("project_directory", type=Path)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--gate", choices=GATE_IDS, required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument(
        "--evidence",
        nargs="*",
        default=[],
        help="portable paths inside the project, or explicit source URLs",
    )
    parser.add_argument("--next-action", required=True)
    parser.add_argument("--acceptance-condition", required=True)
    parser.add_argument(
        "--requires-human",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="mark whether progress now depends on an authorized human",
    )
    parser.add_argument(
        "--blocker",
        action="append",
        default=[],
        help="repeat for multiple exact blockers",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    status = commands.add_parser("status", help="show durable stage and resume state")
    status.add_argument("project_directory", type=Path)
    status.add_argument("--json", action="store_true", dest="as_json")
    status.set_defaults(handler=command_status)

    checkpoint = commands.add_parser(
        "checkpoint", help="record a task checkpoint without passing the gate"
    )
    _add_common_mutation_arguments(checkpoint)
    checkpoint.add_argument(
        "--status", choices=sorted(CHECKPOINT_STATUSES), required=True
    )
    checkpoint.set_defaults(handler=command_checkpoint)

    transition = commands.add_parser(
        "transition", help="record an evidence-gated decision or explicit reopen"
    )
    _add_common_mutation_arguments(transition)
    transition.add_argument(
        "--status", choices=sorted(TRANSITION_STATUSES), required=True
    )
    transition.add_argument(
        "--reopen-dependent-gates",
        action="store_true",
        help="when reopening an earlier gate, reset every dependent gate to not_started",
    )
    transition.set_defaults(handler=command_transition)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.handler(args)
    except CycleError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
