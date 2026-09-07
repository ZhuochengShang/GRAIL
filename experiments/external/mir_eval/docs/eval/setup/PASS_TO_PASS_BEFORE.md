# mir_eval PASS_TO_PASS before AIDEAL treatment

- Date: 2026-09-06 America/Los_Angeles
- Source: `fe73b3533737814f83dbd9739f06e90f5f82f758`
- Working directory: `experiments/external/mir_eval/source/tests`
- Command: `env MPLBACKEND=Agg OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 ../.venv/bin/python -m pytest -q`
- Result: PASS
- Summary: 535 passed, 3 skipped, 176 xfailed, 1 xpassed
- Warnings: 68
- Runtime: 41.92 seconds
- Coverage: 86% (3,042 statements, 436 missed)

The test command runs from `tests/` because this pinned upstream suite resolves
its checked-in data using paths such as `data/beat/ref*.txt` relative to that
directory. The environment includes `pytest-cov` and `pytest-mpl`, so the
configured coverage and stored-image checks are active.
