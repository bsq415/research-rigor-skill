import importlib.util
from pathlib import Path
import unittest
import sympy as sp

SCRIPT = Path(__file__).resolve().parents[1]/"skills/research-rigor/scripts/verify_theory.py"
spec = importlib.util.spec_from_file_location("theory_search", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TheorySearchTests(unittest.TestCase):
    def test_admissible_counterexample_and_excluded_cases(self):
        x = sp.Symbol("x", real=True)
        cases = [{x: -1}, {x: 1}]
        result = mod.counterexample_search(sp, "C1", x >= 0, cases, lambda c: True, "real x")
        self.assertEqual(result["status"], "counterexample")
        result = mod.counterexample_search(sp, "C1", x >= 0, cases, lambda c: c[x] >= 0, "nonnegative x")
        self.assertEqual(result["status"], "search_no_counterexample")
        self.assertIn("no universal proof", result["detail"])

    def test_empty_or_unknown_domain_is_inconclusive(self):
        x = sp.Symbol("x")
        for cases, valid in (([], lambda c: True), ([{x: 1}], lambda c: None)):
            self.assertEqual(mod.counterexample_search(sp, "C", x >= 0, cases, valid, "domain")["status"], "inconclusive")

    def test_numeric_fail_pass_nonfinite_and_underflow(self):
        x = sp.Symbol("x")
        for lhs, rhs, expected in ((x, x, "numeric_pass"), (x, x+1, "numeric_failure"),
                                   (sp.oo+x, x, "inconclusive"), (sp.Rational(1, 10**400)+x, x, "numeric_failure")):
            result = mod.numerical_check(sp, "C", lhs, rhs, [{x: 0}], lambda c: True, "finite", atol=0, rtol=0)
            self.assertEqual(result["status"], expected)

    def test_invalid_tolerance_rejected(self):
        with self.assertRaises(ValueError):
            mod.numerical_check(sp, "C", sp.Integer(1), sp.Integer(1), [], lambda c: True, "finite", atol=-1)
