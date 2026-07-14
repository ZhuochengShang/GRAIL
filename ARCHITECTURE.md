# GRAIL / AIDEAL — structure, pipeline, and flow

_State as of 2026-07-13 (feature branch `aideal/feat-2x2-docfix` @ 9a650c3;
50 unit tests). This is the orientation document: what lives where, what each
stage does, and how the current experiment runs end to end._

## 1. The three-role structure

One repo, three strictly separated roles:

```
GRAIL/
├── grail-agent/                  ① THE TOOL (AIDEAL) — edited, never scanned
│   ├── src/aideal/               ~15 modules (pipeline below)
│   │   ├── defaults.yaml         framework defaults (layer 1)
│   │   ├── adapters/             ecosystem conventions (layer 2)
│   │   │   ├── scala-spark.yaml  Scala+Spark (RDPro, Sedona)
│   │   │   └── python.yaml       plain Python (tslearn)   [java.yaml: PENDING]
│   │   └── default_prompts/      language-NEUTRAL prompt templates
│   └── tests/                    50 pytest (pure-python, no keys needed)
├── experiments/<study>/          ③ STUDY WORKSPACES — run from here
│   ├── rdpro/                    target = beast/ (② TARGET CODE, gitignored clone)
│   │   ├── configs/aideal.yaml   project wiring (layer 3) + project_profile.yaml
│   │   ├── docs/                 generated: LLM_readme.md, manifests, reports
│   │   ├── logs/error_log.jsonl  append-only execution memory (per-ROUND rows)
│   │   ├── RUNBOOK.md            ← the 2x2 protocol commands live here
│   │   ├── compare_2x2.py, run_demo_stability.sh, demo_cases.sh, DEMO_PLAN.md
│   │   └── .aideal_exec/         scratch: per-API compile dirs + checkpoints (gitignored)
│   ├── tslearn/                  Python external baseline (mirror of rdpro layout)
│   └── sedona/                   parked
├── paper/                        VLDB material
├── BRANCHING.md                  git workflow (tool vs condition branches)
└── TODO.md                       the six advisor workstreams
```

**Config layering** (deep-merged, low → high): `defaults.yaml` → `extends:`
adapters → project `configs/aideal.yaml`. Generic knobs live low; ecosystem
conventions in adapters; only wiring + the execution harness are per-project.
Models: `roles: {author, audience, fixer}` → registry; every run can override
via `--role role=provider:model`. Framework defaults are intentionally generic;
the RDPro study config pins all three experimental roles to
`google:gemini-3.2-pro-preview`.

**Language generality:** generic prompts avoid project, domain, and language
syntax; documentation-call patterns and type-context globs are configurable;
visibility scanning understands common Scala, Python, and Java constructs; and
the fabricated-member guard mines the target repository's own vocabulary.
Scala+Spark and Python adapters exist. Some execution/error classification is
still ecosystem-specific, and a complete Java adapter remains a known gap
(JUnit mining and record handling already exist).

## 2. The AIDEAL pipeline (per study)

```
                         STATIC (no key)                        LLM + EXECUTION
┌──────────┐   ┌───────────────────────────────┐   ┌──────────────────────────────────┐
│  init /  │   │ api-surface  → intent → dedup │   │ readme --generate   (AUTHOR)     │
│  profile │ → │ (visibility-correct: def-line │ → │   entire per-API doc: docs/      │
│ (human:  │   │  + container modifiers +      │   │   LLM_readme.md                  │
│  ~30 ln) │   │  exclude_path_patterns)       │   │                                  │
└──────────┘   │ surface-audit · manifest ·    │   │ comprehension --execute (AUDIENCE│
               │ coverage (S/O/G/T)            │   │   reads doc → writes snippet →   │
               └───────────────────────────────┘   │   compile+run → pass/fail →      │
                                                   │   error_log row per ROUND)       │
                                                   │                                  │
     OBSERVABILITY (always on)                     │ fix-docs (FIXER, iterative):     │
┌────────────────────────────────┐                 │   per failing API, ≤N rounds:    │
│ fix-report: readable md per run│ ◄──────────────┤   deep-dive → diagnose → REWRITE  │
│  · verdict vs baseline         │                 │   the doc entry → run API on the │
│  · same-issue-NOT-solved       │                 │   NEW doc (0 snippet retries) →  │
│  · failure clusters            │                 │   keep on pass / revert if all   │
│  · chronic cross-run failures  │                 │   rounds fail. --create-missing  │
│  · per-API round timeline      │                 │   writes entries from scratch.   │
│ surface-audit: catalog vs      │                 │   Understanding check each round │
│  current surface (prune list)  │                 │   (diagnosis changed? error      │
└────────────────────────────────┘                 │   moved?) else early stop.       │
                                                   └──────────────────────────────────┘
   later stages (not in the current experiment): catalogue (per-class index,
   class-context read path — the postponed C arm) · augment (promote verified
   passing snippets into entries) · puzzle (K-function integration) · demo agent
```

Key mechanics:

- **Fix routing A vs B.** A = snippet retry (`--max-fix-rounds N` inside
  comprehension; error_log feeds each retry). B = doc repair (`fix-docs`) —
  failures are treated as evidence about the DOC; fixes persist in the catalog.
  Measured 07-08: doc repair (gemini-3.1, 36/99) beats snippet retry arms.
- **Guards.** Rewrites that call members neither on the raw surface, nor in the
  repo's own mined call vocabulary, nor in YAML category
  sets are rejected as fabricated. Manifests reject names outside the surface.
- **Memory.** `logs/error_log.jsonl` is the pipeline's memory: pass/fixed/fail
  per round with snippets, fix hints, timestamps, run ids. fix-report, deep-dive,
  augment, alias-suggest, and notes-distill all read it.
- **Reproducibility.** Every execute run JSON records `full_doc`, `doc_chars`,
  `manifest_sha256`, `document_sha256`, and an `experiment_fingerprint`;
  resume checkpoints only match rows with the same fingerprint, so arms can
  never contaminate each other.

## 3. The current experiment: the 2×2 (protocol v2.1)

Question: what are (i) authoring documentation and (ii) deep-dive doc-repair
each worth — on the original docs and on generated docs — holding everything
else fixed?

```
source code ──► S = visibility-correct, intent-filtered surface
original bundle (beast/README.md + beast/doc/**/*.md, TEXT ONLY) ──► O = evidence-documented ∩ S
generate readme FIRST (A2 branch) ──► G = entries ∩ S
                        freeze  T = S ∩ O ∩ G   +  coverage report (|O|/|S| vs |G|/|S|)
                                        │
        ┌───────────────────────────────┼────────────────────────────────┐
        ▼                               ▼                                ▼
   A1: original bundle,           A2: generated readme,            (coverage is its own
   whole doc, 0 fixes             whole doc, 0 fixes                first-class result)
        │                               │
        ▼                               ▼
   B1: iterative deep-dive        B2: iterative deep-dive
   repair w/ --create-missing     repair on the generated doc
   (--doc original+aideal)        (--doc aideal)
        │                               │
        ▼                               ▼
   FINAL FULL RERUN               FINAL FULL RERUN
        └───────────────┬───────────────┘
                        ▼
        compare_2x2.py (STRICT: requires one manifest hash, present document
        hashes, full_doc=true, zero snippet-fix rounds, and identical API sets)
```

Invariants every cell obeys: the audience receives the **entire** selected
document (+ one target line); **0 snippet-fix rounds**; the **same frozen
manifest T**; B-cells are **fresh full reruns** on the repaired document.
Effects read off the table: A2−A1 = generation, B1−A1 = repair-from-scratch,
B2−A2 = repair-on-authored, B2−B1 = final repaired-doc comparison.

Exact commands: `experiments/rdpro/RUNBOOK.md` header. Cost note: full-doc
mode sends the whole document per call — pilot with `--sample`.

## 4. Git flow

```
main  ──────────────► integration branch (tool + docs, tested)
  │   merge --no-ff
  ├── aideal/feat-*            tool work (e.g. feat-2x2-docfix @ f60113d+9a650c3)
  ├── aideal/rdpro-a-original      A1: run + results ONLY (no tool changes)
  ├── aideal/rdpro-a-original-fix  B1 (forked from A1's results commit)
  ├── aideal/rdpro-b-readme        A2 setup (readme --generate, tag) + A2 + B2
  ├── aideal/rdpro-c-catalog       postponed catalogue arm (forks from the tag)
  ├── aideal/tsl-*                 same ladder for tslearn
  └── aideal/rdpro-demo            VLDB demo; upstream = rdpro-b-readme
```

Rules: tool changes never land on condition branches; condition branches are
never merged (they exist to be diffed/re-run/cited); commit messages carry the
measured numbers; one condition runs at a time (shared scratch + error log).

## 5. Who runs what

- **Zoe's Mac** (keys + scalac/spark-submit): every LLM/execution run —
  the 2×2 cells, fix-docs, demo suite. Also: merge feat → main, reset
  condition branches, push.
- **Anywhere (no key):** api-surface, intent, dedup, surface-audit, manifest,
  coverage, fix-report on existing JSONs, the 50 unit tests.
- **Reports to read after any run:** `docs/fix_report_latest.md` (refreshes
  after every fix round), the run JSON, `docs/docfix_changes/<api>.roundN.*`
  (per-round audit), `docs/api_coverage.json`, `docs/compare_2x2.md`.
