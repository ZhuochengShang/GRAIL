# tslearn study — RUNBOOK

First **non-Scala, non-geospatial** external baseline. Purpose: show the AIDEAL
workflow transfers to a new codebase with **config + adapter only** (zero
per-repo code edits), and reproduce the doc-effect ladder measured on RDPro.

Everything below runs from `experiments/tslearn/`. Default models are
`google:gemini-3.1-pro-preview` for author/audience/fixer (set in
`configs/aideal.yaml`; override any run with `--role role=provider:model`).
`aideal` here means `PYTHONPATH=../../grail-agent/src python3 -m aideal.cli`.

## 0. One-time setup (Mac)

```bash
cd experiments/tslearn
git clone https://github.com/tslearn-team/tslearn.git
git -C tslearn checkout f8f13ddf4186e2cc99c8ef495aeb46b1254a01f7
python -m pip install -e ./tslearn                       # exact target checkout
export GOOGLE_API_KEY=...                                # gemini key
aideal profile                                           # should show ready:true
```

No dataset download is needed. Both conditions load deterministic small slices
from `tslearn/tslearn/.cached_datasets/Trace.npz`, which is bundled in the target
repository.

Static sanity (no key needed) — verified on the pinned 2026-07-14 checkout
(`f8f13dd`, package version `0.10.0.dev0`):

```bash
aideal api-surface | head -8   # raw public names ≈ 245 (sites ≈ 355)
aideal intent | head -8        # intent-selected = 122 (threshold 5)
```

Cross-check vs the library's own `__all__` (128 exports): overlap 90
(precision 0.73 / recall 0.70). Misses are mostly non-def exports (constants
like `GLOBAL_CONSTRAINT_CODE`), internal mixins, and `_`-prefixed exports —
document this as the static-selection error profile. Docstring coverage
(below-def extraction): 76% of sites. pytest usage examples mined for 116 APIs.

> **2x2 PLAN (2026-07-13):** run the same four-cell table as rdpro —
> A1 = original readme, 0 rounds (`aideal/tsl-a-original`); B1 = original +
> deep-dive fix with `--create-missing` (`aideal/tsl-a-original-fix`, catalog
> starts empty); A2 = generated readme, 0 rounds (`aideal/tsl-b-readme`);
> B2 = A2 + deep-dive fix (same branch). All read the entire flat readme;
> the catalogue arm (old condition C) is postponed. Table:
> `python ../rdpro/compare_2x2.py --a1 ... --a2 ... --b1 ... --b2 ...`.
> Commands below map: §1→A1, §2→A2+B2; B1 mirrors rdpro's B1 block.

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

# 1. comprehension = per-API "LLM run — pass or not" (0 snippet-fix rounds:
#    all iteration budget goes to DOC repair, so attribution stays clean)
aideal comprehension --execute --class-context off --max-fix-rounds 0 \
  > docs/comprehension_B0.json

# 2. ITERATIVE deep-dive doc repair — up to 5 rounds per failing API, each:
#    deep-dive (sees newest failure + current draft) → diagnose → rewrite
#    entry → run the API against the NEW doc (pass-or-not). Rounds must show
#    improved understanding (new diagnosis OR error moved) or the API stops
#    early (--doc-stuck 2). Live log after EVERY round:
#    docs/fix_report_latest.md + per-round audit in docs/docfix_changes/.
aideal fix-docs --from-results docs/comprehension_B0.json \
  --deep-dive-first --doc-rounds 5 --report docs/docfix_B.json

# 3. B's headline number: full pass-or-not run on the repaired doc
aideal comprehension --execute --class-context off --max-fix-rounds 0 \
  > docs/comprehension_B_final.json
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
# (so docfix's single-API runs read index-first too, not just the full runs)
aideal catalogue                                   # per-class index from the doc

aideal comprehension --execute --class-context on --max-fix-rounds 0 \
  > docs/comprehension_C0.json
aideal fix-docs --from-results docs/comprehension_C0.json \
  --deep-dive-first --doc-rounds 5 --report docs/docfix_C.json
aideal comprehension --execute --class-context on --max-fix-rounds 0 \
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
