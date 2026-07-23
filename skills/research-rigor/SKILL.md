---
name: research-rigor
description: Assist human-led research with evidence-gated workflows for idea selection, literature review, novelty analysis, claim design, theory, experiments, implementation, reproducibility, statistics, writing, visualization, reviewer response, release, and postmortem. Use when a researcher asks Codex, Claude Code, or another Agent Skills-compatible assistant to structure, audit, recover, or support a research project. Keep the researcher in control of questions, methods, decisions, interpretation, authorship, ethics, and conclusions; distinguish engineering readiness from scientific validity and stop at unsupported or human-only decisions.
---

# Research Rigor

Support a researcher-directed project as an evidence-gated assistant. Advance only as far as the current artifacts justify, preserve failed gates as information, and make every paper claim traceable to sealed evidence.

Never present this workflow as an autonomous scientist or a substitute for subject-matter expertise, supervision, peer review, or author accountability. The human research team owns the research question, source selection, methods, approvals, interpretation, claims, authorship, disclosure, and release. Treat model output as untrusted until a qualified person verifies it. Do not promise novelty, correctness, validity, acceptance, or completion.

Support any lifecycle stage the researcher authorizes. For portals, authorship, ethics, confidential disclosure, paid resources, and manual reviewer services, prepare an exact handoff and resume only after the authorized human completes the step.

## Resolve bundled paths on supported hosts

This skill follows the shared Agent Skills directory convention and is intended for both Codex and Claude Code. Treat `<SKILL_DIR>` in commands as the directory containing this `SKILL.md`.

- In Claude Code, `${CLAUDE_SKILL_DIR}` resolves to this directory.
- In Codex, resolve `<SKILL_DIR>` from the loaded skill path before running a bundled script.
- Never assume the skill's `scripts/` directory is inside the research project.
- Ignore host-specific metadata that the current host does not use, such as `agents/openai.yaml` in Claude Code.

## Apply the core contract

- Treat live source artifacts, raw outputs, manifests, and executable checks as more authoritative than notes, handoffs, memory, prose summaries, or draft claims.
- Separate engineering readiness from scientific validity. Passing tests proves that a pipeline runs; it does not prove novelty, fairness, statistical validity, or a paper claim.
- Freeze claims before full experiments and freeze the protocol before touching a locked test set.
- Select models and checkpoints on validation evidence only. Evaluate the locked test set once under the frozen protocol unless an explicit, versioned exception is approved.
- Preserve raw outputs, failures, missingness, interrupted prefixes, configs, seeds, environment details, and hashes. Never convert a partial run into a completed result.
- Bound every claim to its evidence tier. State limitations and contrary results directly.
- Keep private research private. Do not export personal identifiers, local paths, unpublished ideas, exact unpublished results, or project-specific examples into generic artifacts.
- Never silently weaken a gate, change a frozen protocol, substitute a resource, repair observed results, or broaden the authorized scope.

## Start with orientation

1. Re-read the user's exact request and distinguish audit, diagnosis, planning, implementation, writing, review, submission, and full-cycle work.
2. Inspect governing instructions, the actual workspace root, version-control state, authoritative plans, current artifacts, and relevant memory when authorized.
3. Identify the current research stage and the most authoritative file for each frozen decision.
4. Report a compact status snapshot:
   - current stage and gate state;
   - authoritative artifacts;
   - verified evidence;
   - scientific gaps versus engineering gaps;
   - blockers and downgrade status;
   - next justified action.
5. If creating a new governed project, run:

```powershell
python "<SKILL_DIR>/scripts/init_research_project.py" <project-directory>
```

This creates a private-by-default `.research/` control layer. Do not overwrite an existing control layer; use `--merge` only to add missing templates.

Read [stage-gates.md](references/stage-gates.md) before advancing a project. Do not skip a gate because later artifacts already exist.

## Route to the relevant protocol

- For question selection, literature work, novelty, venue fit, or idea freezing, read [idea-and-literature.md](references/idea-and-literature.md).
- For theory, experimental design, implementation, pilots, full runs, statistics, or result interpretation, read [experiment-and-evidence.md](references/experiment-and-evidence.md).
- For drafting, figures, reviewer response, submission, cleanup, or archival, read [paper-review-submission.md](references/paper-review-submission.md).
- For external AI pre-review services that require a person to upload and retrieve a review, read [external-ai-reviewers.md](references/external-ai-reviewers.md).
- For any external release, generic synthesis, anonymization, collaboration, or sensitive source material, read [integrity-and-privacy.md](references/integrity-and-privacy.md).

Read only the references needed for the current phase, but always apply this file and `stage-gates.md`.

## Advance one justified gate at a time

Use these gate states exactly:

`not_started | in_progress | passed | failed | blocked | paused | deferred | killed`

- Mark a gate `passed` only when its required evidence exists and has been checked.
- Mark a scientific contradiction `failed` or `paused`; do not relabel the question to preserve the story.
- Mark missing user authority or unavailable external state `blocked`.
- Mark a viable but currently infeasible direction `deferred`.
- Mark a falsified or non-novel direction `killed`.
- Preserve the reason, evidence paths, decision owner, and next condition in `BLOCKERS.md` or `DECISION_LOG.md`.
- If a later discovery invalidates an earlier gate, reopen the earlier gate and invalidate dependent claims.

Run the state audit after material transitions:

```powershell
python "<SKILL_DIR>/scripts/audit_research_state.py" <project-directory>
```

Do not treat the audit script as a scientific judge. It checks structural integrity; humans and evidence still decide scientific validity.

## Use the execution loop

1. Define the decision-relevant problem and explicit non-claims.
2. Attack novelty and evidence feasibility before implementation.
3. Write a claim-evidence matrix with falsifiers, strong baselines, valid denominators, uncertainty, and kill criteria.
4. Build the smallest complete pipeline and test the most brittle end-to-end path.
5. Freeze protocol, identifiers, splits, metrics, configs, and provenance.
6. Run append-only; verify interrupted prefixes before resuming; never overwrite sealed artifacts.
7. Audit coverage and failure taxonomy before reading headline effects.
8. Produce a sealed result-facts table. Generate tables, figures, and prose from it.
9. Red-team the paper for novelty, soundness, evidence sufficiency, reproducibility, scope, privacy, and venue fit.
10. Build the submission from an isolated source package, render it, inspect it visually, and verify its manifest.

Use external AI reviewers only as an additional, human-operated red-team surface. Never upload a private or unpublished manuscript automatically. Require explicit author approval, check the service's current privacy and data-use terms, hash the exact review copy, preserve the raw review, verify every suggested citation or factual criticism, and route accepted items through the same remediation and no-regression gates.

For a selected artifact directory, create and verify a portable SHA-256 manifest:

```powershell
python "<SKILL_DIR>/scripts/seal_artifacts.py" create <artifact-directory> <manifest.json>
python "<SKILL_DIR>/scripts/seal_artifacts.py" verify <artifact-directory> <manifest.json> --strict
```

Seal only a deliberate package directory, not an entire workspace or dataset tree.

## Stop and ask at real decision boundaries

Pause and request direction when any of these would materially change the research:

- target venue, track, year, authorship, ethics, license, privacy, budget, or release policy is unknown;
- a requested claim requires evidence that is absent or unavailable;
- a frozen prompt, dataset, split, metric, model, theorem assumption, grader, or sampling rule would need to change;
- a test set has been exposed and a new selection decision is proposed;
- the strongest baseline, exact nearest neighbor, or a counterexample defeats the current story;
- proceeding requires new paid resources, external coordination, production changes, or destructive cleanup;
- reviewer requests exceed the paper's supported scope and require a new study;
- private or unpublished content may leave the authorized boundary.

When a scientific gate fails, report the evidence and offer only honest outcomes: redesign as a new protocol, narrow the claim with adequate evidence, defer, or kill. Do not use better wording, more figures, or a small real-data illustration to hide a failed main gate.

## Produce decision-grade handoffs

End substantial work with:

- stage and gate status;
- what was verified versus inferred;
- new or modified artifacts;
- scientific validity and engineering readiness reported separately;
- open blockers and any claim downgrade;
- frozen decisions and prohibited silent substitutions;
- exact next action and acceptance condition;
- commands needed to reproduce or verify.

For a status-only request, do not mutate the project unless the user also asks for changes.

## Protect releases

Before exporting a skill, template, public artifact, anonymized submission, or generic retrospective, run:

```powershell
python "<SKILL_DIR>/scripts/scan_release.py" <release-directory> --generic-release
```

Add `--deny-term` or `--denylist` entries for project names, titles, private paths, distinctive method phrases, and other identifiers. The scan is a guardrail, not proof of anonymity; inspect all findings and perform a human semantic review.

Do not place private denylist values inside a reusable skill or public repository.
