# From literature to a research idea

Use when the researcher asks how papers could produce an idea, how an existing
idea was obtained, or how to find a defensible extension. Generate a concrete
candidate before auditing it. Do not turn an ideation request into only a list
of risks, a literature summary, or a full project scaffold.

For a new empirical question or evaluation object rather than a mathematical
operation transfer, use [empirical idea discovery](empirical-idea-discovery.md).
Do not force a measurement contribution to invent a new optimizer.

## Read for complementary roles

Look for two roles, which may be supplied by several papers or by one paper:

| Role | Extract from the source | Question it enables |
|---|---|---|
| Problem source | Physical mechanism, controllable variables, feasible operations, unmet decision need and current bottleneck | What became controllable or necessary? |
| Method source | The operation that removes the bottleneck: elimination, factorization, invariant, relaxation, sufficient statistic or decomposition | Which operation still works after the model changes? |

Record equation/page anchors and assumptions for each. Read the problem source's
actual model, not just its future-work list. Read the method source immediately
before and after its decisive transformation, including any approximation.
Algorithm names and shared keywords alone are weak evidence of compatibility.

For retrospective explanations, distinguish the researcher's stated inspiration,
what the final paper cites, and a technically plausible reconstruction. A final
manuscript cannot establish an undocumented reading order or prove that one
paper historically caused another idea. Mark later developments separately.

## Match the mathematical structure

Make a small correspondence table: old variable/operator, new counterpart,
unchanged structure, changed assumption, and consequence. Check dimensions,
information availability, normalization, constraints and the physical location
of each control. Two matrices occupying the same place in an equation need not
represent the same implementable device.

A productive candidate is often: retain a useful reduction while making one
previously fixed operator depend on a newly controllable variable. Other valid
bridges remove an unrealistic assumption, improve a costly oracle, or exploit
an observation that the old method discarded. Choose the bridge supported by
the sources; do not force all ideas into variable addition.

Write the candidate before the novelty verdict:

> Source A exposes a controllable mechanism and an unresolved cost. Source B
> provides an operation that simplifies the shared structure. Apply that
> operation under the changed model, then solve the new residual obstacle to
> improve a named decision or metric under a stated resource budget.

## Eliminate the easy block; expose the hard remainder

For a problem `min L(z, u, v)` with coupled variable blocks, ask whether fixing
`(u, v)` gives an exact or inexpensive solution `z*(u, v)`. Substitute the solution
back, including its constraints and normalization. This is partial minimization
(also called profiling or variable projection in suitable settings).

- Derive the reduced objective and its feasible set; do not merely delete `z`.
- Keep coupling terms such as Gram matrices, weights, penalties and noise
  factors until the conditions for removing them have been established.
- If the inner problem has multiple minimizers or changes rank, check whether
  the proposed value function/derivative is defined on the intended regime.
- Label each arrow: exact equality, conditional identity, bound, relaxation,
  approximation, or heuristic. Record the condition and direction of each bound.
- Minimizing a lower bound is a design choice, not a certificate that the
  original minimization objective decreases. Increasing a sum of eigenvalues
  does not imply every eigenvalue increases.
- A closed-form block can be evaluated inside an outer objective without being
  treated as a third numerically optimized block. Show which computation is
  repeated and which optimization has actually been removed.

If a surrogate is used, state its relation to the target and recompute the
original target at feasible candidates. If only a surrogate is checked for step
acceptance, any monotonicity statement must name that surrogate. A bounded
monotone sequence of objective values does not establish global optimality or
stationarity of the iterates.

## Turn the migration obstacle into the contribution

List what survives the transfer and what breaks. Typical obstacles include a
constraint projection destroying a required invariant, a new control affecting
both amplitudes and phases, an acquisition cost that invalidates an oracle, or
an ordered/discrete feasible set that invalidates an unconstrained update.

For each consequential obstacle, connect:

`changed assumption -> failure of the naive transfer -> specific repair ->
observable evidence -> claim boundary`.

The repair may be an identity with explicit conditions, a constraint-preserving
solver, a mechanism-aware derivative, or a cheaper measurement protocol.
Alternating optimization, replacing one generic optimizer with another, and
adding a variable are not by themselves a defensible contribution. Explain the
new relation, failure mode, feasible operation or cost/accuracy tradeoff.

Avoid a hindsight story in which every final module was obvious at the first
reading. Separate the seed idea, the first implementable algorithm and the
later work needed to make the claim supportable.

## Run the cheapest discriminating check

Choose checks for the bridge's actual uncertainty, not a universal test quota:

| Uncertainty | Small check that changes the next decision |
|---|---|
| Does the reduction survive? | Compare the original objective evaluated at the eliminated block with the reduced formula on an exact or small numerical case |
| Does enforcing feasibility break an identity? | Measure both the invariant residual and original-target discrepancy before and after projection |
| Does the new variable enter correctly? | Compare its derivative with a directional finite difference; include every model-dependent factor |
| Does the surrogate rank candidates correctly? | Seek a feasible candidate pair with opposite surrogate/target ordering |
| Is the benefit from the claimed mechanism? | Compare fixed new control, naive transfer, targeted repair and a strong alternative on common inputs |
| Is speed the contribution? | Match stopping, restarts and tuning access; record both work count and elapsed time |

An executed toy check supports its tested case, not the source paper's reported
gains or a general theorem. Distinguish a plausible plan from a completed check.
Repair, narrow or reject a failed bridge; preserve the failure.

## Search the bridge, then state the delta

Search combinations of the new control, the reduced mathematical problem and
the proposed repair, including alternate terminology. Follow closest references
and later work. Separate architecture, reused analytical operation, reused solver
and new contribution in a source-linked delta table. A tutorial identifies a
landscape; it does not establish that no one has solved the proposed problem.

Distinguish novelty at the idea's historical date from novelty at the current
search cutoff. Finding a later near-neighbor may narrow today's contribution
without disproving the stated original inspiration. A limited search supports a
provisional assessment, not a priority claim. Continue with the
[novelty protocol](idea-and-literature.md) when a defensible novelty verdict is
part of the requested scope.

## Deliver an explanation and a usable candidate

Use a compact idea card in the existing project notes. The optional
[idea-transfer card](../assets/idea-transfer-card.md) is a writing aid; copy it
only when a persistent record helps. It is not a new required controller gate.

Explain, in the researcher's language:

1. What each source contributes, with source anchors.
2. The exact question connecting them and the mathematical correspondence.
3. The reduction, its conditions and the remaining design variables.
4. What the naive transfer misses and why the proposed repair matters.
5. The nearest competing solution, supported delta and cheapest falsifier.

State `proposed`, `partially checked`, `supported in tested cases`, or `rejected`
according to actual evidence; use existing project statuses when applicable.
For an ideation-only request, deliver a bounded candidate and next decisive
check without imposing the full project's freeze/selection procedure.

When distilling a private case into this skill, keep the exact source register,
equations, identities and results in the private project. Publish the smallest
de-identified decision rule, following [integrity and privacy](integrity-and-privacy.md).
