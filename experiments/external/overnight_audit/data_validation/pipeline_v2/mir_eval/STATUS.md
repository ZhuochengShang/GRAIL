# mir_eval · A2-only repair pipeline

2026-09-08T11:23:17.336596-07:00

A1 original README → zero fixes. A2 generated README → zero fixes.
Frozen A2 failures → source-only snippet repair; independently → generated-README repair → fresh B2.
Original-README repair (historical B1) is intentionally omitted.

| Cell | State | Native pass | API outcomes | Failure categories |
|---|---|---:|---:|---|
| A1 | native partial | 70 | 148 | {'llm-error': 26, 'runtime': 49, 'unknown': 1, 'infra': 2} |
| A2 | native complete | 135 | 148 | {'runtime': 13} |
| B2 | native complete | 137 | 148 | {'runtime': 11} |

Source recovery by new code-fix round: {'0': 0, '1': 11, '2': 13, '3': 13, '4': 13, '5': 13}
Source statuses: {'recovered_native': 13}
Document repair: {'attempted': 13, 'processed': 13, 'blocked': None}

[Source round details](source/REPORT.md) · [Machine-readable live evidence](live.json)

A2 is round zero; at most five new snippet proposals; stuck threshold two. B2 has at most five document rewrite rounds and a fresh zero-code-fix full-manifest evaluation.
Provider events, native acceptance, independent replay and semantic validation are separate. A passing generated assertion is not by itself independent proof of correctness.
