import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1]/"skills/research-rigor/scripts/init_research_project.py"


class LightModeTests(unittest.TestCase):
    def test_quoted_title_is_valid_json(self):
        with tempfile.TemporaryDirectory() as raw:
            call = subprocess.run([sys.executable, str(SCRIPT), raw, "--mode", "full-cycle", "--title", 'Research "Trial"'], capture_output=True)
            self.assertEqual(call.returncode, 0)
            state = json.loads((Path(raw)/".research/research_state.json").read_text())
            self.assertEqual(state["project_title"], 'Research "Trial"')

    def test_default_is_exactly_three_records(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            call = subprocess.run([sys.executable, str(SCRIPT), str(root)], capture_output=True)
            self.assertEqual(call.returncode, 0)
            self.assertEqual(sorted(p.name for p in (root/".research").iterdir()),
                             ["03_CLAIM_EVIDENCE_MATRIX.csv", "05_RUN_LEDGER.csv", "DECISION_LOG.md"])

    def test_upgrade_preserves_existing_records_and_starts_unpassed(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            subprocess.run([sys.executable, str(SCRIPT), str(root)], check=True, capture_output=True)
            record = root/".research/DECISION_LOG.md"
            record.write_text("retained decision\n", encoding="utf-8")
            subprocess.run([sys.executable, str(SCRIPT), str(root), "--upgrade"], check=True, capture_output=True)
            self.assertEqual(record.read_text(), "retained decision\n")
            state = json.loads((root/".research/research_state.json").read_text())
            self.assertEqual(state["current_stage"], "G0")
            self.assertTrue(all(g["status"] != "passed" for g in state["gates"]))

    def test_existing_full_contract_is_preserved_by_light_merge(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            subprocess.run([sys.executable, str(SCRIPT), str(root), "--mode", "full-cycle"], check=True, capture_output=True)
            state = root/".research/research_state.json"
            before = state.read_bytes()
            subprocess.run([sys.executable, str(SCRIPT), str(root), "--merge"], check=True, capture_output=True)
            self.assertEqual(before, state.read_bytes())
