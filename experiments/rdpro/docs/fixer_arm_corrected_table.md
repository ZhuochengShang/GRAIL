# Fixer Arm Corrected Table

Numbers are taken from saved run JSON files where available. For partial
Codex doc-repair, the processed-denominator rate and full-target rate are both
shown because the run stopped before all target failures were processed.

| Fixer arm | Routing | Fixed | Rate | Time | Tokens in / out | Persists? | Source |
|---|---:|---:|---:|---:|---:|---|---|
| gpt-4o (old doc) | A snippet-retry | 3/158 | 1.9% | not recorded | not recorded | no | historical/console note |
| gemini-2.5-pro | A snippet-retry x15 | 7/128 | 5.5% | 197.9 min | 1.24M / 1.38M | no | `docs/comprehension_fixall.json` |
| gpt-5.3-codex | A snippet-retry x15 | 24/99 | 24.2% raw; 27.0% infra-excluded | 77.1 min | 0.97M / 0.05M | no | `results/bench/20260707_140828_g4_codex_fixall.gpt-5.3-codex.json` |
| gemini-2.5-pro | B DOC-REPAIR | 10/117 | 8.5% | 140.8 min | 0.89M / 0.66M | yes, in doc | `docs/docfix_run.json` |
| gpt-5.3-codex | B DOC-REPAIR | 5/28 processed; 5/99 target | 17.9% processed; 5.1% target | 19.8 min partial | 0.17M / 0.02M | yes, in doc for accepted fixes | `docs/docfix_archives/fresh_reset_20260707/docfix_codex_5_3_from_g1.bad_guard_partial_before_reset.json` |
| gemini-3.1-pro-preview (review) | B DOC-REPAIR v2 | 36/99 | 36.4% | 206.6 min | 0.74M / 1.21M | yes, in doc | `docs/docfix_gemini_3_1_pro_from_g1.json` |

Notes:

- Codex doc-repair was not a completed 99-API run. The cleanest partial report
  processed 28 APIs and accepted 5 doc fixes before reset/archival. Reporting
  only `5/28 = 17.9%` overstates full-run recovery; reporting only
  `5/99 = 5.1%` understates observed processed throughput. Use both.
- `gpt-5.3-codex` snippet-retry `24/99` is raw recovery over failed APIs. The
  same file reports `score = 0.270` after excluding 10 infra failures, hence
  `27.0% infra-excluded`.
- `gemini-3.1-pro-preview` doc-repair outcomes were:
  `36 doc-fixed`, `23 still-failing`, `32 not-testable`, and
  `8 rewrite-rejected`.
