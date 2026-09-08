# thumbnailator · A2-only repair pipeline

2026-09-08T02:48:49.791835-07:00

A1 original README → zero fixes. A2 generated README → zero fixes.
Frozen A2 failures → source-only snippet repair; independently → generated-README repair → fresh B2.
Original-README repair (historical B1) is intentionally omitted.

| Cell | State | Native pass | API outcomes | Failure categories |
|---|---|---:|---:|---|
| A1 | native partial | 128 | 149 | {'runtime': 9, 'compile': 8, 'llm-error': 4} |
| A2 | native complete | 127 | 149 | {'compile': 14, 'runtime': 8} |
| B2 | pending native evidence | — | — | {} |

Source recovery by new code-fix round: {'0': 0, '1': 12, '2': 18, '3': 18, '4': 18, '5': 18}
Source statuses: {'recovered_native': 18, 'provider_blocked': 2, 'stuck': 2}
Document repair: {'attempted': 22, 'processed': 22, 'blocked': None}

[Source round details](source/REPORT.md) · [Machine-readable live evidence](live.json)

A2 is round zero; at most five new snippet proposals; stuck threshold two. B2 has at most five document rewrite rounds and a fresh zero-code-fix full-manifest evaluation.
Provider events, native acceptance, independent replay and semantic validation are separate. A passing generated assertion is not by itself independent proof of correctness.
