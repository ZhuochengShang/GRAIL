# RDPro A1/A2 stratified comparison

Protocol: Gemini 3.1 Pro Preview, deterministic relevant-document retrieval,
same harness and fixtures. `zero` uses the dedicated zero-round results where
available; A1 complement zero is reconstructed from `pass_round == 0` in its
five-round run (round zero is isolated from repair history). `fix5` permits up
to five snippet-repair rounds. This is snippet repair, not README repair.

## Frozen strata

| Stratum | Count | Meaning |
|---|---:|---|
| shared | 88 | Validated APIs with code-evidenced original documentation |
| undocumented | 73 | Validated public APIs without code-evidenced original documentation |
| validated surface | 161 | shared + undocumented |
| artifact scale | 171 | Every generated README entry |
| generated extras | 10 | Generated entries outside the validated source surface |

## Raw execution results

| Stratum | A1 original zero | A2 generated zero | A1 original fix5 | A2 generated fix5 |
|---|---:|---:|---:|---:|
| Shared 88 | 37/88 (42.0%) | 39/88 (44.3%) | 70/88 (79.5%) | 69/88 (78.4%) |
| Undocumented 73 | 9/73 (12.3%) | 32/73 (43.8%) | 25/73 (34.2%) | 51/73 (69.9%) |
| Validated 161 | 46/161 (28.6%) | 71/161 (44.1%) | 95/161 (59.0%) | 120/161 (74.5%) |
| Artifact 171 | 46/171 (26.9%) | 73/171 (42.7%) | 97/171 (56.7%) | 125/171 (73.1%) |
| Extra 10 | 0/10 (0.0%) | 2/10 (20.0%) | 2/10 (20.0%) | 5/10 (50.0%) |

Primary descriptive effects:

- Shared zero-round document effect: **+2/88 = +2.3 pp**.
- Undocumented zero-round generated-document effect: **+23/73 = +31.5 pp**.
- Validated-surface zero-round effect: **+25/161 = +15.5 pp**.
- Shared five-round difference: **-1/88 = -1.1 pp** (parity).
- Undocumented five-round generated-document effect: **+26/73 = +35.7 pp**.
- Validated-surface five-round effect: **+25/161 = +15.5 pp**.

The result supports a stratified claim: generated documentation changes little
where code-evidenced original documentation already exists, but materially
improves both first-attempt success and repairability where it does not.

## Identical semantic audit

`semantic_audit.py` applies the same conservative checks to every raw PASS:

1. target name occurs in executable code;
2. an assertion/requirement is present;
3. no explicit failing/insufficient assertion is accepted;
4. no success-marker fallback is accepted;
5. an apparent Spark transformation has a terminal action;
6. same-name multi-site receivers without explicit owner evidence go to manual
   review rather than being credited or rejected.

The manual queue is now resolved in `semantic_receiver_review.json`. The final
verified counts combine automatic verification with the recorded receiver
decisions; rejected same-name collisions are not credited.

### Final semantically verified rates

| Stratum | APIs | A1 zero | A2 zero | A1 fix5 | A2 fix5 |
|---|---:|---:|---:|---:|---:|
| Shared documented | 88 | 37 (42.0%) | 37 (42.0%) | 68 (77.3%) | 66 (75.0%) |
| Validated undocumented | 73 | 9 (12.3%) | 32 (43.8%) | 23 (31.5%) | 49 (67.1%) |
| Validated public surface | 161 | 46 (28.6%) | 69 (42.9%) | 91 (56.5%) | 115 (71.4%) |
| Generated-only extras | 10 | 0 (0.0%) | 2 (20.0%) | 2 (20.0%) | 5 (50.0%) |
| Artifact-scale | 171 | 46 (26.9%) | 71 (41.5%) | 93 (54.4%) | 120 (70.2%) |

The semantic conclusions are stronger than the raw execution table:

- On shared documented APIs, A1 and A2 are exactly tied at zero rounds.
- On undocumented APIs, generated documentation adds **23/73 = 31.5 pp** at
  zero rounds and **26/73 = 35.6 pp** after five snippet-fix rounds.
- On the validated 161, generated documentation adds **23/161 = 14.3 pp** at
  zero rounds and **24/161 = 14.9 pp** after five rounds.

### Receiver-review resolution

Legitimate compiled aliases and implicit extensions are credited. Examples
include Spark-context `shapefile`, spatial-RDD `partitionBy`, Java helper
wrappers, generator-builder chains, and public same-name RDPro methods such as
`Summary.computeForFeatures`.

The following genuine receiver collisions are rejected:

- A1 fix5: `Summary.numPoints`, `LRUCache.size`, and
  `BeastOptions.mergeWith` were used for targets owned by other RDPro types.
- A2 zero: `GeometricSummary.run` and `LRUCache.size` were used instead of the
  intended qualified targets.
- A2 fix5: `MultilevelPlot.plotFeatures`, `GeometricSummary.run`, and
  iterator `size` were used instead of the intended targets.
- Explicit success fallbacks or invalid assertions remain rejected.

## Automatically rejected examples

- A1 fix5 complement: `getPointValue` (success fallback), `end` (apparent lazy
  operation without a terminal action).
- A2 fix5 complement: `computePointHistogramSparse` and `numFields`
  (invalid assertion); `construct`, `end`, and `lastNFiles` (apparent lazy
  operation without a terminal action).
- Other rejected rows remain in the machine-readable audit and require manual
  confirmation because collection `.map` can resemble Spark `.map`.

The machine-readable decisions and all six audited result sets are stored in
`docs/semantic_receiver_review.json` and `docs/semantic_audits/`. The ten
generated extras remain a secondary artifact analysis and are never folded
silently into the validated-161 headline.
