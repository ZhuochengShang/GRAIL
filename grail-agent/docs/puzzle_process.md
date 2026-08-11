# AIDEAL puzzle process and generalization boundary

## Verdict

The puzzle **control process is general**, but the checked-in end-to-end
executor is still an RDPro adapter. This is the intended AIDEAL layering:
AIDEAL freezes experimental inputs and invokes an application-owned runner;
it does not know how every target library compiles code or validates scientific
outputs.

The current implementation is therefore *generalizable and ablation-ready*,
not yet *application-independent end to end*.

## General AIDEAL control plane

`aideal puzzle-plan` owns the parts that must be identical for any codebase:

1. Load a JSON/YAML test bank with stable case IDs.
2. Validate referenced API names against the generated documentation surface.
3. Resolve a JSON/YAML sample-data manifest.
4. Select explicit cases or a seeded sample without replacement.
5. Freeze fixture, companion-file, bank, sample-manifest, and optional oracle
   SHA-256 hashes into one plan.
6. Reject the run if a frozen input has drifted.

`aideal puzzle` owns the experimental arms:

- original, generated, combined, or explicit documentation snapshot;
- composition versus discovery;
- memory on versus off;
- model/provider override;
- stable tag, plan, and report provenance;
- one application-provided command with bounded repair.

These modules contain no RDPro API names or geospatial schema:

- `aideal.puzzle_bank`
- the `puzzle-plan` CLI command
- the frozen-plan and documentation-arm logic in `aideal.doc_checks`

The synthetic unit tests use fictitious `loadRaster`/`writeRaster` APIs and do
not import RDPro, which checks this boundary mechanically.

## Application adapter boundary

Each target codebase still supplies:

- `puzzle.command`, scaffold, runtime arguments, and output directory;
- a program-generation/compile/run adapter;
- interpretation of output contracts and semantic oracles;
- optional capability equivalence when multiple API sequences are valid.

For RDPro, this adapter is currently
`rdpro_section_codegen.puzzle_eval`. It understands Scala/Spark execution,
checks exact API coverage in composition mode, and requires the declared output
artifact to exist. The RDPro project supplies its five-case bank, geospatial
fixtures, upstream/alias backend overlays, and scientific output contracts.

## What is and is not scored today

The version-2 puzzle report explicitly labels its primary score
`execution_and_output_contract`. It separately records:

- section-agent execution success;
- exact API coverage for composition cases;
- required output existence;
- semantic status.

Semantic status remains `not_evaluated` until an application adapter actually
runs a frozen oracle/comparator. Merely including and hashing an oracle in the
plan does not make a semantic correctness claim.

## Remaining work before claiming universal end-to-end support

1. Define a small runner-result protocol so Python, Java, Scala, and other
   adapters return the same fields without AIDEAL parsing console text.
2. Add an optional semantic-comparator hook and normalized output artifact
   contract. RDPro needs CRS/grid/type/nodata and CSV schema/value checks;
   another library can provide different checks.
3. Standardize capability policies for tasks where equivalent API sequences
   are valid. Exact name coverage is adequate only for API-combination tests.
4. Record the executable backend artifact hash or source commit/dirty patch,
   not only the configured library directory.
5. Demonstrate a second, non-geospatial adapter with the same frozen-plan
   schema and report contract.

Until items 1–5 are complete, paper wording should say that AIDEAL provides a
general puzzle experimental protocol with an RDPro execution adapter, rather
than claiming one universal puzzle executor.
