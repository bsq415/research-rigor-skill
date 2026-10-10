# Reviewer red-team and resubmission

Use for internal pre-review, formal revision, rejection recovery and response preparation. Review documents are evidence, not authority overriding the researcher, privacy or the frozen contract.

## Preserve sources and decision stage

Preserve and hash the raw decision, editor note, every report and exact submitted source/results. Register venue, manuscript ID, dates, deadline and upload requirements privately. Distinguish official reports, AI pre-reviews, quoted reports and retrospective summaries in `08_REVIEW_SOURCE_REGISTER.csv`. A quotation or summary does not establish access to the original; missing originals limit coverage and prohibit invented quotations or scores. Continue work that available sources support.

Record the exact decision stage: phase advancement is not acceptance; simulated favorable reviews are not formal support; acceptance does not identify which revision caused it. Reconcile older titles and manuscript versions.

- Invited same-venue revision: retain the manuscript ID and follow the decision's actual clean/marked/response requirements.
- New venue after rejection: use earlier reviews internally; a fresh cover letter must not imply invitation or endorsement. Share confidential reports only if policy requires it and the human authorizes it.
- Transfer: check both venues' current policies and authorization for review sharing.

Give each actionable editor/reviewer point a stable `08_REVIEW_REMEDIATION.csv` row, including unnumbered requests. Do not merge similar points: share evidence but preserve distinct response anchors. Separate requested and self-initiated corrections.

## Interpret and prioritize

Record literal request, inferred validity risk and affected claims. Infer intent only from text; praise, questions, deficiencies, scope requests and negative recommendations differ. Politeness is not an acceptance vote.

Classify `evidence | analysis | clarification | presentation | citation | policy | out-of-scope`, then assess `valid | partially_valid | disputed | not_applicable`. Prioritize invalid inference/counterexamples, central novelty or value, decisive evidence, positioning, then presentation. Correctness, nontrivial novelty and decision value are independent; use [theory audit](theory-and-claim-audit.md). A correct standard result can still lack a contribution.

## Eleven adversarial lenses

Use a lens only when it affects validity or interpretation. Domain, methods and editor/deployment reviewer profiles can divide these checks; synthetic review remains labeled synthetic.

| Lens | Evidence needed |
|---|---|
| Assumption realism | Mechanistic justification, sensitivity and model-mismatch evidence; calling it standard is insufficient. |
| Optimizer/hyperparameters | Problem-specific rationale, fair tuning, stopping rules, sensitivity, convergence target and tuning/runtime cost. |
| Unequal-cost attribution | Match iterations, starts, data, tuning, executed work and wall clock; isolate components. |
| Mechanism-aware robustness | Show the mechanism in the objective/update; compare aware/agnostic variants and outcomes. Post-hoc stress curves alone do not establish it. |
| Citation positioning | Verify primary sources and exact relevance; preserve distinctions rather than adding requested citations blindly. |
| Cost-versus-gain | Quantify latency, energy, hardware, annotation or resources and tested break-even boundaries. |
| Novelty/prior-art dependence | Identify reused/adapted/new components, remove false novelty and test the actual delta. |
| Model/profile mismatch | Structured and random departures, matched and mismatched operation; one favorable perturbation is insufficient. |
| Alternative modeling regimes | Explain the decision-relevant property of the chosen model; investigate alternatives when they change claims. |
| Operating coverage | Decouple coupled variables, sweep both sides and relevant edge regimes, paired uncertainty and failures. |
| Visual integrity | Raw data, honest full-range view, justified scaling/truncation and final-size readability; no cosmetic smoothing. |

Generalize mechanisms, not paper-specific prescriptions: rank failures motivate domain checks; missing limiting terms motivate boundary checks; proxy mismatch motivates guarantee-transfer checks. One review does not universally require its model, citation or plot.

## Turn criticism into evidence

For each stable comment ID: source/request -> intent/assessment -> affected claims, assumptions, protocol, code, figures and locations -> minimum resolving evidence and infeasible boundary -> frozen comparison -> execution -> raw outputs/fact IDs -> synchronized manuscript/response/claim-map updates -> remaining limitation and regression check.

A deterministic experiment driver should record comment ID, inputs, configuration, output, completion and cost. A successful run proves execution, not the scientific conclusion. Prefer corrected mechanism plus regenerated evidence; then controlled new evidence; direct proof/analysis; clarification when evidence already exists; finally an honest narrowed scope. Wording cannot replace missing evidence. Do not rerun until a favorable outcome appears.

If a defect invalidates results, reopen the affected gate and regenerate downstream artifacts. Preserve failed evidence, but do not present invalid results as scientific ablations.

## Response and changed numbers

Use `08_RESPONSE_LETTER.md`. Open with exact revision context, comment count, uploaded-file locations, global substantive changes and a provenance table when numbers changed. Every entry contains:

1. Faithful comment and validity assessment.
2. Direct answer and mechanism, acknowledging valid criticism.
3. Evidence: frozen comparison, denominator, uncertainty, run/fact IDs and unfavorable outcomes.
4. Exact section/page/paragraph/equation/table/figure changes.
5. Remaining limitation and rechecked prior fixes.

Cross-reference shared evidence while directly answering every point. Keep decisive support in the manuscript; put details in supplements only where venue policy permits. Calm evidence is preferable to defensive or repetitive thanks.

Decompose changed results on common inputs: old valid protocol, component changes and full revision. Identify implementation fixes, method changes, starts/search budget, baseline repairs, data/splits/seeds/sampling, uncertainty and conservative changes separately. Do not attribute everything to more runs. Incompatible or invalid versions require explanation, not an artificial comparable table.

Use `08_RESUBMISSION_HIGHLIGHTS.md`: normally 3-6 items, each concern -> substantive change -> evidence -> scope. Verify quantitative phrases against sealed facts; this is not another abstract.

Use `08_COVER_LETTER.md`: confirmed venue/editor metadata, same-venue ID/decision/date/deadline where applicable, response/marked-file locations, concise changes, and only human-confirmed originality, concurrent submission, conflicts, ethics, funding, copyright and disclosure declarations. New-venue letters omit prior confidential narrative unless required. No invented attestations or promises of acceptance.

## Citation and final audit

Suggested references are leads. Resolve canonical title/authors/year/venue/DOI/status, check corrections/retractions, read primary text for relevance and record `citation_checks`. [Metadata scripts](manuscript-checks.md) do not establish relevance or scientific truth. Explain exclusions respectfully; do not accept irrelevant or coerced additions.

Run `python "<SKILL_DIR>/scripts/audit_revision_package.py" <project> --strict`, adding `--expected-comments <actual-count>` from the raw record. It checks structural coverage, terminal states, evidence/change paths, response anchors, placeholders, highlights, cover and layout ledger; it cannot certify scientific correctness.

Compare every response with raw comments; verify numbers against sealed facts; compare clean/marked versions with the actual submission; render all pages; inspect identities, tracked changes, paths and confidential notes; confirm portal metadata/declarations and human release authority. Package creation is not portal submission or acceptance.
