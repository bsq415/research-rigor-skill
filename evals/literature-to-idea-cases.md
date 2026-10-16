# Literature-to-idea behavioral cases

These synthetic cases specify observable behavior for the new
[workflow](../skills/research-rigor/references/literature-to-idea.md).
They are not a completed paired model evaluation, a novelty benchmark, or
evidence of improvement over an unassisted model. Repository tests only check
packaging and existing runtime invariants. Preserve the previous evaluation
baseline and results.

## A. Generate a usable transfer

Request: A sensor-design paper exposes selectable measurement locations and
costly joint estimation. Another paper analytically solves regularized linear
least squares for fixed measurement operators. Explain the bridge and propose
a bounded candidate under a fixed acquisition budget.

Check whether the answer maps locations to the measurement operator, solves
the conditional coefficient block with its regularization intact, states the
remaining placement objective and constraints, and proposes an informative
small comparison against fixed placement and joint optimization. It should
generate an actual candidate before auditing novelty, and distinguish training
residual from the intended prediction/estimation target. Do not invent source
metadata or demand full project initialization.

## B. Detect where naive transfer fails

Steering for A: The new sensor must obey a nonnegative coefficient constraint;
an example unconstrained coefficient is negative. The proposed speedup replaces
the true reduced loss by a lower bound and accepts steps only on that bound.

Check whether the answer withdraws the unconstrained inner optimum where
infeasible, derives or requests a valid constrained inner solve, and limits
monotonicity to the accepted quantity. It should propose a repair and a small
counterexample/check, not just reject the entire research direction or promise
that decreasing a lower bound decreases the true loss.

## C. Explain provenance without inventing chronology

Request: The researcher says A and B inspired an idea. The final paper cites C
for a related operator and a later D already combines the broad architecture.
Only the supplied artifacts and that recollection establish the history.

Check whether the answer distinguishes the stated inspiration, final citations
and analyst reconstruction; separates the seed from later repairs; and narrows
the current novelty delta against D. It must neither invent a reading diary nor
discard the researcher's stated inspiration merely because B is uncited.

For a future model comparison, freeze inputs and scoring before execution, use
fresh sessions, keep source/tool access matched, and report answers and actual
failures. A same-author walkthrough is not independent review.
