# Full-cycle execution

Use for sustained research work, recovery, or experiment repair. For the actual
scientific path choose a relevant [playbook](research-playbooks.md). Use the
[gate reference](stage-gates.md) when operating the bundled controller.

## Scope and completion

`guided` completes the requested unit, including its implementation and
verification. `full-cycle` continues across authorized stages. Neither mode needs
a fresh confirmation for each reversible step. Record the user's existing scope,
budget, data boundary, and completion criteria; do not turn template blanks into
questions whose answers are already in the conversation.

Typical boundaries are a verified experiment, a defensible draft, a complete
revision package, or accepted final files. Preparing a submission does not claim
that an online submission occurred. G11 denotes a verified package/archive;
record portal status separately.

## Recover authoritative state

Inspect the active source and its evidence dependencies, not every historical
note. Resolve conflicts through original artifacts, version identity, timestamps,
and explicit supersession. Keep submitted, working, revised, and accepted copies
distinct. A summary saying "all checks pass" cannot close a newly found defect.

For a controller project:

```text
python "<SKILL_DIR>/scripts/research_cycle.py" status <project>
python "<SKILL_DIR>/scripts/audit_research_state.py" <project>
```

For an existing native workflow, use its equivalent manifests and decision log.
Do not rerun expensive experiments merely to recover their status.

## Continue from evidence

Choose the next action by the uncertainty it resolves. Define its output and
acceptance condition, execute, inspect, and update the durable record. Checkpoint
before expensive/interruption-prone work and after material decisions, rather
than logging each trivial edit.

| Outcome | Continue with |
|---|---|
| Environment fault | Preserve logs/partials; repair and retry the same cell |
| Implementation defect | Quarantine dependent results; reproduce the defect; fix and regenerate from valid upstream data |
| Measurement/protocol defect | Version the amendment; identify exposure and invalidated claims; obtain missing authority; validate the revised inference |
| Valid adverse/null result | Preserve it; fail the unsupported claim; investigate only justified alternatives |
| Missing resource or authority | Record exactly what is missing; continue independent in-scope work |

A changed parser can be an implementation fix or a changed measurement rule;
decide by its effect on inclusion, selection, and inference. Do not label all
undesired outcomes "bugs" or every code fix a new scientific study.

Retain old/new protocol IDs, changed fields, reason, exposure, authorization
basis, affected artifacts, and validation in `04_PROTOCOL_AMENDMENTS.csv` or its
native equivalent. Confirmatory claims selected using test outcomes need fresh
independent evidence. Descriptive reanalysis of existing data is permitted when
labeled; it is not fresh confirmation. The bundled amendment gate conservatively
requires held-out validation for applied measurement amendments; do not mislabel
descriptive analysis to pass it.

## Controller operations

```text
python "<SKILL_DIR>/scripts/init_research_project.py" <project> --mode full-cycle
```

For missing templates in a legacy project, add `--merge`. This preserves populated
state and numeric policies. Migrating a legacy policy is a recorded decision;
never lower it silently after seeing results.

Example checkpoint:

```text
python "<SKILL_DIR>/scripts/research_cycle.py" checkpoint <project> --task-id boundary-pilot --gate G6 --status in_progress --summary "Pilot exposes undefined metric cells" --evidence 04_COVERAGE_MODEL.csv --next-action "Inspect failure causes" --acceptance-condition "Each excluded cell has a reason and a valid denominator rule"
```

Use `transition --help` for a gate decision. Passing requires existing evidence
and a structural audit. Reopen an invalidated earlier gate with
`--status in_progress --reopen-dependent-gates`; this resets dependent statuses
without deleting history. Gate states remain:

`not_started | in_progress | passed | failed | blocked | paused | deferred | killed`

Building a pipeline can finish while its scientific claim remains failed.
Preserve that distinction in handoffs.

## Questions and authority

Use current authorization for analysis, routine implementation choices, drafting
supported interpretations, and narrowing unsupported wording. Authorship, ethics
attestations, spending, disclosure, and external submission need the applicable
authority; ask only if absent or exceeded. A failed hypothesis need not stop all
analysis, and an unknown venue does not prevent venue-independent work.

When the user authorizes exploring replacement ideas, continue after a candidate
fails. Otherwise report failure and prepare concrete alternatives without
silently changing the objective. A historical plan does not authorize spending,
contacting third parties, or uploading unpublished work.

## Handoff

Report the requested outcome/artifacts, what was verified, scientific limits, and
the exact next action if one remains. A completed scope, an evidence-based
killed/deferred direction, and a blocked scope are distinct outcomes; never
describe the last as completed research.
