# AIDEAL external README-generation trio

This directory adds three isolated repositories for the next AIDEAL
generalization study. Upstream source checkouts live in `<repo>/source/` and
are intentionally gitignored; configs, profiles, generated docs, and measured
results stay versioned here.

## Selected repositories (verified 2026-09-06)

| Experiment | Repository | Stack/domain | Pinned source commit | Why selected |
|---|---|---|---|---|
| `glow` | `projectglow/glow` | Scala + Spark / genomics | `7f5a94e7dd9a4513a4e9e75eba294e8760fa0fb3` | Same execution stack as RDPro, different scientific domain; no upstream `AGENTS.md`. |
| `pymatgen` | `materialsproject/pymatgen` | Python / materials science | `0428f232a569ffe6b16fa030d38ea35a56d70fd6` | Rich scientific analysis API and tests; upstream `AGENTS.md` provides a strong agent-guide baseline. |
| `cdk` | `cdk/cdk` | Java / cheminformatics | `4e02291f3378442aa27421e253a908529feb6882` | Large typed molecular API, JUnit evidence, and a third language; no upstream `AGENTS.md`. |

Current GitHub screening values:

| Repository | Stars | Forks | Last push | Archived | License |
|---|---:|---:|---|---|---|
| Glow | 309 | 116 | 2026-06-28 | no | Apache-2.0 |
| pymatgen | 1,957 | 967 | 2026-08-31 | no | repository LICENSE (MIT; GitHub API returned `NOASSERTION`) |
| CDK | 605 | 179 | 2026-09-05 | no | LGPL-2.1 |

The pymatgen experiment targets the current umbrella repository. Its core
objects moved to `pymatgen-core` in 2026, so the first static gate must confirm
that the remaining analysis surface still clears the pre-registered threshold.

## Reproduce the checkouts

From the GRAIL repository root:

```bash
git clone --depth 1 https://github.com/projectglow/glow.git experiments/external/glow/source
git -C experiments/external/glow/source checkout 7f5a94e7dd9a4513a4e9e75eba294e8760fa0fb3

git clone --depth 1 https://github.com/materialsproject/pymatgen.git experiments/external/pymatgen/source
git -C experiments/external/pymatgen/source checkout 0428f232a569ffe6b16fa030d38ea35a56d70fd6

git clone --depth 1 https://github.com/cdk/cdk.git experiments/external/cdk/source
git -C experiments/external/cdk/source checkout 4e02291f3378442aa27421e253a908529feb6882
```

## Common protocol

Run every command with the project-specific config. Start with static gates,
then generate a ten-API pilot before paying for a full README:

```bash
PYTHONPATH=grail-agent/src python -m aideal.cli --config experiments/external/<repo>/configs/aideal.yaml profile
PYTHONPATH=grail-agent/src python -m aideal.cli --config experiments/external/<repo>/configs/aideal.yaml api-surface
PYTHONPATH=grail-agent/src python -m aideal.cli --config experiments/external/<repo>/configs/aideal.yaml intent --all
PYTHONPATH=grail-agent/src python -m aideal.cli --config experiments/external/<repo>/configs/aideal.yaml dedup --out docs/dedup_report.json
PYTHONPATH=grail-agent/src python -m aideal.cli --config experiments/external/<repo>/configs/aideal.yaml readme --generate --limit 10 --force --role author=gemini-3.1-pro
PYTHONPATH=grail-agent/src python -m aideal.cli --config experiments/external/<repo>/configs/aideal.yaml form
```

Acceptance before full generation: nonzero documented and tested signals,
at least 50 selected APIs, and a manually reviewed ten-entry pilot with no
invented API names. Full generation uses `--limit 0` only after that review.

The pilots pin `google:gemini-3.1-pro-preview`. The previously configured
`gemini-3.2-pro-preview` returned `404 NOT_FOUND` on 2026-09-06, while 3.1
remains available to the configured account.

README generation is supported for all three. Execution-grounded
comprehension is already supported by the Python and Scala/Spark adapters;
CDK still needs a project-specific Maven classpath/scaffold before
`comprehension --execute` can be treated as a valid result.
