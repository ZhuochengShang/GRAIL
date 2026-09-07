# AIDEAL five-repository execution status

Status timestamp: 2026-09-06, America/Los_Angeles. Deadline discussed: Wednesday,
2026-09-09.

## Executive status

No new paid production run has been started from the corrected configuration.
That is intentional: the restart fingerprint and YAML isolation defects had to
be corrected first, and two protocol requirements currently conflict with the
Wednesday deadline.

| Repository | Declared experimental surface | Raw current surface | A1 | A2 | B1 | B2 | Corrected YAML |
|---|---:|---:|---|---|---|---|---|
| RDPro | 88 shared APIs | historical larger inventories exist | reusable 37/88 | old unmatched 73/163 scored | missing | old unmatched 132/165 scored | profile/fixtures/protocol corrected; clean worker still needs pinned Beast + manifest |
| tslearn | 99 intended APIs | 245 | historical 71/99, scaffold-confounded | historical 83/99, scaffold-confounded | repair only; no final | repair only; no final | four isolated rerun configs added and validated |
| MDAnalysis | unresolved | 1,032 | incomplete 52/301 checkpoint | historical contaminated 447 pass/661 | missing | repair exists; final only 18/661 | 13 configs corrected/validated; B1 and denominator unresolved |
| Thumbnailator | 149 full names | 149 | not run | not run | not run | not run | ready; 149 names, valid image fixtures, Java 8 harness green |
| mir_eval | 148 full names | 148 | not run | not run | not run | not run | ready; 148 names, 387 test-data files, Python 3.10 upstream tests green |

"Historical" means diagnostic evidence, not a cell that may be combined into a
new 2x2 table. A valid table requires the same manifest, documentation scope,
scaffold, command, source, fixtures, dependency environment, models, and zero
snippet-fix rounds in all four headline evaluations.

## Meaning of A1, A2, B1, and B2

```text
                             documentation treatment
                                      |
                 +--------------------+--------------------+
                 |                                         |
            original docs                              generated docs
                 |                                         |
       A1: zero-round evaluation                 A2: zero-round evaluation
                 |                                         |
       repair A1 documentation                   repair A2 documentation
       (deep-dive-first, <=5 rounds)              (deep-dive-first, <=5 rounds)
                 |                                         |
       B1: fresh zero-round evaluation            B2: fresh zero-round evaluation
                 +--------------------+--------------------+
                                      |
                    matched 2x2 validation + failure audit
```

The repair loop is the treatment. B1/B2 headline evaluation is therefore a new
zero-round audience run; historical snippet-fix results are not B1/B2.

## Crash-safe execution design

```text
static YAML/profile/fixture gate
             |
      PASS_TO_PASS before
             |
    frozen setup commit + environment inventory
             |
     separate branch and worktree per cell
             |
       dependency-aware watchdog (max 3 workers)
             |
     +-------+-------+
     |       |       |
   worker 1 worker 2 worker 3
     |       |       |
 shared Gemini start-time gate (one request start per >=3 seconds)
     |       |       |
 per-API JSONL checkpoints + atomic final JSON
             |
 transient provider rows retried under the same full fingerprint
             |
      PASS_TO_PASS after
             |
 per-function MD + CSV + JSON failure evidence
             |
       explicit commit and push from each worktree
```

Implemented controls:

- `grail-agent/src/aideal/llm.py` uses a process-shared locked rate-state file.
- `grail-agent/src/aideal/doc_checks.py` fingerprint schema 2 includes model,
  full effective execution YAML, scaffold bytes, source bytes, fixture bytes,
  engine bytes, interpreter, environment inventory hash, manifest, and delivered
  documentation. Changed inputs make old checkpoints ineligible.
- Transient `llm-error` rows are never reusable and must be retried.
- `experiments/external/run_condition_watchdog.py` enforces dependencies,
  at most three concurrent worktrees, atomic results, bounded job runtimes,
  indefinite restart by default, plan-hash protection, single-supervisor locking,
  optional `caffeinate`, and optional post-success commit/push commands.
- `experiments/external/analyze_failures.py` produces per-function category,
  exact error, diagnosis, definition site, reached codebase frames, attempts,
  wall time, and token use in Markdown, CSV, and JSON.
- `experiments/external/validate_experiment_yaml.py` is a zero-LLM preflight for
  profile knowledge, 50--200 full-surface gate, source/tests/docs, fixtures,
  model roles, scaffolds, and condition path isolation.
- The GitHub finder now records the query label, requires a 50--200 heuristic
  surface and checked-in sample-data files, and implements the published score
  exactly. Hidden PyPI/library bonuses were removed from ranking. The sweep
  script currently contains 22 domain queries (not 21), which is now recorded
  as an explicit protocol fact.

## Branch and worktree topology

Never switch branches underneath a running process. Each node below must be a
separate worktree.

```text
aideal/<repo>-freeze
  |-- aideal/<repo>-A1-zero --------> aideal/<repo>-B1-repaired-zero
  `-- aideal/<repo>-A2-zero --------> aideal/<repo>-B2-repaired-zero
```

For every branch:

1. Record upstream commit, config/profile/scaffold/fixture hashes and dependency
   inventory.
2. Run and record upstream tests before the AIDEAL condition.
3. Run with `--resume`; checkpoint rows are committed at fixed milestones.
4. Run upstream tests after treatment.
5. Generate failure reports and matched-table validation.
6. Commit only that condition's artifacts, then `git push -u origin HEAD`.

Existing dirty evidence worktrees must first be archived on explicit branches;
they must not be cleaned or overwritten.

## Repository-specific remaining work and failure evidence

### RDPro

Use the frozen 88-name shared manifest and relevant-document scope if the
deadline protocol is accepted. A1 is reusable at 37/88. Run A2 and B1 in
parallel, then B2 from the completed A2 branch. Existing A1 failures include 27
compile failures and 24 runtime/correctness failures. The old unmatched B2 has
16 compile, 17 runtime/correctness, and 6 infrastructure failures. Existing
detailed reports are `A1_FAILURE_DETAILS.md`, `A2_RESULT_MEMO.md`,
`RDPRO_FIX_ROUND_FAILURE_AUDIT_20260715.md`, and
`RDPRO_DOCFIX_OUTCOME_CODE_AUDIT_20260715.md` in the RDPro evidence worktrees.

Before launch, provision each clean worker with Beast commit
`547f7f912131a8032f6b5d26991415a5faf05cef`, its own built jars, and the 88-name
manifest. The infrastructure-template worktree does not yet contain those
gitignored inputs.

### tslearn

All four cells must be rerun. Historical A1 and A2 used different scaffolds,
which changes the audience task and invalidates a matched comparison. The new
four condition overlays share one infrastructure-only scaffold, pinned Python
3.10, pinned source/Trace fixture, balanced four-class data, and distinct paths.
Historical failure clusters are provider 504s, unavailable optional Keras,
wrong API ownership/imports, wrong shape/value expectations, and missing output
directories.

Important scope fact: 99 is the historical semantic intended surface; the raw
scanner finds 245 public names. The knowledge YAML now states this explicitly.

### MDAnalysis

The clean current scanner finds 1,032 names/1,397 definition sites. The old
661-name manifest contains nine helper/test contaminants. A1 is incomplete,
B1 is absent, and B2 final is incomplete. The invalid 286-name network file has
286/286 `ConnectError` and must never be used.

The corrected YAML pins Python, isolates all outputs, fixes adapter inheritance,
and exposes PDB/GRO/XTC/PSF/DCD plus the version-matched checked-in fixture tree.
Existing detailed reports identify wrong receivers/imports, insufficient fixture
variety, optional dependencies, missing periodic-box metadata, helper false
positives, and provider failures. A B1 document/config and valid denominator
still need to be defined.

### mir_eval

Query-qualified by the saved `audio processing` and `signal processing` sweeps.
The exact AIDEAL full surface is 148 names/179 definition sites. All four
condition YAMLs pass the static gate with distinct paths and no fixture warnings.
Pinned Python 3.10 upstream result: 535 passed, 3 skipped, 176 xfailed, 1 xpassed.
The Python 3.14/Matplotlib 3.11 image-baseline failures are environment mismatch,
not repository failures. Remaining work is README generation, frozen manifest,
A1/A2, B1/B2, before/after tests, analysis, commits, and pushes.

### Thumbnailator

The exact AIDEAL full surface is 149 names. All condition YAMLs pass the static
gate; checked-in PNG/JPEG/EXIF fixtures resolve; Java 8 build/Javadocs/harness are
green. Upstream result: 2,766 tests, 0 failures, 0 errors, 3 skipped. Remaining
production work is the same as mir_eval.

Selection caveat: Thumbnailator was manually proposed and is not present in the
saved top-10 domain sweep output. Its knowledge YAML records this truth. Running
it would require accepting a query-provenance exception or rerunning the
deterministic sweep and selecting a qualified image repository.

## Wednesday feasibility and the unresolved decision

The strict requirements cannot all be true simultaneously:

- no sampling / complete public surface;
- every repository has 50--200 APIs;
- all five complete by Wednesday;
- keep MDAnalysis and tslearn.

MDAnalysis has 1,032 raw names and tslearn has 245. Historical MDAnalysis timing
projects roughly 50+ hours for its full four-cell pipeline before contention.
Thumbnailator also fails the saved-query provenance rule.

Two honest execution choices are therefore:

1. **Wednesday protocol:** grandfather RDPro's 88 and tslearn's 99 frozen
   intended surfaces, define a <=200 coherent MDAnalysis intended surface, and
   accept Thumbnailator's provenance exception. This prioritizes the deadline
   but is not a strict raw-full-surface study.
2. **Strict protocol:** run all 245 tslearn and 1,032 MDAnalysis names and replace
   or re-qualify Thumbnailator. This preserves the rule but cannot be promised by
   Wednesday.

No supervisor plan should be launched until this choice is recorded, because it
changes the denominator and scientific claim.
