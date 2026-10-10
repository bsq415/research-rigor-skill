from collections import Counter
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/research-rigor/scripts/rigor_eval.py"
spec = importlib.util.spec_from_file_location("rigor_eval", SCRIPT)
bench = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench)


class RigorEvalTests(unittest.TestCase):
    def prepare(self, root, repeats=1):
        directory = root / "run"
        with contextlib.redirect_stdout(io.StringIO()):
            bench.prepare(directory, "test-model", "medium", repeats=repeats)
        return directory

    def populate(self, directory):
        plan = bench.load_plan(directory)
        rubric = {t["id"]: t for t in bench.read(directory / "rubric.private.json")["tasks"]}
        for row in plan["rows"]:
            bench.write(directory / "responses" / (row["run_id"] + ".json"),
                        dict(status="completed", seconds=1,
                             answer=dict(verdict=rubric[row["task_id"]]["expected_verdict"],
                                         analysis="fixture evidence", revised_text="", next_check="")))
        with contextlib.redirect_stdout(io.StringIO()):
            bench.blind(directory)
        for answer in bench.read(directory / "blind-answers.json"):
            # Fixture grades exercise accounting, not scientific grading.
            grade = dict(blind_id=answer["blind_id"],
                         criteria=[{"pass": True, "quote": "fixture evidence", "reason": "fixture"} for _ in range(4)],
                         critical_failure=False, critical_reason="")
            bench.write(directory / "grades" / (answer["blind_id"] + ".json"),
                        dict(status="completed", answer=grade))

    def test_frozen_plan_has_matched_complete_pairs(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = self.prepare(Path(temp), repeats=2)
            plan = bench.load_plan(directory)
            self.assertEqual(len(plan["rows"]), 40)
            counts = Counter((r["task_id"], r["repeat"], r["condition"]) for r in plan["rows"])
            self.assertEqual(set(counts.values()), {1})
            for task in bench.read(directory / "tasks.json")["tasks"]:
                for repeat in (1, 2):
                    for condition in ("baseline", "skill"):
                        self.assertEqual(counts[task["id"], repeat, condition], 1)
            with self.assertRaises(ValueError):
                self.prepare(Path(temp))

    def test_tampered_context_and_plan_are_rejected(self):
        for name in ("skill-context.txt", "plan.private.json"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp:
                directory = self.prepare(Path(temp))
                with (directory / name).open("a", encoding="utf-8") as stream:
                    stream.write("\nchanged")
                with self.assertRaises(ValueError):
                    bench.load_plan(directory)

    def test_resume_never_retries_a_failed_attempt(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = self.prepare(Path(temp))
            row = bench.load_plan(directory)["rows"][0]
            bench.write(directory / "responses" / (row["run_id"] + ".json"), {"status": "error"})
            with patch.object(bench, "call_codex", return_value={"status": "error"}) as call:
                with contextlib.redirect_stdout(io.StringIO()):
                    bench.run(directory, limit=1)
                self.assertEqual(call.call_count, 1)
                self.assertNotEqual(call.call_args.args[3].stem, row["run_id"])

    def test_blind_requires_all_planned_attempts_and_hides_labels(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = self.prepare(Path(temp))
            with self.assertRaises(ValueError):
                bench.blind(directory)
            self.populate(directory)
            answers = bench.read(directory / "blind-answers.json")
            self.assertEqual(len(answers), 20)
            self.assertTrue(all("condition" not in a and "run_id" not in a for a in answers))

    def test_summary_counts_and_critical_failure_override(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = self.prepare(Path(temp))
            self.populate(directory)
            with contextlib.redirect_stdout(io.StringIO()):
                bench.summarize(directory)
            summary = bench.read(directory / "summary.json")
            for condition in summary["conditions"].values():
                self.assertEqual((condition["points"], condition["full_pass"],
                                  condition["trap_count"], condition["clean_count"]), (40, 10, 8, 2))
            target = next((directory / "grades").glob("*.json"))
            grade = bench.read(target)
            grade["answer"]["critical_failure"] = True
            bench.write(target, grade)
            with contextlib.redirect_stdout(io.StringIO()):
                bench.summarize(directory)
            summary = bench.read(directory / "summary.json")
            self.assertEqual(sum(c["full_pass"] for c in summary["conditions"].values()), 19)

    def test_fabricated_grader_quote_blocks_report(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = self.prepare(Path(temp))
            self.populate(directory)
            target = next((directory / "grades").glob("*.json"))
            grade = bench.read(target)
            grade["answer"]["criteria"][0]["quote"] = "invented evidence"
            bench.write(target, grade)
            with self.assertRaises(ValueError):
                bench.summarize(directory)

    def test_export_preserves_answers_hashes_and_excludes_local_logs(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = self.prepare(Path(temp))
            self.populate(directory)
            (directory / "sensitive.stderr.local").write_text("machine information")
            with contextlib.redirect_stdout(io.StringIO()):
                bench.summarize(directory)
                destination = Path(temp) / "export"
                bench.export(directory, destination)
            self.assertEqual(len(bench.read(destination / "answers.json")), 20)
            manifest = bench.read(destination / "manifest.json")
            self.assertTrue(all(bench.digest(destination / name) == value for name, value in manifest.items()))
            self.assertFalse(any(p.suffix == ".local" or ".private." in p.name for p in destination.iterdir()))


if __name__ == "__main__":
    unittest.main()
