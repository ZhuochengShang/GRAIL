**Input handoff correction:** [Verified A2 errors and CLI paths](INPUT_HANDOFF_CORRECTION.md) supersedes the initial-error-seeding caveat below for repositories whose handoff status is `prepared`. The document-round restart limitation remains.

# AIDEAL active report: three separate stages

[Live HTML](REPORT.html) · [Status](STATUS.md) · [Evidence](live.json)

[Exact design and diagram](PIPELINE_V3.md) · [Report template](REPORT_TEMPLATE_V3.md) · [Registered policy](protocol.yaml) · [Launch plan](watchdog.yaml)

1. S_A2: source-only snippet recovery from frozen A2 failures.
2. Independent README repair from A2 targets, followed by fresh zero-fix B2.
3. S_B2: new source-only snippet recovery from frozen B2 failures.

The v2 workers and their original results remain intact. S_B2 waits for all priority B2 work and A2 source retries to settle. A1 has no repair loop. This adaptive amendment preserves native results, fixed failure cohorts and separate round/cost ledgers. Read the protocol for legacy document-round/error-seeding limitations and semantic-review gaps.

[Existing stage 1–2 details](../pipeline_v2/README.md) · [Data/API methods](../FINAL_REPORT_DATA_AND_API_METHODS.md) · [Thumbnailator replay](../assertion_replay/REPLAY.html) · [Readiness/review queue](../readiness/ASSESSMENT.md)
