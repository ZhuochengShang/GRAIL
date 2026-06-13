# AIDEAL Bare Testbed

A deliberately LLM-hostile library (`barelib`) with **nothing**: cryptic
function names (`gmk`, `apx`, `zst`, ...), no docstrings, no README, no
aliases, terse errors (`ValueError("bad")`), no error log, no tasks, no
project profile. The library itself works — `tests/test_barelib.py` proves it
— so every failure in experiments is attributable to *usability*, not bugs.

Purpose: build up each LLM-ready asset ONE STAGE AT A TIME and quantify the
effect of each on the readiness score. This is the controlled companion to
the RDPro/GRAIL study.

## Setup

```bash
pip install -e ../../grail-agent   # provides `aideal`
pip install pytest && pytest tests/                            # ground truth: must pass
export OPENAI_API_KEY=...
cd experiments/testbed
alias aideal='python -m aideal.cli --config configs/aideal.yaml'
```

## Build-up protocol (measure after every stage)

| Stage | Action | What it adds | Measure |
|---|---|---|---|
| 0 | nothing (baseline) | — | `python runner/puzzle_runner.py --num-puzzles 10` → source-only readiness score |
| 1 | `aideal init` + fill profile; write 2–3 human tasks | intake + gold tasks | profile ready; tasks runnable |
| 2 | `aideal readme` then `aideal readme --generate` | LLM_readme.md | `form`, `completeness`, `comprehension` scores; rerun puzzles (now readme mode) |
| 3 | `aideal tasks --generate 5` | synthetic tasks | human vs generated pass rate |
| 4 | `aideal alias-suggest` → implement top aliases in `barelib/aliases.py` → `aideal alias-add` | alias layer | rerun puzzles; alias histogram |
| 5 | accumulate failures → `aideal notes-distill` | notes_to_self + error log | rerun puzzles WITH fix loop (`aideal puzzle`); delta from hints |
| 6 | improve error messages in a `barelib/errors.py` wrapper | augmented errors | retry-to-success turns |

Keep `--seed 42` fixed: every stage faces the identical puzzles. Record each
stage's `readiness_score` (and tokens) — the resulting curve "score vs. stage"
is the core quantified result.

## Layout

```
barelib/            the hostile library (do not improve directly!)
tests/              ground-truth tests (must always pass)
configs/aideal.yaml single config; configs/integration_tasks.yaml starts empty
prompts/            prompt templates (copied from grail-agent; swap for ablations)
runner/puzzle_runner.py  executes generated Python, scores, logs failures,
                         honors PUZZLE_HINTS for the fix loop
docs/ aliases/ logs/     created by the pipeline as stages progress
outputs/                 puzzle reports per run
```

## Notes

- The runner auto-detects mode: no `docs/LLM_readme.md` → model sees raw
  source only (stage 0); readme present → model sees doc entries.
- Puzzle failures append structured records to `logs/error_log.jsonl`
  automatically — `alias-suggest` and `notes-distill` run on real data.
- Pure Python: no Spark, no conda env, fast iteration.
