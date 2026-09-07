# AIDEAL Wednesday detailed priority report

**Status: PARTIAL — experiments are still running.**

Delivery deadline: 2026-09-09T11:00:00-07:00.

Scope: mir_eval (148 APIs), Thumbnailator (149 APIs), tslearn (235 APIs), each with A1/A2/B1/B2. MDAnalysis, Apache Sedona and an RDPro rerun are outside this deadline package.

## Results, all failures, and every observed retry/repair round

- [mir_eval detailed report](mir_eval/DETAILED_REPORT.md): result table, effects, validity limitations and per-API failure narrative.
  [mir_eval provenance](mir_eval/provenance.json): branches, commits, result and test paths, inventory hashes.
- [thumbnailator detailed report](thumbnailator/DETAILED_REPORT.md): result table, effects, validity limitations and per-API failure narrative.
  [thumbnailator provenance](thumbnailator/provenance.json): branches, commits, result and test paths, inventory hashes.
- [tslearn detailed report](tslearn/DETAILED_REPORT.md): result table, effects, validity limitations and per-API failure narrative.
  [tslearn provenance](tslearn/provenance.json): branches, commits, result and test paths, inventory hashes.

[Live status](STATUS.md) · [Machine-readable status](status.json)

Each repository/cell directory contains ledger.csv and ledger.json covering all manifest APIs. Provider-internal retries that were never logged remain explicitly unknown. Native experiment results and scores are retained unchanged.

The first snapshot at or after 10:45 AM Wednesday is frozen alongside this live report, including partial outcomes if provider failures remain. Missing results are never marked complete to meet the deadline.
