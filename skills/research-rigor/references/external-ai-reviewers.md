# External AI Reviewer Protocol

## Contents

1. Role and limits
2. Review rounds
3. Human-operated workflow
4. Stanford Agentic Reviewer profile
5. Review intake and remediation
6. Reviewer-overfitting controls

## Role and limits

Use an external AI reviewer as one noisy red-team member, not as:

- a novelty certificate;
- a substitute for domain experts or coauthors;
- evidence that experiments are valid;
- a submission acceptance predictor;
- authority to broaden claims or fabricate missing work.

AI reviews may contain factual errors, invented or mismatched references, preference bias, and venue-style overfitting. Verify every consequential criticism against the manuscript, raw evidence, official venue rules, and primary literature.

Do not automate upload, email entry, or review retrieval when the service requires manual use. The human owns the external disclosure decision.

## Review rounds

Use distinct rounds:

1. `R0 internal adversarial review`: one-page paper, claim matrix, and evidence plan; no external upload.
2. `R1 evidence-complete draft review`: evaluate novelty, soundness, baselines, evidence tiers, and missing experiments.
3. `R2 submission-style review`: use the exact near-final manuscript and target venue after privacy authorization.
4. `R3 no-regression review`: confirm that accepted fixes did not reintroduce old problems or create new unsupported claims.

Do not repeatedly resubmit after cosmetic changes to chase a score. Start a new round only when the evidence, claims, or manuscript materially changed.

## Human-operated workflow

### Prepare the review copy

1. Freeze the manuscript commit or source archive.
2. Generate a dedicated review PDF without changing scientific content.
3. Remove names and affiliations when appropriate, embedded metadata, comments, tracked changes, local paths, credentials, and hidden attachments.
4. Check current service limits, supported language, privacy terms, retention, data use, and venue options.
5. If privacy, retention, deletion, or data-use terms are absent or materially unclear, do not upload the unpublished manuscript. Contact the service or use a locally operated reviewer. Author approval is necessary but not sufficient to override institutional, sponsor, coauthor, or confidentiality restrictions.
6. Run `scan_release.py` and visually inspect the PDF.
7. Record the PDF SHA-256, page count, byte size, target venue, service URL, access date, coverage limits, and authorizer in `10_AI_REVIEW_LEDGER.csv`.

### Manual service interaction

1. The human opens the service.
2. The human uploads the approved PDF.
3. The human enters their own contact information and optional venue.
4. The human records submission time and any review identifier without placing contact information in the research ledger.
5. The human waits for notification and retrieves the complete review.

### Preserve the review

1. Save the unedited review as PDF, HTML, JSON, or UTF-8 text.
2. Record its SHA-256 and retrieval time.
3. Never replace the raw review with a summary.
4. Create a separate extraction that maps one reviewer point to one remediation row.

## Stanford Agentic Reviewer profile

Live-check these official pages before every use:

- Submission: <https://paperreview.ai/>
- Technical overview: <https://paperreview.ai/tech-overview>

Public workflow checked on 2026-07-23:

- upload a paper PDF;
- enter an email address;
- optionally choose a target venue;
- receive an email notification;
- return to view the review.

The submission page currently states a 10 MB PDF limit and analysis of the first 15 pages. The technical overview currently states that reviews are AI-generated and may contain errors, that only English-language papers are supported, and that arXiv grounding is expected to work better in arXiv-rich fields. It also discourages conference reviewers from using the tool in ways that violate conference policy.

Treat all of those details as drift-prone. Recheck the live pages instead of assuming this profile is current. If a manuscript exceeds the analyzed page range, record that the review did not cover the remaining pages or appendices.

The public pages describe the workflow and technical limitations but must not be assumed to grant permission for confidential upload. The human must inspect the current privacy, retention, deletion, and data-use terms and approve disclosure. If those terms remain absent or materially unclear, do not upload.

## Review intake and remediation

For each review point:

1. quote or identify the point without altering its meaning;
2. classify it as novelty, significance, theory, experiment, baseline, statistics, reproducibility, scope, ethics, presentation, citation, or policy;
3. check whether the criticism is factually correct;
4. verify every cited or suggested paper from a primary source;
5. mark the disposition:
   - accept;
   - partially accept;
   - reject with evidence;
   - defer as new study;
   - unclear and needs human judgment;
6. identify required evidence and affected claims;
7. implement only authorized changes;
8. run scientific, numerical, manuscript, and visual no-regression checks;
9. preserve unresolved limitations in the paper and response record.

Prioritize fatal scientific issues over style. A low score without a correct, actionable reason is not a remediation item. A high score does not pass a gate.

## Reviewer-overfitting controls

- Do not hide negative results or limitations to improve an AI score.
- Do not add fashionable terminology without scientific need.
- Do not change a title, abstract, or figure to exploit known reviewer preferences while leaving the evidence gap intact.
- Do not treat agreement among several AI reviewers as independent evidence when they may share models, data, or biases.
- Keep raw reviews from every round, including contradictory reviews.
- Compare reviewer comments against the frozen claim-evidence matrix.
- Require an evidence change, not reviewer sentiment alone, to upgrade a claim.
- Have a human or independent domain reviewer arbitrate high-impact disagreements.
