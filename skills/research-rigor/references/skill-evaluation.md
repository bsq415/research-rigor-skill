# Paired evaluation of Research Rigor

Use when asked to measure this skill's value or prepare evidence for promotion.
Do not load benchmark answers into ordinary research tasks. If you are a candidate
being evaluated, never read the rubric, other candidates' answers or prior scores.

## What this suite measures

The [task set](../assets/rigor-eval/tasks.json) has 10 synthetic Chinese research
audits: eight flawed claims/designs and two supported controls. The
[rubric](../assets/rigor-eval/rubric.json) freezes four binary scientific criteria
per task and critical failures. It rewards detection, concrete evidence, valid
repair and bounded interpretation. Verbosity and mentioning the skill earn no
credit. Supported controls penalize blanket skepticism.

| Task | Target | Expected disposition |
|---|---|---|
| T01 | Upper bound promoted to two-sided rate/optimality | Revise |
| T02 | Full-data label selection and preprocessing before split | Revise |
| T03 | Universal abstract despite harm, missing coverage and post-hoc selection | Revise |
| T04 | Positive entrywise weights mistaken for invertible common scaling | Revise |
| T05 | Local relaxation solution called a certified upper bound | Revise |
| T06 | Unequal survivor denominators and unsupported missingness assumption | Revise |
| T07 | Update rule confounded with restart budget; incomplete cost account | Revise |
| T08 | AI praise/phase advancement promoted to formal acceptance | Revise |
| T09 | Valid two-sided asymptotic bounds | Support as scoped |
| T10 | Train-only processing and frozen paired test with bounded reporting | Support as scoped |

Public synthetic examples are a development suite, not a representative sample
of research or an unseen benchmark. A result on them cannot establish overall
scientific correctness, acceptance odds, all-domain benefit or superiority to
another model. Add new hidden tasks before a confirmatory follow-up; do not tune
on these responses and call the next run held out.

## Freeze before generation

Use the same model version, reasoning effort, output format/length budget,
tool policy and sampling settings for both conditions. Record defaults when
temperature/seed is not controllable; the plan seed randomizes order only, not
model sampling. Each task/condition/repeat gets a fresh session. Alternate or
randomize condition order to reduce time/order confounding.

The bundled runner evaluates **prompt-only skill augmentation**: baseline gets
a neutral common instruction; treatment also gets an exact frozen snapshot of
`SKILL.md`, theory-and-claim audit and experiment-and-evidence references. It
does not evaluate native automatic skill discovery, SymPy execution, long-term
project completion or the full workflow. Prompt length is part of this treatment;
it is not a token-matched test of the value of content alone. Report token usage
and latency along with quality. A token-matched neutral context arm can be a
separate future experiment; do not add one after seeing outcomes without versioning.

`rigor_eval.py prepare` copies and hashes tasks/rubric/schema/context, freezes
model/effort and a paired run order, and refuses an existing directory. Keep this
directory outside the candidate workspace. Candidates receive only the current
task, common format and assigned context. Answer keys and conditions are never
sent to candidates. Closed-book calls disable host skill discovery, shell and
apps, use an empty temporary directory and ignore user config; record CLI version
and actual flags because host behavior can change. Inspect traces for tools or
unexpected context. The development feature flag is not proof of isolation.

```text
python "<SKILL_DIR>/scripts/rigor_eval.py" prepare <RUN_DIR> --model <MODEL> --effort medium --repeats 1
python "<SKILL_DIR>/scripts/rigor_eval.py" run <RUN_DIR>
python "<SKILL_DIR>/scripts/rigor_eval.py" blind <RUN_DIR>
python "<SKILL_DIR>/scripts/rigor_eval.py" judge <RUN_DIR>
python "<SKILL_DIR>/scripts/rigor_eval.py" summarize <RUN_DIR>
python "<SKILL_DIR>/scripts/rigor_eval.py" export <RUN_DIR> --destination <NEW_EXPORT_DIR>
```

Uses Python standard library and a logged-in Codex CLI. Local CLI help is the
authority for supported flags. `run --limit 2` is an integration check; a later
`run` resumes only unattempted calls. Failed calls remain in the planned
denominator and are never silently retried. Changing model/effort/prompts creates
a new run. The runner retains source prompt hashes, versioned answers, latency,
usage and local event logs. Treat model/tool/schema errors as execution failures,
not scientific wrong answers. Never fabricate outputs to fill missing cells.

For Claude or another host, use the same frozen plan and prompts in independent
isolated sessions and import records matching the response metadata schema.
Record the host/config and do not combine model-specific results into one gain.
No Claude execution is implied by the existence of this suite.

## Scoring sheet and blinding

For each randomized opaque answer ID, grade each of four criteria 0/1 using the
frozen rubric, recording an exact response quote and brief rationale. Grade
semantic correctness; a keyword match cannot establish diagnosis or proof.
Critical failure overrides full-task pass even if other details are correct.
Full pass requires all four criteria, correct disposition, no critical failure.

The runner's independent-context model judge sees task, rubric and a single
answer, but no condition labels, pair mate, run order or aggregate results.
Text may still reveal the condition, so blinding is imperfect. Its evidence
quotes are checked against the answer; this does not establish that its judgment
is correct. Same-model judging is provisional and is not independent expert
review. Audit disagreements, failures and controls manually before stronger
claims. For confirmation, use two blinded domain raters, preserve disagreements,
and adjudicate with the original rubric without changing it to fit outcomes.
The runner schedules two independent judge contexts at a time, in randomized
blind order; candidate generation is sequential in the frozen run order.

The [human scoring sheet](../assets/rigor-eval/human-score-sheet.csv) supports
one row per answer/criterion/rater. Keep the condition key hidden until grades
are locked. Do not coerce a disagreement into agreement or replace provisional
scores without preserving the earlier version.

Report each condition's planned/completed/graded counts, criterion points out
of 40 per repeat, eight-trap detection, two-control acceptance, full-task pass,
critical failures, raw outputs, paired wins/ties/losses, usage and time. Publish
ties, regressions and failed cases. With 10 fixed tasks and one repeat, report
descriptive counts, not a broad effect size or a population confidence interval.
Follow-up repeats are repeated sampling of the same tasks, not independent new
task evidence. Predefine task-level analysis and clustered uncertainty when
the design supports it.

## Evidence-based release

README promotion must link exact task/rubric versions, skill snapshot/hash,
model/host/settings, raw answers, grades, denominators and limitations. If tied,
say no improvement was observed on this suite. If incomplete, say incomplete.
Do not convert passed software tests, a scripted demonstration or one attractive
example into measured model improvement. A demo using O versus Theta must be
labelled as a demonstration and tied to an actual response if it claims real
behavior; do not invent a baseline failure.

Methodology source: [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
on task-specific evaluations, blinded grading and human calibration. The exact
task set, rubric and thresholds here are this project's design choices.
