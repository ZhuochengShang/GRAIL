# RDPro AIDEAL puzzle experiment

This experiment separates three artifacts that must remain frozen across an
ablation: the test bank, the sample-data manifest, and the selected plan. The
plan records case IDs plus SHA-256 hashes for every fixture and shapefile
companion. Reuse one plan for every documentation, memory, model, or backend
condition.

## 1. Activate the clean implementation

```bash
cd /path/to/GRAIL/experiments/rdpro
export PYTHONPATH="$PWD/../../grail-agent/src"
```

The RDPro/Beast distribution selected by `puzzle.runner_args` must exist before
a compile/run experiment. `puzzle-plan` and `puzzle --dry-run` need no model or
Spark process. This workstation's upstream documentation path is pinned in the
RDPro config; on another machine, use `--api-doc` with a frozen text snapshot.

## 2. Freeze the test cases and fixture bytes once

```bash
python -m aideal.cli --config configs/aideal.yaml puzzle-plan \
  --mode composition \
  --seed 42 \
  --out docs/puzzle_plan_composition_seed42.json
```

For discovery, freeze a separate plan because the prompt intentionally hides
the candidate API names:

```bash
python -m aideal.cli --config configs/aideal.yaml puzzle-plan \
  --mode discovery \
  --seed 42 \
  --out docs/puzzle_plan_discovery_seed42.json
```

Use `--case CASE_ID` repeatedly or `--sample N` when a smaller pilot is needed.
Never resample between ablation arms.

## 3. Smoke-test prompts without spending model tokens

```bash
python -m aideal.cli --config configs/aideal.yaml puzzle \
  --plan docs/puzzle_plan_composition_seed42.json \
  --doc aideal \
  --memory off \
  --tag smoke_generated \
  --dry-run
```

## 4. Documentation ablation

Freeze the initial and repaired generated files before running either arm.
Then use the same plan, model, backend, and repair budget:

```bash
python -m aideal.cli --config configs/aideal.yaml puzzle \
  --plan docs/puzzle_plan_composition_seed42.json \
  --doc original \
  --tag docs_original

python -m aideal.cli --config configs/aideal.yaml puzzle \
  --plan docs/puzzle_plan_composition_seed42.json \
  --api-doc docs/LLM_readme.initial.md \
  --tag docs_generated_initial

python -m aideal.cli --config configs/aideal.yaml puzzle \
  --plan docs/puzzle_plan_composition_seed42.json \
  --api-doc docs/LLM_readme.repaired.md \
  --tag docs_generated_repaired
```

## 5. Backend/alias ablation

Run the same frozen plan first with `configs/aideal.yaml` and then with
`configs/aideal.puzzle_alias.yaml`. The overlay changes only
`puzzle.runner_args --rdpro-lib-dir`. Do not change the task bank to mention aliases
for the upstream condition. If testing alias discovery, add a second bank
version and report it as a separate intervention.

Error-memory is independently ablated with `--memory off` versus
`--memory on`. Do not silently enable memory only for later documentation arms.

## 6. Interpretation

The report distinguishes:

- agent execution success;
- required exact-API coverage in composition mode;
- required output existence;
- semantic status.

An execution pass is not a semantic pass. Add a frozen Python/GDAL oracle to a
case before making a correctness claim, and report prepared demonstrations
separately from on-the-fly puzzle generation.
