# Full-Cycle Execution

## Contents

1. What full-cycle means
2. Start or resume
3. Persistent execution loop
4. Capability playbook
5. Experiment repair router
6. Human-only boundaries
7. Completion contract

## What full-cycle means

Full-cycle mode authorizes the assistant to continue through every reversible,
in-scope, evidence-justified research task without waiting for a new prompt after
each routine step. It is an execution policy, not a transfer of scientific
ownership.

The assistant may autonomously:

- inspect authorized artifacts and recover project state;
- generate, attack, compare, rank, reject, and recommend question candidates;
- search permitted literature sources and build source-anchored novelty evidence;
- design claims, falsifiers, baselines, ablations, controls, protocols, and tests;
- implement and run experiments within frozen resource and privacy limits;
- inspect raw outputs, coverage, failures, uncertainty, and contradictory evidence;
- repair engineering defects, or propose a versioned scientific redesign;
- draft a paper from sealed facts and audit every claim, citation, figure, and limit;
- repeat the inspect, act, verify, and checkpoint loop until a gate passes, fails,
  blocks, defers, or is killed.

It may not autonomously decide authorship, ethics, disclosure, private release,
material spending, destructive cleanup, final scientific interpretation, final
claims, final venue submission, or any protocol change that requires human
authorization.

Do not claim that full-cycle mode guarantees a publishable topic, successful
experiment, correct conclusion, valid paper, favorable review, or acceptance.

## Start or resume

For a new project:

```powershell
python "<SKILL_DIR>/scripts/init_research_project.py" <project-directory> --mode full-cycle
```

Complete both `00_CONSTRAINTS.md` and `00_AUTONOMY_CONTRACT.md`. Ask only for
missing facts that materially change scope, authority, privacy, resource use, or
scientific meaning. Do not ask for routine implementation preferences that can
be resolved from project conventions and reversible inspection.

For any project, recover durable state before acting:

```powershell
python "<SKILL_DIR>/scripts/research_cycle.py" status <project-directory>
python "<SKILL_DIR>/scripts/audit_research_state.py" <project-directory>
```

Inspect the authoritative artifacts named by the current gate. Live files, raw
outputs, executable checks, and hashes outrank the state summary. If they
disagree, stop the affected transition, record the discrepancy, and repair the
control state from evidence.

Legacy projects can add missing templates without overwriting existing files:

```powershell
python "<SKILL_DIR>/scripts/init_research_project.py" <project-directory> --merge --mode full-cycle
```

Review the merged contract and migrate `research_state.json` deliberately; never
replace a populated legacy state with a blank scaffold.

## Persistent execution loop

For every unit of work:

1. **Recover** the current gate, active task, next action, acceptance condition,
   blockers, frozen fields, and relevant protocol version.
2. **Orient** against the live workspace, governing instructions, privacy
   boundary, compute budget, and authoritative spec.
3. **Select** the smallest action that can produce decision-relevant evidence
   for the current gate.
4. **Declare** a stable task ID, expected artifacts, verification command,
   failure meanings, and whether a human decision is required.
5. **Checkpoint** before long-running, expensive, externally dependent, or
   interruption-prone work.
6. **Execute** real work when tools and authority are available. Planning alone
   is not completion when implementation or experiment execution was requested.
7. **Verify** outputs independently of the generating path where practical.
   Inspect raw-scale behavior and failure coverage before headline metrics.
8. **Classify** the outcome using the repair router below. Never call every
   undesirable outcome an implementation bug.
9. **Transition** the gate only when its predeclared evidence exists and the
   structural audit passes.
10. **Continue** immediately to the next reversible, authorized action in
    full-cycle mode. Stop only at a human-only boundary, an exhausted safe search
    space, or a terminal gate outcome.

Record a durable checkpoint:

```powershell
python "<SKILL_DIR>/scripts/research_cycle.py" checkpoint <project-directory> `
  --task-id G4-design-matrix `
  --gate G4 `
  --status in_progress `
  --summary "Defined claim-linked experiment cells and failure thresholds" `
  --evidence 04_EXPERIMENT_MATRIX.csv `
  --next-action "Complete coverage premortem and freeze protocol candidate" `
  --acceptance-condition "All headline claims have required baseline, ablation, denominator, and kill cells"
```

Record a gate decision:

```powershell
python "<SKILL_DIR>/scripts/research_cycle.py" transition <project-directory> `
  --task-id G4-gate-decision `
  --gate G4 `
  --status passed `
  --summary "Experiment design satisfies the frozen claim contract" `
  --evidence 04_EXPERIMENT_PROTOCOL.md 04_EXPERIMENT_MATRIX.csv 04_COVERAGE_MODEL.csv `
  --next-action "Build the smallest complete reproducible pipeline" `
  --acceptance-condition "Clean-room smoke run and structural tests pass"
```

The command is a state-integrity guard, not a scientific judge. A qualified
researcher remains responsible for interpreting evidence and approving
human-owned decisions.

## Capability playbook

### Select and freeze a question

1. Convert constraints into several technically distinct candidates, including
   at least one simple or negative-control direction.
2. Record candidates in `01_IDEA_CANDIDATES.csv`.
3. For each candidate, state decision value, exact delta, strongest
   already-done argument, evidence feasibility, resource fit, privacy fit,
   falsifier, and kill criteria.
4. Search and deep-read according to `idea-and-literature.md`. Attack the best
   candidate with exact nearest neighbors and the strongest baseline before
   recommending it.
5. Reject fashionable combinations without a decision-relevant delta.
6. Recommend a candidate only when it is both scientifically consequential and
   testable under the verified constraints. Mark it `selected` only with an
   explicit decision owner and evidence path.

If no candidate survives, return a reasoned `deferred` or `killed` outcome. Do
not invent novelty to keep the workflow moving.

### Design the evidence

1. Freeze at most three headline claims with falsifiers and non-claims.
2. Expand every claim into required cells in `04_EXPERIMENT_MATRIX.csv`.
3. Include the strongest feasible baseline, matched-budget comparison,
   ablations, negative controls, boundary or tail cases, seeds or repetitions,
   valid denominator, uncertainty method, minimum meaningful effect, and
   pass/redesign/kill threshold.
4. Run a coverage premortem over the full dependency chain.
5. Freeze the protocol before locked-test inspection.

Prefer the smallest design that can falsify the claim. More runs do not repair
an invalid comparison, leaked split, weak baseline, or undefined denominator.

### Implement and execute

1. Implement one authoritative path from configuration to raw output to
   mechanical report.
2. Add provenance, deterministic IDs, hashes, environment locks, interruption
   semantics, and append-only ledgers before full execution.
3. Test units, integration boundaries, corruption handling, leakage guards, and
   result generators.
4. Pilot the most brittle path at final schema fidelity.
5. Run the frozen matrix, preserving partials, invalid cells, failures, costs,
   and missingness.
6. Checkpoint long runs so another turn or compatible agent can resume from
   evidence rather than conversational memory.

Tool availability matters. If the host lacks data access, compute, credentials,
or an executable environment, prepare an exact handoff and mark the state
`blocked`; do not simulate completion.

### Audit results

Inspect in this order:

1. planned, produced, parsed, valid, paired, green, undefined, and failed counts;
2. provenance, hashes, protocol version, leakage, and corruption;
3. raw-scale and domain-scale distributions, tails, peaks, trajectories,
   boundaries, calibration, and relevant subgroups;
4. common denominators and missingness mechanisms;
5. uncertainty, multiplicity, power, and practical effect size;
6. strongest baseline, robustness checks, counterexamples, and negative controls;
7. claim-level verdict and allowed wording.

Seal only facts that survive this audit. A valid negative result is evidence; an
underpowered or invalid measurement is not.

### Repair or redesign

Use the repair router below. Every protocol change goes in
`04_PROTOCOL_AMENDMENTS.csv`. Preserve the old protocol, affected outputs, and
decision evidence. Never overwrite a result or silently rerun until it looks
better.

### Write the paper

1. Draft the one-page paper before expanding sections.
2. Generate quantitative text, tables, and figures from sealed fact IDs.
3. Keep measured results, controlled simulation, diagnostics, and hypothetical
   examples visibly distinct.
4. Link each manuscript claim to facts, evidence tier, denominator, limitations,
   non-claims, and source in `07_PAPER_CLAIM_MAP.csv`.
5. Preserve nulls, contrary results, coverage gaps, and scope limits.
6. Compile and render the actual manuscript; inspect every page.

Good prose cannot upgrade weak evidence. When the claim map lacks support,
downgrade or remove the sentence.

### Audit and revise the paper

Record findings in `07_MANUSCRIPT_AUDIT.csv` across:

- claim-to-evidence consistency;
- novelty positioning and citation verification;
- method and notation consistency;
- baseline, metric, denominator, and statistical fidelity;
- figure/table agreement with sealed facts;
- limitations, non-claims, ethics, privacy, and disclosure;
- reproducibility and artifact links;
- venue rules, build health, and visual rendering.

Treat `fatal` and `major` findings as gate blockers until resolved, accepted as a
visible limitation, or explicitly deferred to a new study. Run reviewer red
teams only after the internal evidence audit. External AI reviewers are optional,
human-operated inputs and follow `external-ai-reviewers.md`.

## Experiment repair router

Classify the observed failure before changing anything.

### 1. Environment or tool failure

Examples: dependency outage, transient API failure, preemption, disk-full event,
or corrupt download with an independent checksum.

Action:

- preserve logs and partial artifacts;
- repair the environment without changing scientific fields;
- rerun regression and provenance checks;
- resume or retry the same frozen cell;
- keep retries visible in the run ledger.

This is engineering repair, not a protocol amendment, unless the environment
change affects numerical behavior, sampling, model version, or comparability.

### 2. Implementation defect

Examples: indexing bug, wrong unit conversion, stale cache, incorrect join,
parser defect, or figure generator reading the wrong column.

Action:

- quarantine every derived artifact downstream of the defect;
- add a regression test that fails on the old behavior;
- fix the implementation and verify with an independent oracle where possible;
- regenerate from unchanged raw inputs;
- record invalidated artifacts and new hashes.

If the defect affected selection, data exposure, metrics, or protocol semantics,
route to a protocol amendment instead.

### 3. Measurement or protocol defect

Examples: invalid denominator, unfair baseline budget, unhandled structural
undefined state, underpowered design, leaked split, or metric that does not
measure the stated construct.

Action:

- do not reuse the affected result as confirmatory evidence;
- open a versioned row in `04_PROTOCOL_AMENDMENTS.csv`;
- identify changed fields and every invalidated artifact;
- obtain the required human authorization;
- validate the revised protocol on fresh held-out evidence;
- reopen all dependent gates.

### 4. Valid scientific failure

Examples: the strong baseline wins, the effect misses the frozen threshold, the
theorem has a counterexample, or the candidate is not novel.

Action:

- preserve and report the result;
- mark the claim or gate failed, deferred, or killed;
- narrow wording only if the narrower claim was independently supported;
- redesign only as a new scientific protocol with new evidence.

Never call a valid scientific failure a bug merely because it is inconvenient.

### 5. Resource, authority, privacy, or external-state block

Action:

- record the exact missing input and safe work that can continue;
- prepare a minimal, reproducible handoff;
- prohibit substitutions that would change the question or evidence;
- wait for the authorized human or external state.

## Human-only boundaries

Stop and ask when:

- two scientifically defensible paths imply materially different questions,
  claims, costs, risks, venues, or interpretations;
- authorship, ethics, license, privacy, disclosure, or release consent is needed;
- unpublished material would leave the local authorized boundary;
- a frozen protocol must change after confirmatory evidence was inspected;
- the test set was exposed and a new selection decision is proposed;
- new paid resources or destructive actions are required;
- final claims, conclusions, submission, or public release need approval.

Do not pause for ordinary reversible choices such as file naming, test
organization, local diagnostics, or choosing between equivalent implementation
details that do not alter the frozen protocol.

## Completion contract

Full-cycle execution is complete only when one of these is true:

- G11 passes with a verified, human-approved submission or archive package;
- the project is honestly killed or deferred with evidence and a reusable record;
- progress is blocked by a documented human-only or external-state dependency.

At every terminal handoff, report scientific validity separately from
engineering readiness, list claim downgrades, identify exact evidence paths, and
provide the command that reproduces the structural status.
