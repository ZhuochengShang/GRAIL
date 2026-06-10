from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path

from .file_utils import read_text, write_text


def _run_command(cmd: list[str], cwd: Path, timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(cwd),
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ((exc.stdout or b"").decode(errors="ignore") if exc.stdout else "")
        stderr = exc.stderr if isinstance(exc.stderr, str) else ((exc.stderr or b"").decode(errors="ignore") if exc.stderr else "")
        stderr = (stderr + f"\nCommand timed out after {timeout_seconds} seconds.\n").strip() + "\n"
        return subprocess.CompletedProcess(cmd, 124, stdout=stdout, stderr=stderr)


def resolve_cached_package_jars(packages_csv: str) -> list[str]:
    jar_paths: list[str] = []
    search_roots = [
      Path.home() / ".ivy2" / "jars",
      Path.home() / ".m2" / "repository",
      Path.home() / ".cache" / "coursier" / "v1",
      Path.home() / ".cache" / "coursier" / "v2",
    ]

    for package_spec in (packages_csv or "").split(","):
        spec = package_spec.strip()
        if not spec or ":" not in spec:
            continue
        parts = spec.split(":")
        if len(parts) != 3:
            continue
        group_id, artifact_id, version = parts
        ivy_name = f"{group_id.replace('.', '_')}_{artifact_id}-{version}.jar"
        for root in search_roots:
            if not root.exists():
                continue
            if root.name == "jars":
                matches = sorted(root.glob(ivy_name))
            else:
                group_path = Path(*group_id.split("."))
                matches = sorted(root.glob(f"**/{group_path}/{artifact_id}/{version}/{artifact_id}-{version}.jar"))
            if matches:
                jar_paths.append(str(matches[0].resolve()))
                break
    return jar_paths


def build_commands(scala_file: Path, run_root: Path, cfg: dict) -> tuple[list[str], list[str], list[str], Path]:
    env_bin = Path(cfg["env_bin"]).resolve()
    spark_submit = Path(cfg["spark_submit"]).resolve()
    if not spark_submit.exists():
        raise FileNotFoundError(f"spark-submit not found: {spark_submit}")

    scalac_path = shutil.which("scalac")
    jar_path = shutil.which("jar")
    if not scalac_path:
        raise FileNotFoundError("scalac not found on PATH")
    if not jar_path:
        raise FileNotFoundError("jar not found on PATH")
    scalac = Path(scalac_path).resolve()
    jar_tool = Path(jar_path).resolve()

    rdpro_lib = Path(cfg["rdpro_lib_dir"]).resolve()
    rdpro_jars = sorted(str(p) for p in rdpro_lib.glob("*.jar"))
    if not rdpro_jars:
        raise FileNotFoundError(f"No RDPro jars found in: {rdpro_lib}")

    pyspark_jars_dir = (env_bin / ".." / "lib" / "python3.10" / "site-packages" / "pyspark" / "jars").resolve()
    spark_jars = sorted(str(p) for p in pyspark_jars_dir.glob("*.jar")) if pyspark_jars_dir.exists() else []
    if not spark_jars:
        raise FileNotFoundError(f"No PySpark jars found in: {pyspark_jars_dir}")

    classes_dir = run_root / "classes"
    classes_dir.mkdir(parents=True, exist_ok=True)
    app_jar = run_root / "app.jar"

    package_jars = resolve_cached_package_jars(cfg.get("spark_packages", ""))
    compile_classpath = ":".join(rdpro_jars + spark_jars + package_jars)
    compile_cmd = [str(scalac), "-classpath", compile_classpath, "-d", str(classes_dir), str(scala_file)]
    jar_cmd = [str(jar_tool), "cf", str(app_jar), "-C", str(classes_dir), "."]
    submit_cmd = [
        str(spark_submit),
        "--class", "GeoJobMain",
        "--master", "local[*]",
        "--repositories", cfg["spark_repositories"],
        "--packages", cfg["spark_packages"],
        "--jars", ",".join(rdpro_jars),
        str(app_jar),
    ]
    return compile_cmd, jar_cmd, submit_cmd, app_jar


def run_compile_package_submit(scala_text: str, section: str, turn: int, cfg: dict, now_stamp) -> dict:
    work_dir = Path(cfg["work_dir"]).resolve()
    stamp = now_stamp()
    run_root = work_dir / f"run_{section}_t{turn}_{stamp}"
    run_root.mkdir(parents=True, exist_ok=True)

    scala_file = run_root / "candidate.scala"
    write_text(scala_file, scala_text)
    compile_cmd, jar_cmd, submit_cmd, app_jar = build_commands(scala_file, run_root, cfg)

    out_log = run_root / "stdout.log"
    err_log = run_root / "stderr.log"
    merged_log = run_root / "merged.log"
    report_log = run_root / "report.log"

    compile_timeout = int(cfg.get("compile_timeout_seconds", 120) or 120)
    jar_timeout = int(cfg.get("jar_timeout_seconds", 60) or 60)
    submit_timeout = int(cfg.get("submit_timeout_seconds", 900) or 900)

    t0 = time.perf_counter()
    tc0 = time.perf_counter()
    compile_res = _run_command(compile_cmd, run_root, compile_timeout)
    compile_seconds = time.perf_counter() - tc0
    jar_res = None
    submit_res = None
    jar_seconds = 0.0
    submit_seconds = 0.0

    if compile_res.returncode == 0:
        tj0 = time.perf_counter()
        jar_res = _run_command(jar_cmd, run_root, jar_timeout)
        jar_seconds = time.perf_counter() - tj0
    if jar_res and jar_res.returncode == 0:
        ts0 = time.perf_counter()
        submit_res = _run_command(submit_cmd, run_root, submit_timeout)
        submit_seconds = time.perf_counter() - ts0

    steps = [("compile", compile_res), ("jar", jar_res), ("submit", submit_res)]
    with out_log.open("w", encoding="utf-8") as fout, err_log.open("w", encoding="utf-8") as ferr, merged_log.open("w", encoding="utf-8") as fmerge:
        for name, res in steps:
            if res is None:
                continue
            out = res.stdout or ""
            err = res.stderr or ""
            if out:
                fout.write(f"\n===== {name} stdout =====\n{out}")
                if not out.endswith("\n"):
                    fout.write("\n")
            if err:
                ferr.write(f"\n===== {name} stderr =====\n{err}")
                if not err.endswith("\n"):
                    ferr.write("\n")
            for ln in out.splitlines(keepends=True):
                fmerge.write(f"[stdout] {ln}")
            for ln in err.splitlines(keepends=True):
                fmerge.write(f"[stderr] {ln}")

    rc = submit_res.returncode if submit_res is not None else (jar_res.returncode if jar_res is not None else compile_res.returncode)
    merged_text = read_text(merged_log)
    marker = f"__STEP__ {section}_done"
    run_ok = (rc == 0) and (marker in merged_text)

    report = [
        f"section={section}",
        f"turn={turn}",
        f"return_code={rc}",
        f"run_ok={run_ok}",
        f"jar={app_jar}",
        "",
        "[commands]",
        "compile: " + " ".join(compile_cmd),
        "jar: " + " ".join(jar_cmd),
        "submit: " + " ".join(submit_cmd),
        "",
        "[stderr full]",
        read_text(err_log),
        "",
        "[stdout full]",
        read_text(out_log),
    ]
    write_text(report_log, "\n".join(report))

    return {
        "run_ok": run_ok,
        "rc": rc,
        "stdout_tail": read_text(out_log)[-12000:],
        "stderr_tail": read_text(err_log)[-12000:],
        "report_log": str(report_log),
        "merged_log": str(merged_log),
        "candidate_path": str(scala_file),
        "compile_seconds": round(compile_seconds, 4),
        "jar_seconds": round(jar_seconds, 4),
        "submit_seconds": round(submit_seconds, 4),
        "total_seconds": round(time.perf_counter() - t0, 4),
    }
