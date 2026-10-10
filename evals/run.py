#!/usr/bin/env python3
"""Run frozen functional evaluations; these do not measure model improvement."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    "citation_authenticity": "test_citation_verification.py",
    "number_consistency": "test_manuscript_numbers.py",
    "light_upgrade": "test_light_mode.py",
    "sealed_hook": "test_sealed_hook.py",
    "theory_search": "test_theory_search.py",
    "plugin_and_references": "test_plugin_package.py",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--compare", type=Path)
    args = parser.parse_args()
    results = {}
    for name, filename in GROUPS.items():
        if not (ROOT / "tests" / filename).exists():
            results[name] = {"status": "not_implemented", "passed": False}
            continue
        call = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", filename, "-v"],
                              cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        results[name] = dict(status="passed" if call.returncode == 0 else "failed",
                             passed=call.returncode == 0, output=call.stdout+call.stderr,
                             test_sha256=hashlib.sha256((ROOT / "tests" / filename).read_text(encoding="utf-8").encode()).hexdigest())
    with tempfile.TemporaryDirectory() as temp:
        call = subprocess.run([sys.executable, str(ROOT / "skills/research-rigor/scripts/init_research_project.py"), temp],
                              capture_output=True, text=True, encoding="utf-8")
        names = sorted(p.name for p in (Path(temp)/".research").glob("*") if p.is_file())
        expected = ["03_CLAIM_EVIDENCE_MATRIX.csv", "05_RUN_LEDGER.csv", "DECISION_LOG.md"]
        results["default_light_footprint"] = dict(passed=call.returncode == 0 and names == expected,
                                                  files=names, file_count=len(names))
    report = dict(schema_version=1, suite="functional-regression-v1", scientific_effect="not_measured",
                  created_utc=datetime.now(timezone.utc).isoformat(), checks=results,
                  source_hash_encoding="UTF-8 with normalized LF for cross-platform source comparisons",
                  implementation_sha256={p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_text(encoding="utf-8").encode()).hexdigest()
                                         for p in sorted([*(ROOT/"skills/research-rigor/scripts").glob("*.py"), *(ROOT/"hooks").glob("*.py")])})
    if args.compare:
        previous = json.loads(args.compare.read_text(encoding="utf-8"))
        report["comparison"] = {name: {"before": previous["checks"].get(name, {}).get("passed"),
                                       "after": result["passed"],
                                       "same_test": previous["checks"].get(name, {}).get("test_sha256") == result.get("test_sha256")}
                                for name, result in results.items()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"{sum(r['passed'] for r in results.values())}/{len(results)} functional groups passed: {args.output}")
    return 0 if all(r["passed"] for r in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
