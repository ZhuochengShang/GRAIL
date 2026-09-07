# AIDEAL 2×2 experiment comparison report

Use this template once a repository has produced all four **matched** cells.
Copy it into the repository's analysis branch and replace every `<...>` field.

The design is:

```text
                         zero fix rounds       after deep repair
original documentation       A1                      B1
generated documentation      A2                      B2
```

`B1` and `B2` must be fresh comprehension reruns against the repaired shared
document. They must not be assembled by adding individual repair successes to
the A-cell results.

## 1. Reproducibility and scope

| Field | Value |
|---|---|
| Repository / version | `<repo> <version>` |
| Source commit | `<sha>` |
| AIDEAL commit | `<sha>` |
| Branches | `A1=<branch>`, `A2=<branch>`, `B1=<branch>`, `B2=<branch>` |
| Manifest path / SHA-256 | `<path>` / `<hash>` |
| Unique public API names | `<N>` |
| Definition sites retained as provenance | `<N>` |
| Public-API visibility rule | `<rule>` |
| Deduplication rule | `<rule; richest signature if same name>` |
| Documentation scope | `<full or relevant>` |
| Fixture/source-data provenance | `<checked-in paths and counts>` |
| PASS_TO_PASS before / after | `<paths and status>` |

All four cells must have the same manifest hash, API-name set, documentation
scope, and evaluation protocol. If not, mark the comparison **invalid**.

## 2. Cell results

| Cell | Document | Repair rounds allowed | APIs evaluated | Pass | Infra/provider excluded | Raw pass % | Scored pass % | Runtime | Attempts/restarts |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A1 | original | 0 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| A2 | generated | 0 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| B1 | repaired original | `<max>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| B2 | repaired generated | `<max>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |

Report both raw percentage (`pass / all APIs`) and scored percentage
(`pass / (all APIs − provider/infra exclusions)`). Never silently drop an API.

## 3. Effects

Use percentage points, not relative percentages:

- Generation effect: `A2 − A1 = <...> pp`.
- Repair effect on original: `B1 − A1 = <...> pp`.
- Repair effect on generated: `B2 − A2 = <...> pp`.
- Total best-vs-floor effect: `B2 − A1 = <...> pp`.
- Interaction: `(B2 − A2) − (B1 − A1) = <...> pp`.

Interpretation: positive values mean improved comprehension. State whether the
effect is raw or scored and include the denominator.

## 4. Failure taxonomy

Every non-pass API must have exactly one primary failure category and may have
secondary tags.

| Category | Definition | Count A1 | A2 | B1 | B2 | Treatment |
|---|---|---:|---:|---:|---:|---|
| `doc-missing` | No usable entry or wrong API identity | `<...>` | `<...>` | `<...>` | `<...>` | add/correct entry |
| `doc-vague` | Entry exists but omits purpose, inputs, outputs, or constraints | `<...>` | `<...>` | `<...>` | `<...>` | targeted doc repair |
| `doc-wrong` | Contradicts implementation or signature | `<...>` | `<...>` | `<...>` | `<...>` | verify against source |
| `example-invalid` | Example cannot execute with repository fixtures | `<...>` | `<...>` | `<...>` | `<...>` | replace with fixture-backed example |
| `api-identity` | Wrong overload/name/module selected | `<...>` | `<...>` | `<...>` | `<...>` | use manifest primary signature |
| `test/scaffold` | Harness, import, fixture, or command failure | `<...>` | `<...>` | `<...>` | `<...>` | classify as infrastructure |
| `llm-error` | Timeout, 504, quota, DNS, or provider failure | `<...>` | `<...>` | `<...>` | `<...>` | retry; exclude only from scored metric |
| `unknown` | Insufficient evidence | `<...>` | `<...>` | `<...>` | `<...>` | manual review |

Provider failures are not documentation failures. Report them separately and
include retry counts.

## 5. Attempt and repair accounting

| API | Cell | Attempt 1 | Attempt 2 | Attempt 3 | Final status | Failure category | Fix rounds used | Stuck rounds | Evidence |
|---|---|---|---|---|---|---|---:|---:|---|
| `<name>` | `<A1/A2/B1/B2>` | `<pass/fail/error>` | `<...>` | `<...>` | `<...>` | `<...>` | `<0–5>` | `<0–2>` | `<log/result path>` |

Record separately:

- provider attempts/retries;
- comprehension attempts;
- document-fix rounds;
- deep-dive rounds;
- watchdog restarts;
- APIs skipped because of infrastructure failure.

Do not count a retry as a repair round. A repair round changes the shared
document; a retry repeats the same evaluation request.

## 6. Failure analysis narrative

### Top failures

1. `<category>` — `<count>` APIs (`<percent>`): `<root cause>`.
2. `<category>` — `<count>` APIs (`<percent>`): `<root cause>`.
3. `<category>` — `<count>` APIs (`<percent>`): `<root cause>`.

### Representative APIs

For each major category, give one passing-after-fix and one persistent failure,
with source signature, documentation excerpt/path, test command, and error.

### What the repair changed

Describe whether repairs added missing entries, corrected signatures, added
constraints, fixed examples, or only recovered provider failures. State whether
the change improved B1, B2, both, or neither.

## 7. Validity checklist

- [ ] All four cells use the same manifest SHA-256 and API set.
- [ ] Public/local-wrapper and duplicate-name policies are recorded.
- [ ] A-cells use zero fix rounds.
- [ ] B-cells are fresh reruns after shared-document repair.
- [ ] PASS_TO_PASS checks exist before and after treatment.
- [ ] Repository-contained fixtures are listed and available.
- [ ] Provider/infra failures are separated from documentation failures.
- [ ] Every API has an attempt/failure ledger entry.
- [ ] Branch, commit, configuration, logs, and result paths are recorded.

## 8. Final decision

**Comparison status:** `<VALID / INVALID / PARTIAL>`  
**Primary limitation:** `<...>`  
**Most important failure mechanism:** `<...>`  
**Recommended next experiment:** `<...>`
