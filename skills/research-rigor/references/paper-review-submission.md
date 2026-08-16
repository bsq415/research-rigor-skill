# Paper, Review, and Submission Protocol

## Contents

1. Draft from sealed facts
2. Create trustworthy tables and figures
3. Audit the manuscript
4. Address reviewer feedback
5. Build and verify the submission
6. Archive safely

Use [figures-and-layout.md](figures-and-layout.md) for final-size figure, table,
equation, response-letter, and page-layout checks. Use
[reviewer-red-team-and-resubmission.md](reviewer-red-team-and-resubmission.md)
for the eleven-lens reviewer battery, decision-letter triage, point-by-point
responses, changed-result provenance, revision highlights, and cover letters.

## Draft from sealed facts

Use `06_RESULT_FACTS.csv` and `07_PAPER_CLAIM_MAP.csv` as the quantitative source of truth. Do not retype values from memory, logs, screenshots, or earlier drafts.

For each claim:

- cite fact IDs and evidence tier;
- state the valid denominator and uncertainty;
- preserve contrary rows and limitations;
- distinguish measured, simulated, replayed, diagnostic, and hypothetical evidence;
- avoid causal, deployment, optimality, safety, robustness, or generalization language that exceeds the design.

Add regression checks for superseded claims and known invalid formulations. A later rewrite, merge, or reviewer response must not reintroduce language that earlier evidence disproved.

Write the paper around the scientific question and evidence, not around the implementation chronology. Keep the main contribution narrow enough to defend.

Before full drafting, prepare a one-page paper containing:

- problem and exact delta;
- at most three contributions;
- strongest baseline;
- expected main figure and denominator;
- strongest limitation;
- venue fit;
- three likely reviewer profiles and rejection reasons.

## Create trustworthy tables and figures

Generate tables and figures mechanically from sealed inputs. Store source hashes and generation commands.

For figures:

- choose the visual form that answers a claim;
- choose the intended single- or double-column placement before export and audit
  the asset at that final physical size;
- show uncertainty and denominators where relevant;
- distinguish methods by more than color alone;
- keep legends off data and captions concise;
- avoid decorative complexity, misleading axes, and crowded panels;
- prefer venue-supported vector output for plots, diagrams, line art, and text;
  record effective DPI for every raster asset;
- verify embedded fonts, crop boxes, final-size text and line weight, and honest
  full-range or explicitly justified axes;
- keep comparable panels at consistent sizes;
- preserve raw numerical data beside rendered outputs;
- render the final document and inspect every page.

Do not force a trend through smoothing, monotone envelopes, selective omission, or visual rescaling. Show and explain genuine non-monotonicity or instability.

For tables:

- state metric direction, unit, split, and aggregation;
- distinguish unavailable, undefined, failed, and not run;
- do not bold a “winner” that violates a calibration, validity, or fairness gate;
- do not mix validation-selected and test-selected results.

## Audit the manuscript

Run separate audits for:

- claim-to-evidence traceability;
- citations and nearest-neighbor positioning;
- notation, assumptions, and theorem boundaries;
- baseline fidelity and experimental fairness;
- numbers, units, denominators, and uncertainty;
- limitations and non-claims;
- anonymity, privacy, ethics, conflicts, and disclosure;
- compilation logs, references, floats, fonts, page limits, and visual layout.

Write every checked surface or finding to `07_MANUSCRIPT_AUDIT.csv`, including
location, audit type, severity, evidence IDs, required action, status, and
resolution evidence. An audit with no defect should still record the checked
surface as `not_applicable`; otherwise the absence of rows is not evidence that
the audit happened. Open `fatal` or `major` findings block G9.

A polished PDF is presentation evidence, not scientific evidence.

## Address reviewer feedback

Create one remediation row per actionable point. Record:

- exact request;
- raw review source and stable response anchor;
- underlying reviewer intent and validity assessment;
- type: evidence, analysis, clarification, presentation, citation, policy, or out-of-scope;
- validity and severity;
- proposed action;
- evidence needed;
- evidence IDs and changed-result provenance;
- changed artifact;
- exact manuscript locations;
- regression checks;
- response text;
- unresolved limitation.

Answer evidence requests with evidence or a transparent scope boundary. Do not simulate an official baseline implementation, hardware test, dataset, or deployment and describe it as real. If a same-profile translation or diagnostic is useful, label it precisely.

Preserve all earlier reviewer fixes. Run a no-regression matrix after each revision. Improve layout and language without changing data or claims unless a new evidence gate is completed.

For a formal rejection/resubmission or revise-and-resubmit package, prepare the
bundled response letter, revision highlights, and cover-letter artifacts. Explain
materially changed results through a common-input component and protocol
decomposition. Disclose valid reviewer-found defects and self-initiated fairness
corrections instead of hiding them in the revised manuscript.

Run the strict revision audit before handoff:

```powershell
python "<SKILL_DIR>/scripts/audit_revision_package.py" <project-directory> --strict
```

For a human-operated external AI pre-review, follow `external-ai-reviewers.md`. Preserve the exact reviewed manuscript hash and raw review before extracting comments. Never optimize for an AI score or rewrite presentation solely to game an AI reviewer.

## Build and verify the submission

Use an isolated temporary directory:

1. copy only required source and assets;
2. build using the venue's required sequence;
3. scan logs for errors, unresolved references, rerun requests, overfull content, and font problems;
4. render every page and inspect figures, tables, equations, captions, and references;
5. compare extracted text or hashes with the canonical PDF;
6. verify clean, conventional upload names;
7. create and verify a portable manifest;
8. run privacy and anonymity scans;
9. obtain human confirmation for authorship, affiliations, funding, conflicts, ethics, and disclosure.

Do not infer missing author or policy metadata.

## Archive safely

Keep:

- canonical source package and PDF;
- sealed evidence and manifests;
- generation code and environment lock;
- final review-remediation and decision records;
- a concise revision history.

Before cleanup:

- independently rebuild the canonical package;
- verify hashes and completeness;
- audit which archives, caches, extracted datasets, and environments remain active;
- calculate recoverable size;
- ask before deleting material data or history.

Do not infer a failed cleanup from workspace size alone. Large retained datasets or archive layers may dominate while the paper package is already clean.
