# Research trace and gap audit — September 7, 2026

Scope: literature for the AIDEAL paper, emphasizing direct documentation optimization and API/readiness assessment rather than only generic coding agents. Cutoff: September 7, 2026. Primary research, proceedings, author manuscripts and dated first-party reports were preferred. Local implementation claims refer to the existing code guide; no experiment was run for this review.

The Deep Research skill required update_plan, but no callable update_plan tool was available. The plan was maintained in session: discovery → primary-source follow-up → synthesis/figure/memo → artifact verification. Two bounded research lanes were delegated as instructed by that skill; neither changed files or invoked experiment models.

## Searches and follow-up

Initial coordinator queries (exact wording):

- LLM documentation optimization API documentation refinement executable tests benchmark paper
- Self-Refine Reflexion TextGrad automated prompt optimization execution feedback paper
- EvalPlus code generation test oracle benchmark LLM generated tests validity paper
- agent readiness codebase documentation benchmark AIDEAL
- site.arxiv.org Self-Refine Iterative Refinement Self-Feedback 2303
- site.arxiv.org Reflexion Language Agents Verbal Reinforcement Learning
- site.arxiv.org GEPA Reflective Prompt Evolution Outperform Reinforcement Learning
- site.arxiv.org "Auditing and Decomposing Feedback-Driven Evolution"
- Robillard DeLine 2011 field study API learning obstacles documentation empirical software engineering
- Uddin Robillard How API documentation fails IEEE Software 2015
- API usability cognitive dimensions framework Clarke measuring API usability 2004

Delegated question families: (1) API documentation generation/refinement, executable library benchmarks and closest direct tool-readiness work; (2) repository readiness, AGENTS.md intervention studies, agent interfaces and human acceptance. Backward chaining from DRAFT, DocsChisel and Probe-and-Refine exposed stronger overlaps than the initial generic papers. Follow-up inspected original methods, publication records and dated vendor pages. Canonical URLs and evidence sections are in source-ledger.json.

## Gap matrix

| Material question | Evidence and confidence | Residual gap / next action |
|---|---|---|
| Is execution-driven documentation refinement new? | High confidence no: DRAFT, PLAY2PROMPT, DocsChisel | Compare adapted baselines under matched access/budgets |
| Is agent-ready API testing with builder input new? | High confidence no: Bandlamudi v3 | Differentiate public-library evidence scope; inspect replication before baseline implementation |
| Is readiness + remediation a new product concept? | High confidence no: dated Factory/Tessl reports | Vendor articles do not establish a controlled comparison to AIDEAL |
| Does added documentation reliably improve performance? | Conditional evidence: context studies differ in outcome, model, task and design | Report negative effects, cost and model/task dependence; do not average incompatible literature results |
| Are current generated tests semantically valid? | Not established for AIDEAL; Doc2OracLL/EvalPlus/DS-1000/SciCode motivate checks | Blinded per-API input/oracle audit and fault sensitivity in a separate protocol |
| Does fresh B testing show held-out transfer? | No; DocsChisel and Probe-and-Refine have distinct evaluation tasks | Freeze held-out tasks/fixtures and a second audience model |
| Does human review improve results? | METR supports distinction between tests and acceptance | AIDEAL needs measured review cases; queue implementation alone is not evidence of benefit |
| Are dates and versions consistent? | Corrected REST v1→v3 counts, AGENTS.md v1→v2 name/conclusion, GEPA v2 venue | Recheck before submission; live docs may change |
| Is scientific-repository maintenance covered? | SWE-bench Science abstract discovered | Full methods remain a follow-up lead, not a supported detailed comparison |
| Have all possible related papers been found? | No exhaustive claim | Targeted review stopped after direct threats and key methodological gaps were supported |

## Access and verification

Highest-impact competitor claims were spot-checked by the coordinator against primary full text: Bandlamudi v3, DocsChisel, DRAFT, Doc2OracLL, Probe-and-Refine, Evaluating AGENTS.md, PLAY2PROMPT, Factory and Tessl. Agent-Diff, Trace-Free+ and JTPRO also received primary follow-up. Background sources were read at varying depth as explicitly recorded.

Persistent failures: DRAFT OpenReview challenge (used official proceedings); old Tessl docs 404 (used dated posts); ACM DOI access issue (used author paper and indexed publication record); GEPA HTML and Nature TextGrad open failures (used primary metadata/abstracts for narrow claims). No repeated unbounded retries.

Stop reason: the direct novelty threats, counterevidence and measurement requirements converged; another broad search was unlikely to change the proposed framing. The remaining gaps require benchmark design, reproduction or experiment completion, rather than more generic literature collection.
