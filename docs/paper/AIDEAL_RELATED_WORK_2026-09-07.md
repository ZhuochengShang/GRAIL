# AIDEAL paper: related work and defensible positioning

**Research date and cutoff:** September 7, 2026. **Audience:** AIDEAL authors and reviewers. **Scope:** API usability, documentation-conditioned code/tool use, repository context, executable evaluation, feedback-based refinement and human-reviewed improvements. This is a targeted primary-source review, not a systematic review or proof of absence of other work. Results in cited studies are author-reported, not reproduced here.

## Executive finding

AIDEAL enters an established and rapidly developing research area. Its paper should lead with an **auditable empirical assessment of documentation-conditioned public-library API use**, rather than claiming the first agent-readiness framework, documentation optimization loop, or human-reviewed remediation system. Close precedents cover each of those ideas: REST API readiness testing, execution-driven documentation rewriting, repository guidance refinement, and commercial readiness/remediation products. [REST API readiness framework](https://arxiv.org/html/2504.15546v3), [DocsChisel](https://arxiv.org/html/2608.10037v1), [Probe-and-Refine](https://arxiv.org/html/2606.20512v2), [Factory Agent Readiness](https://factory.ai/news/agent-readiness).

**Proposed positioning, based on this review:** AIDEAL makes the evidence behind API usability inspectable: a frozen public-API denominator; versioned code, documentation, data and harness; matched original/generated and before/after-repair treatments; failure and intervention histories; and reviewable improvement records. The contribution must be demonstrated by completed results, stronger oracle checks and useful empirical findings. Combining existing ideas into a pipeline is not by itself evidence of a new scientific contribution.

The present study supports a narrow construct: *how successfully a configured LLM can use supplied APIs from a documentation treatment under a prepared harness*. It does not yet establish autonomous repository discovery, environment installation, scientific workflow competence, or universal codebase quality. See the implementation [code guide](../../AIDEAL_CODE_GUIDE.md) and [data/methods appendix](../../experiments/external/FINAL_REPORT_DATA_AND_API_METHODS.md).

## Closest work: compare these first

| Prior work | What it already establishes | AIDEAL comparison to make |
|---|---|---|
| **Bandlamudi et al., REST API readiness framework** — 2025 preprint | Tests direct and agent-mediated API calls, uses data-aware dependencies, classifies errors, recommends changes and includes Tool Builder review. [v3 methods](https://arxiv.org/html/2504.15546v3) | Public source-library APIs versus enterprise REST wrappers; coverage accounting, native failure provenance and matched documentation treatments. Readiness and human input are not new by themselves. |
| **DRAFT** — ICLR 2025 | Explorer, analyzer and rewriter improve documentation through tool interactions, with diversity and termination controls. [Official paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/8c22e5e918198702765ecff4b20d0a90-Paper-Conference.pdf) | Direct execution-feedback document-repair baseline; compare under the same source access and generation budgets. |
| **DocsChisel** — August 2026 preprint | Diagnoses failed agent traces and changes documentation fields, with memories, validation and regression checks. [Methods and evaluation](https://arxiv.org/html/2608.10037v1) | Direct adaptive-refinement baseline; report source/fixture barriers and held-out behavior, not merely repair-loop success. |
| **PLAY2PROMPT** — Findings ACL 2025 | Uses tool play to obtain examples and optimize tool instructions. [Publication](https://aclanthology.org/2025.findings-acl.1347/) | Compare execution-derived examples and optimization costs with AIDEAL generation and repair. |
| **Doc2OracLL** — FSE/PACMSE 2025 | Studies documentation conditions for test-oracle generation, including developer versus generated documentation. [Author paper](https://arxiv.org/html/2412.09360v2) | Closest test-generation measurement precedent; AIDEAL's passing test and a fault-revealing oracle are different outcomes. |
| **Probe-and-Refine** — June 2026 preprint | Refines repository guidance through synthetic probes and evaluates downstream coding issues. [Methods](https://arxiv.org/html/2606.20512v2) | Its tuning uses single-shot simulated judgments without executable tools; AIDEAL uses executed API failures. Evaluate transfer beyond repair cases. |
| **Tessl API evaluations** — January 2026 technical report | Evaluates structured versioned context for public-library API tasks in isolated environments. [Primary report](https://tessl.io/blog/fixing-api-misuse-how-tessl-improves-agent-accuracy-by-up-to-33x) | Direct industry overlap in library use; do not claim API-documentation evaluation as a new category. |
| **Factory Agent Readiness** — January 2026 product announcement | Scores repository readiness, prioritizes changes and offers agent remediation PRs. [Dated announcement](https://factory.ai/news/agent-readiness) | Compare executed behavioral evidence with repository rubric signals. AIDEAL's queue currently records review; it does not launch remediation. |

### Details that materially change the comparison

**Version control matters in the literature too.** The REST-readiness paper's September 2025 v3 reports 2,411 retained natural-language test cases and adds data-aware Tool Dependency Graphs, builder approval of mappings and an ADK CLI. Its earlier v1 reports 750 cases. The method treats direct execution as a reference for agent calls; it does not eliminate all specification/oracle validity questions. Cite one version consistently. [Bandlamudi et al., v3](https://arxiv.org/html/2504.15546v3).

**Held-out evaluation is already present in close work.** DocsChisel uses 74 tools and 2,072 queries split into optimization, validation and test sets; 829 test queries are held out. It repeats optimization and evaluation. AIDEAL's fresh B snippets avoid copying successful repair tests, but the same API and adapted documentation remain in scope. That is not equivalent to an untouched task/fixture test set. [DocsChisel, §III–IV](https://arxiv.org/html/2608.10037v1).

**DRAFT already includes explainable revision trajectories and human documentation assessment.** AIDEAL should not present a traceable author/audience/fixer loop or human review alone as unprecedented. Its measured distinctions must concern the assessment unit, interventions, attribution quality, reproducibility and resulting insights. [DRAFT, methods, experiments and appendices](https://proceedings.iclr.cc/paper_files/paper/2025/file/8c22e5e918198702765ecff4b20d0a90-Paper-Conference.pdf).

## Literature map and implications

### 1. API usability predates LLMs

Human API-learning research identifies documentation, examples, intent and task-to-API mapping as important obstacles. Cognitive-dimensions work evaluates class-library usability rather than relying only on internal code complexity. AIDEAL can extend this line to a model–task–environment setting, but human usability findings should motivate hypotheses rather than be assumed to transfer unchanged to agents. [Robillard and DeLine, 2011](https://www.microsoft.com/en-us/research/publication/field-study-api-learning-obstacles/), [Clarke and Becker, 2003](https://www.ppig.org/papers/2003-ppig-15th-clarke/).

Documentation failures themselves have a substantial empirical history. Ground AIDEAL's taxonomy in that literature, then distinguish LLM-specific errors such as hallucinated identities, invalid receivers and misleading generated assertions through independent evidence. [Uddin and Robillard, 2015](https://www.cs.mcgill.ca/~martin/papers/ieeesw2015.pdf).

### 2. Supplying documentation and optimizing documentation are different interventions

DocPrompting retrieves documentation to condition code generation. CloudAPIBench examines API hallucination and documentation augmentation, including retrieval relevance; its call-validity checks are not equivalent to complete task semantics. These motivate separating *finding relevant information* from *using a supplied document*. AIDEAL's relevant-document scope must be documented precisely. [DocPrompting](https://arxiv.org/pdf/2207.05987), [On Mitigating Code LLM Hallucinations with API Documentation](https://arxiv.org/html/2407.09726).

EasyTool is an important simple baseline: concise, standardized descriptions, parameter guidance and examples. More elaborate refinement should demonstrate value beyond a straightforward structured rewrite. [EasyTool, NAACL 2025](https://aclanthology.org/2025.naacl-long.44/).

Recent methods extend this space further. Trace-Free+ trains description rewriting using execution-derived supervision; JTPRO jointly optimizes instructions and tool/argument descriptions. AIDEAL should freeze global prompts during the current document-treatment comparison and study joint prompt/skill optimization separately. [Learning to Rewrite Tool Descriptions](https://arxiv.org/html/2602.20426v1), [JTPRO](https://arxiv.org/html/2604.19821v1).

### 3. Repository instructions have conditional, sometimes negative effects

Evaluating AGENTS.md compares absent, generated and developer context across repository tasks and finds no general success improvement, with increased average inference cost. Its June 2026 v2 uses the name **CTXbench**; older summaries may use AGENTbench and different headline numbers. [Evaluating AGENTS.md, v2](https://arxiv.org/html/2602.11988v2).

A separate paired study reports efficiency benefits from AGENTS.md but explicitly does not comprehensively evaluate semantic correctness. A smaller two-agent ablation reports bounded null effects under its selected tasks. These are not interchangeable measures or populations; together they argue for reporting correctness, cost and negative transfer separately. [Lulla et al.](https://arxiv.org/abs/2601.20404), [Khatri, 2026](https://arxiv.org/html/2607.27250v1).

Agent READMEs provides a descriptive taxonomy of repository context files; it does not show that every instruction category improves task outcomes. Agent Retrieval Bench evaluates repository context retrieval and explicitly separates retrieval from patch success. These are useful foundations for AIDEAL's currently unmeasured discovery capability. [Agent READMEs](https://arxiv.org/html/2511.12884v1), [Agent Retrieval Bench](https://arxiv.org/html/2607.24882v1).

### 4. Executability, correctness and acceptance must remain distinct

SWE-bench tests repository issue resolution against historical states, while SWE-agent shows that the interface used by an agent affects its behavior. Their role here is to motivate fixed harnesses and a broader future behavioral benchmark, not to suggest that one-API tests already measure repository maintenance ability. [SWE-bench](https://www.swebench.com/original.html), [SWE-agent](https://arxiv.org/abs/2405.15793).

DS-1000 combines executable data-science tasks with constraints and reviewed tests. SciCode uses scientist-curated tasks and domain checks. Both are important for tslearn and MDAnalysis: numerical execution alone does not establish scientifically meaningful inputs or outputs. [DS-1000](https://proceedings.mlr.press/v202/lai23b.html), [SciCode](https://arxiv.org/html/2407.13168).

EvalPlus shows why weak test suites can miss wrong generated programs. Doc2OracLL directly studies documentation's effect on generated assertions. Agent-Diff evaluates state changes in enterprise API tasks rather than relying solely on call syntax. These suggest three separate AIDEAL outcomes: runnable test, semantically valid test, and strength at detecting incorrect behavior. [EvalPlus](https://arxiv.org/html/2305.01210), [Doc2OracLL](https://arxiv.org/html/2412.09360v2), [Agent-Diff](https://arxiv.org/html/2602.11224v1).

A recent oracle-audit preprint cautions that invalid inputs and a single reference implementation can produce apparent improvement. It compares feedback with resampling/placebo conditions and explicitly acknowledges qualification amendments and diagnostic limitations. Treat it as timely methodological evidence, not a settled universal conclusion. [Liang et al., August 2026](https://arxiv.org/html/2608.19626v1).

Finally, METR's maintainer study finds that passing benchmark tests does not ensure a patch would be accepted. Its historical tasks, selected repositories and review setup constrain generalization, but it gives a concrete rationale for keeping AIDEAL's human acceptance stage separate from automated test status. [METR, March 2026](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/).

### 5. Iteration, feedback and readiness products already have substantial prior art

Self-Refine iterates generation, feedback and revision; Reflexion stores linguistic feedback for later trials. TextGrad and GEPA optimize text components using model feedback and observed trajectories. AIDEAL's repair loop should be compared with equal-budget alternatives before attributing gains specifically to diagnosis rather than more attempts. None of these frameworks is used automatically merely because it is cited here. [Self-Refine](https://arxiv.org/abs/2303.17651), [Reflexion](https://arxiv.org/html/2303.11366), [TextGrad](https://arxiv.org/abs/2406.07496), [GEPA](https://arxiv.org/abs/2507.19457v2).

Industry practice is also close. Tessl describes with/without-skill task evaluations and iterative refinement; Anthropic documents evaluation-driven tool development with agents. Cite these as dated first-party engineering reports, not peer-reviewed evidence of universal benefit. [Tessl Task Evals](https://tessl.io/blog/introducing-task-evals-measure-whether-your-skills-actually-work), [Anthropic tool engineering](https://www.anthropic.com/engineering/writing-tools-for-agents).

## What AIDEAL can claim now, and what needs evidence

| Candidate statement | Current assessment | What would justify a stronger claim |
|---|---|---|
| An implemented, auditable API-use assessment and review workflow | Supported by the current code/artifacts; operational success still depends on results | Release reproducible configurations, fixtures, ledgers and linked case studies |
| Documentation changes API-use outcomes | Research question; do not fill in an effect before cells finish | Complete compatible four-cell results, negative transitions and uncertainty |
| Documentation repair improves general agent readiness | Not established | Independent oracle audit, held-out workflows/fixtures and model transfer |
| Full public API coverage | A manifest claim, not behavioral completeness | Validate exports/owners/overloads and report exclusions, missing prerequisites and unreachable APIs |
| Every function receives correct data | Not established by paths, metadata or witness markers alone | Per-API contracts plus runtime target/dataflow evidence and independent semantic checks |
| The improvement queue improves maintainers' decisions | Implemented workflow, not evaluated benefit | Reviewed cases, accepted/rejected reasons, review time and validated outcomes |
| First agent-readiness or execution-driven documentation framework | Not defensible from the retrieved literature | Use a narrowly stated empirical contribution instead |

A useful measurement object is **R(repository revision, model, task, documentation, harness, data, budget)**. This is a proposed formalization for the paper, not an implemented universal score. Report capability-specific evidence and uncertainty rather than collapsing missing dimensions into a number.

## Recommended research questions and analysis

**RQ1 — Documentation treatment.** Under fixed source, manifest, data and harness, how do original and generated documentation affect observed API-use outcomes? Report A1 versus A2 on matched API identities, per repository and category, with the full frozen denominator and unresolved-provider counts.

**RQ2 — Repair and regression.** How do B1−A1 and B2−A2 differ? Report fail→pass, pass→fail, unchanged and unresolved transitions. The contrast `(B2−A2)−(B1−A1)` can describe differential repair response, but adaptive repairs, B1's `original+aideal` context and model stochasticity limit a simple factorial causal interpretation.

**RQ3 — Failure attribution.** How much observed failure is supported as documentation error, versus API identity, fixtures/contracts, scaffold/dependencies, assertion/oracle, or provider infrastructure? Keep native classification, model diagnosis and independently reviewed category separate. A model diagnosis is a hypothesis until checked.

**RQ4 — Cost and attempts.** How much time/tokens and how many provider attempts, test generations, document rounds and reversions lead to each outcome? Final code-fix rounds are zero in the current study. Unlimited supervisor retries are operational behavior, not evidence of agent learning. Treat incomplete runs as incomplete, not zero success or terminal code defects.

**RQ5 — Transfer and reviewer utility, for a subsequent protocol.** Do repairs help held-out tasks/fixtures and another audience model? Can reviewers validate and act on the queue accurately and efficiently? This is future work unless separately executed and measured.

For repeated experiments, preserve pairing and report repository/API clustering rather than treating every regenerated attempt as independent. Pre-specify uncertainty estimation, multiplicity handling and whether missing provider outcomes enter a sensitivity analysis. A single realization across three repositories warrants descriptive conclusions, not broad population claims. These are design recommendations, not analyses already run.

## Baselines and additions after the priority runs

1. **Simple rewrite baseline:** an EasyTool-like concise structure with matched source access and context budget. This tests whether elaborate diagnosis adds value beyond better formatting.
2. **Execution-refinement baseline:** adapt DRAFT or PLAY2PROMPT to the same library harness, documenting adapter deviations. Consider DocsChisel where task traces and held-out task sets exist. Do not copy their published scores into AIDEAL's result table.
3. **Equal-budget resampling:** regenerate tests/docs without detailed feedback using the same call budget; this helps separate feedback benefit from additional sampling.
4. **Independent validity audit:** stratify passes and failures, check canonical API invocation and meaningful input use, verify assertions against specifications/domain invariants, and test fault/mutation sensitivity where feasible. Reviewers should be blinded to treatment when practical.
5. **Transfer evaluation:** freeze unseen tasks and fixture variants before repair, then test separately. Changing prompts, data, harness or source creates a new protocol; preserve the existing measurements.
6. **Human review study:** record review time, accepted/deferred/rejected proposals, category agreement, changes requested, validated before/after behavior and regressions. Self-reported actor labels are an audit trail, not authenticated authorization.

No extra paid experiment or job restart was performed for this literature review.

## Suggested paper contribution paragraph

> We present AIDEAL, an auditable framework for assessing documentation-conditioned public-API usability and organizing evidence-backed improvements. AIDEAL connects a frozen API/data/environment protocol with original and generated documentation treatments, execution-informed document repair, and per-API outcome and intervention histories. Its assessment separates observed API execution from unmeasured readiness dimensions, while an evidence-versioned queue supports human review and human- or agent-executed improvements. Our evaluation investigates when documentation helps, which barriers persist, and what evidence is needed before a passing generated test can support a readiness claim.

This is proposed manuscript language describing the system and research questions. Add numerical contributions and demonstrated findings only after analysis; do not imply that the human workflow or transfer capability has already been experimentally validated.

## Draft related-work section

**API usability and documentation.** Human studies have long connected API learning difficulties to intent, examples, task mapping and documentation presentation. Agent-facing documentation inherits these concerns but requires empirical validation for a different consumer. DocPrompting and documentation-augmented API generation demonstrate ways to supply relevant information to code models, motivating a distinction between document retrieval and document usability. [Robillard and DeLine](https://www.microsoft.com/en-us/research/publication/field-study-api-learning-obstacles/), [DocPrompting](https://arxiv.org/pdf/2207.05987), [CloudAPIBench/DAG](https://arxiv.org/html/2407.09726).

**Documentation optimization.** EasyTool standardizes tool instructions; DRAFT and PLAY2PROMPT improve them through tool interactions. DocsChisel performs trace-driven field-level optimization, while recent methods learn rewrites or jointly optimize tool descriptions and global instructions. AIDEAL studies executable use of a frozen public-library API surface and preserves the provenance of outcomes and interventions. It builds on this optimization literature and does not claim that feedback-based rewriting itself is new. [EasyTool](https://aclanthology.org/2025.naacl-long.44/), [DRAFT](https://arxiv.org/html/2410.08197v1), [PLAY2PROMPT](https://aclanthology.org/2025.findings-acl.1347/), [DocsChisel](https://arxiv.org/html/2608.10037v1), [Trace-Free+](https://arxiv.org/html/2602.20426v1), [JTPRO](https://arxiv.org/html/2604.19821v1).

**Readiness and repository guidance.** REST-readiness testing already links data-aware API execution to error analysis and recommendations. Repository-context studies show conditional effects, and Probe-and-Refine tunes persistent guidance against synthetic probes. Industry systems additionally offer readiness scoring, remediation and context evaluations. AIDEAL's intended distinction is an inspectable assessment protocol and evidence trail for public-library API use, rather than the general concept of readiness or reviewed improvement. [REST-readiness framework](https://arxiv.org/html/2504.15546v3), [Evaluating AGENTS.md](https://arxiv.org/html/2602.11988v2), [Probe-and-Refine](https://arxiv.org/html/2606.20512v2), [Factory](https://factory.ai/news/agent-readiness), [Tessl API evaluation](https://tessl.io/blog/fixing-api-misuse-how-tessl-improves-agent-accuracy-by-up-to-33x).

**Evaluation validity and improvement acceptance.** Repository and scientific coding benchmarks motivate realistic tasks, fixed environments and independent correctness checks. Doc2OracLL and EvalPlus show why generated assertions and limited tests require scrutiny. Maintainer review studies further distinguish test passing from acceptable changes. AIDEAL therefore preserves native execution outcomes, separates semantic review from those outcomes, and treats human acceptance as a separate decision rather than an automatic score increase. [SWE-bench](https://www.swebench.com/original.html), [DS-1000](https://proceedings.mlr.press/v202/lai23b.html), [SciCode](https://arxiv.org/html/2407.13168), [Doc2OracLL](https://arxiv.org/html/2412.09360v2), [EvalPlus](https://arxiv.org/html/2305.01210), [METR](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/).

## Search and evidence limitations

Discovery used three lanes: documentation/API methods; repository readiness/context and review; and feedback/oracle validity. Follow-up traced references from the closest papers and checked their methods, versions and publication records. Search-engine relative dates were not used as publication dates. Preprints are labeled as such where no accepted venue was verified; vendor sources are separated from peer-reviewed studies.

The review includes full-method reads for the closest competitors and narrower abstract/official-overview reads for some background sources. DRAFT's official proceedings substituted for a challenged OpenReview page. Doc2OracLL methods were read from the author preprint after the DOI page failed. One old Tessl documentation URL returned 404; dated primary posts provide the cited evidence. We did not independently reproduce any literature results or comprehensively audit every replication package.

The newly posted [SWE-bench Science](https://arxiv.org/abs/2608.19799) is a relevant follow-up lead: its abstract concerns engineering tasks in scientific repositories. Full methods were not successfully reviewed in this pass, so it does not support a detailed comparison here.

Search stopped after direct novelty threats, counterevidence, measurement precedents and remaining gaps had primary support. This bounded review cannot establish an exhaustive novelty claim. Recheck versions and new publications before paper submission.

## Annotated reading list

Author lists are abbreviated for reading. Dates distinguish first posting from later publication/version where verified. The follow-up lead is not counted as a full-method review.

- **[A Framework for Testing and Adapting REST APIs as LLM Tools](https://arxiv.org/html/2504.15546v3)** — Bandlamudi et al.. 2025-04-22; v3 2025-09-12. arXiv preprint. full methods; v3 count differs from v1.

- **[From Exploration to Mastery: Enabling LLMs to Master Tools via Self-Driven Interactions](https://proceedings.iclr.cc/paper_files/paper/2025/file/8c22e5e918198702765ecff4b20d0a90-Paper-Conference.pdf)** — Qu et al.. 2024-10-10; ICLR 2025. ICLR 2025. official proceedings substituted for OpenReview challenge.

- **[DocsChisel: Adaptive Tool Documentation Optimization Framework for LLM Agents](https://arxiv.org/html/2608.10037v1)** — Lu, Zhang, Chen and Peng. 2026-08-10. arXiv preprint. full methods; not independently reproduced.

- **[PLAY2PROMPT: Zero-shot Tool Instruction Optimization for LLM Agents via Tool Play](https://aclanthology.org/2025.findings-acl.1347/)** — Fang, Zhang, Qian, Glass and Zhu. 2025-03-18; ACL July 2025. Findings ACL 2025. publication and paper read.

- **[EASYTOOL: Enhancing LLM-based Agents with Concise Tool Instruction](https://aclanthology.org/2025.naacl-long.44/)** — Yuan et al.. 2024-01-11; NAACL 2025. NAACL 2025. publication plus readable author methods.

- **[Learning to Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use](https://arxiv.org/html/2602.20426v1)** — Guo, Dong, Gao and Das. 2026-02-23. arXiv preprint. full methods.

- **[JTPRO: A Joint Tool-Prompt Reflective Optimization Framework for Language Agents](https://arxiv.org/html/2604.19821v1)** — Ghoshal et al.. 2026-04-20. arXiv preprint. backend response correctness not the reported metric.

- **[Doc2OracLL: Investigating the Impact of Documentation on LLM-Based Test Oracle Generation](https://arxiv.org/html/2412.09360v2)** — Hossain, Taylor and Dwyer. 2024-12-12; publication 2025-06-19. PACMSE 2(FSE), Article FSE084. author full text; publisher metadata via doi:10.1145/3729354.

- **[DocPrompting: Generating Code by Retrieving the Docs](https://arxiv.org/pdf/2207.05987)** — Zhou et al.. 2022-07-13; ICLR 2023. ICLR 2023. paper and official repository read.

- **[On Mitigating Code LLM Hallucinations with API Documentation](https://arxiv.org/html/2407.09726)** — Jain et al.. 2024-07-13; ICSE 2025. ICSE 2025 SEIP. signature-stub checks are not full semantic correctness.

- **[DS-1000: A Natural and Reliable Benchmark for Data Science Code Generation](https://proceedings.mlr.press/v202/lai23b.html)** — Lai et al.. 2022-11-18; ICML 2023. ICML 2023, PMLR 202. publication and paper read.

- **[SciCode: A Research Coding Benchmark Curated by Scientists](https://arxiv.org/html/2407.13168)** — Tian et al.. 2024-07-18. NeurIPS Datasets and Benchmarks 2024. paper; venue confirmed by author repository.

- **[Introducing Agent Readiness](https://factory.ai/news/agent-readiness)** — Factory. 2026-01-20. First-party product announcement. dated vendor claim; not a controlled independent study.

- **[Fixing API Misuse: How Tessl Improves Agent Accuracy by up to 3.3X](https://tessl.io/blog/fixing-api-misuse-how-tessl-improves-agent-accuracy-by-up-to-33x)** — Macey Baker, Tessl. 2026-01-22. First-party technical report. vendor aggregate results not reproduced.

- **[Introducing Task Evals: Measure Whether Your Skills Actually Work](https://tessl.io/blog/introducing-task-evals-measure-whether-your-skills-actually-work)** — Patrick Debois, Tessl. 2026-02-17. First-party product announcement. dated source replaces inaccessible legacy docs page.

- **[Probe-and-Refine Tuning of Repository Guidance for Coding Agents](https://arxiv.org/html/2606.20512v2)** — Asa Shepard and Jeannie Albrecht. 2026-06-18; v2 2026-06-19. arXiv preprint. tuning has no executable tool loop.

- **[Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?](https://arxiv.org/html/2602.11988v2)** — Gloaguen, Mündler, Müller, Raychev and Vechev. 2026-02-12; v2 2026-06-23. arXiv preprint. v2 name CTXbench; do not reuse outdated v1 summary.

- **[On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents](https://arxiv.org/abs/2601.20404)** — Lulla et al.. 2026-01-28; revised 2026-03-30. arXiv preprint. comprehensive semantic correctness explicitly outside scope.

- **[Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories](https://arxiv.org/html/2607.27250v1)** — Prakhar Khatri. 2026-07-28. arXiv preprint. small selected cohort; bounded null result.

- **[Agent READMEs: An Empirical Study of Context Files for Agentic Coding](https://arxiv.org/html/2511.12884v1)** — Chatlatanagulchai et al.. 2025-11-17. arXiv preprint. file mining does not establish treatment effectiveness.

- **[SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793)** — Yang et al.. 2024-05-06. NeurIPS 2024. historical benchmark results.

- **[SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://www.swebench.com/original.html)** — Jimenez et al.. 2023-10-10. ICLR 2024. official overview and conference metadata.

- **[Many SWE-bench-Passing PRs Would Not Be Merged into Main](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/)** — Whitfill, Wu, Becker and Rush. 2026-03-10. METR research note. selected repositories, historical issues, no revision opportunity.

- **[Agent Retrieval Bench: Evaluating Repository Context Retrieval for Coding Agents](https://arxiv.org/html/2607.24882v1)** — Bowen Qin and Yi Xie. 2026-07-27. arXiv preprint. file retrieval is not exact localization or resolution.

- **[Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation](https://arxiv.org/html/2305.01210)** — Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang and Lingming Zhang. 2023-05-02. Research paper; arXiv version cited. paper read; headline gains not imported.

- **[Auditing and Decomposing Feedback-Driven Evolution in LLM Test Generation under the Oracle Problem](https://arxiv.org/html/2608.19626v1)** — Liang, Gan, Ying, Wei, Cui and Ni. 2026-08-20. arXiv preprint. paper acknowledges qualification amendments and diagnostic limitations.

- **[Agent-Diff: Benchmarking LLM Agents on Enterprise API Tasks via Code Execution with State-Diff-Based Evaluation](https://arxiv.org/html/2602.11224v1)** — Author paper. 2026-02-11. arXiv preprint. methods read; complete author metadata not extracted.

- **[Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)** — Madaan et al.. 2023-03-30. Research paper; arXiv version cited. abstract-level background claim only.

- **[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/html/2303.11366)** — Shinn, Cassano, Berman, Gopinath, Narasimhan and Yao. 2023-03-20; v4 2023-10-10. NeurIPS 2023. primary full text accessible.

- **[TextGrad: Automatic Differentiation via Text](https://arxiv.org/abs/2406.07496)** — Yuksekgonul, Bianchi, Boen, Liu, Huang, Guestrin and Zou. 2024-06-11. arXiv version; later Nature article has different title. abstract-level background; Nature open failed.

- **[GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning](https://arxiv.org/abs/2507.19457v2)** — Agrawal et al.. 2025-07-25; v2 2026-02-14. ICLR 2026, per author metadata. HTML retrieval failed; narrow metadata/abstract claim.

- **[Writing effective tools for agents — with agents](https://www.anthropic.com/engineering/writing-tools-for-agents)** — Anthropic. 2025-09-11. First-party engineering article. engineering guidance, not peer-reviewed comparative evidence.

- **[A field study of API learning obstacles](https://www.microsoft.com/en-us/research/publication/field-study-api-learning-obstacles/)** — Martin P. Robillard and Robert DeLine. 2011. Empirical Software Engineering 16, 703–732. year used because primary listings differ on month.

- **[How API Documentation Fails](https://www.cs.mcgill.ca/~martin/papers/ieeesw2015.pdf)** — Gias Uddin and Martin P. Robillard. 2015. IEEE Software 32(4), 68–75. limited background use; DOI 10.1109/MS.2014.80.

- **[Using the Cognitive Dimensions Framework to evaluate the usability of a class library](https://www.ppig.org/papers/2003-ppig-15th-clarke/)** — Steven Clarke and Curtis Becker. 2003. PPIG 15th Annual Workshop. abstract-level historical background.

- **[SWE-bench Science: Can Coding Agents Resolve Engineering Tasks in Science?](https://arxiv.org/abs/2608.19799)** — Author paper. 2026-08-20. arXiv preprint; follow-up lead. full methods not reviewed; not used for detailed novelty claims.
