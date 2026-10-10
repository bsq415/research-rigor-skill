from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1] / "skills" / "research-rigor"
SCRIPT = ROOT / "scripts" / "verify_theory.py"
HAS_SYMPY = importlib.util.find_spec("sympy") is not None


class TheoryVerificationTests(unittest.TestCase):
    def run_check(self, source):
        with tempfile.TemporaryDirectory() as directory:
            check = Path(directory) / "checks.py"
            output = Path(directory) / "evidence.json"
            check.write_text(source, encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(check),
                                     "--output", str(output)], capture_output=True, text=True)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["source_sha256"], hashlib.sha256(check.read_bytes()).hexdigest())
            return result.returncode, report

    @unittest.skipUnless(HAS_SYMPY, "optional SymPy dependency unavailable")
    def test_identity_and_single_case_keep_separate_evidence_tiers(self):
        code, report = self.run_check('''from verify_theory import identity, exact_case
def run_checks(sp):
    x = sp.Symbol("x", real=True)
    yield identity(sp, "identity", sp.sqrt(x**2), sp.Abs(x), "x real")
    yield exact_case(sp, "one-case", sp.Eq(2+2, 4), "one exact case")
''')
        self.assertEqual(code, 0)
        self.assertEqual([c["status"] for c in report["checks"]], ["symbolic_pass", "case_pass"])

    @unittest.skipUnless(HAS_SYMPY, "optional SymPy dependency unavailable")
    def test_assumption_gap_is_inconclusive_and_admissible_case_refutes(self):
        code, report = self.run_check('''from verify_theory import identity, exact_case
def run_checks(sp):
    x = sp.Symbol("x", real=True)
    yield identity(sp, "gap", sp.sqrt(x**2), x, "x real, sign unrestricted")
    yield exact_case(sp, "negative-case", sp.Eq(sp.sqrt((-1)**2), -1), "x=-1 admissible for real x")
''')
        self.assertEqual(code, 1)
        self.assertEqual(report["status"], "counterexample")
        self.assertEqual([c["status"] for c in report["checks"]], ["inconclusive", "counterexample"])

    @unittest.skipUnless(HAS_SYMPY, "optional SymPy dependency unavailable")
    def test_empty_malformed_and_crashing_checks_fail_closed(self):
        for source in ("def run_checks(sp): return []",
                       "def run_checks(sp): return [{'status': 'formal_proof'}]",
                       "raise RuntimeError('broken check')"):
            with self.subTest(source=source):
                code, report = self.run_check(source)
                self.assertEqual(code, 2)
                self.assertEqual(report["status"], "error")

    def test_missing_input_leaves_error_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            result = subprocess.run([sys.executable, str(SCRIPT),
                                     str(Path(directory) / "missing.py"),
                                     "--output", str(output)], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(output.read_text())["status"], "error")
