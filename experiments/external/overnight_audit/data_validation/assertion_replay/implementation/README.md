# Isolated Thumbnailator assertion replay

The user authorized this secondary replay on September 7, 2026. Preserve all
current measured runs. Report their native outcomes alongside assertions-on
replay outcomes. A replay cannot certify the entire documentation-repair
pipeline and does not change its repair decisions.

Run from the infrastructure repository with Python 3 and the pinned Java 8:

```sh
python3 -m experiments.external.assertion_replay \
  --workspace-parent /path/to/worktrees \
  --out /path/to/audit/experiments/external/overnight_audit/data_validation/assertion_replay \
  --work /path/to/isolated/replay-work \
  --java-home /path/to/java8
```

Add `--watch` for automatic processing of later native results. The process
locks its output namespace and caches each replay by engine, native row,
source, Java version, library and fixture hashes. It handles A2 first, then
A1, then available B1/B2 evidence. A1 partial snapshots use only the explicitly
approved checkpoint compatibility groups. B cells wait for final native JSON.
The watcher exits after all four native finals have been processed. A failed
invocation can safely resume; it never deletes earlier attempts.

No LLM or provider client is imported. There is one replay child at a time,
with 256 MB Java heap limit and the native per-cell execution timeout. Compiler
timeout is 60 seconds. Only the replay's own child process group is killed on
timeout. No experiment worker or observer is stopped or restarted.

`evidence.py` captures native records and assembles retained code;
`execute.py` compiles and executes; `report.py` writes JSON, Markdown and an
offline searchable HTML table; `__main__.py` owns locking, preflight and polling.
Outputs are confined to the supplied output/work directories. Existing report
observers own other filenames. The existing deadline data snapshot includes
this output namespace.

## Evidence and isolation rules

- Passing native JSON includes full generated code and can recover overwritten
  retained snippets. On this case-insensitive filesystem, `Region`/`region`
  and `Watermark`/`watermark` share old paths. Replay directories use hashes.
- Failed native JSON may truncate code at 1,000 characters. Reuse the retained
  full harness only if its normalized code begins with that recorded prefix.
  This is prefix evidence, not a historical full-file hash attestation.
- Legacy rows lacking native code remain explicitly unbound diagnostics;
  ambiguous case-colliding rows are skipped. Provider failures never reuse
  stale files as evidence for the failed provider attempt.
- Only absolute path literals are rebased. Fixture bytes are copied unchanged;
  the negative EXIF fixture is preserved. Generated test logic is not repaired.
- Each test is compiled once and executed with `-da` and `-ea`, using separate
  fresh writable directories. A Java 8 security policy denies network,
  process execution and writes outside the variant's directory. Preflight
  exercises these denials and a deliberately false assertion after markers.
- Fresh outputs and the isolation policy can change outcomes relative to the
  original shared output directory. Use the assertions-off control to identify
  these differences; do not attribute every native-to-replay change to `-ea`.
- Assertions-on acceptance still needs independent target-call, input and
  oracle review. It is not a correctness-certified readiness score.

Verification:

```sh
python3 -m unittest experiments.external.assertion_replay.test_replay
```

Native source paths/hashes, code bindings, relocation mappings, fixture/JAR
hashes, exact commands, exit codes and output tails are in `cases/*.json`.
`summary.json`, `REPORT.md`, and `REPLAY.html` show the separate denominators.
Historical case files are retained after parser or evidence revisions. Count
only the cases referenced by the current summary, not every file in `cases/`.
The September 7 Java-octal-literal parser fix has an explicit compatibility
record proving byte-identical relocated source/mappings for reused executions.
