# Complete outcomes

| Phase / seed | History | Support | Complete /192 | New /24 | Earlier /24 | Negative /48 | Fresh /64 | Losses | Repairs |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| development / 601 | novel | none | 168 | 0 | 24 | 48 | 56 | 0 | 0 |
| development / 601 | novel | novel | 144 | 24 | 24 | 0 | 48 | 48 | 0 |
| development / 601 | novel | bridged | 150 | 24 | 19 | 11 | 48 | 42 | 0 |
| development / 601 | bridged | none | 160 | 0 | 16 | 48 | 54 | 0 | 0 |
| development / 601 | bridged | novel | 120 | 24 | 0 | 0 | 40 | 64 | 0 |
| development / 601 | bridged | bridged | 143 | 24 | 23 | 0 | 48 | 49 | 8 |
| assessment / 701 | novel | none | 168 | 0 | 24 | 48 | 56 | 0 | 0 |
| assessment / 701 | novel | novel | 144 | 0 | 0 | 48 | 48 | 24 | 0 |
| assessment / 701 | novel | bridged | 144 | 24 | 24 | 0 | 48 | 48 | 0 |
| assessment / 701 | bridged | none | 168 | 0 | 24 | 48 | 56 | 0 | 0 |
| assessment / 701 | bridged | novel | 120 | 24 | 0 | 0 | 40 | 72 | 0 |
| assessment / 701 | bridged | bridged | 120 | 24 | 0 | 0 | 40 | 72 | 0 |
| assessment / 702 | novel | none | 157 | 0 | 24 | 37 | 52 | 0 | 0 |
| assessment / 702 | novel | novel | 137 | 24 | 16 | 1 | 47 | 44 | 0 |
| assessment / 702 | novel | bridged | 121 | 24 | 0 | 1 | 41 | 60 | 0 |
| assessment / 702 | bridged | none | 168 | 0 | 24 | 48 | 56 | 0 | 0 |
| assessment / 702 | bridged | novel | 120 | 24 | 0 | 0 | 40 | 72 | 0 |
| assessment / 702 | bridged | bridged | 123 | 24 | 0 | 3 | 41 | 69 | 0 |

Losses and repairs concern only obligations unchanged from version 1 to 2.

## Assessment decisions

| Method | 701 Novel | 701 Bridged | 702 Novel | 702 Bridged | Total /768 | Gap to two-support oracle |
|---|---:|---:|---:|---:|---:|---:|
| constant_novel | novel 144 | novel 120 | novel 137 | novel 120 | 521 | 3 |
| constant_bridged | bridged 144 | bridged 120 | bridged 121 | bridged 123 | 508 | 16 |
| match_history | novel 144 | bridged 120 | novel 137 | bridged 123 | 524 | 0 |
| no_revision | none 168 | none 168 | none 157 | none 168 | 661 | -137 |
| developed_constant | bridged 144 | bridged 120 | bridged 121 | bridged 123 | 508 | 16 |
| history_predictor | bridged 144 | bridged 120 | bridged 121 | bridged 123 | 508 | 16 |
| pre_observation | bridged 144 | bridged 120 | bridged 121 | bridged 123 | 508 | 16 |
| prefix_predictor | bridged 144 | bridged 120 | bridged 121 | bridged 123 | 508 | 16 |
| sparse_validation | novel 144 | bridged 120 | novel 137 | bridged 123 | 524 | 0 |
| full_validation | novel 144 | bridged 120 | novel 137 | bridged 123 | 524 | 0 |

| Method | New /96 | Earlier /96 | Negative /192 | Unchanged losses | Repaired errors |
|---|---:|---:|---:|---:|---:|
| constant_novel | 72 | 16 | 49 | 212 | 0 |
| constant_bridged | 96 | 24 | 4 | 249 | 0 |
| match_history | 72 | 16 | 52 | 209 | 0 |
| no_revision | 0 | 96 | 181 | 0 | 0 |
| developed_constant | 96 | 24 | 4 | 249 | 0 |
| history_predictor | 96 | 24 | 4 | 249 | 0 |
| pre_observation | 96 | 24 | 4 | 249 | 0 |
| prefix_predictor | 96 | 24 | 4 | 249 | 0 |
| sparse_validation | 72 | 16 | 52 | 209 | 0 |
| full_validation | 72 | 16 | 52 | 209 | 0 |

The gap is nonnegative regret for support selectors. No revision is outside the two-support action set: a negative gap means it exceeds both trained candidates on aggregate while still missing new obligations.

## Native investigation costs

| Run | Updates | Input / loss tokens | Generations | Prompt / completion tokens | Active seconds | Wait seconds | Peak MLX bytes |
|---|---:|---:|---:|---:|---:|---:|---:|
| evidence/dev-acquisition-601 | 896 | 80122 / 7168 | 640 | 52640 / 5110 | 371.63 | 0.0 | 9614900252 |
| evidence/assessment-acquisitions | 1280 | 114420 / 10240 | 1088 | 89472 / 8691 | 581.91 | 0.0 | 9614900252 |
| development crossing 601 | 960 | 85740 / 7680 | 1376 | 113376 / 10998 | 593.55 | 0.0 | 9614654492 |
| assessment crossing 701 | 768 | 68592 / 6144 | 1376 | 113376 / 11018 | 556.32 | 0.0 | 9614654492 |
| assessment crossing 702 | 768 | 68592 / 6144 | 1376 | 113376 / 11019 | 555.37 | 0.0 | 9614654492 |

Audit probes, deterministic explicit-table costs and prior S2 development evidence are separate.

Detailed per-policy deployment token, update, observation and use costs are in the JSON ledger.
A selected prefix retains its optimizer; endpoint validation retains its chosen endpoint.
Final evaluation calls are investigation costs; the same calls provide an illustrative 192-order deployment use workload.
