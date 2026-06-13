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


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="aideal", description="LLM-readiness backend")
    p.add_argument("--config", default=None)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="create project_profile.yaml (user fills target users, domain, use cases)")
    sub.add_parser("profile", help="show profile status and missing fields")
    sp = sub.add_parser("readme")
    sp.add_argument("--generate", action="store_true", help="fill entries with the author model")
    sub.add_parser("form")
    sp = sub.add_parser("comprehension")
    sp.add_argument("--sample", type=int, default=None)
    sp.add_argument("--doc", choices=["aideal", "original"], default="aideal",
                    help="original = use the project's pre-existing README as the only context")
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
    elif args.cmd == "readme":
        out = find_or_create(cfg, generate=args.generate)
    elif args.cmd == "form":
        out = form_check(cfg)
    elif args.cmd == "comprehension":
        out = comprehension_check(cfg, sample=args.sample, doc_source=args.doc)
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


if __name__ == "__main__":
    sys.exit(main())
