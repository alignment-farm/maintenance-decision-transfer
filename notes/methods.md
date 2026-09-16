# Primary-method contact, 16 September 2026

Inspected exact HTML versions, cached under `.cache/primary`, with SHA256 pins
in sources/methods/manifest.json. These are source retrievals, not arXiv discovery
queries. No discovery API request was needed.

- Jin and Ren, [2402.01865v3](https://arxiv.org/html/2402.01865v3), §§2–3:
  forecasting uses paid refinement outcomes and upstream forgetting labels.
  Frequency priors, learned logit transfer and representation interactions are
  distinct predictors. The reported effectiveness of representation forecasting
  and replay is author-reported; no local reproduction is claimed. Our history
  mean and sixteen-bit nearest-state controls are much smaller, with explicit
  acquisition-level partitioning.
- Jin et al., [2406.14026v8](https://arxiv.org/html/2406.14026v8), §§3–4:
  additive, factorized and KNN completion use observed entries from a new task
  row. Observed forgetting is a paid input. Completion across examples and
  extrapolation from an early prefix to a later endpoint are different operations.
  We use a separate calibrated affine prefix predictor, not matrix completion.
- Statically inspected `run_matrix_completion.py` from
  AuCson/low-rank-forgetting commit
  `1128e1fdc83752f7a7f30a0dbd237afac3b97fc0`, especially `create_masked_arr`,
  `evaluate_for_all_ocl_ds`, `matrix_factorization_direct`, and CLI setup.
  `rng.choice(..., rand_k)` permits replacement; duplicate draws consume work
  without distinct labels. Our deterministic panels have no duplicate cases.
  The copied file is reference-only and is never imported or executed.
- Elmachtoub and Grigas,
  [1710.08005v5](https://arxiv.org/html/1710.08005v5), §§2–3.1, distinguishes
  prediction error from decision cost. We report selected action correctness and
  regret to the two-candidate bound; we do not implement the SPO surrogate.
- Hay et al., [1207.5879v1](https://arxiv.org/html/1207.5879v1), §§1–2,
  treats computation as a costly decision. We expose native observation and
  training costs without inventing a scalar utility or claiming optimal stopping.

This is a local maintenance comparison, not a novelty claim for forecasting,
decision-aware learning, replay, or evidence tables. Exact author code was
inspected where closest to the paid-observation design; the paper's model-scale
performance results are not local experimental evidence.
