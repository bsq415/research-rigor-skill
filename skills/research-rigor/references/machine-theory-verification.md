# Machine theory verification

Use a small executable check to resolve a specific theorem obligation, not to
add tool use to every paper. Start from `03_THEOREM_CONTRACT.csv` or the project's
equivalent: copy exact statement/version, domains, assumptions, quantifiers,
singularities and order of limits. Have the researcher or an independent review
check the translation: a machine can verify the wrong mathematical statement.

## Choose the evidence tier

| Obligation | Tool/output | Supported interpretation |
|---|---|---|
| Algebraic identity, derivative, transform factor, exact small matrix | SymPy residual, assumptions and expression | Symbolic check for the represented expression/domain |
| Suspected boundary failure | Exact substitution with admissibility checked | Counterexample refutes that statement; a passing case is only one case |
| General inequality, rank law, asymptotic rate or probability statement | Derivation plus scoped checks; Lean if worthwhile | SymPy samples or limits alone do not prove quantifiers or interchange of limits |
| Central reusable lemma requiring formal assurance | Lean kernel check plus theorem/axiom audit | Formal proof of the encoded theorem under recorded axioms |

SymPy assumptions are attached to symbols; declare real/positive/nonnegative
properties explicitly. Preserve original domains and excluded denominator zeros
before simplification. Check branches, strict inequalities, dimensions, complex
conjugates and limit direction. An undecided result stays inconclusive. Never
turn a numeric tolerance, random sample pass or nonzero symbolic residual into
a universal theorem verdict. Official references: [assumptions](https://docs.sympy.org/latest/guides/assumptions.html)
and [equality pitfalls](https://docs.sympy.org/latest/explanation/gotchas.html).

## Executable SymPy route

Use a project virtual environment, installing the bundled pinned requirements
only when this route is needed. `<SKILL_DIR>` is the directory of `SKILL.md`.

```text
python -m venv .venv-theory
<VENV_PYTHON> -m pip install -r "<SKILL_DIR>/assets/theory-checks/requirements.txt"
<VENV_PYTHON> "<SKILL_DIR>/scripts/verify_theory.py" checks.py --output evidence/theory-checks.json
```

`<VENV_PYTHON>` is `.venv-theory/Scripts/python.exe` on Windows or
`.venv-theory/bin/python` on POSIX. Author a **trusted project Python file**
exporting `run_checks(sympy)`; this runner executes code and does not sandbox it.
Do not execute scripts copied from untrusted manuscripts or reviewer attachments.
Import `identity` and `exact_case` from `verify_theory` as in the bundled
[synthetic example](../assets/theory-checks/wireless_sanity.py). Keep project-owned
helpers alongside the check file and record their hashes separately when used.

Each check records `claim_id`, `assumptions`, `status`, `detail`. The runner
records source SHA-256, UTC time and Python/SymPy versions. It rejects empty or
malformed results; failures and missing dependencies produce an error report.
Exit 0 means all supplied checks passed at their stated tier, 1 means a
counterexample or inconclusive result, 2 means execution/schema/dependency error.
The synthetic example intentionally exits 1 for rank invariance under positive
entrywise weights. `case_pass` is never a universal proof; `symbolic_pass` is
never a Lean proof. The check author remains responsible for truthful statuses.

Save results in `03_THEORY_VERIFICATION.csv` or existing project records with
theorem ID/version, assumptions, source/result paths, hash, scope limit, review
and dependent claims. Independently check admissibility of a counterexample.
Reopen affected proofs/abstract/algorithms/figures; do not auto-pass G3 from an
exit code. Freeze the contract before confirmation and retain failed versions.

## Finite search and numeric diagnostics

`counterexample_search(sp, claim_id, proposition, cases, admissible, assumptions)`
checks a supplied finite grid and filters cases through the caller's domain predicate.
An exact false proposition records an admissible counterexample; an exhausted grid
returns `search_no_counterexample`, never a universal proof. Unknown admissibility
or an empty valid domain is inconclusive. Independently justify the domain predicate.

`numerical_check(sp, claim_id, lhs, rhs, cases, admissible, assumptions, atol, rtol, digits)`
uses high-precision residuals and explicit absolute/relative tolerances. `numeric_pass`
supports only those evaluated cases; `numeric_failure` is a diagnostic requiring
exact analysis, not automatically an exact refutation. Nonfinite or unresolved values
are inconclusive. Cancellation and inadequate precision still need human analysis.

Try `assets/theory-checks/search_and_numeric.py` with the runner. It deliberately
includes failing checks so that preservation of negative evidence can be inspected.

## Optional Lean route

Use an existing Lean 4 project with pinned `lean-toolchain`, Lake dependency
manifest and Mathlib revision where needed. Formalize the smallest decisive
lemma first; write an explicit map between paper variables/quantifiers and the
Lean statement. Record assumptions that are hypotheses versus imported axioms.

```text
lake build
lake env lean Theory.lean
```

Include `#print axioms theoremName` for each claimed theorem. Inspect the actual
axiom dependencies, including imported lemmas: compilation can succeed despite
`sorry` and its `sorryAx`. Reject that dependency for a completed proof; justify
other axioms under the project's policy and check no custom axiom simply assumes
the target. Preserve build logs, exact statement, source hashes, versions and
the statement-mapping review. A lexical search for `sorry` alone is insufficient.
See [Lean axiom tracking](https://lean-lang.org/doc/reference/latest/Axioms) and
[Lake](https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/).

If Lean/toolchain/dependencies are unavailable, mark formal verification
unexecuted. Continue scoped symbolic/counterexample work; do not claim Lean
verification or install a large toolchain merely to tick a box.
