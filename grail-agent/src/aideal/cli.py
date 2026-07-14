"""AIDEAL CLI — the backend command surface.

Non-interactive, reads configs/aideal.yaml, prints JSON to stdout, so coding
agents (and GRAIL) can invoke it repeatedly.

  readme [--generate]        find or create LLM_readme.md
  form                       form check (no LLM)
  comprehension [--sample N] readme unit test (audience writes code from doc only)
  completeness               all public functions covered?
  puzzle [--dry-run]         integration puzzles + fix loop (uses app runner)
  all [--static-only]        run the pipeline in order
  tasks                      list integration_tasks.yaml
  alias-report               histogram + added/proposed tracking
  alias-overlap A B          Jaccard overlap between two models' aliases
  alias-suggest              mine error log -> alias candidates
  alias-add ALIAS CANONICAL  mark an alias as ADDED to the codebase
  log-add ...                append structured error record
  log-prompt                 token-efficient error render for prompts
  notes-add --issue --fix [--pattern]
  notes-distill              consolidate repeated errors into notes_to_self
  notes-prompt               render notes for prompt injection
"""

from __future__ import annotations

import argparse
import json
import sys

from .alias_registry import AliasRegistry
from .config import load_config, load_tasks
from .doc_checks import completeness_check, comprehension_check, form_check, puzzle_check
from .error_log import ErrorLog
from .notes_to_self import NotesToSelf
from .readme_agent import find_or_create


def _run(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="aideal", description="LLM-readiness backend")
    p.add_argument("--config", default=None)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="create project_profile.yaml (user fills target users, domain, use cases)")
    sub.add_parser("profile", help="show profile status and missing fields")
    sp = sub.add_parser("readme")
    sp.add_argument("--generate", action="store_true", help="fill entries with the author model")
    sp.add_argument("--limit", type=int, default=10,
                    help="max APIs to generate (0 = all; default 10)")
    sp.add_argument("--force", action="store_true",
                    help="regenerate/overwrite an existing LLM_readme.md (else exits as 'found')")
    sp.add_argument("--role", action="append", default=None, metavar="ROLE=MODEL",
                    help="override a model role for this generation; e.g. "
                         "--role author=codex:gpt-5.3-codex")
    sp = sub.add_parser("api-surface", help="static: discovered public API surface (Step 1)")
    sp.add_argument("--json", action="store_true", help="emit structured details instead of plain text")
    sp.add_argument("--include-nonpublic", action="store_true",
                    help="also show defs filtered out by the visibility model")
    sp = sub.add_parser("scaffold", help="auto-generate the execution scaffold from the API surface")
    sp.add_argument("--generate", action="store_true", help="write the scaffold (else print to stdout)")
    sp.add_argument("--out", default=None, help="output path (default: comprehension.execute.scaffold)")
    sp = sub.add_parser("intent", help="static: evidence-based intended-API scores (auditable)")
    sp.add_argument("--all", action="store_true", help="show every API, not just selected ones")
    sp = sub.add_parser("dedup", help="surface-redundancy audit: overload collapse, "
                                      "forwarder aliases, signature twins, alias-registry cross-check")
    sp.add_argument("--out", default=None,
                    help="also write the FULL report to this path (e.g. docs/dedup_report.json)")
    sp.add_argument("--full", action="store_true",
                    help="print the per-name collapse map and twins too (long)")
    sp = sub.add_parser("intent-compare",
                        help="compare intended-API selection with vs without the LLM signal")
    sp.add_argument("--names", action="store_true",
                    help="also list the APIs each side adds/drops")
    sub.add_parser("intended", help="band-select intended API; LLM adjudicates ambiguous (cached)")
    sp = sub.add_parser("api-tests", help="static: real usage examples mined from the test suite")
    sp.add_argument("--api", default=None, help="show examples for one API name")
    sub.add_parser("form")
    sp = sub.add_parser("comprehension")
    sp.add_argument("--sample", type=int, default=None)
    sp.add_argument("--api", default=None,
                    help="test ONE specific documented API by name (e.g. --api mapPixels)")
    sp.add_argument("--doc", choices=["aideal", "original", "agents"], default="aideal",
                    help="aideal = per-API catalog (GRAIL) · original = repo README only · "
                         "agents = repo AGENTS.md only (baseline: holistic agent guide vs per-API docs)")
    sp.add_argument("--execute", action="store_true",
                    help="compile/run each snippet via comprehension.execute (real ground truth; "
                         "covers all documented APIs unless --sample given)")
    sp.add_argument("--show-code", action="store_true",
                    help="include the audience-generated Scala snippet in JSON details")
    sp.add_argument("--class-context", dest="class_context", choices=["on", "off"], default=None,
                    help="INDEX-FIRST: prefix each API with its catalogue class header (receiver + "
                         "verified sibling pattern). Overrides comprehension.class_context. A/B the "
                         "receiver-failure fix: run --class-context off then on, compare pass rate")
    sp.add_argument("--rerun-failed", dest="rerun_failed", action="store_true",
                    help="re-test ONLY functions whose most-recent error_log outcome is fail "
                         "(skips fixed/pass) — one build, just the last run's failures")
    sp.add_argument("--max-fix-rounds", dest="max_fix_rounds", type=int, default=None,
                    help="override comprehension.execute.max_fix_rounds for THIS run "
                         "(0 = single-shot no-fix baseline; 99 = let the fixer run until it "
                         "gives up — the 'fix as much as possible' condition)")
    sp.add_argument("--role", action="append", default=None, metavar="ROLE=MODEL",
                    help="override a model role for this run; MODEL is a registry key or "
                         "provider:model. Repeatable. e.g. --role audience=codex:gpt-5.1-codex-max "
                         "--role fixer=google:gemini-2.5-pro")
    sp.add_argument("--resume", action="store_true",
                    help="skip APIs already finished in a previous (killed/crashed) run — "
                         "reads the per-API checkpoint .aideal_exec/comprehension_progress.jsonl "
                         "and pre-fills their results; without this flag the checkpoint restarts")
    sp.add_argument("--timeout", dest="timeout_s", type=int, default=None,
                    help="per-attempt compile+run timeout in seconds for THIS run "
                         "(default: comprehension.execute.timeout_seconds, 600). Slow "
                         "visualization APIs (plotImage etc.) hit this; 300 halves worst-case cost")
    sp = sub.add_parser("fix-docs",
                        help="doc-repair fix routing: for each FAILED api — read its real "
                             "source, senior-engineer diagnosis, rewrite its readme entry, "
                             "re-run the test (entry kept on pass, reverted on fail)")
    sp.add_argument("--api", action="append", default=None,
                    help="fix ONE api's entry (repeatable); default: every most-recent FAIL")
    sp.add_argument("--from-results", default=None,
                    help="target failed APIs from a specific comprehension/bench JSON "
                         "(e.g. g1), instead of the mutable latest error_log state")
    sp.add_argument("--max-apis", type=int, default=None, help="cap how many failures to process")
    sp.add_argument("--retry-rounds", type=int, default=2,
                    help="fix rounds allowed in the retry run (default 2)")
    sp.add_argument("--timeout", dest="timeout_s", type=int, default=None,
                    help="per-attempt compile+run timeout for the retry")
    sp.add_argument("--report", default=None,
                    help="write the docfix JSON report here incrementally after each API; "
                         "prevents empty redirected output if the run is interrupted")
    sp.add_argument("--deep-dive-first", action="store_true",
                    help="for each target API, first run the principal-engineer deep-dive "
                         "(source + types + call sites + failure history), feed that report "
                         "into the doc repair prompt, then rewrite and re-test the README entry")
    sp.add_argument("--deep-dive-out", default="docs/deepdive",
                    help="directory for deep-dive reports when --deep-dive-first is used")
    sp.add_argument("--role", action="append", default=None, metavar="ROLE=MODEL",
                    help="model override, e.g. --role fixer=google:gemini-2.5-pro")
    sp.add_argument("--dry-run", action="store_true", help="list target apis, change nothing")
    sp = sub.add_parser("fix-report",
                        help="READABLE markdown analysis of a fix-loop run: improvement "
                             "verdict vs a baseline, same-issue-not-solved list, failure "
                             "clusters, chronic cross-run failures, per-API why-failed "
                             "with round-by-round error evolution")
    sp.add_argument("--run", required=True,
                    help="comprehension/bench or fix-docs result JSON to analyze")
    sp.add_argument("--baseline", default=None,
                    help="previous run JSON of the same kind to diff against")
    sp.add_argument("--out", default=None,
                    help="output .md (default docs/fix_report_<run-stem>.md; "
                         "docs/fix_report_latest.md is always refreshed)")
    sp.add_argument("--top-clusters", type=int, default=12)
    sp.add_argument("--max-api-detail", type=int, default=80)
    sp = sub.add_parser("surface-audit",
                        help="cross-check catalog entries against the CURRENT visibility-"
                             "correct surface: non-public (private/protected incl. "
                             "containers), path-excluded, or intent-deselected entries "
                             "that can never pass and should be pruned/excluded")
    sp.add_argument("--out", default=None, help="also write the full JSON here")
    sp = sub.add_parser("deep-dive",
                        help="principal-engineer deep review of ONE API: max grounded context "
                             "(source + type defs + real call sites + failure history) -> layered "
                             "report incl. self-assessment; saved to docs/deepdive/<api>.md")
    sp.add_argument("--api", required=True, action="append",
                    help="API name (repeatable for several reports in one go)")
    sp.add_argument("--out", default="docs/deepdive", help="output directory")
    sp.add_argument("--context-only", action="store_true",
                    help="assemble and show the context, no LLM call (sanity check)")
    sp.add_argument("--role", action="append", default=None, metavar="ROLE=MODEL",
                    help="e.g. --role fixer=google:gemini-3.1-pro-preview")
    sp = sub.add_parser("augment",
                        help="fold error-log failures/fixes into readme Common Failure Modes + Fix Code Hint")
    sp.add_argument("--dry-run", action="store_true", help="show what would change, don't write")
    sp.add_argument("--only-missing", action="store_true",
                    help="gap-fill: add a verified example / fix-hint code ONLY to entries that "
                         "lack it (don't overwrite existing code); Common Failure Modes still refreshed")
    sp = sub.add_parser("grounding",
                        help="flag readme entries: grounded / sibling-grounded / guessed")
    sp.add_argument("--annotate", action="store_true", help="write a Grounding line into each entry")
    sp = sub.add_parser("organize",
                        help="group APIs by class, rank by robustness, mark the primary per group")
    sp.add_argument("--index", action="store_true", help="write docs/readme_index.md")
    sub.add_parser("catalogue",
                   help="ADDITIVE: export a per-class catalogue (LLM_readme_index.md + api/<Class>.md) "
                        "from LLM_readme.md; touches nothing else")
    sub.add_parser("completeness")
    sp = sub.add_parser("puzzle")
    sp.add_argument("--dry-run", action="store_true")
    sp = sub.add_parser("all")
    sp.add_argument("--static-only", action="store_true")
    sp.add_argument("--dry-run", action="store_true")
    sp = sub.add_parser("tasks")
    sp.add_argument("--generate", type=int, metavar="N", default=0,
                    help="author model generates N tasks from profile use cases")
    sub.add_parser("alias-report")
    sp = sub.add_parser("alias-overlap")
    sp.add_argument("model_a"); sp.add_argument("model_b")
    sub.add_parser("alias-suggest")
    sp = sub.add_parser("alias-add")
    sp.add_argument("alias"); sp.add_argument("canonical")
    sp = sub.add_parser("log-add")
    for f in ("run-id", "step", "language", "task", "function",
              "error", "root-cause", "suggested-fix-code"):
        sp.add_argument(f"--{f}", default="")
    sp.add_argument("--status", default="fail")
    sub.add_parser("log-prompt")
    sp = sub.add_parser("notes-add")
    sp.add_argument("--issue", required=True)
    sp.add_argument("--fix", required=True)
    sp.add_argument("--pattern", default="")
    sub.add_parser("notes-distill")
    sub.add_parser("notes-prompt")

    args = p.parse_args(argv)
    try:
        cfg = load_config(args.config)
    except FileNotFoundError:
        if args.cmd == "init":
            # bootstrap a brand-new project: scaffold the config, then proceed
            from .config import init_config
            created = init_config()
            print(json.dumps({"scaffolded_config": str(created),
                              "note": "fill the TODOs in this config, then rerun init"}, indent=2))
            return 0
        raise
    out: object

    if args.cmd == "init":
        from .profile import init_agents_md, init_profile
        out = {**init_profile(cfg), **init_agents_md(cfg)}
    elif args.cmd == "profile":
        from .profile import load_profile, missing_fields, profile_path, project_context
        prof = load_profile(cfg)
        out = {"path": str(profile_path(cfg)), "missing_fields": missing_fields(prof),
               "ready": not missing_fields(prof), "prompt_context": project_context(prof)}
    elif args.cmd == "api-surface":
        from .readme_agent import public_api_details, render_api_surface, visibility_model
        if args.json:
            details = public_api_details(cfg)
            if not args.include_nonpublic:
                details = [d for d in details if d["visibility"] == "public"]
            out = {"project": cfg.project_name,
                   "visibility_mode": visibility_model(cfg).get("mode"),
                   "public_names": len({d["name"] for d in details}),
                   "definition_sites": len(details),
                   "details": details}
        else:
            print(render_api_surface(cfg, include_nonpublic=args.include_nonpublic))
            return 0
    elif args.cmd == "scaffold":
        from pathlib import Path as _Path
        from .readme_agent import generate_scaffold
        text = generate_scaffold(cfg)
        if args.generate:
            dest = args.out or (cfg.comprehension.get("execute", {}) or {}).get("scaffold")
            if not dest:
                out = {"error": "no --out and no comprehension.execute.scaffold configured"}
            else:
                p = (cfg.root / dest).resolve()
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(text, encoding="utf-8")
                out = {"action": "wrote_scaffold", "path": str(p), "lines": text.count(chr(10)) + 1}
        else:
            print(text)
            return 0
    elif args.cmd == "intent":
        from .readme_agent import intent_scores
        scores = intent_scores(cfg)
        sel = {k: v for k, v in scores.items() if v["selected"]}
        shown = scores if args.all else sel
        out = {"surface_filter": cfg.surface_filter,
               "threshold": next(iter(scores.values()), {}).get("threshold"),
               "raw_surface": len(scores), "selected": len(sel),
               "apis": {k: {"score": v["score"], "selected": v["selected"],
                            "sites": v.get("sites"),
                            "reasons": v["reasons"]} for k, v in shown.items()}}
    elif args.cmd == "dedup":
        from .readme_agent import dedup_report
        rep = dedup_report(cfg)
        written = None
        if args.out:
            p = (cfg.root / args.out).resolve()
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
            written = str(p)
        out = rep if args.full else {k: v for k, v in rep.items()
                                     if k not in ("collapse", "same_signature_twins")}
        if written:
            out = {"written": written, **out}
    elif args.cmd == "intent-compare":
        from .readme_agent import intent_compare
        cmp = intent_compare(cfg)
        if not args.names:
            cmp = {k: v for k, v in cmp.items()
                   if k not in ("added_by_llm", "dropped_with_llm")}
        out = cmp
    elif args.cmd == "intended":
        from .readme_agent import intended_api_llm
        selected, decisions = intended_api_llm(cfg)
        from collections import Counter
        out = {"selected": len(selected), "total": len(decisions),
               "by": dict(Counter(d.get("by") for d in decisions.values())),
               "decisions": decisions}
    elif args.cmd == "api-tests":
        from .readme_agent import api_test_examples
        idx = api_test_examples(cfg)
        if args.api:
            out = {"api": args.api, "examples": idx.get(args.api, [])}
        else:
            out = {"test_globs": cfg.test_globs,
                   "apis_with_examples": len(idx),
                   "examples_per_api": {k: len(v) for k, v in sorted(idx.items())}}
    elif args.cmd == "readme":
        for spec in (args.role or []):
            role, _, val = spec.partition("=")
            if not val:
                print(json.dumps({"error": f"--role needs ROLE=MODEL, got '{spec}'"})); return 2
            cfg.override_role(role.strip(), val.strip())
        out = find_or_create(cfg, generate=args.generate, max_generated=args.limit,
                             force=args.force)
    elif args.cmd == "form":
        out = form_check(cfg)
    elif args.cmd == "comprehension":
        cc = None if args.class_context is None else (args.class_context == "on")
        for spec in (args.role or []):   # e.g. --role fixer=google:gemini-2.5-pro
            role, _, val = spec.partition("=")
            if not val:
                print(json.dumps({"error": f"--role needs ROLE=MODEL, got '{spec}'"})); return 2
            cfg.override_role(role.strip(), val.strip())
        out = comprehension_check(cfg, sample=args.sample, doc_source=args.doc,
                                 execute=args.execute, show_code=args.show_code, api=args.api,
                                 class_context=cc, rerun_failed=args.rerun_failed,
                                 max_fix_rounds=args.max_fix_rounds,
                                 resume=args.resume, timeout_s=args.timeout_s)
        if args.execute and isinstance(out, dict):
            from .fixreport import auto_report
            rep = auto_report(cfg, out)   # readable log; never raises
            if rep:
                out["report_md"] = rep
    elif args.cmd == "fix-report":
        from .fixreport import write_report
        out = write_report(cfg, args.run, baseline_path=args.baseline,
                           out_path=args.out, top_clusters=args.top_clusters,
                           max_api_detail=args.max_api_detail)
    elif args.cmd == "surface-audit":
        from .readme_agent import surface_audit
        out = surface_audit(cfg)
        if args.out:
            from pathlib import Path as _P
            _p = (cfg.root / args.out).resolve()
            _p.parent.mkdir(parents=True, exist_ok=True)
            _p.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
            out = {"written": str(_p), **out}
    elif args.cmd == "deep-dive":
        from .deepdive import deep_dive_run
        for spec in (args.role or []):
            role, _, val = spec.partition("=")
            if not val:
                print(json.dumps({"error": f"--role needs ROLE=MODEL, got '{spec}'"})); return 2
            cfg.override_role(role.strip(), val.strip())
        out = [deep_dive_run(cfg, a, out_dir=args.out, context_only=args.context_only)
               for a in args.api]
        out = out[0] if len(out) == 1 else {"reports": out}
    elif args.cmd == "fix-docs":
        from .docfix import doc_fix_run
        for spec in (args.role or []):
            role, _, val = spec.partition("=")
            if not val:
                print(json.dumps({"error": f"--role needs ROLE=MODEL, got '{spec}'"})); return 2
            cfg.override_role(role.strip(), val.strip())
        out = doc_fix_run(cfg, apis=args.api, max_apis=args.max_apis,
                          retry_rounds=args.retry_rounds,
                          timeout_s=args.timeout_s, dry_run=args.dry_run,
                          from_results=args.from_results,
                          report_path=args.report,
                          deep_dive_first=args.deep_dive_first,
                          deep_dive_out=args.deep_dive_out)
        if not args.dry_run and isinstance(out, dict):
            from .fixreport import auto_report
            rep = auto_report(cfg, out)   # readable log; never raises
            if rep:
                out["report_md"] = rep
    elif args.cmd == "augment":
        from .readme_agent import augment_from_log
        out = augment_from_log(cfg, dry_run=args.dry_run, only_missing=args.only_missing)
    elif args.cmd == "grounding":
        from .readme_agent import grounding_report
        out = grounding_report(cfg, annotate=args.annotate)
    elif args.cmd == "organize":
        from .readme_agent import organize_report
        out = organize_report(cfg, write_index=args.index)
    elif args.cmd == "catalogue":
        from .readme_agent import write_catalogue
        out = write_catalogue(cfg)
    elif args.cmd == "completeness":
        out = completeness_check(cfg)
    elif args.cmd == "puzzle":
        out = puzzle_check(cfg, dry_run=args.dry_run)
    elif args.cmd == "all":
        reports = [find_or_create(cfg), form_check(cfg), completeness_check(cfg)]
        if not args.static_only:
            reports.append(comprehension_check(cfg))
            reports.append(puzzle_check(cfg, dry_run=args.dry_run))
        checks = [r for r in reports if "check" in r]
        out = {"project": cfg.project_name, "steps": reports,
               "llm_ready": all(r["passed"] for r in checks)}
    elif args.cmd == "tasks":
        if args.generate:
            from .task_generator import generate_tasks
            out = generate_tasks(cfg, n=args.generate)
        else:
            out = load_tasks(cfg)
    elif args.cmd == "alias-report":
        out = AliasRegistry(cfg.aliases_file).report()
    elif args.cmd == "alias-overlap":
        out = AliasRegistry(cfg.aliases_file).overlap(args.model_a, args.model_b)
    elif args.cmd == "alias-suggest":
        out = ErrorLog(cfg.error_log).suggest_aliases()
    elif args.cmd == "alias-add":
        out = AliasRegistry(cfg.aliases_file).mark_added(args.alias, args.canonical)
    elif args.cmd == "log-add":
        out = ErrorLog(cfg.error_log).append(
            run_id=getattr(args, "run_id"), step=args.step,
            language=args.language or cfg.language, task=args.task,
            status=args.status, function=args.function, error=args.error,
            root_cause=getattr(args, "root_cause"),
            suggested_fix_code=getattr(args, "suggested_fix_code"))
    elif args.cmd == "log-prompt":
        print(ErrorLog(cfg.error_log).to_prompt()); return 0
    elif args.cmd == "notes-add":
        out = {"added": NotesToSelf(cfg.notes_to_self).add(args.issue, args.fix, args.pattern)}
    elif args.cmd == "notes-distill":
        out = {"notes_added": NotesToSelf(cfg.notes_to_self).distill(ErrorLog(cfg.error_log))}
    elif args.cmd == "notes-prompt":
        print(NotesToSelf(cfg.notes_to_self).to_prompt()); return 0
    else:  # pragma: no cover
        return 2

    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    """Entry point: exit cleanly when piped into `head`/`less` etc. (the reader
    closes the pipe early, raising BrokenPipeError)."""
    try:
        return _run(argv)
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        return 0


if __name__ == "__main__":
    sys.exit(main())
