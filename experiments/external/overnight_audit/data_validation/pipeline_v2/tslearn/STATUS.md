# tslearn · A2-only repair pipeline

2026-09-08T09:52:15.127491-07:00

A1 original README → zero fixes. A2 generated README → zero fixes.
Frozen A2 failures → source-only snippet repair; independently → generated-README repair → fresh B2.
Original-README repair (historical B1) is intentionally omitted.

| Cell | State | Native pass | API outcomes | Failure categories |
|---|---|---:|---:|---|
| A1 | native partial | 120 | 235 | {'infra': 51, 'runtime': 29, 'llm-error': 35} |
| A2 | native partial | 175 | 235 | {'runtime': 31, 'infra': 27, 'llm-error': 2} |
| B2 | pending native evidence | — | — | {} |

Source recovery by new code-fix round: pending
Source statuses: pending
Document repair: {'attempted': None, 'processed': None, 'blocked': None}

[Source round details](source/REPORT.md) · [Machine-readable live evidence](live.json)

A2 is round zero; at most five new snippet proposals; stuck threshold two. B2 has at most five document rewrite rounds and a fresh zero-code-fix full-manifest evaluation.
Provider events, native acceptance, independent replay and semantic validation are separate. A passing generated assertion is not by itself independent proof of correctness.
