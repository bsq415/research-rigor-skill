from __future__ import annotations

import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "research-rigor"
INIT = SKILL_ROOT / "scripts" / "init_research_project.py"
AUDIT = SKILL_ROOT / "scripts" / "audit_revision_package.py"


class RevisionPackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="revision-package-test-")
        self.project = Path(self.temporary.name) / "synthetic-study"
        self.run_cli(INIT, self.project, "--title", "Synthetic Revision Study")
        self.control = self.project / ".research"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(
        self, script: Path, *arguments: object, expected: int = 0
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

    def write_csv(self, name: str, rows: list[dict[str, str]]) -> None:
        path = self.control / name
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            headers = next(csv.reader(handle))
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    def write_project_file(self, relative: str, text: str) -> None:
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def complete_package(self) -> tuple[dict[str, str], dict[str, str]]:
        self.write_project_file(
            "reviews/decision.md",
            "Reviewer 1 asks the authors to clarify the prespecified evidence boundary.",
        )
        self.write_project_file(
            "manuscript/revision.md",
            "The limitations paragraph now bounds the claim to prespecified cases.",
        )
        self.write_project_file("data/figure.csv", "x,y\n0,0\n1,1\n")
        self.write_project_file(
            "scripts/make_figure.py", "print('synthetic deterministic figure')\n"
        )
        self.write_project_file("figures/figure.pdf", "% synthetic vector fixture\n")
        self.write_project_file("renders/manuscript-page.png", "synthetic render\n")

        review = {
            "comment_id": "R1-C01",
            "source": "reviewer_1",
            "source_record": "reviews/decision.md",
            "reviewer_request": "Clarify the evidence boundary",
            "reviewer_intent": "Prevent unsupported generalization",
            "type": "evidence|clarification",
            "severity": "major",
            "assessment": "valid",
            "scientific_validity": "The claim requires a narrower denominator",
            "action": "Narrow the claim and link the supporting fact",
            "evidence_needed": "Prespecified-case result with its denominator",
            "evidence_ids": "fact-1",
            "changed_locations": "Limitations, paragraph 1",
            "change_evidence": "manuscript/revision.md",
            "response_anchor": "R1-C01",
            "regression_checks": "Abstract and conclusion use the same boundary",
            "citation_checks": "not_applicable",
            "unresolved_limitation": "Unknown cases remain outside scope",
            "status": "resolved",
            "response_text": "The claim is now limited to prespecified cases.",
        }
        figure = {
            "figure_id": "FIG-1",
            "claim_id": "claim-1",
            "content_type": "plot",
            "source_data": "data/figure.csv",
            "generation_artifact": "scripts/make_figure.py",
            "final_asset": "figures/figure.pdf",
            "final_render_evidence": "renders/manuscript-page.png",
            "format": "pdf",
            "vector_or_raster": "vector",
            "target_width": "single-column width from official template",
            "effective_dpi": "not_applicable",
            "required_min_dpi": "not_applicable",
            "font_embedded_or_na": "passed",
            "legible_at_final_size": "passed",
            "line_and_marker_check": "passed",
            "color_independent": "passed",
            "crop_checked": "passed",
            "axis_integrity": "full_range",
            "uncertainty_or_na": "not_applicable: deterministic fixture",
            "caption_check": "passed",
            "final_render_checked": "passed",
            "status": "passed",
            "notes": "Synthetic privacy-safe fixture",
        }
        self.write_csv("08_REVIEW_REMEDIATION.csv", [review])
        self.write_csv("07_FIGURE_AUDIT.csv", [figure])

        (self.control / "08_RESPONSE_LETTER.md").write_text(
            """# Response to Reviewers

Status: final

## R1-C01

**Comment.** Please clarify the evidence boundary.

**Response.** We agree and now limit the claim to the prespecified cases.

**Evidence.** Fact `fact-1` records the valid denominator.

**Changes in the manuscript.** The limitations paragraph and conclusion now use
the same boundary.
""",
            encoding="utf-8",
            newline="\n",
        )
        (self.control / "08_RESUBMISSION_HIGHLIGHTS.md").write_text(
            """# Resubmission Highlights

Status: final

## Portal-ready highlights

- The evidence boundary is now explicit and linked to its valid denominator.
- The abstract, limitations, and conclusion now use one consistent claim scope.
- A final-size vector figure audit records source data and rendered-page evidence.
""",
            encoding="utf-8",
            newline="\n",
        )
        (self.control / "08_COVER_LETTER.md").write_text(
            """# Resubmission Cover Letter

Status: final

Dear Editor,

**Re: Resubmission of the synthetic evidence-boundary study**

The revision narrows the claim to the prespecified denominator, links the result
to its sealed fact, and records a final-size figure audit. The point-by-point
response and marked manuscript accompany this letter. All policy declarations
and author metadata require confirmation by the authorized human before upload.

Yours sincerely,

The authorized corresponding author
""",
            encoding="utf-8",
            newline="\n",
        )
        return review, figure

    def test_unfinished_scaffold_fails_strict_audit(self) -> None:
        result = self.run_cli(AUDIT, self.project, "--strict", expected=1)
        self.assertIn("unfinished template marker", result.stdout)
        self.assertIn("requires at least one row", result.stdout)

    def test_complete_revision_package_passes_strict_audit(self) -> None:
        self.complete_package()
        result = self.run_cli(
            AUDIT,
            self.project,
            "--strict",
            "--expected-comments",
            "1",
        )
        self.assertIn("Revision package audit: PASS", result.stdout)

    def test_unresolved_evidence_request_fails_strict_audit(self) -> None:
        review, figure = self.complete_package()
        review["status"] = "open"
        review["evidence_ids"] = ""
        self.write_csv("08_REVIEW_REMEDIATION.csv", [review])
        result = self.run_cli(AUDIT, self.project, "--strict", expected=1)
        self.assertIn("is not terminal in strict mode", result.stdout)

    def test_missing_response_anchor_is_detected(self) -> None:
        self.complete_package()
        response = self.control / "08_RESPONSE_LETTER.md"
        response.write_text(
            response.read_text(encoding="utf-8").replace("R1-C01", "R1-C02"),
            encoding="utf-8",
            newline="\n",
        )
        result = self.run_cli(AUDIT, self.project, "--strict", expected=1)
        self.assertIn("response_anchor is absent", result.stdout)

    def test_expected_comment_count_detects_coverage_gap(self) -> None:
        self.complete_package()
        result = self.run_cli(
            AUDIT,
            self.project,
            "--strict",
            "--expected-comments",
            "2",
            expected=1,
        )
        self.assertIn("expected 2 actionable comments, found 1", result.stdout)

    def test_explicit_no_figure_record_is_supported(self) -> None:
        self.complete_package()
        self.write_csv(
            "07_FIGURE_AUDIT.csv",
            [
                {
                    "figure_id": "FIG-NONE",
                    "content_type": "not_applicable",
                    "vector_or_raster": "not_applicable",
                    "status": "not_applicable",
                    "notes": "The synthetic manuscript contains no submitted figures.",
                }
            ],
        )
        self.run_cli(AUDIT, self.project, "--strict", "--expected-comments", "1")

    def test_low_effective_dpi_and_unjustified_axis_fail(self) -> None:
        review, figure = self.complete_package()
        self.write_project_file("figures/figure.png", "synthetic raster fixture\n")
        figure.update(
            {
                "final_asset": "figures/figure.png",
                "format": "png",
                "vector_or_raster": "raster",
                "effective_dpi": "200",
                "required_min_dpi": "300",
                "font_embedded_or_na": "not_applicable",
                "axis_integrity": "justified_truncation",
                "notes": "",
            }
        )
        self.write_csv("07_FIGURE_AUDIT.csv", [figure])
        result = self.run_cli(AUDIT, self.project, "--strict", expected=1)
        self.assertIn("effective DPI 200 is below", result.stdout)
        self.assertIn("without a recorded justification", result.stdout)

    def test_citation_request_requires_verification_record(self) -> None:
        review, figure = self.complete_package()
        review["type"] = "citation"
        review["citation_checks"] = ""
        self.write_csv("08_REVIEW_REMEDIATION.csv", [review])
        result = self.run_cli(AUDIT, self.project, "--strict", expected=1)
        self.assertIn("lacks citation_checks", result.stdout)


if __name__ == "__main__":
    unittest.main()
