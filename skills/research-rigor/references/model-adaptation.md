# Model and host adaptation

Use when changing models/prompts or diagnosing excessive context, approval
pauses, or unfinished work. Keep research contracts model-neutral.

## Guidance and limits

OpenAI's September 11, 2026 [skills guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
recommends precise descriptions, progressive disclosure, less prescriptive
scaffolding, and explicit completion boundaries. The [GPT-6 guide](https://developers.openai.com/api/docs/guides/latest-model)
addresses unnecessary pauses and conflicting instructions. These motivate the
small entrypoint and conditional protocols here, not weaker evidence standards.

Anthropic's September 22, 2026 [Opus 5.5 announcement](https://www.anthropic.com/claude-opus-5-5)
describes stronger sustained task execution. Applying outcome-oriented design
to it is a portability choice, not an OpenAI recommendation about Claude or a
demonstrated cross-model performance result.

Record actual model ID, reasoning setting, host, tools, and date. A nickname such
as `gpt6h` alone does not establish an API identifier or reasoning parameter.
Preserve the user's configured choice; resolve ambiguity only when actual
selection is needed. Do not switch models or claim runtime testing from format
compatibility alone.

## Give the decision, not an itinerary

Specify goal, evidence, real constraints, and observable completion. Let the
model choose routine details and necessary context. Keep scripts for deterministic
provenance/integrity and repeated transformations, not scientific judgment.

Do not impose fixed numbers of papers, reviewers, agents, retries, or tests as
quality proxies. Honor explicit user requirements. After relevant checks pass,
test further only for a new change, failure, or unresolved scientific concern.

Independent review can expose correlated mistakes when the host/user authorize
delegation. Supply raw artifacts and the question, not a preferred answer. Shared
model agreement is not empirical evidence. If delegation is unavailable, perform
a separate adversarial pass and label its lack of independence; do not block
ordinary work on missing agents.

## Example request contracts

**Scoped revision:** "Revise this section using the attached results. Correct
unsupported wording, reconcile numbers with the facts file, and return the edited
source plus checks. Continue local fixes under the existing scope."

**Full cycle:** "Develop this question within the stated data/compute budget.
Challenge novelty, pilot the full measurement chain, run the justified design,
and produce a verified draft and evidence package. Preserve negative results.
Ask when a missing decision affects the next action; continue other work."

**Review response:** "Analyze original reports against the submitted version.
Fix supported criticisms, execute authorized evidence work, update manuscript
and response together, and verify the local package. Identify missing evidence
rather than substituting a polished assertion."

## Validate after changing models

Use representative cases: narrow edit, adverse result, theorem counterexample,
conflicting handoffs, and missing original reviews. Compare completion, scientific
fidelity, unnecessary pauses, context use, and artifact correctness. Installation
and CLI tests establish portability; they do not predict acceptance or measure
the quality of a model's research behavior.
