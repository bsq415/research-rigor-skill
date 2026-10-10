import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1]/"skills/research-rigor/scripts/verify_citations.py"
spec = importlib.util.spec_from_file_location("citations", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class CitationVerificationTests(unittest.TestCase):
    def test_braced_quotes_parentheses_and_conflicting_given_names(self):
        for text in ('@article{k,title={The 12" Telescope},year={2024}}', '@article(k,title={A (nested) title},year=2024)'):
            self.assertEqual(len(mod.parse_bib(text)), 1)
        code, result = self.check(author="Example, Alan")
        self.assertEqual(code, 1)
        self.assertIn("authors/order", result["entries"][0]["reasons"])

    def check(self, title="Synthetic Study", author="Example, Ada", year="2020", metadata=None):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            bib = root/"refs.bib"
            bib.write_text(f"@article{{fixture, title={{{title}}}, author={{{author}}}, year={{{year}}}, doi={{10.0000/fixture}}}}", encoding="utf-8")
            record = dict(title="Synthetic Study", authors=["Ada Example"], years=[2020, 2021], doi="10.0000/fixture", source="synthetic fixture")
            (root/"records.json").write_text(json.dumps({"10.0000/fixture": record if metadata is None else metadata}), encoding="utf-8")
            call = subprocess.run([sys.executable, str(SCRIPT), str(bib), "--offline", str(root/"records.json"),
                                   "--output", str(root/"report.json")], capture_output=True)
            return call.returncode, json.loads((root/"report.json").read_text(encoding="utf-8"))

    def test_matching_metadata_and_alternative_publication_year(self):
        code, result = self.check(year="2021")
        self.assertEqual(code, 0)
        self.assertEqual(result["mode"], "offline-evidence")
        self.assertEqual(result["entries"][0]["status"], "verified_metadata")

    def test_real_identifier_with_wrong_title_is_mismatch(self):
        code, result = self.check(title="An Invented Unrelated Title")
        self.assertEqual(code, 1)
        self.assertEqual(result["entries"][0]["status"], "metadata_mismatch")
        self.assertIn("title", result["entries"][0]["reasons"])

    def test_wrong_author_and_year_are_not_verified(self):
        code, result = self.check(author="Other, Bruno", year="1999")
        self.assertEqual(code, 1)
        self.assertIn("authors/order", result["entries"][0]["reasons"])
        self.assertIn("year", result["entries"][0]["reasons"])

    def test_provider_failure_and_truncated_authors_stay_unresolved(self):
        for args in ({"metadata": {"error": "429"}}, {"author": "Example, Ada and others"}):
            with self.subTest(args=args):
                code, result = self.check(**args)
                self.assertEqual(code, 1)
                self.assertEqual(result["entries"][0]["status"], "unresolved")

    def test_duplicate_keys_and_unbalanced_input_fail(self):
        with self.assertRaises(ValueError):
            mod.parse_bib("@article{a,title={x}} @article{a,title={y}}")
        with self.assertRaises(ValueError):
            mod.parse_bib("@article{a,title={x}")

    def test_nested_braces_supported_and_macros_do_not_become_verified(self):
        entries = mod.parse_bib('@article{a,title={{Nested} title}, author="Example, Ada", year=2020}')
        self.assertEqual(entries[0]["title"], "{Nested} title")
        entry = mod.parse_bib('@article{a,title=someMacro, author={Example, Ada}, year=2020}')[0]
        self.assertEqual(mod.compare(entry, [])['status'], "unresolved")
