# Experiment Protocol

## Version and authority

- Protocol version:
- Frozen at:
- Authoritative commit:
- Change authority:

## Claim coverage

- Claim IDs:
- Evidence paths:
- Strongest baselines:
- Required ablations and negative controls:

## Data

- Source, version, license, and fingerprint:
- Unit of analysis:
- Sample IDs:
- Train, validation, and locked-test split:
- Mask and missingness policy:
- Train-only selection and preprocessing:
- Leakage checks:

## Models and execution

- Models and checkpoints:
- Prompt, grader, sampler, or inference settings:
- Validation selection rule:
- Seeds and repetitions:
- Hardware and environment:
- Runtime, cost, and contingency:
- Resume and interruption contract:

## Metrics and statistics

- Primary metric:
- Secondary metrics:
- Raw-scale or domain-scale transform:
- Tail, subgroup, calibration, trajectory, or boundary checks:
- Valid denominator:
- Confidence interval or test:
- Multiplicity handling:
- Minimum meaningful effect or equivalence margin:

## Coverage premortem

`input -> generation -> parsing -> grading -> validity -> pairing -> fitting -> metric -> uncertainty -> report`

- Expected validity at each step:
- Structural undefined states:
- Failure taxonomy:
- Minimum green coverage:
- Minimum paired denominator:

## Pilot

- Most brittle path:
- Pilot cells:
- Pass threshold:
- Redesign threshold:
- Defer or kill threshold:

## Frozen-change policy

- No frozen field may change after result inspection without a new protocol version.
- Preserve the original pilot and artifacts.
- Validate a revised protocol on fresh held-out evidence.
- Do not reuse a touched test set for selection.
