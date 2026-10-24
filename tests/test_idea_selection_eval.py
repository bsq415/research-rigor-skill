import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import shutil
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1]/"evals/run_idea_selection.py"
spec = importlib.util.spec_from_file_location("selection_eval", SCRIPT)
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)


class IdeaSelectionEvalTests(unittest.TestCase):
    def test_prepare_can_replay_a_frozen_task_version(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            inputs = root/"frozen-inputs"
            inputs.mkdir()
            for name in ("tasks.json", "rubric.json", "answer-schema.json"):
                shutil.copyfile(SCRIPT.parent/"idea-selection-v1"/name, inputs/name)
            tasks = json.loads((inputs/"tasks.json").read_text(encoding="utf-8"))
            tasks["version"] = "frozen-test-version"
            (inputs/"tasks.json").write_text(json.dumps(tasks), encoding="utf-8")
            baseline = root/"old.txt"
            baseline.write_text("old guidance", encoding="utf-8")
            directory = root/"run"
            with contextlib.redirect_stdout(io.StringIO()):
                suite.prepare(directory, baseline, "test-model", "medium", inputs)
            self.assertEqual(suite.core.read(directory/"tasks.json")["version"], "frozen-test-version")

    def prepare(self, root):
        baseline = root/"old.txt"
        baseline.write_text("OLD_CONTEXT_FIXTURE", encoding="utf-8")
        directory = root/"run"
        with contextlib.redirect_stdout(io.StringIO()):
            suite.prepare(directory, baseline, "test-model", "medium")
        return directory

    def test_both_conditions_get_their_frozen_guidance(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = self.prepare(Path(raw))
            plan = suite.core.load_plan(directory)
            self.assertEqual(len(plan["rows"]), 10)
            prompts = []
            def capture(prompt, model, effort, target, schema):
                prompts.append((target.stem, prompt))
                return {"status": "error"}
            with patch.object(suite.core, "call_codex", side_effect=capture), contextlib.redirect_stdout(io.StringIO()):
                suite.run(directory, limit=2)
            conditions = {row["run_id"]: row["condition"] for row in plan["rows"]}
            old = (directory/"baseline-context.txt").read_text(encoding="utf-8")
            new = (directory/"skill-context.txt").read_text(encoding="utf-8")
            self.assertNotEqual(old, new)
            for run_id, prompt in prompts:
                if conditions[run_id] == "baseline":
                    self.assertIn(old, prompt)
                    self.assertNotIn(new, prompt)
                else:
                    self.assertIn(new, prompt)
                    self.assertNotIn(old, prompt)

    def test_tampered_old_context_or_driver_is_rejected(self):
        for name in ("baseline-context.txt", "driver-snapshot.py"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as raw:
                directory = self.prepare(Path(raw))
                with (directory/name).open("a", encoding="utf-8") as stream:
                    stream.write("changed")
                with self.assertRaises(ValueError):
                    suite.core.load_plan(directory)

    def test_failed_attempt_is_not_retried(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = self.prepare(Path(raw))
            first = suite.core.load_plan(directory)["rows"][0]["run_id"]
            suite.core.write(directory/"responses"/(first+".json"), {"status": "error"})
            with patch.object(suite.core, "call_codex", return_value={"status": "error"}) as call, contextlib.redirect_stdout(io.StringIO()):
                suite.run(directory, limit=1)
            self.assertEqual(call.call_count, 1)
            self.assertNotEqual(call.call_args.args[3].stem, first)
