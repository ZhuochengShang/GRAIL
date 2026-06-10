from __future__ import annotations

import argparse
import json
import socket
import statistics
import subprocess
import time
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run benchmark_compare.py multiple times and aggregate results.")
    parser.add_argument(
        "--python-bin",
        default="/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python",
    )
    parser.add_argument(
        "--benchmark-script",
        default=str(PACKAGE_DIR / "benchmark_compare.py"),
    )
    parser.add_argument(
        "--output-root",
        default=str(PACKAGE_DIR / "benchmark_repeats"),
    )
    parser.add_argument(
        "--raster-path",
        default="/Users/clockorangezoe/Downloads/Annual_NLCD_LndCov_2024_CU_C1V1/Annual_NLCD_LndCov_2024_CU_C_1V1_clip.tif",
    )
    parser.add_argument(
        "--vector-path",
        default="/Users/clockorangezoe/Downloads/boston_neighborhood_boundaries/Boston_Neighborhood_Boundaries_sample.shp",
    )
    parser.add_argument("--provider", choices=["openai", "google"], default="openai")
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--max-connection-retries", type=int, default=5)
    parser.add_argument("--retry-sleep-seconds", type=int, default=15)
    return parser.parse_args()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def mean_or_none(values: list[float]) -> float | None:
    return round(statistics.mean(values), 4) if values else None


def connectivity_ok(hostname: str = "api.openai.com") -> tuple[bool, str]:
    try:
        socket.gethostbyname(hostname)
        return True, ""
    except Exception as exc:
        return False, repr(exc)


def is_connection_failure(stderr_text: str) -> bool:
    stderr = (stderr_text or "").lower()
    return (
        "apiconnectionerror" in stderr
        or "connection error" in stderr
        or "could not resolve host" in stderr
        or "nodename nor servname provided" in stderr
        or "connecterror" in stderr
    )


def write_repeat_status(repeat_root: Path, payload: dict) -> None:
    (repeat_root / "repeat_status.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_once(args: argparse.Namespace, repeat_idx: int, output_root: Path) -> dict:
    repeat_root = output_root / f"repeat_{repeat_idx:02d}"
    repeat_root.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(Path(args.python_bin).resolve()),
        str(Path(args.benchmark_script).resolve()),
        "--output-root",
        str(repeat_root),
        "--raster-path",
        args.raster_path,
        "--vector-path",
        args.vector_path,
        "--provider",
        args.provider,
        "--model",
        args.model,
    ]
    attempts: list[dict] = []
    proc = None
    repeat_started_at = time.perf_counter()
    print(f"[repeat] start repeat={repeat_idx} output_root={repeat_root}", flush=True)
    write_repeat_status(
        repeat_root,
        {
            "repeat": repeat_idx,
            "status": "started",
            "attempts": attempts,
            "report_path": str(repeat_root / "comparison_report.json"),
        },
    )
    for attempt_idx in range(1, args.max_connection_retries + 1):
        print(f"[repeat] repeat={repeat_idx} attempt={attempt_idx} preflight_dns_check", flush=True)
        ok, reason = connectivity_ok()
        if not ok:
            attempts.append(
                {
                    "attempt": attempt_idx,
                    "status": "preflight_dns_failed",
                    "reason": reason,
                }
            )
            print(
                f"[repeat] repeat={repeat_idx} attempt={attempt_idx} dns_failed reason={reason}",
                flush=True,
            )
            write_repeat_status(
                repeat_root,
                {
                    "repeat": repeat_idx,
                    "status": "retrying_after_dns_failure",
                    "attempts": attempts,
                    "report_path": str(repeat_root / "comparison_report.json"),
                },
            )
            time.sleep(args.retry_sleep_seconds)
            continue

        print(f"[repeat] repeat={repeat_idx} attempt={attempt_idx} launch_benchmark_compare", flush=True)
        write_repeat_status(
            repeat_root,
            {
                "repeat": repeat_idx,
                "status": "running_benchmark_compare",
                "active_attempt": attempt_idx,
                "attempts": attempts,
                "report_path": str(repeat_root / "comparison_report.json"),
            },
        )
        proc = subprocess.run(cmd, capture_output=True, text=True)
        attempts.append(
            {
                "attempt": attempt_idx,
                "status": "subprocess_returned",
                "return_code": proc.returncode,
                "connection_failure": is_connection_failure(proc.stderr),
            }
        )
        print(
            f"[repeat] repeat={repeat_idx} attempt={attempt_idx} "
            f"return_code={proc.returncode} connection_failure={is_connection_failure(proc.stderr)}",
            flush=True,
        )
        write_repeat_status(
            repeat_root,
            {
                "repeat": repeat_idx,
                "status": "subprocess_returned",
                "active_attempt": attempt_idx,
                "attempts": attempts,
                "return_code": proc.returncode,
                "connection_failure": is_connection_failure(proc.stderr),
                "report_path": str(repeat_root / "comparison_report.json"),
            },
        )
        if not is_connection_failure(proc.stderr):
            break
        time.sleep(args.retry_sleep_seconds)

    final_stdout = proc.stdout if proc else ""
    final_stderr = proc.stderr if proc else ""
    (repeat_root / "stdout.log").write_text(final_stdout or "", encoding="utf-8")
    (repeat_root / "stderr.log").write_text(final_stderr or "", encoding="utf-8")
    report_path = repeat_root / "comparison_report.json"
    report = read_json(report_path) if report_path.exists() else {"results": [], "comparison": {}}
    repeat_elapsed = round(time.perf_counter() - repeat_started_at, 2)
    print(
        f"[repeat] done repeat={repeat_idx} elapsed_seconds={repeat_elapsed} report_path={report_path}",
        flush=True,
    )
    write_repeat_status(
        repeat_root,
        {
            "repeat": repeat_idx,
            "status": "completed" if report_path.exists() else "incomplete",
            "elapsed_seconds": repeat_elapsed,
            "attempts": attempts,
            "return_code": proc.returncode if proc else 1,
            "report_path": str(report_path),
            "report_exists": report_path.exists(),
            "partial_report_path": str(repeat_root / "comparison_report.partial.json"),
        },
    )
    return {
        "repeat": repeat_idx,
        "return_code": proc.returncode if proc else 1,
        "report_path": str(report_path),
        "report": report,
        "attempts": attempts,
    }


def aggregate_repeat_reports(reports: list[dict]) -> dict:
    grouped: dict[tuple[str, str], list[dict]] = {}
    for item in reports:
        for result in item.get("report", {}).get("results", []):
            key = (result["task_name"], result["mode"])
            grouped.setdefault(key, []).append(result)

    aggregate_results: list[dict] = []
    for (task_name, mode), items in sorted(grouped.items()):
        successes = [1 if item.get("success") else 0 for item in items]
        correctness = [1 if item.get("correctness_proxy") else 0 for item in items]
        fix_iterations = [float(item.get("fix_iterations", 0) or 0) for item in items]
        llm_calls = [float(item.get("total_llm_calls", 0) or 0) for item in items]
        total_tokens = [float(item.get("total_tokens", 0) or 0) for item in items]
        llm_seconds = [float(item.get("total_llm_seconds", 0.0) or 0.0) for item in items]
        run_seconds = [float(item.get("total_compile_jar_submit_seconds", 0.0) or 0.0) for item in items]
        aggregate_results.append(
            {
                "task_name": task_name,
                "complexity": items[0]["complexity"],
                "mode": mode,
                "runs": len(items),
                "success_count": sum(successes),
                "success_rate": round(sum(successes) / len(items), 4),
                "correctness_count": sum(correctness),
                "correctness_rate": round(sum(correctness) / len(items), 4),
                "avg_fix_iterations": mean_or_none(fix_iterations),
                "avg_total_llm_calls": mean_or_none(llm_calls),
                "avg_total_tokens": mean_or_none(total_tokens),
                "avg_total_llm_seconds": mean_or_none(llm_seconds),
                "avg_total_compile_jar_submit_seconds": mean_or_none(run_seconds),
                "fail_reasons": list(dict.fromkeys(str(item.get("fail_reason", "") or "") for item in items if not item.get("success"))),
            }
        )

    by_task: dict[str, list[dict]] = {}
    for row in aggregate_results:
        by_task.setdefault(row["task_name"], []).append(row)

    comparisons: dict[str, dict] = {}
    for task_name, rows in by_task.items():
        direct = next((row for row in rows if row["mode"] == "direct"), None)
        via_python = next((row for row in rows if row["mode"] == "via-python"), None)
        via_python_raw = next((row for row in rows if row["mode"] == "via-python-raw"), None)
        candidates = [(mode, row) for mode, row in (("direct", direct), ("via-python", via_python), ("via-python-raw", via_python_raw)) if row]
        preferable = "tie"
        if candidates:
            candidates.sort(
                key=lambda item: (
                    -float(item[1]["success_rate"] or 0.0),
                    -float(item[1]["correctness_rate"] or 0.0),
                    float(item[1]["avg_fix_iterations"] if item[1]["avg_fix_iterations"] is not None else 10**9),
                    float(item[1]["avg_total_llm_calls"] if item[1]["avg_total_llm_calls"] is not None else 10**9),
                    float(item[1]["avg_total_tokens"] if item[1]["avg_total_tokens"] is not None else 10**12),
                )
            )
            best_mode, best_row = candidates[0]
            ties = [
                mode
                for mode, row in candidates
                if (
                    row["success_rate"] == best_row["success_rate"]
                    and row["correctness_rate"] == best_row["correctness_rate"]
                    and row["avg_fix_iterations"] == best_row["avg_fix_iterations"]
                    and row["avg_total_llm_calls"] == best_row["avg_total_llm_calls"]
                    and row["avg_total_tokens"] == best_row["avg_total_tokens"]
                )
            ]
            preferable = best_mode if len(ties) == 1 else "tie"
        comparisons[task_name] = {
            "direct": direct,
            "via_python": via_python,
            "via_python_raw": via_python_raw,
            "preferable_strategy": preferable,
        }

    return {
        "aggregate_results": aggregate_results,
        "task_comparisons": comparisons,
        "repeat_reports": [
            {
                "repeat": item["repeat"],
                "return_code": item["return_code"],
                "report_path": item["report_path"],
                "attempts": item.get("attempts", []),
            }
            for item in reports
        ],
    }


def main() -> None:
    args = parse_args()
    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    repeat_reports: list[dict] = []
    for repeat_idx in range(1, args.repeats + 1):
        print(f"[repeat] progress repeat={repeat_idx}/{args.repeats}", flush=True)
        repeat_reports.append(run_once(args, repeat_idx, output_root))
        partial_aggregate_path = output_root / "aggregate_summary.partial.json"
        partial_aggregate = aggregate_repeat_reports(repeat_reports)
        partial_aggregate_path.write_text(json.dumps(partial_aggregate, indent=2), encoding="utf-8")

    aggregate = aggregate_repeat_reports(repeat_reports)
    aggregate_path = output_root / "aggregate_summary.json"
    aggregate_path.write_text(json.dumps(aggregate, indent=2), encoding="utf-8")
    print(f"[repeat] aggregate_summary={aggregate_path}", flush=True)
    print(json.dumps(aggregate, indent=2))
    print(f"aggregate_summary={aggregate_path}")


if __name__ == "__main__":
    main()
