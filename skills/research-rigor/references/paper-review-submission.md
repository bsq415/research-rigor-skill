# Paper writing, audit and submission

Write from audited evidence. Preserve the distinction between an executable package, a scientific claim, a local submission bundle and the venue's actual decision.

## Build the argument from facts

Start with a one-page argument: question, closest work, precise contribution, evidence, non-claims and limitations. Map manuscript statements to `03_CLAIM_EVIDENCE_MATRIX.csv` and sealed `06_RESULT_FACTS.csv` fact IDs, versions and denominators. State uncertainty, failures, missingness and contrary outcomes. Do not upgrade empirical behavior to universal guarantees or an upper bound to tightness. Use [theory audit](theory-and-claim-audit.md) for theorem-bearing prose.

Separate confirmatory and exploratory work. Preserve frozen comparisons, baselines, resource budgets and protocol amendments. Abstract, introduction, theorem statements, figures, tables, conclusion and response must share the same claim boundary. A weak result requires narrowing or new valid evidence, not inflated prose.

## Generate tables and figures

Generate from canonical data/code with input hashes, environment and configuration. Record fact IDs and final artifact hashes in `07_FIGURE_AUDIT.csv`; use [figure integrity guidance](figures-and-layout.md) when applicable. A figure from another data version invalidates its linked statement even if it looks plausible.

Keep units, directions, sample sizes, denominators, uncertainty and unavailable cells explicit. Do not bold a winner when budgets, metrics or statistical support are incompatible. Do not turn missing/failed runs into zero or silently omit them.

Inspect actual column width and final-size panels, typography, legend/axis consistency, vector fonts and raster resolution. Show honest ranges and failures; justify log scales or truncation, retain raw curves and disclose aggregation. Never smooth or reshape a convergence curve to match an expected story.

## Audit the whole manuscript

Use `07_MANUSCRIPT_AUDIT.csv`: finding ID, severity, source/version, location, affected claim, evidence, correction, disposition and regression check. Open fatal/major findings block G9. Check theory domain, notation, novelty, baseline fidelity, measurement, leakage, denominators, statistics, units, citations, wording, reproducibility, privacy, disclosure and venue requirements.

Use [manuscript checks](manuscript-checks.md) for citation metadata and explicitly mapped numeric literals. A database match is not primary-text verification, and a matching literal is not a valid inference. Macro-generated text, plotted numbers and rendered pages need additional checks. Structural audit passes do not resolve semantic findings.

Use [reviewer red-team](reviewer-red-team-and-resubmission.md) for adversarial review and formal point-by-point revisions. Distinguish real reports from AI pre-review; retain original sources and exact reviewed versions. Resolve upstream scientific problems across every dependent manuscript surface.

## Build, render and package

Build from an isolated copy of the intended source package, retaining source hashes, environment, compilation logs and warnings. Reconcile citations, labels, cross-references, unresolved references, page limits and included assets. Inspect every rendered page, including supplements and response documents; compilation success alone is insufficient.

Keep clean and marked versions aligned with the exact previously submitted baseline. Record how the diff was produced. Audit file paths, author identity requirements, metadata, comments, tracked changes, private notes, acknowledgments and embedded data. Only human-confirmed declarations may appear in external forms or letters.

Run the existing state/revision/privacy audits for the selected workflow and preserve their reports. Create a deliberate dedicated artifact package with `seal_artifacts.py create`, then `verify --strict`. The manifest checks bytes and completeness, not scientific validity. A registered Claude plugin guard can block subsequent tool edits; see host setup documentation. It does not make files immutable outside the host.

Record the exact manuscript, supplement, response, cover, data/code release and upload field mapping in the release checklist. The authorized human controls submission, required policy attestations and dissemination. A locally prepared package is not proof that the portal received it; record actual receipt and later decisions separately.

## Accepted papers and archives

Freeze scientific results after acceptance. Regenerate publication graphics only from unchanged canonical data and document rendering changes; changes to data, topology, method or conclusions are substantive. Escalate material errors through the authorized authors/editor correction process. Proofs, license choices, copyright and publication records remain distinct from acceptance.

Archive source, environment, data access policy, code, manifests, fact tables, rendered outputs, decision provenance and released versions. Verify the archive before any cleanup. Obtain authorization for material deletions and preserve failed or invalidated runs with their status. The archive must reconstruct which inputs support which claim and what was actually submitted or published.
