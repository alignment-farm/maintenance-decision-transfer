# Maintenance decisions across learned histories

**Commissioned 16 September 2026. Prepared for independent execution; no model
experiment has run in this repository.**

Does a simple decision based on known learning history transfer to newly acquired
learners, and do affordable observations of the current learner improve on it
enough to justify their cost?

This is an independent Construct-2 ancillary study. It owns methods, protocols,
implementation, experiments and publication under [AGENTS.md](AGENTS.md).
Procedure retention and revision (S2) remains complete. The root continues to ask
how agents accumulate useful experience across sessions and where it should live;
this bounded maintenance comparison informs that broader question.

## Begin the investigation

Develop and execute a bounded comparison using the established work-order task
and newly acquired learners. Establish whether known history suffices for support
selection, then determine the added value of a small current-state observation
or trial. Compare complete behavior and actual costs, including direct validation
and competent explicit evidence. A transferred fixed rule, a useful observation,
an inadequate action set or a dominant explicit alternative are all informative.
Routine development and execution within this scope are authorized; no further
root permission is needed for ordinary protocol choices or diagnostic repairs.

The investigator chooses the protocol and numerical budget. The starting scope
below is illustrative, not a requirement to implement every predictor or exhaust
a fixed matrix. Close on explanatory progress, a demonstrated limitation or a
concrete resource constraint. A literature-only restatement is not the intended
outcome when a bounded informative comparison is feasible.

## Starting evidence and its limits

Use the published [S2 repository](https://github.com/alignment-farm/procedure-retention-and-revision/tree/3e71eb5f146e6493c60cef26d15d86dedd2249fb)
([local](../procedure-retention-and-revision/README.md)), pinned at
`3e71eb5f146e6493c60cef26d15d86dedd2249fb`. Read its instructions, README,
FINDINGS-STATE-SUPPORT.md, fixed fresh protocol and reproduction guide before
reusing its implementation. Its known Qwen3-4B-Instruct-2507 / native MLX route
establishes complete acquisition and functioning scoped revisions. Verify current
availability; serving access is not gradient access.

The task has sixteen combinations of channel, priority, certification and stock
across entity identities. A five-field proposal determines eligibility,
reservation, shipment, final stock and status. Two certification waivers are
introduced sequentially. Current support is Novel or Bridged, differing in
original acquisition overlap; both learn the newest waiver, but preservation
depends on the inherited state.

| Acquisition and inherited history | Novel support | Bridged support |
|---|---:|---:|
| 401 Novel | 192 | 122 |
| 401 Bridged | 120 | 120 |
| 501 Novel | 192 | 185 |
| 501 Bridged | 120 | 120 |
| 502 Novel | 143 | 133 |
| 502 Bridged | 121 | 145 |

Each endpoint is out of 192. Root recalculation of 2,304 saved endpoint responses
finds that matching current support to recorded revision-1 support totals
912/1,152, equal to selecting the better endpoint after seeing outcomes. Constant
Novel totals 888; constant Bridged 825. This is retrospective and includes selected
diagnostic material. Six states share three acquisitions; they are not six
independent replications. The matching rule is a strong comparator, not a proven
transfer rule. All published material is development evidence for this question.
Oracle matching still leaves 240 failures and does not establish useful maintenance.

Root background: [comparison brief](../../construct-2/notes/MAINTENANCE_COMPARISON.md),
[preparation ledger](../../construct-2/sources/2026-09-16-maintenance-preparation/README.md),
[AD2 expectation](../../construct-2/notes/ADAPTATION_DECISIONS.md).
This README supplies the essential handoff even without the root checkout.

## Comparison and expectation

The root expects some frozen decisions to lose value across materially changed
histories and a small current-state observation to recover some value. This is
untested. A match-history rule remaining competitive would narrow that expectation.
The task is to challenge both explanations, not force a selector win.

Begin with developed constant support, the explicit match-history rule, and a
simple history-conditioned predictor. Acquisition duration and prior support are
legitimate metadata; seed IDs cannot proxy held-out outcomes. Compare added
observations available before revision or after a short candidate trial. Useful
signals must cover newly required and still-valid behavior, not just training loss
or newest-waiver recall. Define observation panels before fresh assessment.

Keep all descendants of one acquisition in the same development/assessment
partition. Fresh identities alone are insufficient. Separately acquired learners
test acquisition transfer; changed revision order is a different contrast to
declare separately if scientifically warranted. Retain failed acquisitions and
imperfect histories rather than silently replacing inconvenient states.

Use sparse and full direct validation as paid alternatives. Sparse endpoint
validation still requires completing candidate training. Prefix prediction
requires calibration of prefix-to-endpoint relationships; a matrix completion
routine cannot supply that extrapolation by itself. A final evaluation suite
must be separate from observations and action-selection validation.

Include no revision with its unmet new obligations and competent explicit access
to the same checked examples and corrections. The prior formal-policy interpreter
receives privileged executable rules; label it accordingly. A compact retained
example table is a serious alternative on sixteen conditions. Disclose its
addressing assumptions and development effort; do not withhold evidence from it
or add irrelevant difficulty to manufacture repayment.

## Closest public methods

- [What Will My Model Forget?, 2402.01865v3](https://arxiv.org/html/2402.01865v3):
  forecasting and prediction-guided replay, including sequential refinement.
- [Low-rank Example Associations, 2406.14026v8](https://arxiv.org/html/2406.14026v8):
  additive, KNN and factorized completion from paid observed forgetting.
  Its actual linked [code release](https://github.com/AuCson/low-rank-forgetting/tree/1128e1fdc83752f7a7f30a0dbd237afac3b97fc0)
  was statically inspected at `1128e1fdc83752f7a7f30a0dbd237afac3b97fc0`.
  `run_matrix_completion.py` samples with replacement by default; account for
  unique observations and repeated work in any adaptation. Released task rows do
  not supply this study's changing histories or counterfactual support outcomes.
- [Smart Predict, then Optimize, 1710.08005v5](https://arxiv.org/html/1710.08005v5),
  §§2–3.1, and [Selecting Computations, 1207.5879v1](https://arxiv.org/html/1207.5879v1),
  §§1–2: prior theory distinguishing prediction fit, action value and observation
  cost. These do not solve missing counterfactual labels or validate a local policy.

Inspect relevant primary methods and pinned code before adaptation. Broad
forecasting or decision-aware prediction is established prior work; the added
question is usefulness across independently acquired histories.

## Resources, sizing and publication

An illustrative scope is four new development acquisitions and four untouched
assessment acquisitions, each with two revision-1 histories and two candidate
second revisions. At published schedules this is 9,216 revision updates plus
acquisition, or 13,312 total with 512-step acquisitions. This is a planning example,
not a required sample count or a timing promise. Choose proportional numerical
limits after checking local feasibility. A large model or hyperparameter campaign
is outside the initial scope.

Maintain separate investigation and deployment accounting. With two 192-update
candidates and 24-update prefixes, keeping the selected prefix and optimizer can
cost 216 updates; restarting costs 240; full candidate training costs 384; fixed
choice costs 192. Verify the actual continuation equivalence. Full validation can
retain its selected checkpoint without a third training run. Count fitting,
calibration, failed attempts, probes, inference, explicit access and repair in
native units. No scalar conversion of tokens, time and correctness is assumed.

Publish a concise FINDINGS.md with methods, preserved original predictions,
development/fresh boundaries, complete outcomes, costs, limitations, reproduction
instructions and identifiable Git revisions. Link it here. No separate manuscript
or elaborate operational reporting layer is required. Publication acceptance,
completion of this bounded phase and resolution of the broader question remain
separate decisions.
