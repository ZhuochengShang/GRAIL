from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PACKAGE_PARENT = PACKAGE_DIR.parent
if str(PACKAGE_PARENT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_PARENT))

from rdpro_section_codegen.file_utils import read_text, write_text


@dataclass
class BenchmarkTask:
    name: str
    complexity: str
    free_text: str


@dataclass
class RunResult:
    task_name: str
    complexity: str
    mode: str
    output_scala: str
    work_dir: str
    success: bool
    correctness_proxy: bool
    fail_reason: str
    completed_sections: int
    planned_sections: int
    fix_iterations: int
    total_llm_calls: int
    total_prompt_tokens: int
    total_completion_tokens: int
    total_tokens: int
    total_llm_seconds: float
    total_compile_jar_submit_seconds: float
    summary_path: str
    metrics_json_path: str
    metrics_csv_path: str


def parse_args() -> argparse.Namespace:
    root = Path("/Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/rdpro_section_codegen")
    notebook_root = root.parent
    doc_root = notebook_root.parent / "Doc"
    parser = argparse.ArgumentParser(description="Compare direct Scala generation vs via-python translation.")
    parser.add_argument(
        "--agent-script",
        default=str(root / "langgraph_section_agent.py"),
    )
    parser.add_argument(
        "--python-bin",
        default="/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python",
    )
    parser.add_argument(
        "--scaffold",
        default=str(root / "job_scaffold.scala"),
    )
    parser.add_argument(
        "--api-doc",
        default=str(doc_root / "rdpro_api_doc_combined.md"),
    )
    parser.add_argument(
        "--guide",
        default=str(notebook_root / "RDProAgentLoop_perAPI_fix_migration_guide.md"),
    )
    parser.add_argument(
        "--raster-path",
        default="/Users/clockorangezoe/Downloads/Annual_NLCD_LndCov_2024_CU_C1V1/Annual_NLCD_LndCov_2024_CU_C_1V1_clip.tif",
    )
    parser.add_argument(
        "--vector-path",
        default="/Users/clockorangezoe/Downloads/boston_neighborhood_boundaries/Boston_Neighborhood_Boundaries_sample.shp",
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "google"],
        default="openai",
    )
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--output-root", default=str(root / "benchmark_runs"))
    parser.add_argument("--max-retries-per-section", type=int, default=5)
    parser.add_argument("--max-total-turns", type=int, default=40)
    parser.add_argument("--compile-timeout-seconds", type=int, default=120)
    parser.add_argument("--jar-timeout-seconds", type=int, default=60)
    parser.add_argument("--submit-timeout-seconds", type=int, default=900)
    return parser.parse_args()


def _build_tasks(raster_path: str, vector_path: str) -> list[BenchmarkTask]:
    simple = BenchmarkTask(
        name="simple_raster_landcover_summary",
        complexity="simple",
        free_text=(
            "Calculate overall land-use category percentages for the NLCD raster and write a CSV summary. "
            f"Input raster path: {raster_path}. "
            "This is a raster-only workflow with no polygon overlay. "
            "Compute class counts and percentages for the whole raster and save a tabular CSV output."
        ),
    )
    complex_task = BenchmarkTask(
        name="complex_boston_neighborhood_summary",
        complexity="complex",
        free_text=(
            "Calculate land-use category percentages and summary statistics for Boston neighborhoods from NLCD raster data. "
            f"Input raster path: {raster_path}. "
            f"Vector neighborhood polygon path: {vector_path}. "
            "This is a per-polygon zonal workflow. "
            "Produce tabular CSV outputs with per-neighborhood class percentages and a neighborhood-level dominant class summary."
        ),
    )
    return [simple, complex_task]


def _extract_path_from_stdout(stdout: str, prefix: str) -> str:
    for line in (stdout or "").splitlines():
        if line.startswith(prefix):
            return line.split("=", 1)[1].strip()
    return ""


def _load_json(path_str: str) -> dict | list:
    if not path_str:
        return {}
    path = Path(path_str)
    if not path.exists():
        return {}
    return json.loads(read_text(path))


def _compute_fix_iterations(events: list[dict]) -> int:
    reject_results = {"validation_reject", "semantic_reject", "run_failed", "final_review_reject"}
    return sum(1 for ev in events if ev.get("result") in reject_results)


def _compute_llm_calls(events: list[dict]) -> int:
    return sum(1 for ev in events if int(ev.get("llm_total_tokens", 0) or 0) > 0)


def _classify_failure(stderr_text: str, return_code: int) -> str:
    stderr = (stderr_text or "").lower()
    if "apiconnectionerror" in stderr or "connection error" in stderr:
        return "connection_error"
    if "could not resolve host" in stderr or "nodename nor servname provided" in stderr or "connecterror" in stderr:
        return "dns_resolution_failed"
    return f"agent exited with code {return_code}"


def _build_command(args: argparse.Namespace, task: BenchmarkTask, mode: str, output_scala: Path, work_dir: Path) -> list[str]:
    return [
        str(Path(args.python_bin).resolve()),
        str(Path(args.agent_script).resolve()),
        "--translation-mode",
        mode,
        "--free-text",
        task.free_text,
        "--scaffold",
        str(Path(args.scaffold).resolve()),
        "--output-scala",
        str(output_scala.resolve()),
        "--work-dir",
        str(work_dir.resolve()),
        "--api-doc",
        str(Path(args.api_doc).resolve()),
        "--guide",
        str(Path(args.guide).resolve()),
        "--provider",
        args.provider,
        "--model",
        args.model,
        "--max-retries-per-section",
        str(args.max_retries_per_section),
        "--max-total-turns",
        str(args.max_total_turns),
        "--compile-timeout-seconds",
        str(args.compile_timeout_seconds),
        "--jar-timeout-seconds",
        str(args.jar_timeout_seconds),
        "--submit-timeout-seconds",
        str(args.submit_timeout_seconds),
    ]


def _run_one(args: argparse.Namespace, task: BenchmarkTask, mode: str, output_root: Path) -> RunResult:
    task_root = output_root / task.name / mode
    scala_dir = task_root / "scala"
    work_dir = task_root / "work"
    stdout_path = task_root / "stdout.log"
    stderr_path = task_root / "stderr.log"
    scala_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    output_scala = scala_dir / f"{task.name}_{mode}.scala"
    cmd = _build_command(args, task, mode, output_scala, work_dir)
    started_at = time.perf_counter()
    print(
        f"[benchmark] start task={task.name} complexity={task.complexity} mode={mode}",
        flush=True,
    )
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = round(time.perf_counter() - started_at, 2)
    write_text(stdout_path, proc.stdout or "")
    write_text(stderr_path, proc.stderr or "")

    summary_path = _extract_path_from_stdout(proc.stdout, "summary_path=")
    metrics_json_path = _extract_path_from_stdout(proc.stdout, "metrics_json_path=")
    metrics_csv_path = _extract_path_from_stdout(proc.stdout, "metrics_csv_path=")

    summary = _load_json(summary_path)
    events = _load_json(metrics_json_path)
    events = events if isinstance(events, list) else []

    success = bool(summary.get("success", False))
    planned_sections = list(summary.get("planned_sections", []) or [])
    completed_sections = list(summary.get("completed_sections", []) or [])

    result = RunResult(
        task_name=task.name,
        complexity=task.complexity,
        mode=mode,
        output_scala=str(output_scala.resolve()),
        work_dir=str(work_dir.resolve()),
        success=success,
        correctness_proxy=success,
        fail_reason=str(summary.get("fail_reason", "") or _classify_failure(proc.stderr, proc.returncode)),
        completed_sections=len(completed_sections),
        planned_sections=len(planned_sections),
        fix_iterations=_compute_fix_iterations(events),
        total_llm_calls=_compute_llm_calls(events),
        total_prompt_tokens=int(summary.get("metrics", {}).get("total_prompt_tokens", 0) or 0),
        total_completion_tokens=int(summary.get("metrics", {}).get("total_completion_tokens", 0) or 0),
        total_tokens=int(summary.get("metrics", {}).get("total_tokens", 0) or 0),
        total_llm_seconds=float(summary.get("metrics", {}).get("total_llm_seconds", 0.0) or 0.0),
        total_compile_jar_submit_seconds=float(
            summary.get("metrics", {}).get("total_compile_jar_submit_seconds", 0.0) or 0.0
        ),
        summary_path=summary_path,
        metrics_json_path=metrics_json_path,
        metrics_csv_path=metrics_csv_path,
    )
    print(
        f"[benchmark] done task={task.name} mode={mode} success={result.success} "
        f"fix_iterations={result.fix_iterations} elapsed_seconds={elapsed}",
        flush=True,
    )
    if result.summary_path:
        print(f"[benchmark] summary_path={result.summary_path}", flush=True)
    return result


def _aggregate(results: list[RunResult]) -> dict:
    by_complexity: dict[str, list[RunResult]] = {}
    for result in results:
        by_complexity.setdefault(result.complexity, []).append(result)

    comparison: dict[str, dict] = {}
    for complexity, items in by_complexity.items():
        direct = next((item for item in items if item.mode == "direct"), None)
        via_python = next((item for item in items if item.mode == "via-python"), None)
        via_python_raw = next((item for item in items if item.mode == "via-python-raw"), None)
        comparison[complexity] = {
            "direct_success": direct.success if direct else None,
            "via_python_success": via_python.success if via_python else None,
            "via_python_raw_success": via_python_raw.success if via_python_raw else None,
            "direct_fix_iterations": direct.fix_iterations if direct else None,
            "via_python_fix_iterations": via_python.fix_iterations if via_python else None,
            "via_python_raw_fix_iterations": via_python_raw.fix_iterations if via_python_raw else None,
            "direct_total_llm_calls": direct.total_llm_calls if direct else None,
            "via_python_total_llm_calls": via_python.total_llm_calls if via_python else None,
            "via_python_raw_total_llm_calls": via_python_raw.total_llm_calls if via_python_raw else None,
            "preferable_strategy": _choose_preference(
                {
                    "direct": direct,
                    "via-python": via_python,
                    "via-python-raw": via_python_raw,
                }
            ),
        }

    return {
        "results": [asdict(result) for result in results],
        "comparison": comparison,
    }


def _choose_preference(candidates: dict[str, RunResult | None]) -> str:
    available = [(mode, result) for mode, result in candidates.items() if result is not None]
    if not available:
        return "tie"
    available.sort(
        key=lambda item: (
            0 if item[1].success else 1,
            0 if item[1].correctness_proxy else 1,
            item[1].fix_iterations,
            item[1].total_llm_calls,
            item[1].total_tokens,
        )
    )
    best_mode, best_result = available[0]
    ties = [
        mode
        for mode, result in available
        if (
            result.success == best_result.success
            and result.correctness_proxy == best_result.correctness_proxy
            and result.fix_iterations == best_result.fix_iterations
            and result.total_llm_calls == best_result.total_llm_calls
            and result.total_tokens == best_result.total_tokens
        )
    ]
    return best_mode if len(ties) == 1 else "tie"


def _write_progress(output_root: Path, results: list[RunResult], completed_runs: int, total_runs: int, active_task: str, active_mode: str) -> None:
    payload = {
        "completed_runs": completed_runs,
        "total_runs": total_runs,
        "active_task": active_task,
        "active_mode": active_mode,
        "report": _aggregate(results),
    }
    write_text(output_root / "comparison_report.partial.json", json.dumps(payload, indent=2))


def main() -> None:
    args = parse_args()
    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    tasks = _build_tasks(args.raster_path, args.vector_path)
    results: list[RunResult] = []
    total_runs = len(tasks) * 3
    completed_runs = 0
    for task in tasks:
        for mode in ("direct", "via-python", "via-python-raw"):
            completed_runs += 1
            print(
                f"[benchmark] progress run={completed_runs}/{total_runs} "
                f"task={task.name} mode={mode}",
                flush=True,
            )
            _write_progress(output_root, results, completed_runs - 1, total_runs, task.name, mode)
            result = _run_one(args, task, mode, output_root)
            results.append(result)
            _write_progress(output_root, results, completed_runs, total_runs, task.name, mode)
            print(json.dumps(asdict(result), indent=2))

    report = _aggregate(results)
    report_path = output_root / "comparison_report.json"
    write_text(report_path, json.dumps(report, indent=2))
    print(f"[benchmark] comparison_report={report_path}", flush=True)
    print(f"comparison_report={report_path}")


if __name__ == "__main__":
    main()
