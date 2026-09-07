# AIDEAL design and paper research package

Open [the visual research dossier](AIDEAL_RELATED_WORK_2026-09-07.html) for the overview figure, closest-prior-work comparison, literature map, proposed research questions, draft related-work section and annotated reading list.

- [Overview PNG](figures/AIDEAL_OVERVIEW.png), [editable SVG](figures/AIDEAL_OVERVIEW.svg), [vector PDF](figures/AIDEAL_OVERVIEW.pdf).
- [Verbatim memo of the previous explanation](AIDEAL_EXPLANATION_VERBATIM_2026-09-07.md). Historical text is preserved separately from subsequent research findings.
- [Research report in Markdown](AIDEAL_RELATED_WORK_2026-09-07.md).
- [Detailed architecture and code/function guide](../../AIDEAL_CODE_GUIDE.md).

The literature review is dated September 7, 2026 and contains 36 primary-source records, including one abstract-only follow-up lead. It is targeted research, not an exhaustive systematic review. First-party product reports and unreviewed preprints are labeled; no published result was independently reproduced.

## Figure meaning

D means deterministic automation; L means LLM participation; H means a human decision; O means an operator agent using tools. A1/A2/B1/B2 include both LLM generation and deterministic execution. The improvement queue records proposals and reviews; it does not automatically implement or merge them. Full API coverage, valid inputs, scientific correctness and whole-repository readiness are different claims.

## Rebuild

The figure generator uses Python and Matplotlib. The report generator uses Python and Mistune. Both work offline, resolve paths relative to themselves, make no LLM calls and do not access experiment outputs. Use an environment that already provides those packages:

```bash
python docs/paper/figures/render_overview.py
python docs/paper/research/build_dossier.py
```

`research/report-source.md` is the canonical report source. `research/source-ledger.json` records claims, dates, source locations and access limitations; it is generated from the metadata in `build_dossier.py`. The Markdown and HTML dossiers are generated deliverables.

The figure was rendered and visually inspected. HTML received structural/link checks; a full browser visual review was not performed. This package changes documentation only and leaves active supervisors, checkpoints, prompts and experiment configurations unchanged.
