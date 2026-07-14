# tslearn study — RUNBOOK

First **non-Scala, non-geospatial** external baseline. Purpose: show the AIDEAL
workflow transfers to a new codebase with **config + adapter only** (zero
per-repo code edits), and reproduce the doc-effect ladder measured on RDPro.

Everything below runs from `experiments/tslearn/`. Default models are
`google:gemini-3.2-pro-preview` for author/audience/fixer (set in
`configs/aideal.yaml`; override any run with `--role role=provider:model`).
`aideal` here means `PYTHONPATH=../../grail-agent/src python3 -m aideal.cli`.

## 0. One-time setup (Mac)

```bash
cd experiments/tslearn
git clone https://github.com/tslearn-team/tslearn.git   # pinned working copy
pip install tslearn numpy scikit-learn                   # harness imports the lib
export GOOGLE_API_KEY=...                                # gemini key
aideal profile                                           # should show ready:true
```

Static sanity (no key needed) — expected numbers from the 2026-07-13
sandbox validation (tslearn @ 0.9.0 head):

```bash
aideal api-surface | head -8   # raw public names ≈ 245 (sites ≈ 355)
aideal intent | head -8        # intent-selected ≈ 123 (threshold 5)
```

Cross-check vs the library's own `__all__` (128 exports): overlap 90
(precision 0.73 / recall 0.70). Misses are mostly non-def exports (constants
like `GLOBAL_CONSTRAINT_CODE`), internal mixins, and `_`-prefixed exports —
document this as the static-selection error profile. Docstring coverage
(below-def extraction): 76% of sites. pytest usage examples mined for 116 APIs.

## 1. CONDITION A — first baseline: LLM + original repo only  ⟵ branch `aideal/tsl-a-original`

No AIDEAL artifacts at all: the audience model sees the ORIGINAL README/docs
and must call the API cold. This is the "just use the LLM on the original
codebase" floor everything else is measured against.

```bash
aideal comprehension --execute --doc original \
  > docs/comprehension_A_original.json
```

- Pass rate + `docs/fix_report_latest.md` are written automatically.
- Repeat-variance guard: rerun ~3x before trusting small deltas (rdpro: ±2pp).

## 2. CONDITION B — generated README + full fix pipeline (no index)  ⟵ branch `aideal/tsl-b-readme`

B is the COMPLETE flat-readme treatment: author writes the entire doc, then
the fix machinery runs — comprehension's code fix loop (error log feeds every
retry round), then doc-repair with deep-dive. Class-context stays OFF: no
catalogue index in this arm.

```bash
aideal readme --generate --limit 0 --force        # the entire generated doc
# commit here — B and C both branch from THIS state (same doc, same seed)

aideal comprehension --execute --class-context off \
  > docs/comprehension_B0.json                     # pass 0 + code error log
aideal fix-docs --from-results docs/comprehension_B0.json \
  --deep-dive-first --retry-rounds 3 --report docs/docfix_B.json
aideal comprehension --execute --class-context off \
  > docs/comprehension_B_final.json                # B's headline number
aideal fix-report --run docs/comprehension_B_final.json \
  --baseline docs/comprehension_A_original.json
```

B − A = what the full AIDEAL doc pipeline (generation + fix loop + deep-dive
doc-repair) is worth over the raw-LLM floor.

## 3. CONDITION C — B + catalogue index (the ADVANCED step)  ⟵ branch `aideal/tsl-c-catalog`

Identical pipeline to B — generated readme, code fix loop, deep-dive
doc-repair, error log — PLUS the per-class catalogue index built after the
full doc exists, read INDEX-FIRST. Branch from the same post-`readme
--generate` commit as B so the two arms differ ONLY in the index.

```bash
# in configs/aideal.yaml set:  comprehension.class_context: true
# (so docfix's single-API retries read index-first too, not just the full runs)
aideal catalogue                                   # per-class index from the doc

aideal comprehension --execute --class-context on \
  > docs/comprehension_C0.json
aideal fix-docs --from-results docs/comprehension_C0.json \
  --deep-dive-first --retry-rounds 3 --report docs/docfix_C.json
aideal comprehension --execute --class-context on \
  > docs/comprehension_C_final.json                # C's headline number
aideal fix-report --run docs/comprehension_C_final.json \
  --baseline docs/comprehension_B_final.json
```

C − B = the catalogue index's marginal value with everything else held
fixed (this is also the class-context A/B that was never measured on rdpro).

## 5. Hygiene commands

```bash
aideal surface-audit          # catalog entries that are non-public/deselected
aideal fix-report --run <any run json> [--baseline <prev>]   # readable log, any time
```

## Branches (one condition = one branch; see GRAIL/BRANCHING.md)

| branch | condition |
|---|---|
| `aideal/tsl-a-original` | A: pure original repo/README — the LLM-only floor |
| `aideal/tsl-b-readme`   | B: generated README + code fix loop + deep-dive doc-repair + error log (no index) |
| `aideal/tsl-c-catalog`  | C: B + catalogue index, read index-first (ADVANCED; only delta vs B) |

## Gotchas

- Runs are strictly SEQUENTIAL (shared `.aideal_exec` checkpoint + error log).
- `--resume` continues a killed run; the per-API checkpoint costs 0 LLM calls.
- Estimator classes need tiny hyperparameters or fits get slow — the adapter's
  exec_hints already instruct this; if timeouts cluster, drop `--timeout 120`.
- tslearn's optional deps (torch for SoftDTWLossPyTorch, stumpy for
  MatrixProfile) missing → those APIs fail as `infra` and are auto-excluded
  from the doc-quality denominator. `pip install torch stumpy` to score them.
