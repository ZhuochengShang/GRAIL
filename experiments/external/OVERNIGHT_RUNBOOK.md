# Five-repository overnight runner

Use `run_condition_watchdog.py`; the earlier single-worktree external-trio
runner was removed because branch switching underneath jobs is not safe.

## Required preflight

1. Record the chosen surface/provenance protocol in
   `../../FIVE_REPO_EXECUTION_STATUS_2026-09-06.md`.
2. Commit and push the shared infrastructure branch.
3. Archive existing dirty evidence; never clean or overwrite it.
4. Create one Git worktree for every A1/A2/B1/B2 branch.
5. In every worktree, write a dependency inventory file and set it as the job's
   `environment_inventory`.
6. Run `validate_experiment_yaml.py` and upstream PASS_TO_PASS before launch.

## Supervisor guarantees

- At most three jobs run concurrently, and never two jobs in one worktree.
- All Gemini workers share `AIDEAL_GOOGLE_RATE_STATE` and a minimum request
  start interval.
- A changed plan cannot reuse an old supervisor state.
- A changed model/YAML/scaffold/source/fixture/engine/interpreter/environment/
  manifest/document cannot reuse an old API checkpoint.
- Gemini/network failures are transient and retried; compile/runtime failures
  remain experimental outcomes.
- Stdout is written to a temporary file and atomically promoted only after the
  completion predicate passes.
- Killing and restarting the supervisor returns interrupted jobs to pending;
  AIDEAL resumes valid per-API checkpoints.
- `--keep-awake` uses macOS `caffeinate` for the life of the supervisor.

Launch shape after the worktree-specific plan exists:

```bash
PYTHONPATH=grail-agent/src \
  /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  experiments/external/run_condition_watchdog.py \
  experiments/external/five_repo_jobs.yaml --keep-awake
```

Every comprehension job should use completion kind
`json_metrics_no_transient`; every repair job should use `docfix`. Add explicit
`on_success` commit and `git push -u origin HEAD` commands only after its
worktree/branch is frozen and the staged file list is reviewed.

Runtime state is stored beside the plan as `*.state.json`; logs use `*.log` and
per-job `*.stderr.log`. Those files plus AIDEAL JSONL checkpoints provide the
resume trail.
