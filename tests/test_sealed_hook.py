import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("seal_guard", ROOT/"hooks/guard_sealed.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
spec = importlib.util.spec_from_file_location("sealing", ROOT/"skills/research-rigor/scripts/seal_artifacts.py")
seal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seal)


class SealHookTests(unittest.TestCase):
    def test_guard_blocks_results_shell_registry_but_allows_source_and_reads(self):
        with tempfile.TemporaryDirectory() as raw, patch.dict(os.environ, {}, clear=True):
            root = Path(raw)
            (root/"results").mkdir()
            (root/"results/facts.csv").write_text("frozen")
            (root/"manifest.json").write_text("{}")
            (root/".research").mkdir()
            registry = root/".research/seals.json"
            registry.write_text(json.dumps(dict(schema_version=1, seals=[dict(root="results", manifest="manifest.json")])))
            (root/"nested").mkdir()
            def check(tool, target):
                return guard.decision(dict(cwd=str(root/"nested"), tool_name=tool, tool_input=dict(file_path=str(target))))
            self.assertIsNotNone(check("Write", root/"results/facts.csv"))
            self.assertIsNotNone(check("Write", registry))
            self.assertIsNotNone(check("Bash", root/"source.py"))
            self.assertIsNone(check("Edit", root/"source.py"))
            self.assertIsNone(check("Read", root/"results/facts.csv"))
            registry.write_text("broken json")
            self.assertIsNotNone(check("Edit", root/"source.py"))
            self.assertIsNone(check("Read", root/"source.py"))

    def test_actual_hook_protocol_and_no_registry(self):
        with tempfile.TemporaryDirectory() as raw, patch.dict(os.environ, {}, clear=True):
            root = Path(raw)
            self.assertIsNone(guard.decision(dict(cwd=raw, tool_name="Write", tool_input={})))
            (root/".research").mkdir()
            (root/".research/seals.json").write_text("bad")
            call = subprocess.run([sys.executable, str(ROOT/"hooks/guard_sealed.py")], input=json.dumps(dict(cwd=raw, tool_name="Write")), text=True, capture_output=True)
            self.assertEqual(call.returncode, 0)
            self.assertEqual(json.loads(call.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_manifest_rejects_windows_absolute_and_nonportable_paths(self):
        for path in ("C:/outside.txt", "C:\\outside.txt", "../outside", "/outside", "a/../b"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                seal._canonical_record_path(path)

    def test_protect_requires_matching_frozen_bytes(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root/"results").mkdir()
            artifact = root/"results/facts.csv"
            artifact.write_text("frozen")
            script = ROOT/"skills/research-rigor/scripts/seal_artifacts.py"
            for action, extra in (("create", []), ("protect", ["--project", raw])):
                call = subprocess.run([sys.executable, str(script), action, str(root/"results"), str(root/"manifest.json"), *extra], capture_output=True)
                self.assertEqual(call.returncode, 0)
            artifact.write_text("changed")
            call = subprocess.run([sys.executable, str(script), "verify", str(root/"results"), str(root/"manifest.json"), "--strict"], capture_output=True)
            self.assertEqual(call.returncode, 1)
