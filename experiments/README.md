# AIDEAL Experiments

All studies live here. Each is a self-contained AIDEAL project: own
`configs/aideal.yaml` + `configs/project_profile.yaml`; the `aideal` CLI
auto-selects the project from whichever folder you're standing in.

Both case studies START FRESH on purpose — they replicate the real user
journey. Each contains only the experiment definition (`configs/aideal.yaml`:
where the codebase is, which models, which runner) and an empty tasks file.
Everything else (profile, AGENTS.md, LLM_readme, notes, aliases, logs) is
produced BY the pipeline, starting with `aideal init`.

| Study | What it measures | First command |
|---|---|---|
| `testbed/` | controlled: barelib + one LLM-ready asset per stage → per-step effectiveness curve | `aideal init` (stage 1) |
| `rdpro/` | case study 1: original README vs generated vs curated docs | `aideal init` |
| `sedona/` | case study 2: external codebase, generalizability | `git clone` Sedona, then `aideal init` |

## Codebase clones and tracking applied changes

Each case study works on a FRESH upstream clone living inside the study
folder (gitignored — never committed to GRAIL):

```bash
cd experiments/rdpro  && git clone https://bitbucket.org/bdlabucr/beast.git
cd experiments/sedona && git clone https://github.com/apache/sedona.git
```

Every set of applied changes is a branch in that clone, named `aideal/<stage>`:

```bash
cd experiments/rdpro/beast
git checkout -b aideal/stage1-llm-readme     # add generated docs
git commit -am "stage1: LLM_readme entries for raptor APIs"
git checkout master && git checkout -b aideal/stage2-aliases   # independent condition
git commit -am "stage2: alias functions from alias-suggest"
```

Conventions: branch per CONDITION (each from the upstream base, so conditions
stay independent and diffable); one commit per logical change; compare any
condition with `git diff master..aideal/stage2-aliases`.

Because clones are gitignored, export patches into the committed `changes/`
folder whenever a condition is final:

```bash
cd experiments && ./export_changes.sh rdpro/beast
# → rdpro/changes/aideal-stage2-aliases.patch + MANIFEST.md (committable,
#   reproducible: clone upstream + git apply)
```

Record which branch a measurement used in the run's report/notes — the pair
(branch, seed) fully identifies a condition.

## Study 0: Testbed (`testbed/`)

See `testbed/README.md` for the stage-by-stage protocol. Start here — the
stage-0 baseline is the reference number for everything else.

# Case studies: RDPro → Apache Sedona

Both targets have a real, pre-existing README — the measured question is:
**how much does AIDEAL's pipeline improve on the original documentation?**

Conditions per target (same seed = same sampled functions across conditions):

| Condition | Doc given to the audience model | Command |
|---|---|---|
| C0 baseline | original project README only | `comprehension --doc original` |
| C1 generated | AIDEAL `LLM_readme.md` (`readme --generate`) | `comprehension` |
| C2 curated (RDPro only) | hand-tuned `rdpro_api_doc_combined.md` | copy it to `docs/LLM_readme.md`, rerun |
| + puzzles | end-to-end execution score per condition | `puzzle` |

Metrics per condition: comprehension pass rate, puzzle readiness score,
tokens, retry turns. Failures auto-accumulate in each target's
`logs/error_log.jsonl` → `notes-distill` / `alias-suggest`.

## Target 1: RDPro (`experiments/rdpro/`)

Fresh by design. The original readme is wired to
`rdpro-backend/RDPro/README.md` (the thin Beast readme; swap in a richer
doc concatenation later if you want a stronger baseline).

```bash
cd experiments/rdpro                 # `aideal` auto-finds this project's config
aideal init                          # creates profile template + AGENTS.md
# fill configs/project_profile.yaml, then:
aideal profile                       # must say ready: true
aideal completeness                  # static: 196 public fns, 0 documented here
aideal comprehension --doc original  # C0 baseline (needs API key)
aideal readme --generate             # build C1 docs with the author model
aideal comprehension                 # C1
aideal puzzle                        # end-to-end (needs Spark env for compile)
```

## Target 2: Apache Sedona (`experiments/sedona/`)

You input later:

```bash
cd experiments/sedona
git clone --depth 1 https://github.com/apache/sedona   # the codebase
aideal init                                            # profile template + AGENTS.md
# fill configs/project_profile.yaml, then same sequence as RDPro
```

Then the same command sequence as RDPro. The config targets Sedona's Python
API so generated code can be EXECUTED locally (`pip install apache-sedona
pyspark`) via the testbed-style runner — real ground truth, no Spark cluster.

## Why this order

RDPro first: you control it, the curated-doc condition (C2) exists, and the
GRAIL compile loop already works for it. Sedona second: external, popular,
well-documented — if AIDEAL still adds measurable readiness on top of GOOD
original docs, the generalizability claim is strong (and if not, that is the
honest boundary of the method).
