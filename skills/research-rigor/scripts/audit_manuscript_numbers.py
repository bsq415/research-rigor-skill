#!/usr/bin/env python3
"""Inventory LaTeX numeric literals and verify explicitly mapped result facts.

Every literal needs a fact mapping or reasoned non-result classification in
strict mode. This does not expand arbitrary TeX macros or read plotted pixels.
"""
import argparse
import csv
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
import hashlib
import json
from pathlib import Path
import re

NUMBER = re.compile(r"(?<![\d.])[-+]?(?:\d+\.\d+|\d+|\.\d+)(?:[eE][-+]?\d+)?(?!\d|\.\d)")
FIELDS = ["file", "line", "occurrence", "literal", "role", "fact_id", "field", "scale", "decimals", "tolerance", "reason"]


def uncomment(line):
    for index, char in enumerate(line):
        if char == "%":
            preceding = len(line[:index]) - len(line[:index].rstrip("\\"))
            if preceding % 2 == 0: return line[:index]
    return line


def inventory(main):
    root = main.parent.resolve()
    seen, tokens, hashes = set(), [], {}

    def visit(path):
        path = path.resolve()
        if not path.is_relative_to(root): raise ValueError("LaTeX include escapes manuscript root")
        if path in seen: return
        seen.add(path)
        relative = path.relative_to(root).as_posix()
        hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        text = path.read_text(encoding="utf-8")
        for number, raw in enumerate(text.splitlines(), 1):
            line = uncomment(raw)
            for index, match in enumerate(NUMBER.finditer(line), 1):
                tokens.append(dict(file=relative, line=number, occurrence=index, literal=match[0]))
            for include in re.findall(r"\\(?:input|include)\{([^}]+)\}", line):
                target = root / include
                if not target.suffix: target = target.with_suffix(".tex")
                visit(target)
    visit(main)
    return tokens, hashes


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def audit(tokens, mappings, facts):
    # Preserve all input digits across multiplication, subtraction and display rounding.
    values = [str(v) for row in facts + mappings + tokens for v in row.values()]
    precision = 64
    for value in values:
        try:
            number = Decimal(value)
            if number.is_finite():
                precision = max(precision, len(number.as_tuple().digits) + abs(number.as_tuple().exponent))
        except InvalidOperation:
            pass
    precision = precision * 4 + 64
    if precision > 100000:
        raise ValueError("numeric precision exceeds supported audit resource budget")
    with localcontext() as context:
        context.prec = precision
        return _audit(tokens, mappings, facts)


def _audit(tokens, mappings, facts):
    if len({f["fact_id"] for f in facts}) != len(facts): raise ValueError("duplicate fact_id")
    facts = {f["fact_id"]: f for f in facts}
    indexed = {}
    for row in mappings:
        key = row["file"], int(row["line"]), int(row["occurrence"])
        if key in indexed: raise ValueError("duplicate numeric mapping")
        indexed[key] = row
    results = []
    used = set()
    for token in tokens:
        key = token["file"], token["line"], token["occurrence"]
        row = indexed.get(key)
        result = dict(**token, status="unclassified")
        if row:
            used.add(key)
            if row["literal"] != token["literal"]:
                result.update(status="stale_mapping", reason="literal changed at mapped location")
            elif row["role"] == "non_result" and row.get("reason", "").strip():
                result.update(status="excluded", reason=row["reason"])
            elif row["role"] == "fact":
                fact = facts.get(row["fact_id"])
                if not fact or not fact.get(row["field"]):
                    result.update(status="missing_fact", fact_id=row["fact_id"], field=row["field"])
                else:
                    expected = Decimal(fact[row["field"]]) * Decimal(row.get("scale") or "1")
                    observed = Decimal(token["literal"])
                    tolerance = Decimal(row.get("tolerance") or "0")
                    if tolerance < 0: raise ValueError("negative numeric tolerance")
                    if row.get("decimals"):
                        places = int(row["decimals"])
                        if not 0 <= places <= 30: raise ValueError("display decimals must be 0..30")
                        expected = expected.quantize(Decimal(10) ** -places, rounding=ROUND_HALF_UP)
                    if not all(x.is_finite() for x in (expected, observed, tolerance)):
                        raise ValueError("nonfinite fact, observation or tolerance")
                    result.update(status="matched" if abs(expected-observed) <= tolerance else "mismatch",
                                  fact_id=row["fact_id"], field=row["field"], expected=str(expected), observed=str(observed))
        results.append(result)
    for key in set(indexed)-used:
        results.append(dict(file=key[0], line=key[1], occurrence=key[2], status="stale_mapping", reason="mapped token no longer present"))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex", type=Path)
    parser.add_argument("--facts", type=Path)
    parser.add_argument("--map", type=Path)
    parser.add_argument("--init-map", type=Path, help="write unclassified inventory template; refuses overwrite")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    report = dict(schema_version=1, scope="LaTeX literal inventory, explicit fact mapping; no arbitrary macro expansion or image OCR")
    try:
        tokens, hashes = inventory(args.tex.resolve())
        report.update(source_hashes=hashes, literal_count=len(tokens))
        if args.init_map:
            args.init_map.parent.mkdir(parents=True, exist_ok=True)
            with args.init_map.open("x", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(dict(**token, role="unclassified", field="estimate", scale="1", tolerance="0") for token in tokens)
        mappings = read_csv(args.map) if args.map else []
        facts = read_csv(args.facts) if args.facts else []
        report["tokens"] = audit(tokens, mappings, facts)
        if args.facts: report["facts_sha256"] = hashlib.sha256(args.facts.read_bytes()).hexdigest()
        if args.map: report["map_sha256"] = hashlib.sha256(args.map.read_bytes()).hexdigest()
        counts = {status: sum(t["status"] == status for t in report["tokens"]) for status in
                  ("matched", "excluded", "unclassified", "mismatch", "missing_fact", "stale_mapping")}
        report["counts"] = counts
        failures = counts["mismatch"]+counts["missing_fact"]+counts["stale_mapping"]
        code = 1 if failures or (args.strict and (counts["unclassified"] or not tokens)) else 0
        report["verification_complete"] = not failures and counts["unclassified"] == 0 and counts["matched"] > 0
    except (OSError, ValueError, KeyError, InvalidOperation) as exc:
        report["error"], code = str(exc), 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Numeric inventory/audit: {args.output}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
