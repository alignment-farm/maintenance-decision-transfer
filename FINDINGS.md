# Matching history transfers as a selector, but does not maintain the procedure

**Bounded comparison and verification completed 16 September 2026.**

The fixed match-history rule selects **524/768 complete work orders** across four
histories from two fresh acquisitions, equal to the retrospective best-of-two
support bound. Sparse and full-condition endpoint validation make the same choices
and add no aggregate correctness. Nevertheless, every fresh endpoint is incomplete;
the bound leaves 244 failures. Matching history also misses 24 newest obligations
in a tied cell. The retained-example table completes **192/192** orders using
16 condition keys, with explicit addressing and entity-invariance assumptions.
This bounded phase establishes an inadequate neural action set and a strong
explicit alternative, rather than a useful observation-based selector.

The original expectation was that a fixed history rule might lose value and a
small observation might recover it. The fresh aggregate results do not support
that expectation for these controls. They do not establish that current-state
observations are generally uninformative.

The [protocol](protocol/comparison-v1.md) was fixed at `2d80a3b` before any model
run. Development acquisition 601 and its descendants are separate from assessment
acquisitions 701/702. No seed is replaced. S2's published 401/501/502 results are
prior development information; no S2 adapter is reused. Native MLX trains newly
initialized eight-layer, rank-eight LoRA adapters on the pinned
Qwen3-4B-Instruct-2507 base, using the inherited AdamW/CE recipe and 192 updates
per revision. Model hashes, actual updates, frozen-base invariants and saved
optimizer continuation are checked. Immediate S2 source provenance is commit
`3e71eb5f146e6493c60cef26d15d86dedd2249fb`; [sources](sources/README.md) and
[primary-method contact](notes/methods.md) distinguish inspection from reproduction.

Acquisition 601 fails at 256 updates (58/64 original, 28/32 development complete
orders), then passes at 512 (64/64, 32/32). Its failed checkpoint is preserved;
the missing shipments disappear under the prespecified continuation. Both fresh
acquisitions pass at 256 with 64/64 and 32/32. First-revision Novel/Bridged scores
are 192/184 in development, 192/192 for 701 and 181/192 for 702. The imperfect
histories are retained. Seed 702's eleven errors falsely waive certification on
unchanged boundary cases. Acquisition duration changes alongside initialization
and shuffle order; this is not an isolated causal intervention on duration.

Every candidate starts from the same saved first-revision weights within its
history. Novel and Bridged support differ in original-acquisition identity overlap,
not labels, condition order or update count. They do not denote globally unseen
identities at revision 2. Pre-observation uses all sixteen conditions on one fixed
identity; prefix trials use 24 updates and that panel; sparse validation uses eight
conditions; full-condition validation uses sixteen conditions on two identities.
The 192-order final suite uses eight familiar and four fresh identities, disjoint
from selection-panel identities. All decisions are recorded before the relevant
final evaluation. Full characterization outputs are unavailable to selectors.

| Fresh acquisition | First-revision history | No revision | Novel support | Bridged support |
|---|---|---:|---:|---:|
| 701 | Novel | 168 | 144 | 144 |
| 701 | Bridged | 168 | 120 | 120 |
| 702 | Novel | 157 | 137 | 121 |
| 702 | Bridged | 168 | 120 | 123 |

Each entry is out of 192. Development's NN/NB/BN/BB outcomes are 144/150/120/143;
they are excluded from the fresh totals. Full condition, component, familiar/fresh,
loss and repair counts appear in [tables](evidence/tables.md) and the independently
rescored [ledger](evidence/final-analysis.json).

| Frozen decision | Complete /768 | New obligations /96 | Previously correct unchanged orders lost |
|---|---:|---:|---:|
| Match-history | 524 | 72 | 209 |
| Constant Novel | 521 | 72 | 212 |
| Constant Bridged | 508 | 96 | 249 |
| Developed constant / history predictor / pre-observation / prefix predictor | 508 | 96 | 249 |
| Sparse or full-condition endpoint validation | 524 | 72 | 209 |
| No revision | 661 | 0 | 0 |

No fresh candidate repairs any of the eleven existing errors. Matching history
retains only 16/96 earlier-waiver obligations. No revision has a higher aggregate
score but leaves every newest obligation unmet; it is not successful maintenance.
Superseded obligations are excluded from unchanged-loss counts.

The tie in 701's Novel history is consequential. Novel support fails both waiver
scopes (0/24 each) while preserving all 48 still-ineligible orders. Bridged support
learns both waivers (24/24 each) but wrongly waives all 48 still-ineligible orders.
Both score 144. The newest-waiver failure is visible on validation (0/4 versus
4/4) but aggregate validation ties and follows the frozen match-history tie-break.
Choosing Bridged in this tied cell would fulfill the new obligation without changing
the aggregate score; both endpoints still fail other duties. Zero aggregate regret
does not certify maintenance. This cell fails current acquisition as well as losing
earlier behavior: the paired alternative and the other history's Novel-support
cell establish that the supplied evidence and runtime can acquire the new waiver.
The internal cause of the failure is unresolved.

The [development decision](notes/development-decision.md), coefficients and source
manifest were frozen at `735f941` before fresh acquisition. Both development
histories favor Bridged, making the fitted history and nearest-pre-observation
controls constant. The fitted prefix predictor also chooses Bridged over its entire
possible input range. Raw prefix ranking already reverses relative to endpoint
ranking in one development history. These are preserved unsuccessful attempts
to obtain informative selectors. One development acquisition supplies very little
calibration diversity; their fresh equality with constant Bridged cannot measure
the potential information value of observations. Paid validation does contain
obligation-level warnings even though it adds no aggregate selection value here.

The explicit control retains checked original examples and overwrites the two
changed condition keys at each revision. It scans 64 original records and 64
correction records per revision, stores a 757-byte serialized table, and performs
192 key reads. All 48 version/condition checks and all 192 final orders pass.
It receives structured fields and investigator-supplied entity invariance, exact
addressing and correction authority. Labels come from the same checked evidence
available to training; it needs no executable policy at use time. Construction and
checked-use times are about 0.00046 and 0.00068 seconds, respectively, including
the disclosed operations, not an isolated timing benchmark. Programmer effort is
not priced. This is a serious finite-task alternative, not a claim about arbitrary
unstructured tasks. [Evidence and costs](evidence/explicit-v1/report.json),
[independent checks](evidence/explicit-audit.json).

Per deployed second revision, fixed/history choice uses 192 updates and no new
observation calls. The attempted pre-observation pipeline adds 16 calls; prefix
selection uses 216 updates and 32 calls. Disk restoration of the 24-update prefix
and AdamW state exactly matches uninterrupted training in the prespecified extra
192-update diagnostic. Sparse/full validation uses 384 updates and 16/64 calls,
retaining the chosen endpoint. These are additional to acquisition and the first
revision. The fitted selectors' known constant behavior can be simplified to
Bridged with no observations; their nominal observation costs are unnecessary for
their actual decisions. Fitting takes 0.0447 seconds after calibration acquisition,
training and labels have already been paid for. [Cost interpretation](notes/cost-interpretation.md)
separates historical S2 evidence, calibration, model use, repair and investigation.

Actual investigation uses **4,672 updates and 5,856 generations**: 417,466 training
input tokens, 37,376 loss tokens, 482,240 generation prompt tokens and 46,836
completion tokens. Active model-run time is 2,658.78 seconds (44.31 minutes), with
zero recorded shared-resource waits and peak MLX allocation 9,614,900,252 bytes.
Saved adapters and optimizer states total 152,247,226 bytes. The 192-update
continuation diagnostic and failed readiness attempt are included; reload audits
are additional. They retokenize/check every response and update, verify schedules
and paired restores, and reproduce 546 probes across all 34 saved adapters in
separate processes. Audits add 44,965 prompt tokens, 4,407 completion tokens and
183.28 seconds, with no waits; those probes are not new accuracy samples. The
[phase audit](evidence/phase-audit.json) reconciles all runs and checks the frozen
predictor against its pre-assessment Git version. All 288 output-field mutation
checks, schedule checks and panel-boundary checks pass. Limits were 6,720 updates,
one active hour per runner and 40 GB
MLX allocation. No new model download, paid experimental model API call or sibling
modification was required. Assistant orchestration and engineering are not assigned
invented dollar costs.

These are two independent adapter acquisitions on one base, one finite task and
one revision order. Descendant histories and individual orders are correlated;
no population confidence interval or p-value is claimed. The matching rule reaches
the two-action aggregate bound in this assessment, while the bound itself is poor.
The bounded phase closes on that demonstrated limitation and the working explicit
alternative, without expanding training to seek a neural win. Broader theory,
publication acceptance and general maintenance remain separate questions.

Reproduce using [the sequential commands](notes/reproduction.md). Every model run
preserves exact sources, protocol, revision, updates, responses, checkpoints and
hashes. Experimental evidence and rescoring were committed at `340688f`; the final
audit is recorded in evidence/phase-audit.json and its referenced run manifests.
