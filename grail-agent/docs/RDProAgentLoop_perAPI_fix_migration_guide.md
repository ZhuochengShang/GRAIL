# Python -> Scala Section-by-Section Migration Guide

Target notebook:
- `RDProAgentLoop_perAPI_fix.ipynb`

Use this file as the instruction source for your coding agent so it fixes one section at a time.

## 1) Working Rules (apply to every section)

- Change only the current section scope.
- Keep behavior equivalent to Python unless a bug fix is explicitly requested.
- Use Scala with explicit types and clear error handling.
- Keep paths/config values externalized (no hard-coded local paths except existing constants).
- Log enough detail to debug failures in one run.
- Add a short section-level validation check before moving on.
- Stop after finishing one section and report status.

## 2) Standard Prompt Template (copy/paste)

```text
Task: Migrate only SECTION <SECTION_NAME> from Python to Scala.

Scope:
- Edit only: <cells/functions/files in scope>
- Do not modify other sections.

Behavior contract:
- Preserve Python behavior and outputs.
- Use Scala + Spark APIs where relevant.
- Add explicit type annotations.
- Handle null/empty/error cases.

Validation:
- Add or run a section-only validation.
- Print expected vs actual behavior.
- If validation fails, propose minimal fix in this section only.

Output format:
1) Files/functions changed
2) Scala code patch
3) Validation command(s)
4) Validation result
5) Remaining risks in this section
```

## 3) Migration Sections

### Section A: Runtime setup and paths

Scope candidates from notebook:
- Path constants and environment setup
- Spark classpath/jars and shell args setup

Goals:
- Keep one source of truth for directories.
- Validate required files/jars exist before run.
- Ensure Scala/Spark launch args are deterministic.

Done criteria:
- Setup compiles/runs and prints resolved paths/classpath.
- Missing file gives clear error message.

Prompt snippet:
```text
SECTION A: Runtime setup and paths
Focus on constants and environment assembly (run dirs, jars, spark args).
Do not touch fix-loop logic yet.
```

### Section B: Data loading

Scope:
- Data ingestion utilities and input initialization.

Goals:
- Load all required inputs in Scala.
- Validate existence, readability, and basic row/size expectations.
- Keep IO behavior equivalent to Python code.

Done criteria:
- Data load succeeds on sample input.
- Missing/corrupt input fails fast with actionable error.

Prompt snippet:
```text
SECTION B: Data loading
Implement Scala load step for each required input and add fail-fast checks.
Return structured load summary (path, rows/items, schema/basic info).
```

### Section C: Data type checks

Scope:
- Any schema/dtype checks currently done in Python logic.

Goals:
- Verify schema types, nullability, and required columns.
- Report column-level mismatches.
- Keep casting rules explicit; no silent lossy conversion.

Done criteria:
- Expected schema assertion passes on known-good input.
- Known-bad input fails with a clear per-column report.

Prompt snippet:
```text
SECTION C: Data type checks
Add schema validation for required columns and types.
Print mismatch report: column, expected type, observed type, nullable.
```

### Section D: Raster metadata checks

Scope:
- Raster metadata extraction/validation logic.

Goals:
- Check CRS, extent/bounds, resolution, width/height, band count, nodata.
- Enforce consistency checks required by downstream processing.
- Keep metadata checks isolated and reusable.

Done criteria:
- Valid raster passes all checks.
- Invalid metadata returns explicit reasons (not generic failure).

Prompt snippet:
```text
SECTION D: Raster metadata checks
Implement metadata validator in Scala for CRS, extent, resolution, dims, bands, nodata.
Return a structured validation report and fail on critical violations.
```

### Section E: Rule checks and guardrails

Scope candidates from notebook:
- Rule validators similar to: uniform integer assumptions, save rules, scaffold cleanup.

Goals:
- Port rule-check functions with same pass/fail behavior.
- Keep rule error messages stable and specific.

Done criteria:
- Rule tests pass for both allowed and disallowed cases.

Prompt snippet:
```text
SECTION E: Rule checks and guardrails
Port rule validators with equivalent behavior and explicit reasons for each violation.
```

### Section F: Run loop and logging orchestration

Scope candidates from notebook:
- run-and-log loop, fix turns, log parsing hints, success detection.

Goals:
- Reproduce loop behavior (run -> inspect -> fix -> rerun) with max-turn limit.
- Keep per-turn logs, command body snapshots, and summary status.
- Ensure deterministic stop conditions.

Done criteria:
- Loop exits on success or max turns exactly as defined.
- Every turn writes logs with timestamp and decision reason.

Prompt snippet:
```text
SECTION F: Run loop and logging orchestration
Port iterative run/fix loop with identical stop conditions and turn-level logging.
```

## 4) Tracking Table

Update this after each section:

| Section | Status | Owner | Last update | Notes |
|---|---|---|---|---|
| A Runtime setup and paths | Not started | | | |
| B Data loading | Not started | | | |
| C Data type checks | Not started | | | |
| D Raster metadata checks | Not started | | | |
| E Rule checks and guardrails | Not started | | | |
| F Run loop and logging orchestration | Not started | | | |

Status values:
- `Not started`
- `In progress`
- `Blocked`
- `Done`

## 5) Quick Execution Order

1. Finish A before any other section.
2. Finish B then C (schema checks depend on loaded data).
3. Finish D before rule checks that assume valid metadata.
4. Finish E before F.
5. Only start full end-to-end test after A-F are all `Done`.
