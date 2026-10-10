#!/usr/bin/env python3
"""Run trusted, project-owned SymPy checks and retain reproducible evidence.

A check file exports run_checks(sympy), yielding dictionaries with claim_id,
assumptions, status and detail. This executes Python, not untrusted paper text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import runpy
import sys
from datetime import datetime, timezone


def identity(sp, claim_id, lhs, rhs, assumptions):
    """Zero residual supports only this symbolic identity on its stated domain."""
    residual = sp.simplify(lhs - rhs)
    return dict(claim_id=claim_id, assumptions=assumptions,
                status="symbolic_pass" if residual == 0 else "inconclusive",
                detail=f"simplified residual: {residual}")


def exact_case(sp, claim_id, proposition, assumptions):
    """Caller must independently justify that this case satisfies the contract."""
    result = sp.simplify(proposition)
    status = ("case_pass" if result == sp.true else
              "counterexample" if result == sp.false else "inconclusive")
    return dict(claim_id=claim_id, assumptions=assumptions, status=status,
                detail=f"exact-case proposition: {result}")


def counterexample_search(sp, claim_id, proposition, cases, admissible, assumptions):
    """Exhaust a caller-owned finite grid, checking each case's admissibility."""
    tested, skipped, undecided = 0, 0, 0
    for case in cases:
        valid = admissible(case)
        if valid not in (True, sp.true):
            if valid in (False, sp.false): skipped += 1
            else: undecided += 1
            continue
        tested += 1
        result = sp.simplify(proposition.subs(case))
        if result == sp.false:
            return dict(claim_id=claim_id, assumptions=assumptions, status="counterexample",
                        detail=f"admissible substitution {case}: False; tested={tested}, skipped={skipped}")
        if result != sp.true: undecided += 1
    return dict(claim_id=claim_id, assumptions=assumptions,
                status="search_no_counterexample" if tested and not undecided else "inconclusive",
                detail=f"finite-grid search only: tested={tested}, skipped={skipped}, undecided={undecided}; no universal proof")


def numerical_check(sp, claim_id, lhs, rhs, cases, admissible, assumptions, atol=1e-10, rtol=1e-8, digits=50):
    """Pointwise finite-case residual checks; tolerances do not certify a theorem."""
    if not all(math.isfinite(x) and x >= 0 for x in (atol, rtol)) or digits < 15:
        raise ValueError("require finite nonnegative tolerances and at least 15 digits")
    tested, worst, undecided = 0, 0.0, 0
    for case in cases:
        valid = admissible(case)
        if valid not in (True, sp.true):
            if valid not in (False, sp.false): undecided += 1
            continue
        try:
            left, right = sp.N(lhs.subs(case), digits), sp.N(rhs.subs(case), digits)
            error, scale = sp.Abs(left-right), sp.Abs(right)
            if error.is_finite is not True or scale.is_finite is not True:
                undecided += 1
                continue
            tested += 1
            worst = max(worst, error)
            allowed = sp.Float(str(atol), digits) + sp.Float(str(rtol), digits) * scale
            if error > allowed:
                return dict(claim_id=claim_id, assumptions=assumptions, status="numeric_failure",
                            detail=f"substitution={case}, absolute_error={error}, allowed={allowed}, digits={digits}; numeric diagnostic, not an exact refutation")
        except (TypeError, ValueError, OverflowError):
            undecided += 1
    return dict(claim_id=claim_id, assumptions=assumptions,
                status="numeric_pass" if tested and not undecided else "inconclusive",
                detail=f"finite cases: tested={tested}, undecided={undecided}, max_absolute_error={worst}, atol={atol}, rtol={rtol}, digits={digits}; no universal proof")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("check_file", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    report = dict(schema_version=1, backend="sympy", status="error",
                  created_utc=datetime.now(timezone.utc).isoformat(),
                  python_version=platform.python_version(), checks=[])
    code = 2
    try:
        source = args.check_file.resolve()
        report.update(source=str(source), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
        import sympy as sp
        report["backend_version"] = sp.__version__
        module = runpy.run_path(str(source))
        checks = list(module["run_checks"](sp))
        if not checks:
            raise ValueError("no checks were produced")
        statuses = {"symbolic_pass", "case_pass", "counterexample", "inconclusive",
                    "search_no_counterexample", "numeric_pass", "numeric_failure"}
        ids = set()
        for check in checks:
            if not isinstance(check, dict):
                raise ValueError("each check must be a dictionary")
            for key in ("claim_id", "assumptions", "status", "detail"):
                if not isinstance(check.get(key), str) or not check[key].strip():
                    raise ValueError(f"missing/non-text check field: {key}")
            if check["status"] not in statuses or check["claim_id"] in ids:
                raise ValueError("invalid status or duplicate claim_id")
            ids.add(check["claim_id"])
        report["checks"] = checks
        if any(c["status"] == "counterexample" for c in checks):
            report["status"], code = "counterexample", 1
        elif any(c["status"] in {"inconclusive", "numeric_failure"} for c in checks):
            report["status"], code = "inconclusive", 1
        else:
            report["status"], code = "checks_passed", 0
    except Exception as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{report['status']}: {args.output}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
