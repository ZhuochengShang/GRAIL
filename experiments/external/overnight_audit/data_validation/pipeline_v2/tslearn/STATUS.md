# tslearn · A2-only repair pipeline

2026-09-08T14:09:46.820542-07:00

A1 original README → zero fixes. A2 generated README → zero fixes.
Frozen A2 failures → source-only snippet repair; independently → generated-README repair → fresh B2.
Original-README repair (historical B1) is intentionally omitted.

| Cell | State | Native pass | API outcomes | Failure categories |
|---|---|---:|---:|---|
| A1 | native partial | 121 | 235 | {'infra': 51, 'runtime': 29, 'llm-error': 34} |
| A2 | native complete | 175 | 235 | {'runtime': 32, 'infra': 28} |
| B2 | pending native evidence | — | — | {} |

Source recovery by new code-fix round: {'0': 0, '1': 8, '2': 8, '3': 8, '4': 8, '5': 8}
Source statuses: {'recovered_native': 8, 'pending': 24}
Document repair: {'attempted': None, 'processed': None, 'blocked': None}

[Source round details](source/REPORT.md) · [Machine-readable live evidence](live.json)

A2 is round zero; at most five new snippet proposals; stuck threshold two. B2 has at most five document rewrite rounds and a fresh zero-code-fix full-manifest evaluation.
Provider events, native acceptance, independent replay and semantic validation are separate. A passing generated assertion is not by itself independent proof of correctness.
