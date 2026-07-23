# Experiment and Evidence Protocol

## Contents

1. Design from claims
2. Contract theory
3. Plan fair experiments
4. Build reproducible execution
5. Pilot the brittle path
6. Execute without result repair
7. Audit and interpret results

## Design from claims

For every headline claim, specify:

- exact wording and claim type;
- falsifier;
- strongest relevant baseline;
- comparison unit and valid denominator;
- minimum meaningful effect or equivalence margin;
- sample size, power, confidence interval, and multiplicity handling;
- confounds, controls, and alternative explanations;
- expected evidence tier;
- explicit non-claims.

Do not define the main claim after inspecting test results. Do not treat non-significance as equivalence without an equivalence design.

## Contract theory

Before naming a theorem or using it in the paper:

1. define every object and domain;
2. list all assumptions and the physical or statistical meaning of each;
3. verify dimensions, invariances, limiting cases, and degenerate cases;
4. search for counterexamples and known special cases;
5. obtain an independent symbolic or numerical oracle;
6. run Monte Carlo or exhaustive checks where applicable;
7. separate exact results, bounds, approximations, heuristics, and empirical observations;
8. ensure the narrative does not claim more than the formal statement.

Do not transfer a guarantee from a surrogate to a target metric without proof. Do not turn an effective-rank, heuristic, or coding-gain quantity into a diversity order or causal mechanism.

## Plan fair experiments

Freeze:

- dataset version, license, sample IDs, split, mask, and preprocessing;
- models, checkpoints, prompts, graders, sampling, and inference budgets;
- selection metric and validation rule;
- test-set access rule;
- random seeds and repeated-run protocol;
- baselines under matched data, compute, tuning, and information access;
- ablations that remove or replace each claimed mechanism;
- raw-scale metrics plus task-relevant tail, calibration, subgroup, spatial, temporal, trajectory, or peak diagnostics;
- failure taxonomy and missingness policy.

Use a common evaluation interface. Do not rank heterogeneous models with a metric that only some models define. Report coverage together with interval width, accuracy together with calibration, and aggregate results together with critical slices.

Construct the strongest baseline in the same feasible action space. Do not forbid revisits, information, tuning, or resources for a baseline merely to manufacture an advantage. Separate scheduler-, model-, data-, and backbone-level gains.

For transformed or generative targets, inspect inverse-transform tails, clipping, overflow, samples, intervals, trajectories, and peak behavior before trusting averages.

Fit preprocessing, feature selection, normalization, masks, thresholds, and spatial or temporal region selection on training data only. Use identical valid units and windows across methods. If exploratory work already used test results for selection, label it exploratory and require a fresh locked test block for confirmatory claims.

## Build reproducible execution

Record and verify:

- source commit and dirty state;
- data, model, prompt, config, and environment hashes;
- hardware and software versions;
- deterministic sample IDs and ordering;
- run ID, seed, start and finish time;
- raw outputs, logs, failures, and completion markers;
- parent artifact hashes for every derived table or figure.

Make runs append-only. A resume must:

1. identify the same approved environment and source;
2. validate the existing prefix row by row;
3. confirm no premature completion manifest exists;
4. resume at the next frozen ID;
5. preserve the original prefix and its hash;
6. seal only after the full contract passes.

Use corruption, leakage, provenance, and tamper tests. A cached or templated backend may prove pipeline plumbing, but it is not scientific evidence unless the claim explicitly concerns that backend.

Physically separate template, toy, smoke, partial, legacy, invalid, and scientific artifacts. Reject a checkpoint or cache that lacks the matching run contract, completion marker, source state, or data fingerprint.

Exercise the real integration surface before full execution. Stub tokenizers, template backends, tiny synthetic data, and unit tests can preserve the same wrong assumption; use a bounded live pilot with the actual model, data schema, device, parser, and external runtime.

## Pilot the brittle path

Pilot the most failure-prone chain, including parsing, validity, pairing, fitting, metric, uncertainty, and reporting. Include strong baselines and the most extreme planned condition.

Pre-write:

- minimum coverage and class balance;
- minimum paired denominator;
- pass, redesign, defer, and kill thresholds;
- runtime, cost, and thermal or stability limits;
- tolerated parser, grader, or measurement error;
- structural undefined states.

Use the same schema and analysis code as the full run. If observations motivate a design change, preserve the pilot, increment the protocol version, and validate on fresh held-out evidence.

## Execute without result repair

During a frozen run:

- monitor coverage and integrity before effects;
- keep planned, partial, failed, invalid, and complete states distinct;
- do not retry only unfavorable cells;
- do not change a prompt, filter, metric, seed, model, split, or grader silently;
- do not replace requested compute with a weaker fallback without approval;
- do not remove failures from the denominator;
- stop on leakage, canary failure, corruption, provenance mismatch, or contract violation.

Engineering faults may be fixed under a versioned protocol if the change cannot select on outcomes. Scientific redesign creates a new protocol and requires new confirmation data.

When an implementation bug is found, preserve raw upstream artifacts, quarantine affected derived outputs, fix the code, add a regression test for the observed pattern, and regenerate derived artifacts from unchanged raw inputs. Do not edit reported rows in place. Distinguish a code defect from a valid structural failure such as undefined output or a model that never reaches an answer.

When time or compute shrinks, reduce breadth only through an explicit scope amendment. Preserve per-cell rigor, denominators, signals, seeds, and validation rules. Report incomplete coverage rather than weakening each cell or stopping early to protect a cleaner story.

## Audit and interpret results

First audit:

- planned versus completed cells;
- parse, grade, validity, pairing, and green rates;
- common valid denominator;
- missingness and failure reasons;
- split, model, and artifact provenance;
- whether any test evidence influenced selection.

Then evaluate:

- validation-selected checkpoint;
- raw-scale primary and secondary metrics;
- confidence intervals and practical magnitude;
- strongest baseline and matched-budget comparisons;
- tail, calibration, trajectory, subgroup, and boundary sanity checks;
- ablations, counterexamples, sensitivity, and robustness;
- cross-seed and cross-condition consistency;
- runtime, memory, and cost.

Classify evidence:

- measured and directly reproducible;
- controlled simulation;
- replay or profile-based;
- diagnostic or proxy;
- hypothetical envelope;
- unsupported or future work.

Write claims at the weakest applicable tier. Preserve a strong competing result or failed ablation as a limitation. A valid negative result can be valuable; a broken measurement cannot.

Never smooth, envelope, reorder, censor, or post-process a curve to force monotonicity or a preferred trend. Explain finite-run or finite-sample irregularities and retain the raw values.
