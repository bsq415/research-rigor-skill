"""Synthetic search/approximation diagnostics; intentional failures exit 1."""
from verify_theory import counterexample_search, numerical_check


def run_checks(sp):
    x = sp.Symbol("x", real=True)
    cases = [{x: sp.Rational(n, 2)} for n in range(-4, 5)]
    yield counterexample_search(sp, "sqrt-square-unrestricted", sp.Eq(sp.sqrt(x*x), x),
                                cases, lambda c: True, "x real; finite grid -2 to 2 with step 1/2")
    positive = [{x: sp.Rational(n, 10)} for n in range(1, 11)]
    yield numerical_check(sp, "first-order-exp-approximation", sp.exp(x), 1+x,
                          positive, lambda c: c[x] >= 0, "0<=x<=1; first-order approximation tested pointwise",
                          atol=1e-6, rtol=1e-6)
