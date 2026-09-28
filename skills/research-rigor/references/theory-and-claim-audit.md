# Theory and claim audit

Use for mathematical claims, model-dependent guarantees, or a theory-heavy
review. Record statement, quantifiers, assumptions, proof obligations,
counterexamples, allowed wording, and downstream locations in a claim contract.

## Audit the whole chain

`physical object → model → assumptions → result → algorithm → metric → abstract`

Read the strongest exposed statement alongside the precise theorem. A correct
theorem does not rescue an unqualified abstract. Distinguish incorrect proof,
incorrect extension, missing condition, inaccurate summary, and implementation
defect.

| Reviewer question | Decisive check | False reassurance |
|---|---|---|
| What is quantified? | Fixed/worst-case target? Average over which distribution? Uniform over which domain? | One favorable instance |
| What happens at degeneracy? | Zero variance/rank, deterministic components outside random support, repeated eigenvalues, boundaries | Only nonsingular random draws |
| Does transformation preserve the property? | Required factorization/invertibility; row scaling versus entrywise weights | All coefficients are positive |
| Which mixture term controls the limit? | Retain deterministic/random terms; state fixed parameters and order of limits | Extending a pure-component law to a mixture |
| Is the claimed order two-sided? | Matching lower/upper bounds with the same quantity and quantifiers | A tight-looking upper-bound curve |
| Does a surrogate certify the target? | Transfer bound or direct discrepancy measurement in the stated domain | Surrogate improvement |
| Is an optimizer a bound? | Global certificate or exhaustive finite domain with stated error | Local solution labeled upper bound |
| Is validation independent? | Different derivation, full model, exact small case, independent measurement | Same approximation in formula and simulator |
| Are rare events resolved? | Counts, intervals, tolerances, analytic/empirical labels | Smooth curves below sampling resolution |
| Is it novel and useful? | Prior-art delta and a decision that changes after costs | New notation for standard tools |

### Synthetic sanity examples

These are generic mathematical checks, not source-project results.

- `L(b) <= c/b^2` permits `L(b)=0`: an `O` upper bound does not establish a
  universal `Theta` rate. A lower bound needs its own conditions.
- The all-ones 2-by-2 matrix has rank one. Elementwise positive weights with
  rows `(1, 1)` and `(1, 3)` can yield rank two. Positivity alone does not imply
  a common invertible row transformation.
- `Z=a+X`, with deterministic `a>0` and `X>=0`, has a positive support lower
  bound. Low-threshold event probability may be zero, unlike a positive
  probability floor. Transforms must retain the factor due to `a`.
- A local maximizer of a continuous relaxation need not upper-bound the best
  discrete feasible point. The true continuous global maximum does.

Run the relevant counterexample against the statement and, where useful, the
implementation. A prose defect does not prove all code wrong; a code pass does
not prove generality. Retain both findings.

## Validation with scientific value

Use figures to distinguish competing explanations. Combine redundant identity
checks; test where approximations diverge, assumptions fail, or decisions change.
Report numerical-rank threshold sensitivity when small eigenvalues matter.
Separate exact calculation, simulation, extrapolation, and measured data.

Specify information acquisition: observations, actions, noise, sample count,
stationarity, calibration, and costs. An estimator must not assume unavailable
observations. Adaptive/nonadaptive designs, same-realization/independent-block
observations, and known/unknown means can change identifiability.

Disambiguate domain terms. An information-theoretic low-SNR expansion is not
automatically a frequency-selective wideband system result; an asymptotic order
is not a finite-regime gain; a sample or configuration count is not net throughput.
An illustrative comparator is not a reproduced published baseline.

## Remediation priority

Fix correctness and invalid inference, then contribution/value, then exposition.
Keep reviewer claims and independently verified findings distinct. Praise is
prose unless an actual recommendation is supplied; do not infer acceptance votes.

Choose a supported disposition: retain, narrow conditions, replace proof, repair
implementation, invalidate, or open a new study. Reopen dependent claims and
regenerate affected artifacts. Do not make every requested extension a new main
contribution; explain justified scope limits with evidence.
