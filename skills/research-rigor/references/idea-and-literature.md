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

## Build an auditable literature corpus

Use at least three independent discovery paths:

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

Use the configured minimum in `research_state.json`. For a default publication-grade idea freeze, use 300 verified deep reads, 30–50 forensic nearest neighbors, and a 10% independent source audit.

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

Create the strongest version of the candidate and the strongest “already done” argument independently. When one person performs both roles, use a separate context or independent reviewer and do not reveal the intended answer.

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
- configured deep-reading and audit targets complete;
- exact nearest-neighbor matrix;
- explicit falsifier and non-claims;
- viable evidence path under available resources;
- independent novelty and evidence sign-off.

Use these outcomes:

- `FROZEN`: novelty and evidence paths survive all gates.
- `PROVISIONAL`: promising but not fully audited.
- `DEFERRED`: viable, but evidence or resources are unavailable this cycle.
- `KILLED`: already done, ill-posed, contradicted, or unable to produce meaningful evidence.

Do not freeze a title or contribution list first and retrofit novelty later.
