# Wireless communications, signal processing and optimization

Use for theoretical or computational communication-system studies: channel
models, arrays, beamforming, RF architectures, estimation and constrained
optimization. This playbook is a local synthesis of research failure modes,
not a literature survey or evidence that a particular method is novel.
Check current primary literature and the actual venue rules for each project.

## Start with the engineering decision

Write one question: which feasible design or estimator changes which observable
metric, for which channel/hardware/information regime, after what acquisition
and computation costs? Freeze the strongest intended claim and a cheap falsifier.
Stop or redesign if the method requires unavailable information, an infeasible
hardware operation, or an already-known relation with no new decision value.

| Decision | Decisive work | Evidence to retain |
|---|---|---|
| Does the model represent the system? | Draw signal path and noise insertion; map each matrix dimension, unit, normalization, power/phase constraint and RF loss to code | Diagram–equation–code map; model version |
| What does the method know? | Separate instantaneous CSI, slow statistics, estimated quantities and oracle inputs; define pilot count, noise, stationarity and calibration | Observation/acquisition contract |
| Is the contribution new? | Compare equivalent results under alternate terminology; separate architecture, reused operator and new relation | Source-linked nearest-neighbor delta |
| Is the theorem valid? | Audit support, rank and limiting regime using the cases below; run symbolic/exact checks for decisive obligations | Theorem contract and versioned machine results |
| Is optimization evidence certified? | Distinguish global optimum, relaxation bound, feasible incumbent and local solver output; check original feasibility after projection | Objective/constraint residuals and certificate or explicit absence |
| Are comparisons fair? | Match feasible sets, channel realizations, CSI, tuning access, restarts and termination; record iteration and wall-clock costs | Paired raw results; budget and implementation provenance |
| Does it help after costs? | Separate spectral efficiency, net throughput, energy, training/feedback overhead, RF losses and latency | Metric definition and observed break-even in tested regimes |

## Theory falsification before expensive simulation

For literature-driven ideation, use [literature to idea](literature-to-idea.md):
map the signal path and control locations, solve any conditional digital block,
retain its Gram/power factors, then identify what the changed channel or feasible
set breaks. Distinguish the seed transfer from its new analytical or algorithmic
repair. A trace surrogate is not automatically an exact error/rate objective.

Select cases from the actual claim, not a universal test quota:

- **Rank and transformations:** zero/rank-deficient covariance, repeated
  eigenvalues, overloaded/underloaded systems; distinguish invertible common
  transforms from entrywise weighting. Track numerical threshold sensitivity.
- **Mixed channels:** retain deterministic and random components, their support
  and transform factors. A deterministic gain floor and an outage-probability
  floor are different statements. Check threshold below support and pure limits.
- **Asymptotics:** name the limiting variable and what stays fixed. Separate
  upper bound from two-sided rate; test vanishing leading coefficients and
  singular regimes. Derive limit/interchange conditions rather than infer them
  from matching curves. Low-SNR asymptotics alone do not describe every wideband
  frequency-selective implementation.
- **Surrogates and projections:** verify the identity before and after enforcing
  constraints. A small matrix residual does not automatically certify final
  rate/MSE; derive a transfer statement or directly measure target discrepancy.
- **Estimation:** test identifiability with actual observations before estimator
  design; distinguish configuration count from total samples and acquisition
  time. Separate reconstruction guarantees from decision-task guarantees.

Use [machine verification](machine-theory-verification.md). A verified lemma
does not validate hardware assumptions, novelty or experimental inference.

## Minimal evidence pipeline

First run an exact small case or exhaustive finite feasible oracle independently
of the production approximation. Exercise the full path from generated channel
to solver, feasibility, metric, facts and figure; preserve failed instances.
Then freeze paired comparisons and disclose protocol changes.

Separate architecture baselines, strong algorithm baselines, module ablations,
and diagnostic oracles. A locally constructed comparator is not a reproduced
published baseline. If restarts/tuning change, apply the same comparison policy
to all applicable methods; decompose method changes and budget changes on common
inputs, retaining interactions and unfavorable results.

Vary formerly coupled parameters separately: antennas/RF chains/users, load,
SNR, correlation/rank, estimation error, loss and calibration. Include both sides
of the claimed operating regime. For robustness, compare an aware design, an
agnostic design evaluated under the same mismatch, and a matched baseline;
inspect behavior as well as final performance.

For outage/tail claims retain event counts, denominators, uncertainty and sampling
resolution. Zero observed events does not prove zero probability. Mark exact,
analytical, empirical and extrapolated curve segments separately. Pairing must
follow the realization or independent block in the design; account for dependence.

## Manuscript and repair decisions

Every abstract guarantee points to a theorem contract, every reported gain to
raw paired results and a cost account. Derive tables, figures and prose numbers
from one facts layer. State tested domains and information assumptions alongside
the gain. Distinguish mathematical bound, empirical observation and engineering
prediction in captions.

If the decisive claim fails, choose: narrow conditions, replace the proof,
repair implementation and regenerate affected evidence, or terminate/rebuild.
Do not preserve an attractive headline after the evidence invalidates it. For
revision, retain original review and submitted version, separate reviewer claims
from verified defects, and provide an evidence/location/limitation response.
Use the [general research paths](research-playbooks.md) for revision and handoff.
