from __future__ import annotations

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "research-rigor"
INIT = SKILL_ROOT / "scripts" / "init_research_project.py"
AUDIT = SKILL_ROOT / "scripts" / "audit_research_state.py"
CYCLE = SKILL_ROOT / "scripts" / "research_cycle.py"


class ResearchCycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="research-cycle-test-")
        self.project = Path(self.temporary.name) / "synthetic project"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(
        self, script: Path, *arguments: str, expected: int = 0
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(script), *map(str, arguments)],
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        if result.returncode != expected:
            self.fail(
                f"expected exit {expected}, got {result.returncode}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def initialize(self, literature_policy: str = "quota") -> Path:
        self.run_cli(
            INIT,
            self.project,
            "--title",
            "Synthetic Evidence Study",
            "--mode",
            "full-cycle",
            "--literature-policy",
            literature_policy,
            "--deep-read-min",
            "0",
            "--forensic-neighbor-min",
            "0",
            "--independent-audit-fraction",
            "0",
        )
        return self.project / ".research"

    def complete_g0_contracts(self, control: Path) -> None:
        for name in ("00_CONSTRAINTS.md", "00_AUTONOMY_CONTRACT.md"):
            path = control / name
            path.write_text(
                path.read_text(encoding="utf-8").replace("- [ ]", "- [x]"),
                encoding="utf-8",
                newline="\n",
            )

    def append_csv_row(
        self, control: Path, name: str, values: dict[str, str]
    ) -> None:
        path = control / name
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            headers = next(csv.reader(handle))
        with path.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writerow(values)

    def replace_csv_rows(
        self, control: Path, name: str, rows: list[dict[str, str]]
    ) -> None:
        path = control / name
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            headers = next(csv.reader(handle))
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    def transition(
        self,
        gate: str,
        *,
        evidence: list[str],
        summary: str | None = None,
        next_action: str | None = None,
        acceptance: str | None = None,
        status: str = "passed",
        expected: int = 0,
    ) -> subprocess.CompletedProcess[str]:
        return self.run_cli(
            CYCLE,
            "transition",
            self.project,
            "--task-id",
            f"{gate.lower()}-{status}",
            "--gate",
            gate,
            "--status",
            status,
            "--summary",
            summary or f"Synthetic evidence decision for {gate}",
            "--evidence",
            *evidence,
            "--next-action",
            next_action or f"Advance beyond {gate}",
            "--acceptance-condition",
            acceptance or f"The next gate after {gate} has decision-grade evidence",
            expected=expected,
        )

    def transition_g0(self, control: Path) -> None:
        self.run_cli(
            CYCLE,
            "transition",
            self.project,
            "--task-id",
            "g0-accept",
            "--gate",
            "G0",
            "--status",
            "passed",
            "--summary",
            "Scope and authority accepted",
            "--evidence",
            "00_CONSTRAINTS.md",
            "00_AUTONOMY_CONTRACT.md",
            "--next-action",
            "Screen research questions",
            "--acceptance-condition",
            "A viable candidate has decision value and a feasible evidence path",
        )

    def test_full_cycle_initialization_and_status(self) -> None:
        control = self.initialize()
        state = json.loads((control / "research_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["schema_version"], 2)
        self.assertEqual(state["execution"]["mode"], "full-cycle")
        for name in (
            "00_AUTONOMY_CONTRACT.md",
            "01_IDEA_CANDIDATES.csv",
            "04_EXPERIMENT_MATRIX.csv",
            "04_PROTOCOL_AMENDMENTS.csv",
            "07_FIGURE_AUDIT.csv",
            "07_MANUSCRIPT_AUDIT.csv",
            "08_RESPONSE_LETTER.md",
            "08_RESUBMISSION_HIGHLIGHTS.md",
            "08_COVER_LETTER.md",
            "RESEARCH_CYCLE_LOG.csv",
        ):
            self.assertTrue((control / name).is_file(), name)
        self.run_cli(AUDIT, self.project)
        status = self.run_cli(CYCLE, "status", self.project, "--json")
        payload = json.loads(status.stdout)
        self.assertEqual(payload["mode"], "full-cycle")
        self.assertEqual(payload["current_gate"], "G0")
        self.assertTrue(payload["structural_audit_ok"])

    def prepare_coverage_gate(self) -> Path:
        control = self.initialize("coverage")
        self.complete_g0_contracts(control)
        self.transition_g0(control)
        self.append_csv_row(control, "01_IDEA_CANDIDATES.csv", {
            "candidate_id": "idea-coverage", "research_question": "Can an audit detect stale summaries?",
            "decision_value": "Prevents stale evidence use", "technical_delta": "Version-aware audit",
            "strongest_already_done_argument": "Existing lineage tools may cover the question",
            "evidence_feasibility": "Local synthetic artifact graph",
            "falsifier": "Existing tool resolves every prespecified case",
            "kill_criteria": "No unresolved scientific delta", "status": "selected",
            "decision_owner": "synthetic owner", "decision_evidence": "01_PROBLEM_CARD.md",
        })
        self.transition("G1", evidence=["01_IDEA_CANDIDATES.csv"])
        self.append_csv_row(control, "02_SEARCH_LOG.csv", {
            "query_id": "q1", "searched_at": "2026-01-01", "source": "synthetic corpus",
            "query": "stale summary lineage", "retrieved_ids": "p1",
        })
        self.append_csv_row(control, "02_LITERATURE_LOG.csv", {
            "paper_id": "p1", "full_text_verified": "true", "forensic": "true",
            "anchors": "Synthetic source section 2", "audit_status": "passed",
        })
        self.append_csv_row(control, "02_NEAREST_NEIGHBOR_MATRIX.csv", {
            "paper_id": "p1", "research_question": "Artifact lineage",
            "unit_or_shift": "Changed source version", "candidate_exact_delta": "Summary supersession",
            "strongest_already_done_argument": "Version graphs may imply the proposed rule",
            "anchors": "Synthetic source section 2", "forensic_status": "verified",
        })
        assessment = {
            "status": "supported", "search_scope": "Synthetic fixture corpus only",
            "search_saturation": "All fixture records and their references inspected",
            "exact_delta": "The synthetic record omits summary supersession",
            "strongest_counterargument": "Could be a direct application of lineage tracking",
            "evidence_feasibility": "Bounded local fixture; no scientific novelty claim",
            "unresolved_risks": ["Synthetic record cannot establish real-world novelty"],
            "decision_basis": "Proceed only for testing structural coverage",
            "verified_source_ids": ["p1"], "nearest_neighbor_ids": ["p1"],
            "source_audit": {"kind": "same-agent-source-check", "auditor": "test fixture",
                             "source_ids": ["p1"], "findings": "Anchors checked in the fixture"},
        }
        (control / "02_NOVELTY_ASSESSMENT.json").write_text(json.dumps(assessment), encoding="utf-8")
        return control

    def test_default_policy_uses_coverage_without_universal_counts(self) -> None:
        self.run_cli(INIT, self.project)
        state = json.loads((self.project / ".research" / "research_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["literature_policy"]["mode"], "coverage")
        self.assertEqual(state["literature_policy"]["verified_deep_read_min"], 0)
        self.assertIsNone(state["claim_policy"]["headline_max"])
        self.assertFalse(state["execution"]["requires_human"])
        self.assertEqual(state["execution"]["status"], "ready")
        self.run_cli(AUDIT, self.project)

    def test_source_linked_coverage_can_pass_without_large_corpus(self) -> None:
        control = self.prepare_coverage_gate()
        self.transition("G2", evidence=["02_NOVELTY_ASSESSMENT.json"])
        self.run_cli(AUDIT, self.project)
        state = json.loads((control / "research_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["gates"][2]["status"], "passed")

    def test_coverage_rejects_empty_assessment_and_rolls_back(self) -> None:
        control = self.prepare_coverage_gate()
        (control / "02_NOVELTY_ASSESSMENT.json").write_text("{}", encoding="utf-8")
        result = self.transition("G2", evidence=["02_NOVELTY_ASSESSMENT.json"], expected=2)
        self.assertIn("coverage assessment", result.stderr + result.stdout)
        state = json.loads((control / "research_state.json").read_text(encoding="utf-8"))
        self.assertNotEqual(state["gates"][2]["status"], "passed")

    def test_coverage_rejects_unverified_and_unlinked_sources(self) -> None:
        control = self.prepare_coverage_gate()
        self.replace_csv_rows(control, "02_LITERATURE_LOG.csv", [{
            "paper_id": "p1", "full_text_verified": "false", "anchors": "Abstract only",
            "forensic": "true", "audit_status": "passed",
        }])
        result = self.transition("G2", evidence=["02_NOVELTY_ASSESSMENT.json"], expected=2)
        self.assertIn("verified full text", result.stderr + result.stdout)
        self.replace_csv_rows(control, "02_LITERATURE_LOG.csv", [{
            "paper_id": "p1", "full_text_verified": "true", "anchors": "Section 2",
            "forensic": "true", "audit_status": "passed",
        }])
        self.replace_csv_rows(control, "02_NEAREST_NEIGHBOR_MATRIX.csv", [])
        result = self.transition("G2", evidence=["02_NOVELTY_ASSESSMENT.json"], expected=2)
        self.assertIn("complete matrix rows", result.stderr + result.stdout)

    def test_coverage_honors_explicit_quota_and_merge_preserves_it(self) -> None:
        control = self.prepare_coverage_gate()
        state_path = control / "research_state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["literature_policy"]["verified_deep_read_min"] = 2
        state_path.write_text(json.dumps(state), encoding="utf-8")
        before = state_path.read_bytes()
        self.run_cli(INIT, self.project, "--merge")
        self.assertEqual(state_path.read_bytes(), before)
        result = self.transition("G2", evidence=["02_NOVELTY_ASSESSMENT.json"], expected=2)
        self.assertIn("requires 2", result.stderr + result.stdout)

    def test_coverage_rejects_pending_nearest_neighbor(self) -> None:
        control = self.prepare_coverage_gate()
        path = control / "02_NEAREST_NEIGHBOR_MATRIX.csv"
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        rows[0]["forensic_status"] = "pending"
        self.replace_csv_rows(control, path.name, rows)
        result = self.transition("G2", evidence=["02_NOVELTY_ASSESSMENT.json"], expected=2)
        self.assertIn("complete matrix rows", result.stderr + result.stdout)

    def test_claim_limit_is_optional_but_legacy_contract_is_preserved(self) -> None:
        control = self.prepare_coverage_gate()
        self.transition("G2", evidence=["02_NOVELTY_ASSESSMENT.json"])
        for index in range(4):
            self.append_csv_row(control, "03_CLAIM_EVIDENCE_MATRIX.csv", {
                "claim_id": f"c{index}", "exact_text": f"Synthetic claim {index}",
                "falsifier": "A contrary fixture", "strongest_baseline": "Existing lineage audit",
                "non_claims": "No scientific conclusion from these fixtures", "status": "frozen",
            })
        self.transition("G3", evidence=["03_CLAIM_EVIDENCE_MATRIX.csv"])
        path = control / "research_state.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state.pop("claim_policy")
        path.write_text(json.dumps(state), encoding="utf-8")
        result = self.run_cli(AUDIT, self.project, expected=1)
        self.assertIn("configured 3 frozen headline claims", result.stdout + result.stderr)
        state["claim_policy"] = {"headline_max": 4}
        path.write_text(json.dumps(state), encoding="utf-8")
        self.run_cli(AUDIT, self.project)

    def test_legacy_policy_without_mode_keeps_quota_behavior(self) -> None:
        control = self.prepare_coverage_gate()
        path = control / "research_state.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        del state["literature_policy"]["mode"]
        state.pop("claim_policy")
        path.write_text(json.dumps(state), encoding="utf-8")
        (control / "02_NOVELTY_ASSESSMENT.json").unlink()
        self.transition("G2", evidence=["02_SEARCH_LOG.csv"])
        self.run_cli(AUDIT, self.project)

    def test_coverage_assessment_rejects_path_escape(self) -> None:
        control = self.prepare_coverage_gate()
        path = control / "research_state.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state["literature_policy"]["assessment_file"] = "../elsewhere.json"
        path.write_text(json.dumps(state), encoding="utf-8")
        result = self.transition("G2", evidence=["02_SEARCH_LOG.csv"], expected=2)
        self.assertIn("portable relative path", result.stderr + result.stdout)

    def test_legacy_review_matrix_remains_structurally_auditable(self) -> None:
        control = self.initialize()
        legacy_headers = [
            "comment_id",
            "reviewer_request",
            "type",
            "severity",
            "scientific_validity",
            "action",
            "evidence_needed",
            "artifact_or_diff",
            "regression_checks",
            "unresolved_limitation",
            "status",
            "response_text",
        ]
        with (control / "08_REVIEW_REMEDIATION.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=legacy_headers)
            writer.writeheader()
            writer.writerow(
                {
                    "comment_id": "legacy-review-1",
                    "reviewer_request": "Clarify scope",
                    "type": "clarification",
                    "severity": "minor",
                    "scientific_validity": "No change",
                    "action": "State the boundary",
                    "evidence_needed": "Existing claim map",
                    "artifact_or_diff": "07_ONE_PAGE_PAPER.md",
                    "regression_checks": "Conclusion remains bounded",
                    "unresolved_limitation": "External cases",
                    "status": "resolved",
                    "response_text": "The scope is now explicit.",
                }
            )
        result = self.run_cli(AUDIT, self.project)
        self.assertIn("legacy schema", result.stdout)

    def test_checkpoint_persists_resume_state(self) -> None:
        control = self.initialize()
        self.run_cli(
            CYCLE,
            "checkpoint",
            self.project,
            "--task-id",
            "g0-orientation",
            "--gate",
            "G0",
            "--status",
            "in_progress",
            "--summary",
            "Inspected constraints and workspace",
            "--evidence",
            "00_CONSTRAINTS.md",
            "--next-action",
            "Resolve the remaining authority fields",
            "--acceptance-condition",
            "Every G0 acceptance checkbox is checked",
        )
        state = json.loads((control / "research_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["stage_status"], "in_progress")
        self.assertEqual(state["execution"]["status"], "running")
        self.assertEqual(state["execution"]["active_task"], "g0-orientation")
        with (control / "RESEARCH_CYCLE_LOG.csv").open(
            "r", encoding="utf-8", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["task_id"], "g0-orientation")
        self.run_cli(AUDIT, self.project)

    def test_pass_without_evidence_is_rejected_without_mutation(self) -> None:
        control = self.initialize()
        result = self.run_cli(
            CYCLE,
            "transition",
            self.project,
            "--task-id",
            "g0-invalid-pass",
            "--gate",
            "G0",
            "--status",
            "passed",
            "--summary",
            "Attempted unsupported pass",
            "--next-action",
            "Continue",
            "--acceptance-condition",
            "Not applicable",
            expected=2,
        )
        self.assertIn("requires at least one --evidence", result.stderr)
        state = json.loads((control / "research_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["gates"][0]["status"], "not_started")
        with (control / "RESEARCH_CYCLE_LOG.csv").open(
            "r", encoding="utf-8", newline=""
        ) as handle:
            self.assertEqual(list(csv.DictReader(handle)), [])

    def test_unchecked_human_contract_rolls_back_pass(self) -> None:
        control = self.initialize()
        original_state = (control / "research_state.json").read_text(encoding="utf-8")
        original_log = (control / "RESEARCH_CYCLE_LOG.csv").read_text(encoding="utf-8")
        result = self.run_cli(
            CYCLE,
            "transition",
            self.project,
            "--task-id",
            "g0-unchecked",
            "--gate",
            "G0",
            "--status",
            "passed",
            "--summary",
            "Attempted pass before human acceptance",
            "--evidence",
            "00_CONSTRAINTS.md",
            "00_AUTONOMY_CONTRACT.md",
            "--next-action",
            "Screen research questions",
            "--acceptance-condition",
            "A viable candidate exists",
            expected=2,
        )
        self.assertIn("rolled back", result.stderr)
        self.assertEqual(
            (control / "research_state.json").read_text(encoding="utf-8"),
            original_state,
        )
        self.assertEqual(
            (control / "RESEARCH_CYCLE_LOG.csv").read_text(encoding="utf-8"),
            original_log,
        )

    def test_pass_and_explicit_reopen_reset_dependent_gate(self) -> None:
        control = self.initialize()
        self.complete_g0_contracts(control)
        self.transition_g0(control)
        candidates = control / "01_IDEA_CANDIDATES.csv"
        with candidates.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(
                [
                    "idea-1",
                    "Does a deterministic checksum catch synthetic corruption?",
                    "Prevents invalid artifacts from entering a report",
                    "Gate corruption before aggregation",
                    "Checksum validation is established practice",
                    "Testable with synthetic bytes",
                    "Fits local CPU",
                    "No private data",
                    "Corruption passes undetected",
                    "No decision-relevant detection gain",
                    "viable",
                    "test owner",
                    "01_PROBLEM_CARD.md",
                ]
            )
        self.run_cli(
            CYCLE,
            "transition",
            self.project,
            "--task-id",
            "g1-select",
            "--gate",
            "G1",
            "--status",
            "passed",
            "--summary",
            "A viable synthetic question survived value screening",
            "--evidence",
            "01_PROBLEM_CARD.md",
            "01_IDEA_CANDIDATES.csv",
            "--next-action",
            "Attack novelty and select one candidate",
            "--acceptance-condition",
            "Exactly one candidate is selected with evidence",
        )
        self.run_cli(
            CYCLE,
            "transition",
            self.project,
            "--task-id",
            "g0-reopen",
            "--gate",
            "G0",
            "--status",
            "in_progress",
            "--reopen-dependent-gates",
            "--summary",
            "Resource limit changed and invalidated dependent planning",
            "--evidence",
            "00_CONSTRAINTS.md",
            "--next-action",
            "Reconfirm compute budget",
            "--acceptance-condition",
            "Updated constraints receive human acceptance",
        )
        state = json.loads((control / "research_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["current_stage"], "G0")
        self.assertEqual(state["gates"][0]["status"], "in_progress")
        self.assertEqual(state["gates"][1]["status"], "not_started")
        self.run_cli(AUDIT, self.project)

    def test_applied_protocol_amendment_requires_fresh_validation(self) -> None:
        control = self.initialize()
        amendment = {
            "amendment_id": "amend-1",
            "opened_at": "2026-01-01T00:00:00+00:00",
            "trigger_type": "measurement_defect",
            "trigger_evidence": "pilot/raw-output.json",
            "old_protocol_version": "v1",
            "changed_fields": "valid denominator",
            "scientific_impact": "Original pilot cannot support the claim",
            "invalidated_artifacts": "pilot/result.json",
            "new_protocol_version": "v2",
            "authorization_basis": "authorized test owner",
            "fresh_validation_required": "true",
            "fresh_validation_evidence": "",
            "status": "applied",
        }
        self.append_csv_row(control, "04_PROTOCOL_AMENDMENTS.csv", amendment)
        failed = self.run_cli(AUDIT, self.project, expected=1)
        self.assertIn("requires fresh validation evidence", failed.stdout)
        evidence = self.project / "fresh" / "validation.txt"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("fresh held-out validation passed\n", encoding="utf-8")
        amendment["fresh_validation_evidence"] = "fresh/validation.txt"
        self.replace_csv_rows(
            control, "04_PROTOCOL_AMENDMENTS.csv", [amendment]
        )
        self.run_cli(AUDIT, self.project)

    def test_valid_scientific_failure_can_end_without_cosmetic_repair(self) -> None:
        control = self.initialize()
        self.complete_g0_contracts(control)
        self.transition_g0(control)
        self.append_csv_row(
            control,
            "01_IDEA_CANDIDATES.csv",
            {
                "candidate_id": "idea-null",
                "research_question": "Does the candidate beat the strongest baseline?",
                "decision_value": "Avoids investing in an ineffective direction",
                "technical_delta": "A prespecified candidate comparison",
                "strongest_already_done_argument": "The baseline already solves it",
                "evidence_feasibility": "Synthetic paired test",
                "resource_fit": "Local CPU",
                "privacy_ethics_fit": "No private data",
                "falsifier": "Candidate does not beat the baseline",
                "kill_criteria": "Frozen margin is missed",
                "status": "viable",
                "decision_owner": "test owner",
                "decision_evidence": "01_PROBLEM_CARD.md",
            },
        )
        self.transition("G1", evidence=["01_PROBLEM_CARD.md", "01_IDEA_CANDIDATES.csv"])
        result = self.transition(
            "G2",
            status="killed",
            evidence=["01_IDEA_CANDIDATES.csv"],
            summary="The exact nearest neighbor already answers the question",
            next_action="Archive the negative novelty decision",
            acceptance="Decision evidence and reusable search terms are preserved",
        )
        self.assertIn("G2 -> killed", result.stdout)
        state = json.loads((control / "research_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["gates"][2]["status"], "killed")
        self.assertEqual(state["execution"]["status"], "complete")
        self.assertNotEqual(state["gates"][2]["status"], "passed")
        self.run_cli(AUDIT, self.project)

    def test_synthetic_full_cycle_reaches_audited_submission_state(self) -> None:
        control = self.initialize()
        self.complete_g0_contracts(control)
        self.transition_g0(control)

        self.append_csv_row(
            control,
            "01_IDEA_CANDIDATES.csv",
            {
                "candidate_id": "idea-1",
                "research_question": "Can a checksum gate prevent corrupted synthetic facts?",
                "decision_value": "Prevents invalid evidence from entering a report",
                "technical_delta": "Verify artifacts before aggregation",
                "strongest_already_done_argument": "Checksums are already standard",
                "evidence_feasibility": "Deterministic byte corruption test",
                "resource_fit": "Local CPU",
                "privacy_ethics_fit": "No private or human data",
                "falsifier": "Corruption enters the fact table undetected",
                "kill_criteria": "No detection advantage over the baseline",
                "status": "selected",
                "decision_owner": "synthetic test owner",
                "decision_evidence": "01_PROBLEM_CARD.md",
            },
        )
        self.transition("G1", evidence=["01_PROBLEM_CARD.md", "01_IDEA_CANDIDATES.csv"])

        self.append_csv_row(
            control,
            "02_SEARCH_LOG.csv",
            {
                "query_id": "search-1",
                "searched_at": "2026-01-01",
                "source": "synthetic corpus",
                "query": "checksum corruption evidence gate",
                "retrieved_ids": "none",
            },
        )
        self.transition(
            "G2",
            evidence=[
                "01_IDEA_CANDIDATES.csv",
                "02_SEARCH_LOG.csv",
                "02_LITERATURE_LOG.csv",
                "02_NEAREST_NEIGHBOR_MATRIX.csv",
            ],
        )

        self.append_csv_row(
            control,
            "03_CLAIM_EVIDENCE_MATRIX.csv",
            {
                "claim_id": "claim-1",
                "exact_text": "The gate detects all prespecified corruptions.",
                "falsifier": "Any prespecified corruption is accepted",
                "strongest_baseline": "No verification",
                "non_claims": "No claim about unknown corruption classes",
                "status": "frozen",
            },
        )
        self.transition("G3", evidence=["03_CLAIM_EVIDENCE_MATRIX.csv"])

        self.append_csv_row(
            control,
            "04_COVERAGE_MODEL.csv",
            {
                "step": "verify",
                "planned_count": "4",
                "expected_valid_rate": "1",
                "pilot_valid_rate": "1",
                "minimum_required": "4",
                "action_if_below": "kill claim",
            },
        )
        self.append_csv_row(
            control,
            "04_EXPERIMENT_MATRIX.csv",
            {
                "cell_id": "cell-1",
                "claim_id": "claim-1",
                "role": "confirmatory",
                "dataset_or_source": "synthetic bytes",
                "split": "locked synthetic cases",
                "condition": "prespecified corruption",
                "method": "checksum gate",
                "baseline": "no verification",
                "ablation": "verification disabled",
                "seed_or_repetition": "deterministic",
                "metric": "detection rate",
                "valid_denominator": "all prespecified corruptions",
                "pass_threshold": "1.0",
                "kill_or_redesign_threshold": "<1.0",
                "planned_status": "required",
                "artifact_path": "artifacts/cell-1.json",
            },
        )
        self.transition(
            "G4",
            evidence=[
                "04_EXPERIMENT_PROTOCOL.md",
                "04_EXPERIMENT_MATRIX.csv",
                "04_COVERAGE_MODEL.csv",
            ],
        )

        implementation = self.project / "src" / "pipeline.py"
        implementation.parent.mkdir(parents=True)
        implementation.write_text(
            "def verified(expected, observed):\n    return expected == observed\n",
            encoding="utf-8",
        )
        smoke = self.project / "artifacts" / "smoke.txt"
        smoke.parent.mkdir(parents=True)
        smoke.write_text("clean-room smoke passed\n", encoding="utf-8")
        self.transition("G5", evidence=["src/pipeline.py", "artifacts/smoke.txt"])

        self.append_csv_row(
            control,
            "05_RUN_LEDGER.csv",
            {
                "run_id": "run-1",
                "planned_cell": "cell-1",
                "protocol_version": "v1",
                "started_at": "2026-01-01T00:00:00Z",
                "finished_at": "2026-01-01T00:00:01Z",
                "source_commit": "synthetic-commit",
                "config_hash": "config-sha256",
                "data_hash": "data-sha256",
                "seed": "deterministic",
                "hardware": "local-cpu",
                "status": "complete",
                "raw_artifact": "artifacts/run-1.json",
                "artifact_hash": "artifact-sha256",
                "completion_manifest": "artifacts/manifest.json",
            },
        )
        raw = self.project / "artifacts" / "run-1.json"
        raw.write_text('{"planned":4,"detected":4}\n', encoding="utf-8")
        self.transition("G6", evidence=["05_RUN_LEDGER.csv", "artifacts/run-1.json"])
        self.transition("G7", evidence=["05_RUN_LEDGER.csv", "artifacts/run-1.json"])

        self.append_csv_row(
            control,
            "06_RESULT_FACTS.csv",
            {
                "fact_id": "fact-1",
                "claim_id": "claim-1",
                "run_id": "run-1",
                "metric": "detection rate",
                "unit": "proportion",
                "estimate": "1.0",
                "ci_low": "1.0",
                "ci_high": "1.0",
                "denominator": "4 prespecified corruptions",
                "split": "locked synthetic cases",
                "evidence_tier": "confirmatory",
                "status": "green",
                "source_artifact": "artifacts/run-1.json",
                "source_hash": "artifact-sha256",
                "limitations": "Synthetic corruptions only",
            },
        )
        self.transition("G8", evidence=["06_RESULT_FACTS.csv", "artifacts/run-1.json"])

        self.append_csv_row(
            control,
            "07_PAPER_CLAIM_MAP.csv",
            {
                "section": "Results",
                "claim_id": "claim-1",
                "claim_text": "All four prespecified corruptions were detected.",
                "fact_ids": "fact-1",
                "evidence_tier": "confirmatory",
                "valid_denominator": "4 prespecified corruptions",
                "limitations": "Synthetic corruptions only",
                "non_claims": "No unknown-corruption generalization",
                "citation_or_source": "06_RESULT_FACTS.csv",
                "status": "supported",
            },
        )
        open_finding = {
            "finding_id": "finding-1",
            "location": "Abstract",
            "audit_type": "claim-evidence",
            "severity": "major",
            "claim_or_text": "The method catches all corruption",
            "evidence_ids": "",
            "issue": "The sentence generalizes beyond prespecified cases",
            "required_action": "Remove or narrow the unsupported sentence",
            "status": "open",
            "resolution_evidence": "",
        }
        self.append_csv_row(control, "07_MANUSCRIPT_AUDIT.csv", open_finding)
        rejected = self.transition(
            "G9",
            evidence=[
                "07_ONE_PAGE_PAPER.md",
                "07_PAPER_CLAIM_MAP.csv",
                "07_MANUSCRIPT_AUDIT.csv",
            ],
            expected=2,
        )
        self.assertIn("unresolved fatal or major", rejected.stderr)
        state_after_rejection = json.loads(
            (control / "research_state.json").read_text(encoding="utf-8")
        )
        self.assertEqual(state_after_rejection["current_stage"], "G9")
        open_finding["claim_or_text"] = "All four prespecified corruptions were detected"
        open_finding["evidence_ids"] = "fact-1"
        open_finding["status"] = "resolved"
        open_finding["resolution_evidence"] = "07_PAPER_CLAIM_MAP.csv"
        self.replace_csv_rows(
            control, "07_MANUSCRIPT_AUDIT.csv", [open_finding]
        )
        self.transition(
            "G9",
            evidence=[
                "07_ONE_PAGE_PAPER.md",
                "07_PAPER_CLAIM_MAP.csv",
                "07_MANUSCRIPT_AUDIT.csv",
            ],
        )

        review_source = self.project / "reviews" / "internal-review.md"
        review_source.parent.mkdir(parents=True)
        review_source.write_text(
            "Clarify the evidence boundary for the synthetic cases.\n",
            encoding="utf-8",
        )
        self.append_csv_row(
            control,
            "08_REVIEW_REMEDIATION.csv",
            {
                "comment_id": "review-1",
                "source": "internal_red_team",
                "source_record": "reviews/internal-review.md",
                "reviewer_request": "Clarify the evidence boundary",
                "reviewer_intent": "Prevent unsupported generalization",
                "type": "clarification",
                "severity": "major",
                "assessment": "valid",
                "scientific_validity": "No change",
                "action": "State synthetic-case limitation",
                "changed_locations": "Limitations paragraph",
                "change_evidence": "07_ONE_PAGE_PAPER.md",
                "response_anchor": "review-1",
                "regression_checks": "claim map remains supported",
                "unresolved_limitation": "Unknown corruptions",
                "status": "resolved",
                "response_text": "Scope was narrowed to prespecified cases.",
            },
        )
        self.transition("G10", evidence=["08_REVIEW_REMEDIATION.csv"])

        checklist = control / "09_SUBMISSION_CHECKLIST.md"
        checklist.write_text(
            checklist.read_text(encoding="utf-8").replace("- [ ]", "- [x]"),
            encoding="utf-8",
            newline="\n",
        )
        state = json.loads((control / "research_state.json").read_text(encoding="utf-8"))
        state["privacy"]["release_scan_passed"] = True
        state["privacy"]["semantic_review_passed"] = True
        (control / "research_state.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        self.transition(
            "G11",
            evidence=["09_SUBMISSION_CHECKLIST.md", "11_ARCHIVE_RECORD.md"],
            next_action="Preserve the canonical synthetic package",
            acceptance="A human can reproduce the verified archive",
        )

        final_state = json.loads(
            (control / "research_state.json").read_text(encoding="utf-8")
        )
        self.assertTrue(all(gate["status"] == "passed" for gate in final_state["gates"]))
        self.assertTrue(final_state["frozen"]["claims"])
        self.assertTrue(final_state["frozen"]["protocol"])
        self.assertTrue(final_state["frozen"]["submission_ready"])
        self.assertEqual(final_state["execution"]["status"], "complete")
        self.run_cli(AUDIT, self.project)
        final_status = self.run_cli(CYCLE, "status", self.project, "--json")
        self.assertTrue(json.loads(final_status.stdout)["structural_audit_ok"])


if __name__ == "__main__":
    unittest.main()
