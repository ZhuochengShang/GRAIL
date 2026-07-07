# README Generation — Version A (static grounding) vs Version B (execution-first)

_Purpose: a second generation strategy to run **alongside** the current pipeline so the two can be compared on the same RDPro function set. Version B is the "learn by trying first" idea, positioned against prior work with concrete things to borrow._

---

## The two versions

**Version A — static-grounding-first (current pipeline).**
Enumerate public functions → intent-score to the commonly-used set → for each function build the doc from whatever static evidence exists: an existing **test**, the **original README**, a **sibling** method on the same class, ranked by grounding tier (verified > grounded > sibling > guessed). Then generate a test/usage snippet **from the doc**. Direction: **doc → test**.

Failure mode (observed): a function with no test, no README mention, and no sibling has nothing to ground on → the doc is signature-only ("guessed" tier) → the downstream snippet fails to compile or run. This is exactly the `guessed_that_failed_execution` set the grounding report already flags.

**Version B — execution-first ("try first").**
For a function (especially a zero-grounding one), **probe it directly**: synthesize plausible inputs from its type signature, run it in a small sandbox, and capture what actually worked (and what threw). Generate the doc **from the execution evidence** — a compiled-and-ran example plus observed input/output shapes and contracts. Direction: **execution → doc**.

Best case is the inverse of A's: B is _strongest_ exactly where A is weakest (undocumented functions), because it manufactures ground truth instead of needing it to pre-exist.

| | Version A (static) | Version B (execution-first) |
|---|---|---|
| Grounding source | existing test / README / sibling | live execution of the function |
| Direction | doc → test | execution → doc |
| Zero-grounding function | thin doc, downstream test fails | still yields a verified example (its best case) |
| Correctness signal | "doc looked plausible" | "compiled + ran" (+ mined invariants, see below) |
| Cost | cheap — no execution | expensive — needs runs, sandbox, small data |
| Main risk | hallucinated/ungrounded docs | compiled-but-semantically-wrong |
| Closest prior art | RepoAgent, LARCH, MAPO, Buse & Weimer | Randoop, Daikon, ChatTester / TestART, self-debug |

They are **complementary, not either/or**: B is the fallback branch that covers A's failure region, and A stays the cheap default where static evidence already exists.

---

## Related work, mapped

**Version A's neighbours — all static, none execute.**
- **RepoAgent** (Luo et al., EMNLP 2024 demo; arXiv 2402.16667): global structure analysis → doc generation → update; builds caller–callee structure by parsing. Repository-level, but purely static.
- **LARCH**: retrieval-augmented README generation — pulls representative code chunks to condition generation. The standard README-gen baseline in recent comparisons.
- **MAPO** (Zhong et al., ECOOP 2009) and **Buse & Weimer, "Synthesizing API Usage Examples"** (ICSE 2012): mine usage patterns/examples from a source corpus and render them as human-readable docs. Doc-shaped output, but static corpus mining.

→ Takeaway: the entire README/doc-generation line grounds on *text and static structure*. None run the code. That is the gap Version B occupies.

**Version B's roots — execution as the signal.**
- **Randoop — feedback-directed random testing** (Pacheco, Lahiri, Ernst, Ball, ICSE 2007): builds method-call sequences incrementally; each new input is executed and checked against contracts/filters, and the result decides whether it is illegal, redundant, or a useful building block for the next input. This is the canonical "sample → try → learn from pass/fail → extend" loop.
- **Daikon — dynamic detection of likely invariants** (Ernst et al., Sci. Comp. Prog. 2007): run the program, observe the values it computes, and report properties that held across runs (pre/postconditions, relationships like `y = 2*x+3`, `array sorted`). Explicitly used to *generate documentation and specifications*.
- **Krka et al., "Automatically Mining Specifications from Invocation Traces"** (FSE 2014): dynamic traces → behavioral specs. Same family as Daikon, trace-driven.
- **LLM + execution-repair for tests** — **ChatTester** (Yuan et al., FSE 2024; arXiv 2305.04207) feeds compiler errors back to refine generated tests (+34.3% compilable, +18.7% correct assertions); **TestART** (arXiv 2408.03095) co-evolves generation and repair; **CodaMosa** combines an LLM with search-based testing. The generate → run → repair loop is *standard practice in test generation*.
- **Self-debugging / execution-guided generation** (e.g. "Teaching LLMs to Self-Debug"; execution-guided within-prompt, ICLR 2025): the LLM iterates on code using execution feedback, typically a few attempts.

**Evidence that the output shape is right** — **ReadMe.LLM** (arXiv 2504.09798): human-oriented docs are weak context for LLMs. No-context baseline ≈ **30%** task success; function info *or* examples each raise it to **64%**; **README + functions → 88%**; examples alone → **96%**; combined → near **100%**. This directly supports building the doc as *verified functions + examples*, not prose — and it hands you a ready evaluation metric.

---

## What to borrow (each mapped to an `aideal` module)

1. **Randoop's building-block reuse** → the missing half of your loop.
   You already prune with the error log (failed combos logged, replayed as `failures_for`). Randoop's other half is that *successful* inputs become the arguments for the next call. Borrow it: a verified object/value from one probe becomes a candidate input for the next. **Improve on it** with a *typed* selector instead of random args — this is your unbuilt type-signature index (pipeline gap #1): sample within type-compatible candidates, not the raw function list.

2. **Daikon's invariant mining** → the answer to "compiled ≠ correct."
   Don't stop at "it ran." Over the probe runs, record observed input/output shapes and simple relations, and write them into the doc as pre/postconditions. This upgrades a Version-B entry from *"here's a call that ran"* to *"here's a call that ran, and here's the contract it obeyed"* — the single biggest differentiator from plain execution-verification, and a direct mitigation for the semantic-correctness risk. Lands as a new field in the `error_log` `pass` record and a new README section.

3. **ChatTester/TestART repair loop** → you already have it.
   `comprehension --execute` (doc_checks.py ~L585–665) generates a snippet, compiles+runs, retries with fix hints, logs pass/fixed/fail. The one change for Version B: seed the snippet from the **signature + a type-matched verified input**, not from `entry.body` (the doc). That flips A → B for the zero-grounding case without new infrastructure.

4. **ReadMe.LLM's output contract + metric** → structure and score.
   Emit functions + verified examples (you do this; `augment_from_log` promotes `status:pass` snippets into "Valid Call Patterns"). Adopt their metric — *task success rate with vs. without the generated doc* — which is exactly what your K-function `puzzle_eval.py` already measures. That makes A-vs-B a single clean number.

---

## Positioning (the one-sentence novelty)

> Execution-grounded generation is standard for **tests** (Randoop, ChatTester) and dynamic **spec mining** exists (Daikon), but README/library-doc generation is still **static** (RepoAgent, LARCH). Version B is execution-first *documentation* generation: probe undocumented functions, mine invariants from the runs, and write the doc from that evidence — then measure it with a composition (puzzle) test.

## Suggested comparison protocol

Same RDPro function set, same puzzle harness, three conditions:
1. **A** — current static-grounding docs.
2. **B** — execution-first docs (probe → run → invariant-mine → write).
3. **A+B** — A everywhere, B as the fallback for the "guessed" tier only.

Metric: puzzle-test success rate (compile + run + correctness witness) and % of entries reaching "verified" tier. Hypothesis: B ≫ A on the zero-grounding subset; A+B ≥ both overall at lower cost than B-everywhere.

---

## Sources
- ReadMe.LLM — https://arxiv.org/abs/2504.09798
- RepoAgent (EMNLP 2024) — https://arxiv.org/abs/2402.16667 · https://aclanthology.org/2024.emnlp-demo.46/
- Randoop / feedback-directed random testing (ICSE 2007) — https://homes.cs.washington.edu/~mernst/pubs/pacheco-randoop-oopsla2007.pdf
- Daikon (Sci. Comp. Prog. 2007) — https://plse.cs.washington.edu/daikon/ · https://dl.acm.org/doi/10.1016/j.scico.2007.01.015
- Krka et al., Mining Specifications from Invocation Traces (FSE 2014) — https://people.cs.umass.edu/~brun/pubs/pubs/Krka14fse.pdf
- ChatTester (FSE 2024) — https://arxiv.org/pdf/2305.04207 · https://dl.acm.org/doi/10.1145/3660783
- TestART — https://arxiv.org/html/2408.03095v2
- Buse & Weimer, Synthesizing API Usage Examples (ICSE 2012) — https://web.eecs.umich.edu/~weimerw/p/apidoc-icse12-final.pdf
- Self-debugging / execution-guided generation (ICLR 2025) — https://proceedings.iclr.cc/paper_files/paper/2025/file/98e967164ae2f6811b975d686dece3eb-Paper-Conference.pdf
