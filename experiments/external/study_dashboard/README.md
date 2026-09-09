# Offline study evidence dashboard

Run `python -m experiments.external.study_dashboard --workspace-parent PATH
--out OUTPUT [--watch]` with the AIDEAL environment. The optional observer refreshes
every 60 seconds, holds one output lock and makes no model calls. It writes a
standalone HTML page, embedded/downloadable JSON, source hashes and a heartbeat.
Failed collection preserves the last page and publishes an error heartbeat.

The dashboard separates native A1/A2/B2 outcomes, S_A2/S_B2 recovery, retained
document rounds, Thumbnailator assertions replay, historical RDPro strata, and
MDAnalysis preparation/current v4 results. Missing observations are not zero
successes. Charts export SVG; the API table supports filters, search and paging.
Provider retry intervals and attempts are distinct from repair rounds.

`data.py` reconciles denominators and checks RDPro shared-88 raw counts against
saved metrics. `mdanalysis.py` reads only the explicitly registered new study,
rejecting mixed checkpoint identities. `lessons.html` preserves the developer
insights and their concrete examples. `dashboard.html` contains the visual
pipeline with LLM, automatic execution and reviewer boundaries.

The error-only repair comparison is **not launched**. A clean pilot would use two
new matched arms from the same mir_eval A2 README and 13 failures, followed by
148 fresh tests per arm. Remove source windows, tests, deep-dive output and
source-derived hints from the error-only prompts. Disabling deep-dive alone is
insufficient. Use the same engine and input contracts in both arms; old v3 source
results versus a new v4 error-only arm are not a matched experiment. The 4–7 hour
pilot allowance is a judgment estimate; provider delays can exceed it. One pair
cannot establish statistical equivalence. MDAnalysis now has execution priority.
