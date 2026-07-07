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
