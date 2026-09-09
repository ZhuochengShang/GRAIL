# All-repository study status

Inspected 2026-09-08T22:34:40.026037-07:00. Native snapshot: 2026-09-08T22:33:38.500132-07:00; detail/feedback snapshot: 2026-09-08T22:34:24.857323-07:00.

All nine priority A1/A2/fresh-B2 cells have recorded outcomes with no unresolved provider cases. Native completion still includes failed tests and setup/import blockers; it does not certify every intended API executed correctly.

| Repository | A1 original documentation | A2 generated README | Source/tests → snippet fixes (S_A2) | Source-informed README repair | Fresh B2 |
|---|---|---|---|---|---|
| mir_eval | 77/148 (52.0%) | 135/148 (91.2%) | 13/13 recovered | 6/13 retained; 13/13 processed | 137/148 (92.6%) |
| Thumbnailator | 130/149 (87.2%) | 127/149 (85.2%) | 20/22 recovered | 16/22 retained; 22/22 processed | 139/149 (93.3%) |
| tslearn | 129/235 (54.9%) | 175/235 (74.5%) | 32/32 recovered | 44/60 retained; 60/60 processed | 217/235 (92.3%) |
| MDAnalysis | 81 passes so far; 182/1032 outcomes, including 21 provider failures | No evaluation outcomes; README 774/1032 entries | Pending | Pending | Pending |
| RDPro historical | 37/88 direct documented cohort | 73/171 artifact | No comparable S_A2 arm | 67/98 retained; 98/98 processed | 132/171 artifact |

RDPro historical A1 and A2/B2 denominators differ. The 171-entry artifact has ten entries outside the validated 161 APIs. The existing dashboard retains the separate reconstructed 161-API A1 stratum; it is not substituted for the directly measured 88 here. Historical fix5 uses a new round zero and is not frozen-A2 source/tests recovery. Historical native outcomes and semantic reviews/replays stay separate.

tslearn S_A2 uses 32 eligible failures and excludes 28 setup/import blockers; its new B2-1 uses all 60 frozen A2 failures. A retained README edit is not a fresh-test pass.

## Current B2-1 (README + errors; no new source/tests diagnosis)

- mir_eval: {'recovered_native': 13} out of 13 frozen failures; active=None; complete=True.
- Thumbnailator: {'recovered_native': 21, 'stuck': 1} out of 22 frozen failures; active=None; complete=True.
- tslearn: {'recovered_native': 13, 'infra_blocked': 7, 'exhausted': 2, 'ready': 38} out of 60 frozen failures; active=compute; complete=False.
- MDAnalysis: waiting for complete A2.

New RDPro v5: 0/161 A2 outcomes; waiting reason: priority B2-1 work. It remains separate from historical RDPro. No A1 rerun is scheduled.

## Running processes and remaining work

Verified live: tslearn B2-1 PID 89199; MDAnalysis A1 PID 49495; MDAnalysis generation PID 49490; RDPro admission waiter PID 65315. Existing dashboard/report observers have healthy heartbeats. No experiment process was restarted or duplicated.

MDAnalysis A1 logs still show approximately 600-second Gemini 504 errors. Generation continues independently. At the cumulative A1 rate (~182 outcome records in 4.7 hours), its ~850 remaining APIs alone represent roughly 22 more hours before retries; only about 12.4 hours remain to Wednesday 11 AM PDT. This rough scenario does not support claiming a complete MDAnalysis study by that deadline. Other stages and provider variation add uncertainty.

## Input evidence

- `GRAIL_overnight_evidence_audit/experiments/external/overnight_audit/data_validation/study_dashboard_v1/data.json` — SHA256 `931e3b80bf512c613252996e179297c72d2293953929c5f52078333fa087130a`
- `GRAIL_overnight_evidence_audit/experiments/external/overnight_audit/data_validation/main_plan_v5/live/data.json` — SHA256 `cae6f94d40d4a163a5cd127b9adb65d924a5bf2dce6df5c931afc3dd9dda903b`
- `GRAIL_overnight_evidence_audit/experiments/external/overnight_audit/data_validation/rdpro_v5/status.json` — SHA256 `307ab1893cc997af88f864c49899ccfc202d5ff96962d643ff83e63a0df56f33`
- `GRAIL_overnight_evidence_audit/experiments/external/overnight_audit/data_validation/rdpro_v5/waiting.json` — SHA256 `1577dd96604eb7f1d5f7ac5137f83028d27c9cbda588710006163cd427389827`
- `GRAIL_rdpro_final_A1/experiments/rdpro/docs/comprehension_A1_original.json` — SHA256 `40358213ade736b71a30c23ddb242831f33f7188f58f955df914fb13070aef9c`
- `GRAIL_rdpro_final_A2/experiments/rdpro/docs/comprehension_A2_generated_all.json` — SHA256 `b79f10f66e97b6dd07bb1b1c32dc659b17c7ee44849af84d305223142b54023d`
- `GRAIL/experiments/rdpro/docs/docfix_B2_all171.completed.json` — SHA256 `36f4e19b2a5a719d5829f37a4f076687672bcff146b368ec09ce184d2a308747`
- `GRAIL/experiments/rdpro/docs/comprehension_B2_final_all171.json` — SHA256 `0e097d6978a7fd274a4f6b440197686d09e904dde3ab06a5a258507d1395292b`
