#!/usr/bin/env python3
"""Run trusted, project-owned SymPy checks and retain reproducible evidence.

A check file exports run_checks(sympy), yielding dictionaries with claim_id,
assumptions, status and detail. This executes Python, not untrusted paper text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
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
        statuses = {"symbolic_pass", "case_pass", "counterexample", "inconclusive"}
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
        elif any(c["status"] == "inconclusive" for c in checks):
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
