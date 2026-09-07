# RDPro shared-88 unattended experiment

This coordinator completes the comparable RDPro 2x2 without changing the
historical dirty worktrees and without silently starting paid model calls.

## Frozen protocol

- Upstream: Beast `beast-0.10.1` at
  `547f7f912131a8032f6b5d26991415a5faf05cef`.
- Denominator: all 88 names in `docs/api_manifest_shared.json`; inventory hash
  `1dc1f1c758ae9829c2654e853899603f12f1d7174afdfeffd9edd1f29dde14e1`.
- Documentation exposure: deterministic `relevant` scope in every cell.
- Final measurement: `--max-fix-rounds 0`; no snippet repair is credited.
- A1: validated reuse of the already-complete 88-API original-doc result.
- A2: fresh generated-doc zero-round result on the same 88 APIs.
- B1: deep repair from A1 failures, with a deliberately empty generated
  catalog and `--create-missing`, then a fresh original+generated zero-round run.
- B2: deep repair from the new matched A2 result, then a fresh generated-doc
  zero-round run.

## Isolation and flow

```text
A1 PASS_TO_PASS -> validate/copy historical A1 -> checkpoint push -> failure analysis -> PASS_TO_PASS -> push A1
                                      |
                                      v
B1 PASS_TO_PASS -> empty catalog -> repair/checkpoint push -> zero88 -> analysis -> PASS_TO_PASS -> push B1

A2 PASS_TO_PASS -> fresh zero88 -> checkpoint push -> failure analysis -> PASS_TO_PASS -> push A2
                         |
                         v
B2 PASS_TO_PASS -> copy exact A2 baseline -> repair/checkpoint push -> zero88 -> analysis -> PASS_TO_PASS -> push B2
```

The watchdog runs at most two RDPro jobs concurrently. All Google calls share
one file-locked four-second rate gate, a 300-second request timeout, and eight
provider retries. AIDEAL writes a fingerprinted checkpoint after each API;
docfix writes its report after each repair round. Restarting the same watchdog
resumes these checkpoints. `caffeinate` keeps the Mac awake while it runs.

## Branches and worktrees

| Cell | Branch | Worktree |
|---|---|---|
| A1 | `aideal/rdpro-final-a1-shared88` | `GRAIL_rdpro_final_A1` |
| A2 | `aideal/rdpro-final-a2-shared88` | `GRAIL_rdpro_final_A2` |
| B1 | `aideal/rdpro-final-b1-shared88` | `GRAIL_rdpro_final_B1` |
| B2 | `aideal/rdpro-final-b2-shared88` | `GRAIL_rdpro_final_B2` |

Each branch gets its own Beast clone, execution/output directory, error log,
comprehension checkpoint, upstream test evidence, result, repair evidence, and
per-function failure analysis. Both matched baselines and repair completion are
committed and pushed before a downstream cell consumes them; the finalized cell
is committed and pushed again only after both upstream gates pass.

## Commands

Read-only inspection:

```bash
PYTHONPATH=. /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  experiments/rdpro/run_rdpro_2x2_pipeline.py plan
```

Provision isolated workers and generate the durable watchdog plan (no LLM):

```bash
PYTHONPATH=. /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  experiments/rdpro/run_rdpro_2x2_pipeline.py prepare
```

Only after the queue owner authorizes paid Gemini traffic:

```bash
PYTHONPATH=. /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  experiments/rdpro/run_rdpro_2x2_pipeline.py run --confirm-paid-llm
```

Runtime state is in `.aideal_exec/rdpro_2x2/watchdog.state.json`; the adjacent
log contains stage transitions. Re-running the last command resumes it.

## Failure evidence

Every final cell writes `docs/eval/<CELL>/failure_analysis/` containing:

- `FAILURE_ANALYSIS.md`: readable function-by-function diagnosis;
- `failure_details.csv`: analysis-table input;
- `failure_details.json`: exact category, error, generated code, source
  definition, codebase frames, token counts, and round history.

Infrastructure failures remain explicit and are never treated as documentation
failures. Provider/network failures make the watchdog retry rather than enter a
partially observed cell into the paper table.
