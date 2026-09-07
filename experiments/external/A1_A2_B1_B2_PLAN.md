# External trio A1/A2/B1/B2 execution plan

Status date: 2026-09-06. This is the pre-run protocol for Glow, pymatgen,
and CDK. No result is called A1/A2/B1/B2 until its repository-specific
execution harness has passed a model-independent smoke test.

## 1. Question and four cells

The experiment asks two separate questions:

1. Does an automatically generated AIDEAL README improve an audience model's
   ability to write code that really executes, compared with the repository's
   original documentation?
2. Does execution-grounded document repair improve either starting document?

| Documentation condition | Before document repair | After document repair |
|---|---|---|
| Original upstream documentation | A1 | B1 |
| Generated AIDEAL README | A2 | B2 |

- **A1** is a fresh, zero-snippet-fix execution run with the original
  upstream documentation.
- **A2** is the same run with the frozen generated README.
- **B1** starts from the A1 failures. `fix-docs --create-missing` creates an
  AIDEAL entry beside the unchanged original bundle. The reported B1 value is
  a fresh, full zero-snippet-fix run against `original+aideal`, not the union
  of A1 passes and repair retries.
- **B2** starts from the A2 failures and repairs the generated entries. The
  reported B2 value is another fresh, full zero-snippet-fix run.

The effects are A2-A1 (generation), B1-A1 (repair on original), B2-A2
(repair on generated), and the repair-by-starting-document interaction.

## 2. Non-negotiable invariants

Every cell for one repository must have:

- the same ordered, frozen API manifest and manifest SHA-256;
- the same pinned upstream commit, runtime, dependencies, fixtures, scaffold,
  audience model, and prompt version;
- `--max-fix-rounds 0` for all four headline runs;
- the same documentation scope and retrieval budget;
- an independently hashed delivered document;
- fresh B1/B2 full reruns after repair;
- infrastructure failures excluded and reported separately, never repaired as
  documentation failures;
- no historical error-log feedback in the first attempt of A1 or A2;
- source and upstream-test PASS_TO_PASS checks before and after treatments.

Because these repositories have much larger documentation bundles than RDPro,
the external-trio protocol will use `--doc-scope relevant` in every cell. This
is deterministic retrieval with the same character cap for each condition.
`full` and `relevant` results must never be mixed in one table.

## 3. Current blockers found before running

The existing ten-entry files are README-generation pilots, not executable
2x2 results. With the current README-only original bundles, all three shared
manifests are empty:

| Repository | Selected surface S | Original coverage | Pilot generated coverage | Shared T |
|---|---:|---:|---:|---:|
| Glow | 47 | 4.3% | 21.3% | 0 |
| pymatgen | 486 | 0.4% | 2.1% | 0 |
| CDK | 333 | 0.3% | 3.0% | 0 |

Execution is also not yet qualified:

- Glow has no pinned AIDEAL jar/classpath/scaffold/fixture wiring. The source
  defaults to Spark 3.5.1 and Scala 2.12.19, while the existing machine-wide
  Spark installation is 3.3.1. The experiment must use an isolated matching
  Spark runtime rather than silently mixing versions.
- pymatgen requires Python >=3.11 and `pymatgen-core>=2026.8.30`; the current
  AIDEAL Python 3.10 interpreter cannot import it. A Python 3.12 experiment
  environment and Python execution scaffold are required.
- CDK has Maven and Java 17 available, but AIDEAL needs a Java scaffold,
  `javac`/runtime command, classpath construction, and Java-specific compiler
  error classification before execution results are meaningful.

## 4. Stage 0: isolate and freeze conditions

For each repository, create four condition configs with separate mutable
artifacts:

```text
configs/aideal_A1.yaml        logs/A1/       .aideal_exec/A1/
configs/aideal_A2.yaml        logs/A2/       .aideal_exec/A2/
configs/aideal_B1.yaml        logs/B1/       .aideal_exec/B1/
configs/aideal_B2.yaml        logs/B2/       .aideal_exec/B2/
docs/eval/A1/                 docs/eval/A2/
docs/eval/B1/                 docs/eval/B2/
```

A1 and B1 share the immutable original-doc bundle; A2 and B2 begin from one
frozen generated README. B1's generated-entry file starts empty. B2 receives
a byte-for-byte copy of A2 before repair. This avoids branch/log/checkpoint
leakage without modifying any upstream checkout.

Record a `provenance.json` containing upstream commit, dirty state, config
hash, manifest hash, scaffold hash, fixture hashes, runtime versions, model
identifiers, prompt hashes, and the PASS_TO_PASS commands.

## 5. Stage 1: build and qualify execution harnesses

### Glow

1. Install an experiment-local Spark 3.5.1 runtime and use its Spark jars and
   `spark-submit`.
2. Build the pinned source with Spark 3.5.1 / Scala 2.12.19 via sbt.
3. Point AIDEAL at the built `glow-spark3` jar and dependency classpath.
4. Create a Scala scaffold that starts local Spark, registers Glow, and
   exposes a tiny DataFrame plus the repository's small `1kg_sample.vcf`.
5. Hand-run five API families (SQL function, array/vector helper, genotype
   summary, VCF reader, transformer) before any LLM run.

### pymatgen

1. Create an isolated Python 3.12 virtual environment.
2. Install the pinned checkout and its declared `pymatgen-core` dependency;
   freeze the complete environment with `pip freeze`.
3. Create a Python scaffold exposing tiny in-memory `Lattice`, `Structure`,
   `Molecule`, and `Composition` objects. Network/database APIs remain out of
   scope.
4. Hand-run five API families (structure analysis, matching, transformations,
   local environment, and a numerical analysis) before using the audience
   model.

### CDK

1. Build the pinned Maven reactor with Java 17 and produce a reproducible
   bundle/runtime classpath.
2. Add a Java scaffold with a `main`, structured success/error markers, and
   an insertion region for each generated snippet.
3. Extend AIDEAL's execution classifier to parse `javac` diagnostics and Java
   runtime exceptions, with regression tests.
4. Expose an in-memory `SilentChemObjectBuilder`, small molecules from SMILES,
   and one tiny pinned MOL/SDF fixture.
5. Hand-run five API families (object model, SMILES, SMARTS, fingerprint, and
   descriptor) before any model-generated snippet is scored.

Harness acceptance is five of five hand-written calls with deterministic
witnesses plus a deliberately broken call correctly classified as a model/
code failure. Missing dependencies must be classified as infrastructure.

## 6. Stage 2: freeze fair documentation and API samples

The original condition must contain the upstream user-facing documentation,
not just the root README:

- Glow: root README, Python README, and the user-facing RST documentation.
- pymatgen: root README plus usage, compatibility, installation, addons, and
  other user-facing Markdown documentation. Administrative files are omitted.
- CDK: root README plus reproducibly generated upstream Javadocs. Javadocs are
  built from the pinned source comments; raw implementation bodies are not
  supplied to the audience model.

Hash the ordered file list and concatenated bundle. Recompute `S` and `O`
after this correction.

Use a two-stage scale-up:

1. **Protocol pilot:** ten seeded, family-stratified APIs per repository from
   `S intersect O`. Run the entire A1/A2/B1/B2 sequence. This validates
   attribution, logging, repair, and comparison at bounded cost.
2. **Production run:** up to 40 seeded, family-stratified APIs per repository
   from `S intersect O`, seed 42. Forty is pre-registered because Glow has 47
   selected APIs and it keeps the three repository denominators cost-matched.
   If a corrected original bundle has fewer than 40 eligible APIs, use all of
   them and report the smaller denominator rather than weakening the evidence
   rule.

AIDEAL currently chooses `--limit` entries alphabetically. Before the pilot,
add a manifest-driven README-generation option so the generated document is
written for exactly the frozen representative sample. Do not use the current
alphabetical ten entries as the experimental manifest.

## 7. Stage 3: run the cells

For each repository, after freezing `docs/eval/api_manifest_shared.json`:

```bash
# A1: original documentation, cold
aideal --config configs/aideal_A1.yaml comprehension --execute \
  --doc original --doc-scope relevant \
  --manifest docs/eval/api_manifest_shared.json --max-fix-rounds 0

# A2: byte-frozen generated documentation, cold
aideal --config configs/aideal_A2.yaml comprehension --execute \
  --doc aideal --doc-scope relevant \
  --manifest docs/eval/api_manifest_shared.json --max-fix-rounds 0

# B1: repair A1 failures, creating entries beside original docs
aideal --config configs/aideal_B1.yaml fix-docs \
  --from-results docs/eval/A1/comprehension.json --create-missing \
  --deep-dive-first --doc-rounds 5 --doc-stuck 2 --retry-rounds 0 \
  --doc original+aideal --doc-scope relevant \
  --manifest docs/eval/api_manifest_shared.json \
  --report docs/eval/B1/docfix.json
aideal --config configs/aideal_B1.yaml comprehension --execute \
  --doc original+aideal --doc-scope relevant \
  --manifest docs/eval/api_manifest_shared.json --max-fix-rounds 0

# B2: repair a copy of the frozen A2 document
aideal --config configs/aideal_B2.yaml fix-docs \
  --from-results docs/eval/A2/comprehension.json \
  --deep-dive-first --doc-rounds 5 --doc-stuck 2 --retry-rounds 0 \
  --doc aideal --doc-scope relevant \
  --manifest docs/eval/api_manifest_shared.json \
  --report docs/eval/B2/docfix.json
aideal --config configs/aideal_B2.yaml comprehension --execute \
  --doc aideal --doc-scope relevant \
  --manifest docs/eval/api_manifest_shared.json --max-fix-rounds 0
```

Write command output atomically or use the per-API resume checkpoint so an
interrupted paid run does not lose completed rows. Never reuse a checkpoint
whose experiment fingerprint differs.

## 8. Stage 4: validate and report

Run `compare_2x2.py` without `--force`; it must refuse any mismatched manifest,
scope, document hash, or nonzero snippet-fix cell. Report for every cell:

- raw pass / total and scored pass / non-infrastructure total;
- compile, runtime, timeout, infrastructure, and provider-error counts;
- document characters/tokens, model calls, input/output tokens, latency, and
  estimated cost;
- API-family results and failure clusters;
- A2-A1, B1-A1, B2-A2, B2-A1, and the interaction;
- original/generated surface coverage separately from matched-sample quality;
- PASS_TO_PASS before/after results.

Stop a repository before paid production runs if the harness smoke test fails,
the shared pilot manifest is empty, more than 10% of pilot rows are
infrastructure failures, or the comparison validator rejects any invariant.

## 9. Expected cost boundary

At `K=40`, the four headline cells alone require 160 audience calls per
repository (480 across the trio), plus 120 author calls and failure-dependent
deep-dive/repair calls. Five repair rounds can dominate the total. Therefore
the ten-API end-to-end protocol pilot is mandatory before authorizing the
production run. Existing ten-entry generation artifacts can inform manual
review but are regenerated after representative sample freeze.
