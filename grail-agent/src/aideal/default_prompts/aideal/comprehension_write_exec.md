SYSTEM:
You write {language} code that will be spliced into a runnable test harness.
{execution_context}

Pick the input variable(s) whose type matches the API's parameters. Do not
redeclare provided variables or write wrapper boilerplate unless the execution
context explicitly asks for it. Output ONLY the body statements that exercise the
API. Use ONLY the documentation provided. Output only code, no markdown fences.

{project_context}

USER:
Documentation:
{api_body}

Available input path variables already in scope (choose the matching one(s) by type):
{available_inputs}

RECEIVER — call `{api_name}` on the RIGHT type (calling it on the wrong receiver is
the #1 failure; if it is an instance method, first obtain a value of the owner type,
do NOT call it on an unrelated preloaded input):
{receiver}

{known_failures}

Write minimal body statements that use `{api_name}` correctly per the docs,
reading from the appropriate input variable(s) above.
{io_hints}
The snippet MUST EXECUTE the operation AND VERIFY the result is correct — not just
that it ran (some frameworks defer/lazily evaluate, and a wrong pixel TYPE can read
garbage without throwing). End with a CORRECTNESS CHECK:
- force the result to materialize and compute a small witness of it — a count, a
  size, or a sampled element;
- assert the witness is NON-DEGENERATE with `require(...)`, so a wrong type or an
  empty output fails loudly instead of silently passing. E.g.
  `require(n > 0, "empty result for {api_name}")`, or for a sampled numeric value
  require it is finite (not NaN/Inf) and in a plausible range;
- then print it as a STRUCTURED line exactly like:
  `println("__CHECK__ {api_name} " + <witness>)`.
If `{api_name}` is itself the writer/output API, write to `output_dir`, then
`require` the output exists / is non-empty and print the same `__CHECK__` line.
Do not call other heavyweight operations unless `{api_name}` is the writer; keep the
body focused on `{api_name}` so the run isolates that one call.
{exec_hints}
