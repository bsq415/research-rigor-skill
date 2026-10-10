import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1]/"skills/research-rigor/scripts/audit_manuscript_numbers.py"
spec = importlib.util.spec_from_file_location("numbers_audit", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ManuscriptNumberTests(unittest.TestCase):
    def test_no_precision_loss_and_thirty_display_decimals(self):
        token = dict(file="main.tex", line=1, occurrence=1, literal="1")
        row = dict(**token, role="fact", fact_id="F", field="estimate", scale="1", tolerance="0")
        self.assertEqual(mod.audit([token], [row], [dict(fact_id="F", estimate="1.00000000000000000000000000001")])[0]["status"], "mismatch")
        token["literal"] = row["literal"] = "1.000000000000000000000000000000"
        row["decimals"] = "30"
        self.assertEqual(mod.audit([token], [row], [dict(fact_id="F", estimate="1")])[0]["status"], "matched")

    def test_matching_wrong_and_unclassified_numbers(self):
        token = dict(file="main.tex", line=1, occurrence=1, literal="0.80")
        mapping = dict(**token, role="fact", fact_id="F1", field="estimate", scale="1", decimals="2", tolerance="0", reason="")
        facts = [dict(fact_id="F1", estimate="0.80")]
        self.assertEqual(mod.audit([token], [mapping], facts)[0]["status"], "matched")
        self.assertEqual(mod.audit([token], [mapping], [dict(fact_id="F1", estimate="0.75")])[0]["status"], "mismatch")
        self.assertEqual(mod.audit([token], [], facts)[0]["status"], "unclassified")

    def test_percentage_scaling_and_decimal_rounding(self):
        token = dict(file="main.tex", line=1, occurrence=1, literal="75.46")
        mapping = dict(**token, role="fact", fact_id="F1", field="estimate", scale="100", decimals="2", tolerance="0")
        self.assertEqual(mod.audit([token], [mapping], [dict(fact_id="F1", estimate="0.75455")])[0]["status"], "matched")

    def test_stale_mapping_and_repeated_tokens_use_exact_location(self):
        tokens = [dict(file="main.tex", line=1, occurrence=i, literal="5") for i in (1, 2)]
        mapping = dict(**tokens[0], role="fact", fact_id="F1", field="estimate")
        result = mod.audit(tokens, [mapping], [dict(fact_id="F1", estimate="5")])
        self.assertEqual([r["status"] for r in result], ["matched", "unclassified"])
        mapping["literal"] = "6"
        self.assertEqual(mod.audit(tokens, [mapping], [dict(fact_id="F1", estimate="5")])[0]["status"], "stale_mapping")

    def test_includes_comments_and_sentence_punctuation(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root/"main.tex").write_text("Score 0.80. % hidden 999\n\\input{table}\n")
            (root/"table.tex").write_text("80\\% and -1e-3\n")
            tokens, hashes = mod.inventory(root/"main.tex")
            self.assertEqual([r["literal"] for r in tokens], ["0.80", "80", "-1e-3"])
            self.assertEqual(set(hashes), {"main.tex", "table.tex"})

    def test_escaping_include_is_rejected(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)/"paper"
            root.mkdir()
            (root/"main.tex").write_text("\\input{../outside}")
            with self.assertRaises(ValueError): mod.inventory(root/"main.tex")

    def test_strict_cli_rejects_unmapped_literal(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root/"main.tex").write_text("Observed 0.80.")
            call = subprocess.run([sys.executable, str(SCRIPT), str(root/"main.tex"), "--strict", "--output", str(root/"out.json")], capture_output=True)
            self.assertEqual(call.returncode, 1)
            self.assertFalse(json.loads((root/"out.json").read_text())["verification_complete"])
