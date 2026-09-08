# Input and execution contracts

Configuration is not proof that the generated snippet used the right input.
There are three separate checks: the configured fixture exists; the harness
binds it with the right role; the generated code actually uses it correctly.

## Fixes owned by AIDEAL

`input_contract.prepare()` validates configured input files and creates the
condition-owned output directory. It refuses missing files, external output
paths and an existing file where a directory is required. Input fixture bytes
are hashed and never edited. The four newly enrolled baseline retry workers
use this setup check when they start naturally. Previous test outcomes remain
unchanged and retain their original setup provenance.

Use explicit roles in future matched prompt/harness versions:

| Binding | Role | Required behavior |
|---|---|---|
| `grid_png`, `beat_reference_file` | input_file | Read this exact existing path; do not guess sibling files |
| `output_dir` | output_directory | Harness creates it; write child files inside it |
| `outputPath` ending in `thumbnail.png` | output_file | Use it as the destination file; never append child paths |
| `ref_intervals` | array, shape (n,2) | Pair with n pitches/labels where required |
| `ref_freqs` | frequency array | Do not assume it has the same length as every interval fixture |

`input_contract.guidance()` renders exact paths and roles without losing them
when preloaded typed variables are added. It is available for a new matched
prompt version. It is NOT silently appended to this study's frozen prompts.

## Observed cases

- mir_eval load_key/load_tempo/load_wav: the scaffold bound output_dir but did
  not create it. Input-file preparation failed before the named API was called.
  Directory creation is an AIDEAL setup correction, not a Gemini code fix.
- Thumbnailator FileImageSink/FileThumbnailTask/allowOverwrite: outputPath was
  already a file path. Appending another filename was a generated-code error.
  Correct the binding guidance in the next matched condition, but do not rewrite
  the generated snippet or credit a native pass in this condition.
- mir_eval load_patterns: the model guessed an unconfigured pattern/reference.txt.
  No checked-in fixture was supplied under that variable. Preserve this failure;
  a future per-API fixture manifest needs an explicit valid pattern input.

## Outcome language

- Provider pending: no usable generation result; no code execution this attempt.
- Compile failed: code was generated, but the test did not execute.
- Setup/import blocked: dependency or initialization failed; target reach unproven.
- Execution failed: the test ran and failed; it may fail before the target call.
- Passed native checks: the harness accepted the test. This does not independently
  prove a correct oracle, target reach, or full semantic correctness.

Do not replace Gemini's wrong calls, shape assumptions, fabricated paths or
incorrect assertions with hand-written successes. Keep harness-corrected replay,
assertion replay, source recovery and native scores separately labelled.
