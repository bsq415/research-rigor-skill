# Idea and Literature Protocol

## Contents

1. Start from a decision-relevant failure
2. Build an auditable literature corpus
3. Perform forensic nearest-neighbor review
4. Attack novelty
5. Freeze or reject the idea

## Start from a decision-relevant failure

Write the problem before the method. Record:

- who makes the affected decision;
- what fails today;
- the measurable cost, risk, or scientific ambiguity;
- why existing benchmarks or metrics miss it;
- what a valid positive result changes;
- what a valid negative result changes;
- the unit, distribution shift, mechanism, or intervention that makes the question precise.

Reject weak formulations such as “apply method X to domain Y,” “combine several signals,” or “compare more models” unless the combination enables a new scientific answer.

Generate several technically distinct candidates and record them in
`01_IDEA_CANDIDATES.csv`. For each one, precommit decision value, exact delta,
strongest already-done argument, evidence feasibility, resource and privacy fit,
falsifier, and kill criteria. A full-cycle assistant may rank and reject
candidates, but the selected row must name the human decision owner and the
evidence used for selection.

## Build an auditable literature corpus

Choose complementary discovery paths that resolve the claim, such as:

1. official venues, proceedings, repositories, or standards;
2. bibliographic and full-text search with synonyms;
3. references, cited-by links, code, datasets, and benchmark lineage from close papers.

Keep landscape discovery separate from verified deep reading. Count a paper as a verified deep read only when the relevant full text was read and the annotation records:

- stable identifier, bibliographic data, retrieval date, and source;
- problem, claim, method, assumptions, data, baselines, metrics, evidence, and limitations;
- relation to the candidate;
- page, section, figure, or table anchors for consequential judgments;
- reader, read date, annotation version, and audit status.

Leave uncertain fields null. Never infer a missing detail merely to complete a table. Never invent a source.

For new projects, stop searching when coverage is justified relative to the
actual novelty question, not when a universal paper count is reached. Record
search scope, saturation evidence, exact delta, strongest counterargument,
feasibility, remaining risks, and the decision basis in
`02_NOVELTY_ASSESSMENT.json`. Link its verified sources and closest papers to the
literature ledger and nearest-neighbor matrix; audit at least the consequential
closest source. Label a same-agent source check honestly rather than calling it
independent review. In coverage mode, closest-paper matrix rows need a completed
`forensic_status` (`verified`, `passed`, or `complete`); pending work is not coverage.

Honor configured numeric requirements in `research_state.json`. To explicitly
use the legacy quota policy, initialize with `--literature-policy quota` and the
desired `--deep-read-min`, `--forensic-neighbor-min`, and
`--independent-audit-fraction`. Zero count defaults in coverage mode do not allow
an empty evidence record to pass G2. Counts never certify originality.

## Perform forensic nearest-neighbor review

For the closest papers, inspect the main text, experiments, appendices, code, data construction, benchmark lineage, references, and subsequent work. Compare:

- research question;
- unit of analysis, intervention, or shift;
- mechanism, model, or theorem;
- observable signal;
- training, testing, and deployment setting;
- datasets and model families;
- evaluation design and valid denominator;
- headline claims and limitations;
- candidate's exact delta and required evidence.

Search not only for the same keywords, but also:

- same question with another method;
- same method on another question;
- same evaluation object under different terminology;
- work whose title and abstract hide the relevant result;
- negative results, replications, and baseline papers.

## Attack novelty

Develop the strongest candidate and the strongest "already done" argument.
Where independent review is available and authorized, give it source artifacts
without the preferred answer. Otherwise perform a separate adversarial pass and
record that it is not independent; do not block on an unavailable agent.

Ask:

- Does the exact `question x unit-or-shift x required-evidence` combination already exist?
- Is the delta technically consequential or merely broader?
- Could a reviewer restate the contribution as an ablation, engineering integration, or additional benchmark?
- Does the candidate change a scientific or deployment decision?
- Can the exact novelty sentence be defended line by line?

Novelty based only on scale, number of axes, or “first systematic study” is fragile unless that scale or unification produces a previously impossible conclusion.

## Freeze or reject the idea

Before freezing, require:

- G0 constraints complete;
- source-linked coverage assessment and any configured numeric targets complete;
- exact nearest-neighbor matrix;
- explicit falsifier and non-claims;
- viable evidence path under available resources;
- explicit novelty/evidence assessment, including whether review was independent;
- exactly one `selected` row in `01_IDEA_CANDIDATES.csv`.

Use these outcomes:

- `FROZEN`: novelty and evidence paths survive all gates.
- `PROVISIONAL`: promising but not fully audited.
- `DEFERRED`: viable, but evidence or resources are unavailable this cycle.
- `KILLED`: already done, ill-posed, contradicted, or unable to produce meaningful evidence.

Do not freeze a title or contribution list first and retrofit novelty later.

Prior estimates of an attractive effect are planning hypotheses. A pilot's
purpose is to establish measurement viability and information value; lack of a
preferred positive effect alone need not kill a valid measurement question.
