# tslearn · A2-only repair pipeline

2026-09-08T19:29:05.997010-07:00

A1 original README → zero fixes. A2 generated README → zero fixes.
Frozen A2 failures → source-only snippet repair; independently → generated-README repair → fresh B2.
Original-README repair (historical B1) is intentionally omitted.

| Cell | State | Native pass | API outcomes | Failure categories |
|---|---|---:|---:|---|
| A1 | native partial | 125 | 235 | {'infra': 55, 'runtime': 35, 'unknown': 1, 'llm-error': 19} |
| A2 | native complete | 175 | 235 | {'runtime': 32, 'infra': 28} |
| B2 | native complete | 217 | 235 | {'infra': 13, 'runtime': 5} |

Source recovery by new code-fix round: {'0': 0, '1': 26, '2': 32, '3': 32, '4': 32, '5': 32}
Source statuses: {'recovered_native': 32}
Document repair: {'attempted': 60, 'processed': 60, 'blocked': None}

[Source round details](source/REPORT.md) · [Machine-readable live evidence](live.json)

A2 is round zero; at most five new snippet proposals; stuck threshold two. B2 has at most five document rewrite rounds and a fresh zero-code-fix full-manifest evaluation.
Provider events, native acceptance, independent replay and semantic validation are separate. A passing generated assertion is not by itself independent proof of correctness.
