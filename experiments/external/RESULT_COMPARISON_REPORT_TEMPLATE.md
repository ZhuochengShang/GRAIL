**Current report:** use the [v3 separated-stage template](post_b2/REPORT_TEMPLATE_V3.md). Report S_A2, README/B2, and S_B2 independently; native B2 and the B2+S_B2 composite have separate fields.

**Timing and execution amendment:** the current v3 template now requires per-API
attempt durations, measured retry intervals, transport-policy provenance and
explicit execution/provider states. See [reporter and timing definitions](provider_retry/README.md).
The legacy 2×2 material below is historical, not the active experiment protocol.

# AIDEAL 2×2 experiment comparison report

**Protocol change, September 8:** the user omitted original-README repair.
Use [the A2-only repair template](recovery/REPORT_TEMPLATE_V2.md) and
[the active pipeline definition](recovery/PIPELINE_V2.md) for current results.
The four-cell tables and interaction formulas below are retained for historical
2×2 studies, and must not be presented as the revised priority experiment.

## Measurement labels and validation gates

Never use **attempted**, **executed**, and **passed** interchangeably.

| Stage | Meaning | Required evidence |
|---|---|---|
| API evaluation attempted | Harness recorded an outcome for an API; it may be a provider failure | Per-API checkpoint event |
| Usable test generated | Provider returned code that reached local validation | Generated code/artifact; not merely a request-start log |
| Compiled | Compiler completed successfully; not applicable to every language | Compiler exit status |
| Test process started | Generated test was launched | Runner/process evidence |
| Target API reached | Intended receiver-qualified API call actually executed | Trace/instrumentation or explicitly qualified source/stack review; otherwise unknown |
| Recorded pass | Native harness accepted the process/markers | Native result, preserved even when a validation limitation is found |
| Verified correctness | Target was exercised and meaningful checks were active and passed | Assertion-enablement probe, target evidence, checked postcondition |

An execution failure can occur during receiver/data setup before reaching the
target API. A call inside a disabled assertion does not execute. Presence of
`__CHECK__` and exit code zero does not establish correctness by itself.
Keep unsupported/unknown stages explicit rather than deriving all stages from
one pass/fail field. Record denominator and snapshot time for every percentage.

For Java, verify the **effective** assertion setting with a sentinel assertion
that must fail, not just a YAML field named `require_correctness`. Compile
complete documentation examples against the pinned dependency. Validate fixture
meaning (e.g. actual EXIF orientation), not only format/path/file existence.
Changes to assertion behavior, fixtures, or eligible API identities require a
versioned matched comparison; do not silently modify one running condition.

When checkpoint compatibility records authorize reuse, report stable legacy
rows plus current-fingerprint outcomes with native current evidence taking
precedence. Preserve row-level provenance and provider errors. Do not count
only the new fingerprint as if all reused APIs had become unattempted, and do
not combine best scores across unrelated historical fingerprint groups.

Use this template once a repository has produced all four **matched** cells.
Copy it into the repository's analysis branch and replace every `<...>` field.

The live reporting framework is `audit_overnight.py`; input identity and API-test
data evidence are checked independently by `audit_experiment_data.py`. Follow
`REPORTING_AND_DATA_VALIDATION.md` for authoritative inputs, field definitions,
automatic delivery, and evidence limitations. Never enter a predicted value as
a measured result. Pending cells remain pending at the Wednesday deadline.

The design is:

```text
                         before doc repair     after source-informed doc repair
original documentation       A1                      B1
generated documentation      A2                      B2
```

`B1` and `B2` must be fresh comprehension reruns against the repaired shared
document. They must not be assembled by adding individual repair successes to
the A-cell results.

All four final evaluations use **zero snippet/code-fix rounds**. Document
repair is the B treatment; its budget is a separate column. The staged
`recovery/README.md` extension measures snippet recovery after these cells,
under a separate protocol and result namespace.

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

| Cell | Document | Doc rounds before final test | Code-fix rounds in final test | APIs evaluated | Pass | Infra excluded | Raw pass % | Scored pass % | Runtime | Attempts/restarts |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A1 | original | 0 | 0 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| A2 | generated | 0 | 0 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| B1 | original + repaired supplemental entries | ≤5/API | 0 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| B2 | repaired generated document | ≤5/API | 0 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |

Report both raw percentage (`pass / all APIs`) and scored percentage
(`pass / (all APIs − native infra exclusions)`). Unresolved provider failures
keep a cell partial and ineligible for the final comparison. Report their
attempt counts separately. Never silently drop an API. Because infra exclusions
can differ by cell, use the common manifest for raw effects and additionally
report paired effects on the common evaluable API intersection; do not treat
different scored denominators as the same paired population.

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

Every non-pass API retains its native execution category. Assign one primary
review category (or `unknown`) and optional secondary tags with evidence and
confidence. A compiler/runtime symptom alone cannot establish a documentation
cause.

| Category | Definition | Count A1 | A2 | B1 | B2 | Treatment |
|---|---|---:|---:|---:|---:|---|
| `doc-missing` | No usable entry or wrong API identity | `<...>` | `<...>` | `<...>` | `<...>` | add/correct entry |
| `doc-vague` | Entry exists but omits purpose, inputs, outputs, or constraints | `<...>` | `<...>` | `<...>` | `<...>` | targeted doc repair |
| `doc-wrong` | Contradicts implementation or signature | `<...>` | `<...>` | `<...>` | `<...>` | verify against source |
| `example-invalid` | Example cannot execute with repository fixtures | `<...>` | `<...>` | `<...>` | `<...>` | replace with fixture-backed example |
| `api-identity` | Wrong overload/name/module selected | `<...>` | `<...>` | `<...>` | `<...>` | use manifest primary signature |
| `test/scaffold` | Harness, import, fixture, or command failure | `<...>` | `<...>` | `<...>` | `<...>` | classify as infrastructure |
| `llm-error` | Timeout, 504, quota, DNS, or provider failure | `<...>` | `<...>` | `<...>` | `<...>` | retry; final cell remains partial while unresolved |
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

Distinguish a transport retry from a changed snippet and from a candidate
document rewrite. Count rejected/reverted document proposals as attempted doc
rounds too. Provider events can occur inside either repair workflow.

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
- [ ] All four headline cells use zero snippet-fix rounds.
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

## 9. Data identity and API-test suitability

Include the populated `FINAL_REPORT_DATA_AND_API_METHODS.md` appendix in the
delivered package, not just this blank table. For each repository, report exact
fixture paths and formats, full fixture size versus the sample actually used,
construction/slicing parameters, and examples connecting inputs to API calls
and assertions. Include resolved YAML layers, runtime/package evidence, and
known input or oracle mismatches. Keep deferred repositories explicitly deferred.

Identity checks prove which bytes were supplied. API suitability requires an
additional check of shapes, types, units, API ownership, and assertion meaning.
An upstream test-suite pass does not validate every generated test's oracle.

| Input | Role | Absolute path or in-memory construction | Source commit / Git blob | SHA-256 | Decoded shape/type/units | Pinned bytes match? |
|---|---|---|---|---|---|---|
| `<binding>` | `<input fixture / synthetic input / output>` | `<...>` | `<...>` | `<...>` | `<...>` | `<yes/no/not applicable>` |

Keep generated output paths out of the input-fixture inventory. For synthetic
inputs, retain the preamble/code hash, construction parameters and expected
invariants. A numerical utility API may correctly require no dataset file.

| API | Canonical owner/signature | Fixture/preloaded values used | Required shape/type/units | Actual call evidence | Assertion/witness | Suitability decision | Evidence |
|---|---|---|---|---|---|---|---|
| `<name>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<verified / mismatch / needs review / not applicable>` | `<script/hash/source>` |

- Verify ordered API names against the frozen full manifest, not an older
  subset or a same-sized result from another experiment.
- Verify each fixture against the blob at the pinned source commit; record
  source/config/profile/scaffold hashes and decoded input metadata.
- Identify the exact documentation treatment and result/checkpoint fingerprint.
- Confirm the generated snippet actually calls the intended public API and
  uses valid inputs. A binding declared in the scaffold is not proof of use.
- Inspect API-specific constraints: array dimensions/dtypes, class coverage,
  units, coordinate conventions, image modes, file formats, and output paths.
- Record textual call/assertion detection as preliminary evidence only.
  Correctness markers and a passing process do not by themselves prove a
  correct oracle, target ownership or meaningful exercise of the API.
- Keep diagnostic reruns separate from A1/A2/B1/B2 and from credited repairs.

## 10. Round and time definitions

| Quantity | Definition / authoritative evidence |
|---|---|
| Configured provider limit | Literal transport environment/config value; not an observed count |
| Observed provider-error attempts | Provider failures recorded in the per-API checkpoint |
| Provider-internal retries | Actual provider-attempt log; `unknown` when the SDK did not expose it |
| Comprehension attempts | Per-API checkpoint events under one compatible fingerprint |
| Code-fix rounds | Snippet changes within an invocation; final headline runs must use zero |
| Document-fix rounds | Shared-document treatment rounds from `docfix.json`, including unsuccessful/reverted rounds |
| Deep-dive rounds | Recorded deep-dive operations, separate from rewrite and evaluation |
| Stuck rounds | Consecutive unchanged/no-progress rounds as recorded by the repair loop; not total failures |
| Watchdog attempts | Process launches from state/logs; identify admission-only waits separately |
| Wall time | First actual computation start to final completion, with queue and retry waits separately reported |
| Model usage | Recorded per-attempt calls/tokens; a resumed final JSON alone omits prior invocations |

The current documentation loop has two stagnation paths: a member-validator
rejection increments the counter without execution; an executed candidate
increments it only if neither the normalized diagnosis nor error signature
changes. Progress resets it. `doc_stuck=2` is a registered cost-control heuristic,
not an empirically established optimum or proof that the API is unfixable.
Record the rejection reason, diagnosis-change/error-progress flags and stop
reason. A third round's outcome is unknown when the run stopped at two.

## 11. Cross-repository summary and deadline snapshot

| Repository | APIs per cell | Four matched final cells? | A1 | A2 | B1 | B2 | Generation effect (pp) | Repair effect (pp) | Main failure mechanism | Data validity |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| mir_eval | 148 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<B2-A2>` | `<...>` | `<...>` |
| Thumbnailator | 149 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<B2-A2>` | `<...>` | `<...>` |
| tslearn | 235 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<B2-A2>` | `<...>` | `<...>` |

State whether percentages are raw or scored; do not pool unlike API
denominators without specifying the weighting. MDAnalysis, Sedona and RDPro
reruns are deferred from this deadline package.

Record the snapshot timestamp, report commit, completed cells, remaining
provider/validation blockers, and exact missing artifacts. The scheduled
10:45 AM Wednesday snapshot provides a reviewable package before 11:00 AM;
the live report continues to fill as additional validated results finish.

## 12. Separate source-informed snippet recovery (staged)

Use `recovery/protocol.yaml` and `recovery/README.md`. Run both modes on the same
eligible failures from each completed baseline cell: feedback-only snippet
repair and source-deep-dive-assisted snippet repair. Freeze documents, fixtures,
scaffolds, source, model, timeout, maximum code rounds and stopping threshold.
Never fold recovery successes into A1/A2/B1/B2. B-only recovery cannot establish
how recovery interacts with all four document treatments.

| Repository / baseline cell | Eligible failures | Mode | Max code rounds / stuck threshold | Native recoveries | Independently validated recoveries | Provider blocked | Exhausted / stopped | Calls / tokens / time |
|---|---:|---|---|---:|---:|---:|---|---|
| `<repo>/<cell>` | `<...>` | feedback | `5 / 2 (accepted study policy)` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| `<same repo/cell>` | `<same set>` | source | `<same limits>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |

Recovery rate uses the fixed eligible-failure denominator. Show blocked and
missing outcomes rather than dropping them. Source mode includes one additional
diagnosis call, so a difference is the effect of the **source-assisted package**,
not source access alone under an equal token/call budget. Record diagnosis cost
separately. A source-only causal claim needs a matched analysis-call control.

This study fixes the stagnation threshold at **2**. Alternative thresholds
belong to a separate protocol. Report thresholds 2 and 3 only as a future
sensitivity question, not an optimization claim or extra scheduled experiment.
Replay only observed histories; mark unobserved continuations censored. Do not
combine different thresholds into one matched comparison. The recovery rule
(equal category/error prefix) differs from the documentation rule above.


## Secondary execution replay (separate from native study)

| Cell | Native pass / native API outcomes | Replayed / native API outcomes | Assertions-off pass / replayed | Assertions-on pass / replayed | Off-pass → on-fail | Unbound historical snippets | Unavailable evidence |
|---|---:|---:|---:|---:|---:|---:|---:|
| A1 | | | | | | | |
| A2 | | | | | | | |
| B1 | | | | | | | |
| B2 | | | | | | | |

Preserve code/fixture/library hashes, exact commands, effective assertion flags, isolation policy and preflight evidence. Distinguish assertion-toggle effects from failures also present in the assertions-off control. Report provider outcomes without stale test reuse; explain case collisions, truncated code evidence, source recovery and cache-compatibility decisions. Historical cache files are not additional API samples.

A replay alone cannot certify the entire documentation-repair pipeline: native repair decisions remain unchanged. Assertions-on acceptance is not independently certified correctness. Current replay evidence belongs to `data_validation/assertion_replay/`; its findings remain outside native headline scores.
