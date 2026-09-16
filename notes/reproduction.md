# Reproduction

Run from this study on Apple Silicon with 64 GB memory. Use `uv sync --python
3.14.7 --extra adaptation --frozen`. The existing model symlink is ignored by
Git; independent reproduction downloads Qwen/Qwen3-4B-Instruct-2507 revision
`cdbee75f17c01a7cc42f958dc650907174af0554` into `models/qwen3-4b-instruct`.
Required files and hashes are in sources/model-reference.json. Native MLX-LM
revision is `86b48c461feebf87c58788655b7e57b5574b9e6d`; every run verifies model
hashes and records the installed packages before loading. No inference endpoint
can replace this gradient runtime.

Use NEW output directories. These commands run sequentially; never overlap
native model runners, including auditors. All runners yield to observed sibling
model scripts. Timings are observational, not exclusive-device benchmarks.

```sh
uv run --no-sync python scripts/check_instrument.py
uv run --no-sync python scripts/state_support_acquire.py --seeds 601 --output evidence/NEW-dev-acquisition
uv run --no-sync python scripts/decision_experiment.py --start-run evidence/NEW-dev-acquisition --seed 601 --verify-continuation --output evidence/NEW-dev-crossing
uv run --no-sync python scripts/analyze.py --fit evidence/NEW-dev-crossing --output evidence/NEW-predictors.json
```

Commit the developed predictor file before acquiring the two assessment learners.
Do not use the assessment results to change the panel, coefficients or recipe.

```sh
uv run --no-sync python scripts/state_support_acquire.py --seeds 701 702 --output evidence/NEW-assessment-acquisitions
uv run --no-sync python scripts/decision_experiment.py --start-run evidence/NEW-assessment-acquisitions --seed 701 --predictors evidence/NEW-predictors.json --output evidence/NEW-crossing-701
uv run --no-sync python scripts/decision_experiment.py --start-run evidence/NEW-assessment-acquisitions --seed 702 --predictors evidence/NEW-predictors.json --output evidence/NEW-crossing-702
uv run --no-sync python scripts/explicit_evidence.py --output evidence/NEW-explicit
uv run --no-sync python scripts/analyze.py --runs evidence/NEW-dev-crossing evidence/NEW-crossing-701 evidence/NEW-crossing-702 --acquisitions evidence/NEW-dev-acquisition evidence/NEW-assessment-acquisitions --output evidence/NEW-analysis.json
uv run --no-sync python scripts/audit.py --runs evidence/NEW-dev-acquisition evidence/NEW-dev-crossing evidence/NEW-assessment-acquisitions evidence/NEW-crossing-701 evidence/NEW-crossing-702 --output evidence/NEW-audit
```

If an acquisition exhausts its ladder, preserve it and diagnose the saved errors;
do not invoke crossings for absent histories or replace the seed. The frozen
protocol bounds all updates, elapsed time and memory. The optimizer-equivalence
diagnostic compares all endpoint adapter values after disk restoration against
an uninterrupted 192-update path. Audits retokenize all generations and updates,
check paired starts and all schedules, and reload every saved adapter to probe
all sixteen conditions plus otherwise uncovered failed output forms. Audit probes
are verification calls, not additional evaluation samples.

The acquisition runner is copied unchanged from S2 and reads
protocol/state-support-final-v1.md, whose contents are this study's initial
comparison protocol. Its `phase=final` denotes the inherited execution mode,
not this study's development/assessment classification: seed 601 is development;
701 and 702 are assessment. Actual comparison design.json records that distinction.
Historical ancestor metadata in runtime.py does not supersede sources/README.md.
