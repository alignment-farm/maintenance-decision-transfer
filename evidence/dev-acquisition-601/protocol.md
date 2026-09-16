# Bounded maintenance decision transfer v1

Frozen before any study model run, 16 September 2026. Development acquisition
601; untouched assessment acquisitions 701 and 702. Every descendant stays in
its acquisition partition. S2's published 401/501/502 are prior development
evidence, not assessment. No seed substitutes. Same task, waiver order and
pinned S2 runtime; this tests initialization/acquisition-order transfer, not a
new task or revision-order transfer.

## Acquisition and resources

Use the S2 256/512/1024 update ladder: earliest >=60/64 acquired and >=28/32
development complete calls. Preserve every failed checkpoint. Both 192-update
first-revision histories proceed without filtering. Maximum three acquisitions
(3,072 updates), 1,152 first-revision and 2,304 second-revision updates. At most
one additional 192-update optimizer-continuation equivalence diagnostic, plus
bounded reload probes. Maximum 6,720 updates; no hyperparameter/seed search.
40 GB MLX peak ceiling, one active hour and two hours waiting per runner;
stop on exhausted acquisition ladder and report condition-level failures.
Expected <12 GB allocation and roughly 45 active minutes overall.

We are running on the Mac Studio itself. Reuse the existing model read-only;
hash-check weights and capture installed packages. Passive process inspection
before loading and every five seconds yields to sibling Python model scripts.
No visible sibling job at preparation. This is local resource coordination,
not an exclusive timing reservation. Do not modify sibling files or processes.

## Observations and final evaluation

The acquired/target identifiers and all sixteen conditions are unchanged.
Original development identities select acquisition readiness only. Acquisitions
use S2's runner, including its 192-order first-revision characterization; these
full characterization outputs are unavailable to the selectors.

Selection panel: all sixteen conditions on `torvek`; sparse direct validation:
eight conditions on `torvek`, indices 0,2,4,6,9,11,13,15 in task.CONDITIONS.
This panel covers both new/earlier waivers, still-ineligible and certified cases,
and both stock values across the panel. Full validation: all sixteen conditions
on `torvek` and `jaspel` (32 calls per candidate). Prefix: 24 of the fixed 192
updates per candidate then sixteen `torvek` calls. No final-test calls are used
for decisions. Pre-update observation: sixteen `torvek` calls scored against
current version 1. All panels are fixed here before development.

Final suite: acquired + target identities + `vornel`, `hespak`, `queldin`,
`zartum` (192 calls), scored against version 2; evaluate each pre-update state
and both endpoints. These fresh identities never select acquisition or action.
Evaluation also reports 64 fresh-identity calls separately. The same templates
and finite conditions are shared, so these are not independent task samples.

## Decisions and expectations

Frozen comparators: constant Novel, constant Bridged, match revision-1 history,
no revision, sparse endpoint validation and full endpoint validation. Endpoint
validation ties choose match-history. Both candidate checkpoints may be retained;
there is no third training run. Retrospective best-of-two is only an oracle bound.

Developed constant: highest development complete score, ties Novel. Simple
history predictor: nearest development acquisition duration, then same prior
support, choosing mean-best endpoint (ties match-history). Duration is legitimate
metadata; seed is never a feature. With one new development acquisition this
deliberately remains a low-capacity history-conditioned mean, not a fitted neural
forecasting model. Pre-observation selector: nearest development vector of sixteen
pre-update correctness indicators, tie prefer same history, then mean endpoint
scores. Prefix selector: fit one affine endpoint-score-on-prefix-score relation
per support on the four development candidate cells, ridge slope regularization
of 1; choose predicted higher endpoint, ties match-history. Freeze coefficients
and choices before assessment. Small calibration is a disclosed limitation.

Expectation from the commission: match-history may weaken on new acquisitions;
observations/prefix may recover value. Neither is assumed. Primary contrast is
selected complete final score per acquisition/history and regret to the two-arm
oracle. Report all endpoints, new obligations, still-valid earlier behavior,
paired unchanged losses and repaired errors. A superseded obligation is excluded
from preservation. No confidence intervals over correlated individual orders.

## Explicit evidence and costs

Retain a keyed table of checked original examples (16 condition keys) and apply
the exact correction examples from each revision, updating changed keys. Entity
invariance and exact four-field addressing are supplied assumptions. Never infer
labels from final evaluation. Assert repeated training evidence agrees and use
the same table on all final cases. Report original evidence scans, correction
scans, overwrites, key reads, serialized bytes and execution time. The table's
engineering and correction authority are investigator supplied. Privileged formal
policy interpretation is prior context only; this table is the serious control.

Deployment costs: fixed/history/pre-observation choice uses 192 revision updates;
prefix uses 216 if optimizer restoration is verified, otherwise 240 restarting;
endpoint validation uses 384. Charge panel calls separately; final evaluation
is investigation-only. Acquisition, earlier history, calibration labels, failed
attempts, fitting, inference tokens/time, updates, storage, audits and explicit
repair are reported separately. No invented scalar conversion or amortization.

Inspect exact primary method versions and pinned implementation before adapting
forecasting; local low-dimensional predictors are controls, not reproductions of
published forecasting models or matrix completion.
