# How benchmark suites pick GitHub repos — and what GRAIL should do instead

2026-07-07. Sources: HF dataset card `patched-codes/generate-readme-eval`;
OpenAI "Introducing SWE-bench Verified" (2024-08, updated 2025-02).

## 1. Generate README Eval — selection + eval mechanics

Selection: **top-400 Python repos by popularity — ≥1,000 stars AND ≥100
forks** — then keep only repos whose ENTIRE content is **<100K tokens** (so
one LLM call sees the whole repo). Result: 198 repos (158 train / 40 test).
The sample confirms the popularity-first bias: alongside real libraries
(httpie) it contains `awesome-machine-learning` (a link list),
`python-mini-projects` (tutorial snippets), `babyagi`, `MHDDoS` — things with
famous READMEs, not API libraries.

Eval: LLM regenerates a README from repo content; score = weighted mix of
similarity-to-the-ORIGINAL-README (BLEU 0.1, ROUGE 0.1, cosine 0.1) +
structural similarity 0.1 + information retrieval 0.2 + code consistency 0.2
+ readability 0.2. Telling artifacts: the **oracle (the real README itself)
scores only 56.79/100**, and the oracle's readability sub-score is 14.84 —
i.e. real READMEs lose to LLM output on the benchmark's own readability
metric. Gemini-1.5-flash was SOTA (33.43); more few-shot examples HURT.

## 2. SWE-bench / SWE-bench Verified — selection + eval mechanics

Selection: **12 mainstream Python repositories** (django, sympy,
scikit-learn, sphinx, ... — chosen for popularity and rich issue/PR/test
history). A sample = a RESOLVED GitHub issue whose merged PR added unit
tests: `FAIL_TO_PASS` tests (fail before patch, pass after) define success;
`PASS_TO_PASS` tests guard against regressions. Verified: OpenAI paid **93
professional developers** to triple-annotate 1,699 random samples for
(a) underspecified problem statements — 38.3% flagged, (b) unfair tests —
61.1% flagged; **68.3% of samples were filtered out**, leaving the 500-sample
Verified set. They also ship difficulty labels and a Docker harness. They
explicitly acknowledge **contamination**: models pre-trained on GitHub have
seen these repos and often the fixing PRs.

## 2b. Cross-check: would any SWE-bench repo pass the GRAIL funnel?

The 12 SWE-bench repos vs our gates (stars ≈ mid-2025 figures — verify at
adoption with the one-command check in §5):

| repo | ~stars | R2 (100–5K) | R1 (domain lib) | R5 (doc headroom) | R6 (contamination) |
|---|---|---|---|---|---|
| django, flask, requests, scikit-learn, matplotlib, seaborn | 20K–80K+ | ✗ | mostly frameworks/mainstream | ✗ | ✗ |
| sympy, pytest, sphinx, pylint | 5K–13K | ✗ | sympy yes; rest dev-tools | ✗ | ✗ |
| **astropy** | ~4.5K | ✓ borderline | ✓ (astronomy) | ✗ best-in-class docs | ✗ probe would fail |
| **xarray** | ~3.7K | ✓ | ✓ (labeled arrays) | ✗ excellent docs | ✗ extreme |

Verdict: **none pass.** Only astropy and xarray clear the star gate, and both
fail the two gates that carry GRAIL's premise: R5 (their documentation is
already the best in scientific Python — no headroom for a doc intervention)
and R6 (every model has seen millions of usage examples; the no-doc probe
would score high). Being in SWE-bench is itself a disqualifier now: frontier
models are *optimized against* these 12 repos, so any measured gain confounds
with benchmark training. The reverse direction is more useful: our adopted
repos (pymatgen, MDAnalysis have rich issue+PR+test histories) could support
a small SWE-bench-STYLE F2P task set as a secondary eval — SWE-bench's
mechanics transfer to niche repos even though its selection never would.

## 3. Why neither selection matches GRAIL's goal

GRAIL's target: *solid codebase, real users, NOT mainstream — a domain
library like RDPro or Sedona.* Both benchmarks select the opposite end:

| axis | readme-eval | SWE-bench | GRAIL needs |
|---|---|---|---|
| popularity | ≥1k stars, top-400 | mainstream top-tier | **mid-tail: enough users to matter, niche enough to be unmemorized** |
| unit of task | whole-repo summary | issue-level maintenance | **API-level USE: write new code against the library** |
| ground truth | similarity to original README | executed tests (F2P/P2P) | executed generated code (GRAIL already does this) |
| repo size | <100K tokens (toy) | large | real systems (beast ≫ 100K tokens) |
| language | Python only | Python only | Scala/Spark + Python (+ adapter per stack) |
| contamination | high (famous repos) | high (admitted) | **low by construction — that's the point of niche repos** |

The deepest mismatch is readme-eval's **gold standard = the original
README**. GRAIL's premise is that original human docs are inadequate context
for LLM code use — the readme-eval oracle scoring 56.79 (and losing on its
own readability metric) is accidental evidence FOR that premise. Optimizing
similarity to the original would penalize exactly the changes GRAIL makes
(verified call patterns, failure modes, fix hints).

## 4. What GRAIL should borrow anyway

From SWE-bench: (a) **execution as the only ground truth** — already our
design (comprehension `--execute` pass/fail = F2P analog); (b)
**PASS_TO_PASS analog**: after GRAIL treats a repo (aliases injected, docs
added), the UPSTREAM TEST SUITE must still pass — a non-regression gate we
should add per condition branch; (c) **"Verified" lesson**: filter unfair
tasks from the denominator — we already exclude `infra`; extend with a
fixture-infeasible annotation (retile-class failures) so the scored set is
defensible; (d) difficulty labels — our attempts/rounds-to-fix is a free,
automatic difficulty proxy per API.

From readme-eval: the static metric bundle (structure, info-retrieval,
readability) as a CHEAP secondary metric for doc form — never as the primary
outcome; and the train/test split idea if we ever tune prompts.

## 5. GRAIL repo-selection rubric (quantified, checkable per candidate)

R1 API-shaped domain library (not app/CLI/link-list): ≥50 intent-selected
   names. R2 niche-but-alive: **~100–5,000 stars**, ≥2 releases or active
   commits in last 24 months, ≥3 contributors. R3 runs locally with an
   existing adapter (scala-spark or python), build ≤30 min. R4 has tests:
   ≥20 test-called API names (grounding + `tested` signal). R5 has an
   original README (baseline arm) but not LLM-oriented docs (headroom).
   R6 contamination probe: **no-doc audience run** pass rate must be low
   (high = model memorized the lib; disqualifies the generalization claim).
   R7 raw surface 300–2,000 names (full-surface run stays ~1h / ~$5).

Verify a candidate in one command:
`curl -s https://api.github.com/repos/<org>/<repo> | jq '{stars:.stargazers_count, pushed:.pushed_at, lang:.language, forks:.forks_count}'`

## 6. Candidate pool — NON-geospatial (decision 2026-07-07)

Constraint: RDPro/beast + Sedona already cover geospatial; the
generalization targets must come from **other domains** — cross-domain
transfer is the stronger claim than same-domain replication. Tooling:
`tools/repo_finder/` (the sedona-shape finder, now with `--exclude-regex`
geo-filtering, + `run_grail_domains.sh` sweeping 14 non-geo domains ×
Scala/Python/Java with rubric filters: stars 100–5,000, forks >10, pushed
recently, ≥50 estimated API names).

Scala/Spark — adapter already exists, zero harness work (preferred):
- **Glow** (projectglow/glow) — genomics on Spark; the cleanest "same stack,
  different domain" test. Top pick.
- **Frameless** (typelevel/frameless) — typed Spark API; meta-domain
  (type-safe wrappers), heavy implicits = hard-for-LLM API shapes.
- **Apache Wayang** — cross-platform data processing plane; VLDB-native
  domain.
- **Breeze** (scalanlp/breeze) — numerics/linear algebra; foundational,
  operator-heavy API.
- Spark-NLP (JohnSnowLabs) — verify stars (may exceed the 5K cap).

Python — after the two signal fixes (docstring-below extraction, pytest
mining; Sedona 670→7 collapse is the motivating bug):
- **pymatgen** (materialsproject) — materials science; big real API, strong
  tests, institutional users.
- **MDAnalysis** — molecular-dynamics trajectories; complex typed objects.
- **QuTiP** — quantum dynamics; operator algebra API.
- **pydicom** — medical imaging format; parser-shaped, clear ground truth.
- **python-control** — control systems; compact math API.
- **lifelines** (survival analysis) / **arch** (econometrics) — statistics
  arm, small clean surfaces.

Java — visibility model exists, execution adapter would be new (backlog):
- **CDK** (cheminformatics) — the RDPro of chemistry.

Recommended next two: **Glow** (same stack, new domain → isolates domain
transfer with zero harness cost) then **pymatgen** or **MDAnalysis** (new
stack AND new domain, once Python signals are fixed). Sedona stays as the
configured Python debug target but not as the generalization claim.

## 6b. Why these domains and languages — and why not totally random

**Why not random sampling of GitHub.** Three reasons, one honesty mechanism.
(1) Yield: the population we study (solid, niche, API-shaped domain
libraries) is a tiny fraction of GitHub; even our TARGETED genomics query
returned 3 candidates of which 2 were rejected — a uniform random sample
would be almost entirely apps, tutorials, forks and abandonware, and stage-A
yield would collapse. (2) The claim being tested is not "GRAIL works on the
average repo"; it is "GRAIL generalizes across domains and stacks FOR THE
CLASS IT TARGETS". Claims about a class are tested by sampling that class —
stratified/purposive sampling with pre-registered gates, standard practice
when the class is rare in the frame. (3) Comparability: candidates must be
buildable ≤30 min with obtainable fixtures, or "GRAIL failed" confounds with
"repo unbuildable". **The honesty mechanism** that separates this from
cherry-picking: gates (R1–R7) are fixed BEFORE outcomes are seen, the sweep
enumerates EVERY match per domain query (no hand-picking within results),
and every rejection is logged with its reason — the whole selection is
reproducible from the script + a GitHub token.

**Why these 14 domains.** Chosen where (a) rich TYPED domain data models
exist — sequences, molecules, spectra, circuits, time series — the analogue
of rasters/geometries, because our genericity analysis shows domain-typed
receivers are exactly where LLMs fail; (b) the 100–5K-star mid-tail is
actually populated by maintained libraries; (c) non-geospatial by decision
(RDPro + Sedona already cover geo; cross-domain transfer is the stronger
claim).

**Why bioinformatics/genomics FIRST.** Minimal-change experiment design:
ADAM and Glow are Spark/Scala pipelines over big typed scientific data —
RDPro's exact architecture and build stack. Holding the STACK constant while
changing the DOMAIN isolates the domain-transfer variable at zero harness
cost. Chemistry/quantum/etc. come after because they change stack AND domain
at once.

**Why Scala, Python, Java.** Two grounds. (1) Harness cost: Scala's
execution adapter exists and is proven (RDPro) — zero engineering; Python is
the cross-LANGUAGE arm (Sedona configured, two signal fixes pending — the
670→7 lesson); Java shares the JVM toolchain and the visibility model is
implemented (CDK is the candidate). (2) RESEARCHER VERIFIABILITY: these are
the languages the experimenter reads fluently, which matters because every
LLM output in this study is human-auditable — failure classifications,
doc-repair diffs, and NOT-TESTABLE verdicts must be CHECKED, not trusted. An
unfamiliar language would make the audit itself unreliable. C++/Rust/Go are
deferred (adapter cost + audit cost), explicitly recorded as scope, not as a
claim about the method.

## 6c. Stage-A results (measured 2026-07-08) + Stage-B shortlist

Full sweep: 22 domains × {Scala, Python, Java} = 66 queries → **141 unique
repos across 17 populated domains** (RANKED_BY_DOMAIN.md / RANKED.md). Drop
rate per language: Scala 20/22 domains empty (2 candidates: cromwell, glow) —
niche Scala domain libs are RARE, the evidence for targeted-not-random
sampling; Python dense (bioinformatics alone total 154) → ~90 candidates;
Java ~50. Every match enumerated and finder-scored; every rejection logged
(e.g. `bigdatagenomics/adam` REJECTED on the 12-month activity gate —
development moved to the repo; `apache/incubator-kie-optaplanner` REJECTED,
active fork is `TimefoldAI/timefold-solver`).

**Stage-B shortlist (primary trio — 3 languages × 3 unrelated domains):**

| repo | lang | domain | ★ | APIs | score | rationale |
|---|---|---|---|---|---|---|
| projectglow/glow | Scala | genomics | 305 | 194 | 66 | zero harness cost (RDPro Spark stack); real library |
| materialsproject/pymatgen | Python | materials science | 1,920 | 577 | 93 | top score; rich typed surface (crystal structures) |
| cdk/cdk | Java | cheminformatics | 590 | 469 | 68 | big API, molecular types, no AGENTS.md |

Two calls that override raw finder score (which rewards stars/activity, not
library-shape-for-our-purpose): **glow over cromwell** (score 84) — cromwell
is a workflow ENGINE (app-shaped, orchestration APIs); glow is a Spark
LIBRARY on RDPro's exact stack, zero adapter cost. **cdk over gatk** (score
83) — gatk is genomics again (overlaps glow); cdk is a distinct domain with a
richer surface. Alternates: MDAnalysis (Py/MD), BoofCV (Java/CV), tslearn
(Py/time-series). Prerequisite before ANY Python target: the two Python
signal fixes (docstring-below extraction, pytest mining) from the Sedona
670→7 lesson — Scala (glow) + Java (cdk) need none, run those first.

## 7. Combined selection→baseline protocol (readme-eval × SWE-bench-Verified × our finder)

The funnel merges the three methods: readme-eval's **automated breadth
filters** (stage A), our finder's **library-shape scoring** (stage A), the
GRAIL static pipeline as an **automated deep screen** readme-eval doesn't
have (stage B), SWE-bench Verified's **human verification of task fairness**
— affordable because we verify ~10 repos, not 1,699 issues (stage C), and
SWE-bench's **execution ground truth** plus our contamination probe as the
baseline measurement (stage D). Report the drop rate at every stage
(Verified-style transparency: they dropped 68.3%).

### Stage A — automated discovery (~500 → ~30 repos, 1 day, no LLM)

A1. `export GITHUB_TOKEN=...` (env only), then
    `tools/repo_finder/run_grail_domains.sh` — 14 non-geo domains ×
    {Scala, Python, Java}, filters stars 100–5,000 · forks >10 · pushed
    within 12 mo · est. API ≥50 · `--exclude-regex` geo terms.
A2. Merge + rank by finder score (command printed at end of the script);
    keep top ~30. Record: query, date, counts per stage (reproducibility).

### Stage B — automated deep screen with the GRAIL static pipeline (~30 → ~8, no key)

Per repo (scriptable; each check is one command):
B1. Shallow-clone into `experiments/<repo>/`; write the 10-line project
    `aideal.yaml` (name, language, RELATIVE source/test globs, README path)
    — `extends: [scala-spark]` or the python adapter.
B2. `aideal api-surface` → gate **R7: 300–2,000 raw names** (big enough to
    be real; full-surface run stays ~1 h / ~$5).
B3. `aideal intent` → gate **R1: ≥50 selected**, AND signal health: the
    `documented` and `tested` reason counts must be >0 — the Sedona lesson
    (670→7 with both signals dead means a language gap, not a bad repo).
B4. `aideal dedup --out docs/dedup_report.json` → record redundancy profile
    (no gate; feeds the per-repo story).
B5. Build + upstream tests run locally in ≤30 min (**R3**); record the
    upstream pass state — this becomes the PASS_TO_PASS non-regression
    reference for every later GRAIL treatment.
B6. Token accounting: repo tokens, README tokens (readme-eval's size axis,
    kept as a measurement, not a cut).

### Stage C — human verification, Verified-style (~8 → 2–3, ≤30 min each)

C1. Confirm library-shape by eye: importable API, not an app/CLI/tutorial;
    original README exists (needed for the baseline arm); license permits
    modification experiments.
C2. **Fixture-feasibility annotation** (our analog of Verified's "unfair
    tests" filter, learned from `retile`/`saveAsGeoTiff`): list which API
    families cannot be exercised with obtainable sample data. If >30% of the
    intended surface is fixture-infeasible → drop or descope; the rest are
    annotated OUT of the scored denominator, with the count reported.
C3. Effort label (SWE-bench difficulty analog): estimated hours to wire the
    execute block (build wiring, fixtures, preamble). Adopt the cheapest
    repos first.

### Stage D — baseline measurement (per adopted repo; the numbers everything is compared to)

D1. **Contamination probe (R6, ours):** sample 20 intent-selected APIs;
    audience model writes code from NAME+SIGNATURE ONLY (no docs). High pass
    rate = the model memorized this library = weak generalization evidence.
    (Small harness addition: `doc_source=none`.)
D2. **No-catalog baseline:** `aideal comprehension --execute --doc original`
    — original README as the only context. This is "the repo as-is".
D3. **Catalog start point:** `aideal readme --generate --force` then
    `aideal comprehension --execute` — the AIDEAL treatment's day-0 number.
D4. Record per-API attempts (free difficulty distribution), failure
    categories, tokens/wall/$; report infra + fixture-infeasible exclusions
    explicitly (Verified-style: state the filter rate).
D5. Re-run the upstream test suite → must equal B5 (PASS_TO_PASS gate holds
    before any intervention; re-check after every alias/doc injection).
D6. Write `docs/baseline_<date>.md` (format: rdpro's
    `comprehension_baseline_2026-07-06.md`) and append the adoption decision
    + gate values to `docs/decision_log.json`.

Cost envelope per adopted repo: stage B ≈ 1 h machine time; stage C ≤ 30 min
human; stage D ≈ 2 full comprehension runs ≈ 2 h + ~$10 (gpt-4o-class) plus
the regen. RDPro numbers to beat/compare: 60–64/218 pass, ±2pp repeat
variance, 27.5% score, 129-compile-dominated failure mix.

## 8. Concrete baseline plan from `tools/repo_finder`

### What is ready now

`tools/repo_finder/sedona_shape_repo_finder.py` is the current finder to use.
Despite the historic "Sedona-shaped" name, it is now a general niche-library
finder: it searches GitHub, filters out templates/apps/tutorials/hardware,
checks package/test/docs structure, estimates public API count from source,
checks recent non-trivial source commits, and scores adoption plus library
shape. `run_grail_domains.sh` is the preferred driver because it sweeps
non-geospatial domains and applies the geo exclusion regex. There are no saved
finder outputs in the repo yet, so Stage A must be run fresh.

Avoid `run_all_languages.sh` for the paper run. It is an older broad language
sweep, does not encode the non-geospatial domain plan, and still has the
legacy `TOKEN=YOUR_TOKEN_HERE` interface. Keep it only as a scratch tool.

### First baselines to try

Use two adopted repos after the screen, not one:

| role | candidate | why it is useful | risk |
|---|---|---|---|
| B0 sanity baseline | RDPro/beast | already wired; establishes current pipeline behavior and failure taxonomy | same-domain only |
| B1 same-stack transfer | Glow (`projectglow/glow`) | Scala/Spark like RDPro, but genomics; isolates domain transfer without new harness work | may be too small or stale; verify |
| B2 new-stack transfer | pymatgen or MDAnalysis | non-geospatial scientific domain with real users and complex APIs | needs Python signal/execution quality |
| B3 optional hard transfer | QuTiP, pydicom, python-control, lifelines, arch | smaller domain APIs; good if B2 is too big or over-documented | may have too much existing usage in model memory |

Do not use SWE-bench repos as primary baselines. They are intentionally
mainstream, heavily benchmarked, and contamination-prone. Do not use
Generate-README-Eval repos directly either; that dataset admits app/tutorial
repos and evaluates similarity to original README, while GRAIL evaluates
whether docs let an LLM write executable API code.

### Fresh Stage A run

Run the finder from the repo root, sequentially. Do not run this in the same
experiment directory while an AIDEAL comprehension/docfix job is writing logs.

```bash
cd /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL
export GITHUB_TOKEN=...

LANGS="Scala Python Java" tools/repo_finder/run_grail_domains.sh
```

For a fast first pass, start with Scala only:

```bash
cd /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL
export GITHUB_TOKEN=...

LANGS="Scala" tools/repo_finder/run_grail_domains.sh
```

Merge/rank after the run:

```bash
python3 - <<'EOF'
import json, glob
rows = {}
for f in glob.glob('tools/repo_finder/results_grail/*.json'):
    for r in json.load(open(f)):
        rows[r['repo']] = r
top = sorted(rows.values(), key=lambda r: -r.get('final_score', 0))[:40]
for r in top:
    print(f"{r.get('final_score',0):6.1f}  {r['repo']:45s} "
          f"{r.get('stars','?'):>6}★  api={r.get('public_api_count','?'):>4}  "
          f"tests={r.get('has_tests')}  docs={r.get('has_docs')}  "
          f"{(r.get('description') or '')[:70]}")
EOF
```

### Stage B command template per candidate

For each top candidate, clone shallowly outside the RDPro experiment and make
a minimal AIDEAL config. Keep all generated artifacts inside that candidate's
own experiment directory.

```bash
cd /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL
mkdir -p experiments/external
git clone --depth 1 https://github.com/<org>/<repo>.git experiments/external/<repo>/source
mkdir -p experiments/external/<repo>/configs experiments/external/<repo>/docs
```

Then create `experiments/external/<repo>/configs/aideal.yaml` with relative
paths. Example for a Scala/Spark candidate:

```yaml
project_name: <repo>
language: scala
extends: [scala-spark]
repo_root: source
llm_readme: docs/LLM_readme.md
source_globs:
  - source/**/*.scala
  - source/**/*.java
test_globs:
  - source/**/src/test/**/*.scala
  - source/**/src/test/**/*.java
original_readme: source/README.md
```

Run the static gates:

```bash
cd /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experiments/external/<repo>
aideal api-surface
aideal intent
aideal dedup --out docs/dedup_report.json
```

Accept for baseline only if the static screen is healthy: raw surface roughly
300-2,000 names, selected surface at least 50 names, and both documented and
tested signals are nonzero. If documented/tested are zero, fix the adapter or
config before judging the repo.

### Stage D baseline sequence per adopted repo

For each adopted repo, freeze three baselines:

1. Original-doc baseline: model uses the repo's original README only.
2. AIDEAL catalog baseline: generated `LLM_readme.md`, no repair.
3. Repair-aware baseline: source-aware `fix-docs` from the g1 failed set,
   then full all-API comprehension rerun.

Record for every baseline: pass rate, scored denominator, excluded infra and
fixture-infeasible APIs, tokens, cost, wall time, and attempts-to-fix
histogram. The adopted repo is only defensible if upstream tests still match
the pre-treatment result after any AIDEAL-generated docs/aliases are added.

## 6d. Two added gates (2026-07-08): avoid frameworks; prefer bundled/generated data

**R8 — library, NOT framework/orchestration engine.** A workflow engine
(cromwell, galaxy-as-app, nextflow-like) mostly WIRES other tools together;
you cannot write a standalone snippet that exercises ONE of its APIs and get
a meaningful pass/fail — the "API" is orchestration, its execution needs
external backends. GRAIL's comprehension test requires an importable library
whose APIs transform typed data in-process. → cromwell REMOVED from the pool
(it was already flagged app-shaped; R8 makes the removal a rule, not a
judgment). Scala therefore has effectively ONE strong candidate (glow) —
further evidence of Scala domain-library scarcity, not a pipeline failure.

**R9 — data + reproducibility ease (Stage-C, now explicit & tiered).**
Rank candidates by how the comprehension harness obtains inputs:
  T0 GENERATED — API computes its own data (no fixture at all): best.
  T1 BUNDLED — sample data ships inside the package/test suite: trivial.
  T2 SMALL DOWNLOAD — a few MB, one command: fine.
  T3 LARGE/EXTERNAL — GBs, registration, or a live service: descope.
Plus install/runtime: pip/maven one-liner + no heavy runtime = green;
needs a cluster/DB/GPU = amber (dockerize or descope).

Applied to the pool (verify specifics at Stage C):

| repo | shape | data tier | install / runtime | verdict |
|---|---|---|---|---|
| pennylane | library | T0 generated (circuits/state-vectors) | pip, CPU | BEST — zero fixture |
| tslearn | library | T0/T1 synthetic + bundled datasets | pip, CPU | BEST |
| MDAnalysis | library | T1 bundled (MDAnalysisTests) | pip, CPU | excellent |
| pymatgen | library | T1 bundled test structures | pip, CPU | excellent |
| cdk | library | T1 bundled test molecules | maven, JVM | excellent |
| BoofCV | library | T1 any image / bundled | maven, JVM | excellent |
| pyroomacoustics | library | T0/T1 synthetic rooms + WAV | pip, CPU | excellent |
| glow | library | T1 small VCF | needs SPARK runtime | good (RDPro stack; dockerize) |
| mne-python | library | T2/T3 mne.datasets download (~GB) | pip, CPU | ok — pin a SMALL dataset |
| cromwell | FRAMEWORK | n/a (orchestrator) | needs backends/DB | EXCLUDED (R8) |

Priority insight: **T0/T1 candidates (generated or in-package data) are the
ideal GRAIL targets** — the fixture-feasibility risk that produces
`retile`-class runtime failures on RDPro disappears when the library ships or
computes its own data. pennylane, tslearn, MDAnalysis, pymatgen, cdk, BoofCV
all qualify.

## 6e. R10 — select BOTH AGENTS.md types, domain-matched (baseline selection)

The AGENTS.md comparison needs both flavors of baseline IN THE SELECTION
(not just at compare time):
  • NO-AGENTS.md repo → baseline = README-only / no-doc (weak-doc premise, R5).
  • HAS-AGENTS.md repo → baseline = the repo's OWN author-written AGENTS.md
    (the strong industry-standard control GRAIL must beat).
R10 refines R5: R5 keeps picking no/weak-doc repos as the PRIMARY intervention
targets, but the candidate set must ALSO include has-AGENTS.md repos so the
"GRAIL vs a real agent guide" arm exists — ideally as SAME-DOMAIN pairs so
domain difficulty is held constant across the two baseline types. (If no
same-domain has-AGENTS.md repo exists, an unpaired one is fine — the user's
call.)

Cleanest library↔library, same-domain pairs (both pass R8; from the sweep):

| domain | NO-AGENTS.md (baseline=README) | HAS-AGENTS.md (baseline=its AGENTS.md) | note |
|---|---|---|---|
| molecular dynamics | MDAnalysis (Py, 245 API) | deepmd-kit (Py, 252 API, score 95) | both libraries |
| time series | tslearn (Py, 166 API) | skforecast (Py, 275 API) | both libraries |
| audio/signal | pyroomacoustics (Py, 273 API) | TarsosDSP (Java, 249 API) | bonus: cross-LANGUAGE too |

Each pair yields a clean 2×2: {GRAIL, baseline-doc} × {no-agent repo,
has-agent repo}, same domain. Excluded as has-agent candidates (R8 fail —
platforms/apps, not libraries): galaxy, hail, geti, nomad. RDPro itself has
no natural AGENTS.md (its real one is a meta-doc pointing at aideal, archived
as AGENTS.aideal-meta.md); a neutral hand-written AGENTS.baseline.md supplies
the synthesized has-agent arm for RDPro.
