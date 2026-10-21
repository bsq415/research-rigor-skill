# Research proposals: build, challenge and revise

Use for a PhD/application research proposal (RP), a proposal rebuilt around a
better question, or substantive improvement within an existing direction.
These are de-identified lessons from proposal drafting and executed corrections,
including early claims later overturned by closer reading. They establish a
workflow, not the novelty of a future topic or an application outcome.

## Contents

1. Establish the revision boundary and applicant evidence
2. Find a valuable question and challenge the gap
3. Read sources before relying on them
4. Build the proposal's argument
5. Make the method and evaluation executable
6. Audit guarantees and operational cost when relevant
7. Revise globally and verify the deliverable

## Establish the revision boundary and applicant evidence

Infer the mode from the request and preserve it in the working notes:

| Mode | Keep | Reconsider |
|---|---|---|
| New proposal or authorized rebuild | The researcher's goals, constraints and verified experience | Topic, title, questions, methods and organization when the evidence warrants it |
| Improve without rebuilding | The explicitly protected direction, title, questions or chapter structure | Incorrect claims, weak paragraphs, method details, evaluation and feasibility inside that boundary |
| Focused review or edit | Everything outside the requested scope | The named issue and its dependent statements |

"Optimize as much as possible" does not override "do not rewrite the topic."
A preserved framework permits substantial paragraph replacement and correction
of false claims; it does not require retaining a broken novelty argument. If
the evidence defeats the protected core, state that conflict and finish useful
in-scope corrections before asking whether the topic may change. Permission to
rebuild already authorizes choosing a stronger surviving candidate.

Inspect the actual RP, CV, relevant papers/reports and available resources.
Distinguish a publication, submission, pilot and future plan. Ground personal
fit in an identifiable contribution or demonstrated skill; coauthorship alone
does not establish mastery of every component. Map experience to a work package,
then identify what must be learned. Do not invent access to hardware, data,
supervision or compute. A familiar method is a feasibility asset, not evidence
that its application is important or new.

For an application-specific version, verify the current program's official
instructions: audience, purpose, length, required sections and submission
format. Use university/funder guidance and identifiable researcher-authored
proposal advice for the argument; keep general advice separate from binding
program requirements. If no target is specified, produce a usable master draft
and label that assumption. Do not impose a universal page count or stop the
whole project to obtain an optional institutional preference.

## Find a valuable question and challenge the gap

Use [idea and literature](idea-and-literature.md) for discovery and novelty,
and [literature to idea](literature-to-idea.md) for a concrete technical bridge.
For a rebuild, compare materially different candidates before selecting one.
For a protected direction, search for defensible questions within it.

Build an evidence chain:

`decision need -> observed failure -> mechanism -> closest existing solutions
-> consequential unresolved question -> proposed test`.

External requirements, hardware observations and independent analyses can
support different links. Read a standard's version, definitions, table title,
notes and normative status: an expanded scope does not automatically extend
every old performance table. A draft study assumption is not a binding service
requirement. A benchmark number needs its denominator, operating point and
pipeline stage; failure before a downstream filter is not automatically the
final system failure rate.

Search both recent applications and older methodological ancestry, using
equivalent objects and alternate terminology. A method renamed in a new field
may have a long history elsewhere. Compare the exact information, assumptions,
decision unit, guarantee and costs in the nearest work. Missing abstracts need
another discovery route, not automatic exclusion. Check query construction
against a known relevant source when a search returns suspiciously few hits.

A matrix of checkmarks is a navigation aid. An empty combination of columns
does not establish a contribution. Separate reused architecture, classical
result, domain-specific obstacle and proposed improvement. Ask what the new
combination enables that the strongest existing procedure cannot already do.
Applying a known theorem to a newly named scalar score may be immediate;
power, information requirements, physical constraints or a proved extension
may contain the real question, but each still needs its own evidence.

Write novelty as a bounded finding: which specific question was not found in
which reviewed sources, through what cutoff, with what unresolved neighbors.
Search non-discovery cannot prove universal absence. If a counterexample
appears, retract the defeated claim rather than append another qualifier to
preserve "first." Promote the counterexample to a baseline and reassess whether
a meaningful delta survives. A carefully narrowed question can be useful;
endless qualification cannot rescue a question with no remaining contribution.

## Read sources before relying on them

Default to retrieving permitted primary full texts into an organized local
corpus before substantive citation use. Keep stable identity/version, source,
retrieval date and a local path; a hash helps when versions affect conclusions.
For access-limited material, use an authorized open/author version or request
the user's sign-in when needed, while continuing independent work. Mark missing
full text as unresolved. A replacement must support the same claim, not merely
be downloadable. Never treat local possession as proof of scientific reliability.

Maintain honest reading states: metadata only, abstract screened, named sections
read, or full text read. A keyword hit, truncated extraction or a summary of a
paper is not a full read. Review the assumptions and surrounding argument for
claims about absence, comparisons, guarantees, method dependencies and numbers;
inspect relevant proofs, appendices and experiment settings. For standards,
record the clauses read rather than claiming to read the entire standard.

Honor an explicit requirement to read every cited paper in full. Do not silently
reduce it to abstract screening to save effort, or declare completion while
promised reading remains. Without that requirement, prioritize consequential
sources and disclose the remaining reading depth; no fixed paper quota proves
sufficiency. Preserve the reading queue across interruptions.

Use extraction/OCR as an aid, keeping the primary PDF and page anchors. Check
equations, figures, tables and scanned pages visually when extraction is lossy.
Respect a user's chosen reading medium. For each consequential source, record
what the RP says, what the original supports or contradicts, exact locations,
and the resulting revision. Keep verified corrections distinct from suggestions
still awaiting source checks. Metadata verification establishes identity, not
relevance or claim correctness; see [manuscript checks](manuscript-checks.md).

## Build the proposal's argument

Make the opening understandable on its own: the problem and stakes, the precise
limitation of current work, the proposed idea, why it may work, and what would
count as success. Explain the causal mechanism before listing model names.
Organize related work around competing answers and their assumptions rather
than a chronological catalogue of papers.

Connect each gap to a research question, a hypothesis where appropriate, a
work package, decisive evidence, a resource account and a milestone. The
optional [proposal evidence map](../assets/proposal-evidence-map.md) is useful
when existing notes lack these links; it is not a new controller requirement.

- RQs ask answerable scientific questions, not just name implementation tasks.
- Hypotheses identify a mechanism and a falsifier. Quantitative targets need a
  stated reference setting and planning rationale; they are not completed gains.
- Work packages explain inputs, operations, dependencies and outputs. A later
  package should consume a defined result of an earlier one, not just share its
  vocabulary. Keep a feasible core before optional extensions.
- Evaluation distinguishes success, useful negative findings and redesign.
  A negative result can establish a boundary when the study can identify it;
  "publish negative results" is not a substitute for a valid experiment.
- Timeline duration, calendar dates, quarters, dependencies and milestones must
  agree. Reserve time for data access, validation, writing and integration.
- Risks name a concrete failure, an observable trigger and a feasible fallback;
  the fallback must still address a worthwhile question.

A proposal promises a research program. Separate established facts, preliminary
results, proposed developments and optional extensions throughout; do not give
unproved future contributions the same status as completed prior work. Explain
candidate fit through verified capability and a credible learning plan. Tailor
emphasis to a supervisor's actual research without inventing an endorsement.

## Make the method and evaluation executable

Define the observation model, decision variables, feasible operations and what
information is available at each stage. Explain how measurements reach the
controller, including feedback or labels. Score candidates using quantities
available at that stage; reserve hidden ground truth for final evaluation and
explicit diagnostic oracles. A local optimization result is a comparator or
incumbent, not a global oracle without a certificate.

Inspect the claimed mechanism rather than trusting its name:

- A projection step cannot support a projection-free claim. For a direct
  feasible parameterization, establish boundaries, constraint satisfaction,
  coverage and any excluded boundary cases. Recheck the final feasible output.
- A finite training grid does not by itself support continuous decisions. State
  the interpolation/query mechanism; test off-grid behavior and discretization
  sensitivity. Separate an estimator's error floor from the downstream model.
- Exact model likelihood or diverse samples do not establish calibrated
  uncertainty. Separate the prior from observation conditioning; justify any
  likelihood guidance so the same observation is not counted twice.
- For posterior-assisted decisions, compare with a matched point-estimate
  version and account for sampling cost. If an accelerated/student model changes
  uncertainty or fidelity, measure that loss as well as the speed gain.

Match observations, acquisition energy, training data, tuning and compute
budgets across applicable baselines. Include the closest classical/simple
procedure and the strongest relevant recent alternative. Distinguish extra
information from a better decision rule. Verify a baseline's actual algorithm
before assigning complexity or iteration counts; use matched measured costs
when blanket family-level comparisons are unsupported. Use scenario/site/subject-level data
splits when lower-level samples share their generating environment; define
uncertainty at the independent unit. Report tails and failure regimes when the
decision depends on reliability rather than only average reconstruction error.

Treat latency as a pipeline: acquisition, feedback, inference, physical action
and any settling time, including channel/state aging. A batch-one inference
target does not establish end-to-end real-time operation. Record offline
training/label costs, hardware and update frequency. Start from an affordable
reference regime; mark larger systems and physical trials as conditional on
resources instead of promising unavailable infrastructure.

## Audit guarantees and operational cost when relevant

For a guarantee-bearing proposal, use a compact semantics table. Write the
randomness, population, conditioning, controlled quantity and assumptions in
the mathematical claim, not just the word "guaranteed."

| Claim type | Distinction to preserve |
|---|---|
| Marginal validity | Averaging over fitted data and future observations does not certify every fitted procedure |
| Training-conditional confidence | A high-probability statement over calibration samples requires its own sampling assumptions and a fixed/appropriately selected procedure |
| Per-group validity | A pooled guarantee need not hold in every group; simultaneous high-confidence group certificates need joint confidence accounting |
| Weighted target-population validity | State overlap and conditional-law assumptions; estimated weights need justified error control |
| Dependent observations | Exchangeability, independent sampling and a specific dependence correction are different conditions; thinning alone proves none of them |
| Online long-run control | State feedback availability, timing and noise; an average over time is not an instantaneous probability guarantee |
| Monitoring | An error bound for the monitor does not restore the monitored system's guarantee after arbitrary drift |

State the decision unit and denominator. Per-item, per-event, per-report and
conditional-on-detection errors are different objects. A known-count selection
task may not decide whether any object exists at all. Derive any claimed
equivalence under its stated null rather than carrying it into mixed states.

Audit every attractive sample-size claim for a fixed procedure/population,
group multiplicity, simultaneous confidence, selection/tuning, temporal
dependence, rare-group acquisition and desired tightness or power. Show enough
calculation to reproduce the budget. Minimum sufficient sample size under one
rule is not a universal lower bound or a wall-clock acquisition promise.
Freezing the score/model after looking at certification data requires an
appropriate correction or untouched data. Approximate similarity of groups
does not prove that evidence can be pooled with conditional validity.
When testing a probability guarantee in repeated finite validation sets, account
for estimation noise before classifying an apparent violation as a true failure.

Keep proof, simulation and deployment conclusions separate. A proof covers its
assumptions; simulation checks implementation and tested departures. A
certificate calibrated in a simulator concerns that source population. A field
claim needs representative field evidence or a separately justified transfer
argument. Physical trials may be optional for a methodological thesis while
remaining necessary for its proposed deployment claim. Proxy labels, simulated
labels and verified real outcomes are not interchangeable evidence.

## Revise globally and verify the deliverable

For criticism, separate the observation, possible validity problem, original
evidence and verdict: accept, partly accept, reject with reasons, or unresolved.
Suggestions are hypotheses to check; even a plausible suggested replacement
may remain too broad. Track the decision, manuscript location and residual limit.
Correct valid criticisms without asking again for permission already given.

When a gap or assumption changes, search the whole RP: title/summary, related
work, comparison tables, hypotheses, equations, work packages, expected
contributions, figures, resources and risks. Update the evidence map and reading
ledger too. Fixing one paragraph while retaining a defeated headline is an
incomplete revision. Preserve the original file and make the new canonical
version explicit; paragraph comparisons help for a protected-framework edit.

Use the requested Word/LaTeX workflow and available document tooling. Compile
or render the saved artifact, check citations and equations, and visually inspect
every final page after substantive layout changes. Address overflow, broken
tables, symbols and sparse reference-only pages without shrinking away the
argument. Recheck bibliographic publication versions before application use.
Compilation and polished pages establish artifact usability, not scientific
validity or novelty. Deliver the edited RP plus a concise change/evidence note,
honest reading coverage, remaining scientific limits and any exact missing input.
