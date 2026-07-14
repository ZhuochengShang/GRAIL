# VLDB demo plan (workstream 6)

Goal: every case shown live passes deterministically; everything else is
pre-baked. Protocol + storyline in one page.

## 1. Stability protocol

```bash
./run_demo_stability.sh              # N=5 x all 17 cases, --execute
./run_demo_stability.sh 1.1 2.1 3.1  # re-check just the headline cases
```

Verdicts: **STABLE** (N/N — allowed live) · **FLAKY** (intermittent — demo
only with a cached fallback) · **BROKEN** (0/N — fix or cut). Reports land in
`results/demo_stability_<stamp>.md`; failing tails in
`results/demo_stability_logs/`. Baseline from 2026-07-06: demo-critical 7/12
passing — rerun after the gemini-3.2 switch and the surface cleanup before
picking the live set.

## 2. Freeze the demo conditions

- Model: pin the demo to one model id (`gemini-3.2-pro-preview`) and
  temperature 0 — no mid-demo model roulette; `--role` overrides stay for
  rehearsal only.
- Fixtures: the pinned `sample_data` paths in `configs/aideal.yaml` (NLDAS
  raster + Boston polygons + land-use CSV). Never rely on fixture
  auto-discovery during the demo.
- Cached fallbacks: after a STABLE run, copy each case's outputs to
  `results/demo_cache/<case-id>/` and keep the generated Scala next to it.
  If the live run hiccups (conference wifi, Ivy resolution), show the cached
  output and the diff-in-git instead of re-running.

## 3. Group 1 fixture gap — pin a real land-cover raster (NLCD)

`raster_tif` today is NLDAS (continuous climate values), so the classic
"land-use % per neighborhood" story is UNANSWERABLE from the raster (see the
note at the top of `demo_test_cases.md`). To restore it as a Group-1 case:

1. Download an NLCD land-cover clip covering Boston (30 m, categorical
   classes) — e.g. from MRLC; clip to the neighborhoods' bbox
   (-71.19, 42.23, -70.99, 42.40), GeoTIFF, EPSG matching the polygons.
2. Save as `grail-agent/examples/fixtures/nlcd_boston_30m.tif` and add under
   `comprehension.execute.sample_data` as `raster_landcover_tif` (keep NLDAS
   as `raster_tif` — Groups 1-2 keep working unchanged).
3. Add the restored case to `demo_cases.sh`:
   `"1.4 land-use-pct|Using the land-cover raster and the Boston neighborhood
   polygons, compute the percentage of each land-cover class per neighborhood
   and write one row per (neighborhood, class, pct) to CSV."`
4. `./run_demo_stability.sh 1.4` until STABLE, then cache the output.

Until then, the land-use story is told through case 4.1 (CSV attribute join).

## 4. Storyline (before/after moment)

1. **Cold open (baseline branch):** original repo + original README only —
   `aideal comprehension --execute --doc original` numbers on screen; run one
   failing demo case live to show the raw-LLM floor.
2. **Treatment:** flip to the AIDEAL branch — catalog + verified examples +
   doc-repair marks; same case now passes; show the README entry's
   before/after (docs/docfix_changes/) and the fix-report's
   "same issue not solved → solved" delta.
3. **Live set:** only STABLE cases (target: 1.1, 2.1 or 2.3, 3.1, 4.1 — one
   per group); FLAKY cases appear as cached results only.
4. **Close:** surface-audit + fix-report as the "operator view" — the tool
   telling you what to fix next, not just a score.
