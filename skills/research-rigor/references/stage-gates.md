# Stage Gates

## Contents

1. Gate model
2. G0 orientation, privacy, and constraints
3. G1 problem and value
4. G2 literature and novelty
5. G3 claim and theory contract
6. G4 evidence and experiment design
7. G5 reproducible implementation
8. G6 brittle-path pilot
9. G7 frozen full execution
10. G8 result and statistical audit
11. G9 paper and visual evidence
12. G10 reviewer red team and remediation
13. G11 submission, release, and archive
14. Status and handoff format

## Gate model

Advance in order. A later artifact does not retroactively pass an earlier gate. Reopen earlier gates when new evidence changes novelty, assumptions, validity, or feasibility.

For every gate, record:

- owner and decision date;
- status;
- evidence paths and hashes where appropriate;
- pass criteria written before inspection of confirmatory results;
- failure, kill, defer, or redesign condition;
- downstream artifacts invalidated by a failure.

In full-cycle mode, also checkpoint the active task, evidence, next action,
acceptance condition, and human-decision flag in `RESEARCH_CYCLE_LOG.csv`.

Treat a deadline as a scope or venue constraint, never as permission to lower a scientific gate.

## G0: Orientation, privacy, and constraints

Freeze:

- exact workspace and authoritative specification;
- target venue, year, track, deadline, page and policy limits;
- question owner, authorship boundaries, ethics, licenses, confidentiality, and release class;
- available data, models, code, compute, budget, API access, and continuous runtime;
- authorized actions and actions requiring approval;
- canonical artifact locations and retention policy.

Pass evidence:

- completed `00_CONSTRAINTS.md`;
- completed `00_AUTONOMY_CONTRACT.md`, including execution scope and human-only decisions;
- initialized `research_state.json`;
- explicit privacy and export policy;
- current-state audit for an existing project.

Fail or block if critical authority, ownership, privacy, or resource limits are unknown.

## G1: Problem and value

Define the decision owner, costly failure, unit of analysis, and why a valid positive or negative result would change behavior. Reject ideas whose sole value is combining fashionable components, adding another dataset, or moving a leaderboard decimal.

Pass evidence:

- completed problem card;
- compared candidates in `01_IDEA_CANDIDATES.csv`;
- concrete decision consequence;
- explicit scope and non-goals;
- plausible evidence path under G0 constraints.

## G2: Literature and novelty

Build three distinct corpora:

- landscape corpus for broad discovery;
- verified full-text deep-reading corpus;
- forensic nearest-neighbor set for claim-level comparison.

For publication-oriented idea freezing, default to:

- at least 300 unique verified full-text deep reads;
- 30–50 forensic nearest neighbors;
- at least 10% independent source audit;
- no title/abstract-only item counted as a deep read.

Change these defaults only through an explicit G0 contract. If the contract cannot be met, keep the idea provisional or defer it; never silently reduce the target.

Pass evidence:

- search log and deduplicated corpus;
- source-anchored annotations;
- nearest-neighbor matrix and strongest already-done argument;
- independent novelty attack;
- exact, technically consequential delta.
- exactly one selected candidate with an explicit decision owner and evidence path.

Kill if the exact question, unit or shift, and required evidence already exist without a meaningful delta.

## G3: Claim and theory contract

Freeze no more than three headline claims before full implementation. For each claim record:

- exact wording and type;
- falsifier;
- required cells and strongest baselines;
- paired unit and valid denominator;
- minimum meaningful effect or equivalence margin;
- uncertainty method and power;
- confounds and controls;
- failure interpretation;
- explicit non-claims.

For theoretical claims, also freeze definitions, assumptions, boundary cases, counterexamples, proof obligations, independent oracle checks, and numerical validation.

Pass evidence:

- frozen rows in `03_CLAIM_EVIDENCE_MATRIX.csv`;
- theorem contract where applicable;
- no claim that can only be defined after seeing results.

## G4: Evidence and experiment design

Map each claim to a complete dependency chain:

`input -> generation -> parsing -> grading -> validity -> pairing -> fitting -> metric -> uncertainty -> report`

Estimate coverage at every step, shared denominators, compute, wall-clock time, failure modes, and contingency. Pre-register splits, seeds, model selection, metrics, stopping, exclusions, and test policy.

Pass evidence:

- completed experiment protocol;
- claim-linked `04_EXPERIMENT_MATRIX.csv`;
- coverage and failure premortem;
- fair baseline and ablation plan;
- predefined pass, kill, redesign, and defer thresholds;
- at least two reasonably independent evidence paths for each headline claim when feasible.

## G5: Reproducible implementation

Implement:

- source, data, model, prompt, and configuration provenance;
- environment and dependency lock;
- deterministic IDs, splits, seeds, and hashes;
- raw-output and failure preservation;
- append-only run ledger;
- resume and interruption semantics;
- unit, integration, corruption, leakage, and tamper tests;
- mechanical result and figure generation from sealed inputs.

Maintain one authoritative specification. Preserve superseded rules and claim text in an audit trail, but add machine-checkable regression guards so invalidated claims, configs, or artifacts cannot silently re-enter the active paper.

Pass evidence:

- clean-room smoke run from a fresh directory or machine;
- structural tests passing;
- provenance chain and manifest;
- explicit statement that engineering readiness is not scientific validity.

## G6: Brittle-path pilot

Pilot the path most likely to invalidate the project, not the easiest cell. Use the final schema, metrics, validity checks, and report generator; reduce only scale.

Pass evidence:

- end-to-end pilot across representative families and the most extreme condition;
- adequate coverage and paired denominator;
- strong baseline comparison;
- runtime and cost extrapolation;
- no unhandled structural undefined state;
- written go, redesign, defer, or kill decision.

If a parser, prompt, grader, metric, filter, or protocol changes after pilot inspection, version it and validate on fresh held-out evidence. Preserve the original pilot.

Record every scientific protocol change in `04_PROTOCOL_AMENDMENTS.csv`, including
the trigger, changed fields, authorization basis, invalidated artifacts, and
fresh validation evidence.

## G7: Frozen full execution

Run only the frozen protocol. Record every planned cell, completed cell, failure, partial, retry, interruption, and approved deviation.

Rules:

- never overwrite sealed artifacts;
- never re-run solely to obtain a preferred result;
- never treat an interrupted prefix as complete;
- verify IDs, hashes, config, and provenance before resume;
- preserve missing and failed cells in the denominator;
- stop on canary, leakage, corruption, or protocol violations.

If scope must contract, reduce the number of cells or claims through a versioned amendment; do not reduce the rigor of retained cells.

Pass evidence:

- completed run ledger;
- coverage gate;
- sealed raw and derived artifacts;
- approved deviation log;
- no unresolved core-cell blocker.

## G8: Result and statistical audit

Audit validity before effect size:

- planned, produced, parsed, valid, paired, green, undefined, and failed counts;
- common denominators and missingness;
- raw-scale metrics and task-relevant tail, calibration, trajectory, subgroup, or boundary behavior;
- uncertainty intervals, multiple comparisons, power, and practical effect size;
- strongest baseline and matched-budget comparisons;
- robustness, sensitivity, counterexamples, and negative controls.

Treat a null as scientific evidence only when the measurement is valid and powered. Treat undefined, parse failure, leakage, corruption, and zero coverage as measurement failure.

Pass evidence:

- sealed `06_RESULT_FACTS.csv`;
- result audit with claim-level verdicts;
- explicit limitations and contradictory rows;
- reframe, defer, or kill decision for unsupported claims.

## G9: Paper and visual evidence

Draft from sealed facts, not memory or hand-copied numbers. Link every quantitative statement to fact IDs. Separate measured evidence, controlled simulation, diagnostic analysis, and hypothetical envelopes.

Pass evidence:

- paper claim map;
- completed `07_MANUSCRIPT_AUDIT.csv` with no open fatal or major findings;
- figures and tables generated from sealed data;
- claim, citation, notation, and limitation audit;
- compiled and visually rendered manuscript;
- no unsupported deployment, causal, generalization, or optimality language.

## G10: Reviewer red team and remediation

Attack:

- novelty;
- significance;
- theoretical and empirical soundness;
- baseline fidelity;
- evidence sufficiency;
- reproducibility;
- scope and generalization;
- ethics, privacy, and disclosure;
- presentation and venue fit.

Classify every request as evidence, analysis, clarification, presentation, policy, or out-of-scope extension. Do not answer an evidence request with wording alone. Do not fabricate a missing experiment.

Pass evidence:

- remediation matrix;
- raw external AI-review records and manuscript hashes when a human-authorized service was used;
- response text linked to changes and evidence;
- no-regression checks for earlier fixes;
- unresolved limitations retained visibly.

External AI review is optional, never a substitute for independent scientific review, and never permission to upload private material. If used, follow `external-ai-reviewers.md`.

## G11: Submission, release, and archive

Verify:

- current venue policy and metadata;
- authorship, funding, conflicts, ethics, and AI disclosure by an authorized human;
- anonymization and privacy;
- page count, references, fonts, figures, logs, and source completeness;
- isolated rebuild of the exact source archive;
- text or hash agreement between canonical PDF and rebuilt PDF;
- portable manifest and clean upload names;
- canonical package plus auditable revision history.

Do not delete historical or large artifacts until the canonical package is independently rebuilt and verified. Audit storage layers and active code paths before deleting datasets, archives, or caches.

Pass evidence:

- completed submission checklist;
- release scan and semantic privacy review;
- isolated build logs and rendered-page inspection;
- verified manifest;
- canonical archive decision.

## Status and handoff format

Use this compact structure:

```text
Stage:
Gate status:
Authoritative spec:
Verified evidence:
Engineering readiness:
Scientific validity:
Claim downgrades:
Blockers:
Frozen decisions:
Forbidden silent changes:
Next justified action:
Acceptance condition:
Reproduction or verification command:
```
