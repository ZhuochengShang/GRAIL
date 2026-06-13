"""Puzzle-game LLM-readiness evaluator.

Measures how "LLM-ready" a target codebase is: randomly sample N public APIs
from the API documentation, compose them into a small task ("puzzle"), run the
existing GRAIL pipeline on it, and score compile/run success.

The aggregate success rate over many puzzles is the LLM-readiness score.
Run the same puzzles against ablated docs (no aliases, no fix guides) to get
an ablation table.

Usage (dry run, no LLM/Spark needed - just shows sampled puzzles):
    python -m rdpro_section_codegen.puzzle_eval --dry-run --num-puzzles 3

Full run (requires OpenAI key + local Spark/RDPro setup):
    python -m rdpro_section_codegen.puzzle_eval \
        --api-doc docs/rdpro_api_doc_combined.md \
        --num-puzzles 10 --num-functions 5 --seed 42 \
        --work-dir outputs/puzzle_runs

Ablation example (docs without alias functions):
    python -m rdpro_section_codegen.puzzle_eval \
        --api-doc docs/rdpro_api_doc_no_aliases.md --tag no_aliases ...
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent
AGENT_SCRIPT = PKG_DIR / "langgraph_section_agent.py"
GRAIL_AGENT_ROOT = PKG_DIR.parent.parent  # grail-agent/

API_HEADER_RE = re.compile(r"^## API Test: `([^`]+)`\s*$", re.MULTILINE)


# ---------------------------------------------------------------------------
# 1. Function inventory: parse API docs into (name, goal, snippet) entries
# ---------------------------------------------------------------------------

@dataclass
class ApiEntry:
    name: str
    goal: str
    snippet: str
    body: str  # full doc section, used to build the puzzle-scoped api doc


def _section_between(body: str, header: str) -> str:
    m = re.search(rf"^### {re.escape(header)}\s*$(.*?)(?=^###? |\Z)", body, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def load_api_inventory(api_doc_path: Path) -> list[ApiEntry]:
    text = api_doc_path.read_text(encoding="utf-8", errors="ignore")
    matches = list(API_HEADER_RE.finditer(text))
    if not matches:
        raise ValueError(
            f"No '## API Test: `name`' headers found in {api_doc_path}. "
            "Puzzle sampling needs the per-API doc format."
        )
    entries: list[ApiEntry] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        entries.append(
            ApiEntry(
                name=m.group(1),
                goal=_section_between(body, "Goal"),
                snippet=_section_between(body, "Prompt Snippet"),
                body=body,
            )
        )
    return entries


# ---------------------------------------------------------------------------
# 2. Puzzle composition: sampled functions -> free-text task
# ---------------------------------------------------------------------------

@dataclass
class Puzzle:
    puzzle_id: str
    api_names: list[str]
    task_text: str
    scoped_api_doc: str  # only the sampled APIs' doc sections


def compose_puzzle(entries: list[ApiEntry], puzzle_id: str) -> Puzzle:
    lines = [
        "Write a single RDPro Scala program that composes the following "
        f"{len(entries)} APIs into one coherent workflow. "
        "Every listed API must be called at least once. "
        "Use only the provided input path variables; do not invent file paths. "
        "The program must compile and run end to end on a small input.",
        "",
    ]
    for e in entries:
        lines.append(f"- `{e.name}`: {e.goal or 'see API documentation.'}")
    lines.append("")
    lines.append(
        "Order the calls so data flows naturally (load before transform, "
        "transform before save/inspect). Print one line of evidence per API "
        "call (e.g., a count, a pixel type, or an output path) so success is "
        "verifiable from stdout."
    )
    scoped_doc = "\n\n".join(e.body for e in entries)
    return Puzzle(
        puzzle_id=puzzle_id,
        api_names=[e.name for e in entries],
        task_text="\n".join(lines),
        scoped_api_doc=scoped_doc,
    )


def sample_puzzles(
    inventory: list[ApiEntry], num_puzzles: int, num_functions: int, seed: int
) -> list[Puzzle]:
    rng = random.Random(seed)
    k = min(num_functions, len(inventory))
    puzzles = []
    for i in range(num_puzzles):
        sampled = rng.sample(inventory, k)
        puzzles.append(compose_puzzle(sampled, puzzle_id=f"puzzle_{i:03d}"))
    return puzzles


def load_task_puzzles(tasks_path: Path, inventory: list[ApiEntry]) -> list[Puzzle]:
    """Build puzzles from integration_tasks.yaml benchmark tasks instead of
    random sampling. Each task's `apis` are matched to doc entries."""
    import yaml

    data = yaml.safe_load(tasks_path.read_text(encoding="utf-8")) or {}
    by_name = {re.sub(r"\[.*\]$", "", e.name): e for e in inventory}
    puzzles = []
    for t in data.get("tasks", []):
        entries = [by_name[a] for a in t.get("apis", []) if a in by_name]
        if not entries:
            continue
        names = ", ".join(f"`{e.name}`" for e in entries)
        task_text = (
            f"{t.get('goal', '').strip()}\n\n"
            f"Use these RDPro APIs (each at least once): {names}. "
            "Use only provided input path variables; do not invent file paths. "
            "Print one line of evidence per API call."
        )
        puzzles.append(Puzzle(
            puzzle_id=str(t.get("id", f"task_{len(puzzles)}")),
            api_names=[e.name for e in entries],
            task_text=task_text,
            scoped_api_doc="\n\n".join(e.body for e in entries),
        ))
    return puzzles


def read_hints() -> str:
    """Fix-loop memory: PUZZLE_HINTS env var points at a hints file rendered
    from notes_to_self + the error log. Injected into every puzzle prompt."""
    path = os.environ.get("PUZZLE_HINTS", "")
    if path and Path(path).exists():
        text = Path(path).read_text(encoding="utf-8").strip()
        if text:
            return "\n\nLessons from previous failed attempts (avoid these mistakes):\n" + text
    return ""


# ---------------------------------------------------------------------------
# 3. Run a puzzle through the existing pipeline (subprocess; zero refactor)
# ---------------------------------------------------------------------------

@dataclass
class PuzzleResult:
    puzzle_id: str
    api_names: list[str]
    success: bool = False
    fail_reason: str = ""
    completed_sections: list[str] = field(default_factory=list)
    planned_sections: list[str] = field(default_factory=list)
    total_tokens: int = 0
    llm_seconds: float = 0.0
    events_count: int = 0  # generate/repair turns; higher = more repair effort
    wall_seconds: float = 0.0
    error: str = ""


def run_puzzle(puzzle: Puzzle, args: argparse.Namespace, run_root: Path) -> PuzzleResult:
    pdir = run_root / puzzle.puzzle_id
    pdir.mkdir(parents=True, exist_ok=True)
    (pdir / "task.md").write_text(puzzle.task_text, encoding="utf-8")
    scoped_doc_path = pdir / "scoped_api_doc.md"
    scoped_doc_path.write_text(puzzle.scoped_api_doc, encoding="utf-8")
    api_doc_for_run = scoped_doc_path if args.scoped_docs else Path(args.api_doc).resolve()

    cmd = [
        sys.executable, str(AGENT_SCRIPT),
        "--translation-mode", "direct",
        "--free-text", puzzle.task_text,
        "--api-doc", str(api_doc_for_run),
        "--scaffold", str(Path(args.scaffold).resolve()),
        "--output-scala", str(pdir / "generated.scala"),
        "--work-dir", str(pdir),
        "--provider", args.provider,
        "--model", args.model,
        "--max-retries-per-section", str(args.max_retries_per_section),
    ]
    if args.guide:
        cmd += ["--guide", str(Path(args.guide).resolve())]
    cmd += args.agent_args  # raw pass-through (spark paths etc.)

    result = PuzzleResult(puzzle_id=puzzle.puzzle_id, api_names=puzzle.api_names)
    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=args.puzzle_timeout_seconds
        )
        (pdir / "stdout.log").write_text(proc.stdout, encoding="utf-8")
        (pdir / "stderr.log").write_text(proc.stderr, encoding="utf-8")
        summaries = sorted(pdir.glob("summary_*.json"))
        if summaries:
            s = json.loads(summaries[-1].read_text(encoding="utf-8"))
            result.success = bool(s.get("success"))
            result.fail_reason = s.get("fail_reason", "")
            result.completed_sections = s.get("completed_sections", [])
            result.planned_sections = s.get("planned_sections", [])
            m = s.get("metrics", {})
            result.total_tokens = int(m.get("total_tokens", 0) or 0)
            result.llm_seconds = float(m.get("total_llm_seconds", 0.0) or 0.0)
            result.events_count = int(m.get("events_count", 0) or 0)
        else:
            result.error = f"no summary json (exit code {proc.returncode})"
    except subprocess.TimeoutExpired:
        result.error = f"timeout after {args.puzzle_timeout_seconds}s"
    except Exception as exc:  # noqa: BLE001 - record and continue the batch
        result.error = repr(exc)
    result.wall_seconds = round(time.time() - t0, 2)
    return result


# ---------------------------------------------------------------------------
# 4. Scoring and report
# ---------------------------------------------------------------------------

def write_report(results: list[PuzzleResult], run_root: Path, tag: str, meta: dict) -> dict:
    n = len(results)
    successes = sum(1 for r in results if r.success)
    section_progress = [
        len(r.completed_sections) / len(r.planned_sections)
        for r in results
        if r.planned_sections
    ]
    report = {
        "tag": tag,
        "readiness_score": round(successes / n, 3) if n else 0.0,
        "puzzles": n,
        "successes": successes,
        "mean_section_progress": round(sum(section_progress) / len(section_progress), 3)
        if section_progress
        else 0.0,
        "mean_turns": round(sum(r.events_count for r in results) / n, 2) if n else 0.0,
        "total_tokens": sum(r.total_tokens for r in results),
        "meta": meta,
        "results": [asdict(r) for r in results],
    }
    (run_root / "puzzle_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    with (run_root / "puzzle_report.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["puzzle_id", "apis", "success", "fail_reason", "turns", "tokens", "wall_s", "error"])
        for r in results:
            w.writerow([
                r.puzzle_id, ";".join(r.api_names), r.success, r.fail_reason,
                r.events_count, r.total_tokens, r.wall_seconds, r.error,
            ])
    return report


# ---------------------------------------------------------------------------
# 5. CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Puzzle-game LLM-readiness evaluator")
    p.add_argument("--api-doc", default=str(GRAIL_AGENT_ROOT / "docs/rdpro_api_doc_combined.md"))
    p.add_argument("--scaffold", default=str(GRAIL_AGENT_ROOT / "configs/job_scaffold.scala"))
    p.add_argument("--guide", default="", help="migration/fix guide; empty = ablate fix guides")
    p.add_argument("--work-dir", default=str(GRAIL_AGENT_ROOT / "outputs/puzzle_runs"))
    p.add_argument("--tag", default="default", help="label for this configuration (e.g. no_aliases)")
    p.add_argument("--tasks", default="",
                   help="integration_tasks.yaml: run these benchmark tasks instead of random puzzles")
    p.add_argument("--num-puzzles", type=int, default=5)
    p.add_argument("--num-functions", type=int, default=5)
    p.add_argument("--seed", type=int, default=42, help="same seed = same puzzles across ablations")
    p.add_argument("--scoped-docs", action="store_true",
                   help="give the agent only the sampled APIs' docs instead of the full doc")
    p.add_argument("--provider", choices=["openai", "google"], default="openai")
    p.add_argument("--model", default="gpt-4o")
    p.add_argument("--max-retries-per-section", type=int, default=5)
    p.add_argument("--puzzle-timeout-seconds", type=int, default=1800)
    p.add_argument("--dry-run", action="store_true", help="print sampled puzzles, run nothing")
    p.add_argument("agent_args", nargs="*", default=[],
                   help="extra args passed through to langgraph_section_agent.py "
                        "(e.g. -- --spark-submit /path --rdpro-lib-dir /path)")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    api_doc_path = Path(args.api_doc).resolve()
    inventory = load_api_inventory(api_doc_path)
    if args.tasks:
        puzzles = load_task_puzzles(Path(args.tasks).resolve(), inventory)
        if not puzzles:
            print("no runnable tasks in tasks file (apis not found in api doc?)", file=sys.stderr)
            return 2
    else:
        puzzles = sample_puzzles(inventory, args.num_puzzles, args.num_functions, args.seed)

    hints = read_hints()
    if hints:
        for pz in puzzles:
            pz.task_text += hints

    print(f"inventory: {len(inventory)} APIs from {api_doc_path.name}")
    print(f"puzzles: {len(puzzles)} ({'tasks file' if args.tasks else f'{args.num_functions} random fns'}, "
          f"seed={args.seed}, tag={args.tag}, hints={'yes' if hints else 'no'})")

    if args.dry_run:
        for pz in puzzles:
            print(f"\n=== {pz.puzzle_id}: {', '.join(pz.api_names)} ===")
            print(pz.task_text)
        return 0

    stamp = time.strftime("%Y%m%d_%H%M%S")
    run_root = Path(args.work_dir).resolve() / f"{args.tag}_{stamp}"
    run_root.mkdir(parents=True, exist_ok=True)

    results = []
    for pz in puzzles:
        print(f"[{pz.puzzle_id}] {', '.join(pz.api_names)} ...", flush=True)
        r = run_puzzle(pz, args, run_root)
        status = "OK" if r.success else f"FAIL ({r.fail_reason or r.error})"
        print(f"[{pz.puzzle_id}] {status}  turns={r.events_count} wall={r.wall_seconds}s")
        results.append(r)

    meta = {
        "api_doc": str(api_doc_path),
        "guide": args.guide,
        "scoped_docs": args.scoped_docs,
        "model": args.model,
        "seed": args.seed,
        "num_functions": args.num_functions,
    }
    report = write_report(results, run_root, args.tag, meta)
    print(json.dumps({k: report[k] for k in
                      ("tag", "readiness_score", "puzzles", "successes",
                       "mean_section_progress", "mean_turns", "total_tokens")}, indent=2))
    print(f"report: {run_root / 'puzzle_report.json'}")
    # non-zero on failures so AIDEAL's fix loop can react
    return 0 if report["successes"] == report["puzzles"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
