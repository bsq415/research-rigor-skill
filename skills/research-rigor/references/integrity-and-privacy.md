# Integrity and Privacy Protocol

## Contents

1. Evidence integrity
2. Private-by-default handling
3. Generic synthesis
4. Release review
5. Memory and handoff hygiene

## Evidence integrity

- Never fabricate a source, result, run, baseline, proof, review, or deployment.
- Preserve failures, missingness, partial states, and contradictory evidence.
- Keep source artifacts immutable after sealing.
- Require an explicit provenance chain for derived tables, figures, and prose.
- Distinguish observation, inference, hypothesis, and recommendation.
- Label memory-derived or stale information and verify it when drift is plausible.
- Do not treat a test suite, polished manuscript, or large workload as proof of scientific validity.

## Private-by-default handling

Classify each source and output:

- `private`: personal, unpublished, confidential, locally identifying, or restricted;
- `internal`: shareable only inside the authorized team or environment;
- `public`: explicitly cleared for release.

Default an unknown research project to `private`. Keep secrets and credentials out of notes, logs, prompts, manifests, and memory. Never store transient access addresses or tokens as research evidence.

Before using external tools or collaborators, confirm that the source material is allowed to leave the local boundary.

## Generic synthesis

When converting private experience into a reusable skill, template, or lesson:

1. extract the process pattern, failure mode, decision rule, and acceptance gate;
2. remove names, usernames, affiliations, contact details, account identifiers, and local paths;
3. remove project names, paper titles, distinctive method names, unpublished equations, exact experimental settings, exact results, and unique dataset combinations;
4. replace examples with domain-neutral placeholders;
5. avoid phrases that allow reverse identification through search;
6. keep private denylist terms outside the reusable artifact;
7. review whether combined harmless details could re-identify the source project.

Do not include a private case study merely because the individual facts are not secret. The combination may disclose the paper.

## Release review

Run the scanner with a private denylist:

```powershell
python "<SKILL_DIR>/scripts/scan_release.py" <release-path> --generic-release --denylist <private-denylist.txt>
```

Use `--deny-case-term` for a case-sensitive acronym that would otherwise match an ordinary word.

The scanner must:

- report file, line, and finding category;
- redact the matched value in its own output;
- return nonzero when findings remain;
- avoid certifying anonymity.

Then perform semantic review:

- Can the output identify a person, institution, account, machine, or project?
- Does it reveal an unpublished question, method, result, dataset combination, theorem, or review history?
- Does it contain a local path, email, ORCID, IP, repository URL, cloud resource ID, or hidden metadata?
- Can a distinctive phrase be searched to find the source paper?
- Does a generated document retain author metadata, comments, tracked changes, or embedded file paths?

Release only after both mechanical and semantic review pass.

## Memory and handoff hygiene

Store durable project decisions and state, not full transcripts or secrets. For a research project, preserve:

- goal and core question;
- current stage;
- authoritative artifacts;
- frozen decisions and protocol version;
- verified findings and limitations;
- blockers and stop rules;
- next acceptance gate.

When creating a public or generic artifact from memory, re-open the live source if accuracy matters and apply the same privacy transformation as for raw project files.
