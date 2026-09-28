# Reusable research paths

These paths distill process lessons from projects with different outcomes. They
are not causal evidence that a workflow wins acceptance. Choose the path matching
the research; keep identities and original reviews in private records. Use only
the stages that remain unresolved.

## Focused methods paper: question to revision to final files

| Decision | Work that changes the decision | Evidence to retain |
|---|---|---|
| What problem is actually modeled? | Align diagram, variable dimensions, objective, constraints, code, and baselines; invalidate results from a superseded model | Model-to-code map and dependencies |
| What is new? | Compare the closest actual methods; separate reused operators, adapted construction, and the new relation | Exact delta and strongest already-done argument |
| Why should the method work? | Identify the condition linking the design objective to the desired metric; state where it is exact/approximate | Derivation, condition, residual/error measurement |
| Does the implementation measure it? | Run an end-to-end pilot and an independent small-case oracle; inspect raw curves | Raw data, pilot verdict, tested failures |
| Is the gain attributable? | Use common inputs; match feasible sets, starts, tuning access, stopping, and evaluation; use ablation/factorial design | Effects, interactions, executed work, uncertainty |
| When is it useful? | Decouple parameters previously moved together; test edge regimes, mismatch, and costs | Boundary failures, observed break-even, limits |
| Can readers verify the story? | Organize around one question; derive numbers and figures from the same facts; audit abstract-to-conclusion scope | Claim map and final-size figures |
| Did revision resolve the concern? | Read original reviews; produce evidence-bearing changes; disclose global result changes; keep every response anchor | Raw review, response matrix, change decomposition |
| Can the exact package be used? | Diff against the submitted baseline; verify clean/marked equivalence; rebuild an isolated archive; follow the actual decision's file requirements | Manifest, rendered pages, upload mapping, portal status |

### What makes revision reusable

**Correct the mechanism before advertising novelty.** If a standard projection
destroys the condition needed by an identity, measure the identity's actual error,
then repair or weaken the claim. A small residual is diagnostic, not proof of
the downstream guarantee. Adding familiar operators is insufficient novelty
without a defensible new relation and evidence.

**Distinguish cost accounts.** Outer iterations, isolated kernel cost, in-loop
line searches, full runtime, tuning, and restarts answer different questions.
Equal iteration caps need not mean equal cost. Report stronger baselines even
when they win. Identify an oracle tuned per evaluation instance and compare
against implementable tuning; do not use it selectively to favor either side.

**Test robustness inside the decision process.** Compare an aware optimizer in a
changed environment, an agnostic optimizer evaluated in that same environment,
and a matched baseline. Measure the predicted behavior and final quality. A small
quality gain remains a small claim.

**Use edge regimes to expose assumptions.** For coupled quantities such as
capacity and load, fix one and vary the other on both sides of the nominal point.
Check rank, shape, feasibility, and undefined metrics. Repair surfaced defects
and check that unaffected regimes remain consistent.

**Explain changed numbers on common inputs.** Separate old/new method from
old/new search protocol, with matched baselines in every valid cell. Estimate
interactions; do not assume gains add. Keep a defective old implementation only
as an invalid diagnostic. Do not rerun just an almost-tied or disappointing
comparison to obtain a favorable result; an additional precision study needs a
recorded rule and must show the original result.

**Distinguish paper stages.** A marked revision is relative to the version the
reviewers saw, not a working draft. Later editorial requests can change the
upload set. After acceptance, preserve scientific content unless a substantive
correction is authorized; regenerate figures from unchanged data and verify
diagram connectivity. A format extension does not prove an image is vector.

Response mechanics: [reviewer protocol](reviewer-red-team-and-resubmission.md).
Final files: [paper protocol](paper-review-submission.md).

## Empirical study: idea selection to evidence-driven manuscript

1. **Choose by question and feasibility.** Scan the field, then attack shortlisted
   ideas with exact nearest neighbors. Keep a kill log. Verify actual resources
   and the hardest integration path. Predicted headline numbers are hypotheses.
2. **Define an observable intervention.** A nominal prompt, budget, treatment, or
   policy label does not establish behavior change. Measure realized exposure
   and compliance. Post-hoc compliance subgroups are descriptive unless the
   design supports more.
3. **Pilot the full evidence chain.** Generation completion is insufficient.
   Check parsing, grading, validity, pairing, splits, features, fitting, metrics,
   intervals, and reporting on the brittle case. A feature manifest is not a
   trained model; an allocated cell is not a valid result.
4. **Freeze interpretable comparisons.** Specify unit, eligible population,
   pairing, splits, failure rules, and analysis family. Within-condition effects
   and cross-condition transfer hold different things fixed; separate estimands.
5. **Audit coverage before effects.** Track planned → produced → parsed → valid
   → paired → estimable → reported. Explain missingness by mechanism/condition.
   Similar missing rates do not prove missing-at-random. Assess survivor bias and
   which population observed cells support. Zero coverage is not no effect.
6. **Let results revise the hypothesis.** Replace unsupported universal stories
   with supported heterogeneous results, including improvements, nulls, and
   undefined cases. Version claims; label discoveries as exploratory and reserve
   confirmation for independent validation.
7. **Repair the bottleneck.** Inventory artifacts before buying compute. Existing
   raw generation may support a CPU repair. Budget compute + reanalysis + all
   downstream regeneration + numeric/visual verification. Changed validity rules
   need versioning and bias analysis, not merely a larger coverage percentage.
8. **Build from a facts layer.** Derive counts, denominators, effects, intervals,
   tables, plots, abstract, and supplement from consistent inputs. Verify actual
   code settings against prose. Audit numbers inside overview diagrams. Sync any
   separately stored submission abstract and retain the exact submitted package.

Use AI pre-review for correct, actionable criticisms, tied to the reviewed
version. Favorable AI reports are neither formal reviews nor independent
scientific validation. Distinguish local readiness, user-reported progress,
official phase decisions, and final acceptance. Phase advancement supports
continuing the process, not a claim of eventual acceptance or soundness of every
method choice. If a decision notification uses an older title, reconcile version
identity before applying later review comments; do not assume the portal changed.

Experiment rules: [experiment and evidence](experiment-and-evidence.md).
Idea coverage: [idea and literature](idea-and-literature.md).

## Rejected theory paper: repair, reassess, or rebuild

Start from the editorial decision and original reports. If only a summary exists,
label attribution as secondhand and seek originals; meanwhile test claims against
the actual manuscript/code. Keep editor priorities separate from reviewer votes.

Separate correctness, nontrivial novelty, and scientific/engineering value.
Passing one does not pass the others. Many formulas or matching curves cannot
answer all three. Use [theory and claim audit](theory-and-claim-audit.md) to
localize defects. Retain valid lemmas; retract unsupported extensions. Propagate
corrections to abstract, corollaries, algorithm claims, figures, and conclusions.

If repair leaves only standard machinery, identify one unresolved decision rather
than add extensions. Compare equivalent results under other terminology. Test
identifiability, observability, finite-data stability, acquisition cost, and
whether the result improves the decision metric. Fewer configurations need not
mean fewer total samples or better net utility. A reconstruction lower bound
need not be a task-specific decision lower bound.

Preserve failed candidate routes. Successive proposals are not validated results.
A candidate theorem, numerical audit, and resubmission policy are different
evidence tiers. Check current venue rules when resubmitting; lack of an invitation
alone proves neither eligibility nor prohibition.
