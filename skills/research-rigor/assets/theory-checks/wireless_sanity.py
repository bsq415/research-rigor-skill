"""Synthetic demonstrations; these are not validations of a research paper.

Run with verify_theory.py. The intentional counterexample makes exit code 1.
"""
from verify_theory import identity, exact_case


def run_checks(sp):
    x = sp.Symbol("x", real=True)
    a = sp.Symbol("a", positive=True)
    s = sp.Symbol("s", nonnegative=True)
    yield identity(sp, "shifted-laplace-factor", sp.exp(-s * (a + x)),
                   sp.exp(-s * a) * sp.exp(-s * x),
                   "a>0, s>=0, x real; transform factor only, not a distribution theorem")
    original = sp.ones(2)
    weighted = original.multiply_elementwise(sp.Matrix([[1, 1], [1, 3]]))
    yield exact_case(sp, "positive-entrywise-weights-preserve-rank",
                     sp.Eq(original.rank(), weighted.rank()),
                     "exact 2x2 all-ones matrix; all entrywise weights positive; claimed rank invariance")
    yield identity(sp, "sqrt-square-with-real-domain", sp.sqrt(x**2), sp.Abs(x),
                   "x real; sqrt(x^2)=x would need x>=0")
