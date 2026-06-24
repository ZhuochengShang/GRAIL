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
    sp = sub.add_parser("api-surface", help="static: discovered public API surface (Step 1)")
    sp.add_argument("--json", action="store_true", help="emit structured details instead of plain text")
    sp.add_argument("--include-nonpublic", action="store_true",
                    help="also show defs filtered out by the visibility model")
    sp = sub.add_parser("scaffold", help="auto-generate the execution scaffold from the API surface")
    sp.add_argument("--generate", action="store_true", help="write the scaffold (else print to stdout)")
    sp.add_argument("--out", default=None, help="output path (default: comprehension.execute.scaffold)")
    sp = sub.add_parser("intent", help="static: evidence-based intended-API scores (auditable)")
    sp.add_argument("--all", action="store_true", help="show every API, not just selected ones")
    sub.add_parser("intended", help="band-select intended API; LLM adjudicates ambiguous (cached)")
    sp = sub.add_parser("api-tests", help="static: real usage examples mined from the test suite")
    sp.add_argument("--api", default=None, help="show examples for one API name")
    sub.add_parser("form")
    sp = sub.add_parser("comprehension")
    sp.add_argument("--sample", type=int, default=None)
    sp.add_argument("--doc", choices=["aideal", "original"], default="aideal",
                    help="original = use the project's pre-existing README as the only context")
    sp.add_argument("--execute", action="store_true",
                    help="compile/run each snippet via comprehension.execute (real ground truth; "
                         "covers all documented APIs unless --sample given)")
    sp.add_argument("--show-code", action="store_true",
                    help="include the audience-generated Scala snippet in JSON details")
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
                            "reasons": v["reasons"]} for k, v in shown.items()}}
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
        out = find_or_create(cfg, generate=args.generate, max_generated=args.limit,
                             force=args.force)
    elif args.cmd == "form":
        out = form_check(cfg)
    elif args.cmd == "comprehension":
        out = comprehension_check(cfg, sample=args.sample, doc_source=args.doc,
                                 execute=args.execute, show_code=args.show_code)
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
