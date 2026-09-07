#!/usr/bin/env python3
"""Observe existing pipelines and preserve retry/repair evidence; never run jobs.

Reports belong in a separate audit worktree. Raw snapshots are local, immutable,
and content-addressed. Checkpoint ledgers retain all fingerprints and attempts;
only the current fingerprint contributes to the displayed provisional counts.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import time
from zoneinfo import ZoneInfo

import yaml


REPOS = {
    "mir_eval": ("GRAIL_mir_eval", "experiments/external/mir_eval", "docs/eval", 148),
    "thumbnailator": ("GRAIL_thumbnailator", "experiments/external/thumbnailator", "docs/eval", 149),
    "tslearn": ("GRAIL_tslearn_full235", "experiments/tslearn", "docs/eval", 235),
    "mdanalysis": ("GRAIL_mdanalysis_full1032", "experiments/mdanalysis", "docs/full_1032", 1032),
}
CELLS = ("A1", "A2", "B1", "B2")
DEADLINE = datetime(2026, 9, 9, 11, tzinfo=ZoneInfo("America/Los_Angeles"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic(path: Path, value: str) -> None:
    if path.exists() and path.read_text() == value:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(value, encoding="utf-8")
    tmp.replace(path)


def dump(path: Path, value) -> None:
    atomic(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text())
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def read_checkpoint(path: Path) -> tuple[list[dict], list[str]]:
    try:
        lines = path.read_text().splitlines(keepends=True)
    except FileNotFoundError:
        return [], []
    rows, errors = [], []
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            if not isinstance(row, dict) or not row.get("name"):
                raise ValueError("checkpoint row lacks API name")
            rows.append(dict(row, checkpoint_line=index + 1))
        except ValueError:
            # A writer may be between write and flush on its final line.
            if index != len(lines) - 1 or line.endswith("\n"):
                errors.append(f"invalid checkpoint line {index + 1}: {path}")
    return rows, errors


def primary_category(row: dict, detail: dict | None = None) -> tuple[str, str]:
    if row.get("status") == "pass":
        return "pass", ""
    category = row.get("error_category") or "unknown"
    error = str(row.get("error") or "")
    if category == "llm-error":
        return "llm-error", "Provider outcome; retry, never count as a documentation failure."
    if "cannot import name" in error:
        return "api-identity", "Import/member selection failed; the runner's infrastructure label needs review."
    if category == "infra":
        return "test/scaffold", "Runner classified this as infrastructure."
    code = detail.get("code", "") if isinstance(detail, dict) else ""
    writes_file = ("open(" in code and any(token in code for token in ('"w"', "'w'", '"wb"', "'wb'"))) or "wavfile.write(" in code
    if "FileNotFoundError" in error and "/output/" in error and writes_file:
        return "test/scaffold", "Generated code tried to write under the supplied, absent output directory."
    # Execution symptoms alone cannot prove that the documentation is wrong.
    return "unknown", f"Observed {category}; doc attribution requires source, document, and snippet review."


def summarize(names: list[str], events: list[dict], final: dict, repair: dict) -> dict:
    run = final.get("run") or {}
    fingerprint = run.get("experiment_fingerprint") or next((
        e.get("experiment_fingerprint") for e in reversed(events)
        if e.get("experiment_fingerprint")), None)
    current = [e for e in events if e.get("experiment_fingerprint") == fingerprint]
    latest = {e["name"]: e for e in current}
    metrics = final.get("metrics") or latest
    attempts = defaultdict(list)
    for event in current:
        attempts[event["name"]].append(event)
    rows = []
    for name in names:
        metric = metrics.get(name) or {}
        repair_api = (repair.get("apis") or {}).get(name) or {}
        category, reason = primary_category(metric, (final.get("details") or {}).get(name))
        history = attempts[name]
        rows.append({
            "api": name,
            "status": metric.get("status", "pending"),
            "primary_category": category if metric else "pending",
            "runner_category": metric.get("error_category"),
            "category_reason": reason if metric else "Not yet observed.",
            "error": metric.get("error"),
            "source": metric.get("source"),
            "doc_chars": metric.get("doc_chars"),
            "checkpoint_attempts": len(history),
            "provider_error_attempts": sum(e.get("error_category") == "llm-error" for e in history),
            "provider_internal_retries": None,
            "recorded_successful_llm_calls": sum(e.get("llm_calls", 0) or 0 for e in history),
            "attempt_history": [{k: e.get(k) for k in (
                "checkpoint_line", "status", "error_category", "error", "attempts",
                "wall_s", "llm_calls", "input_tokens", "output_tokens", "pass_round")}
                for e in history],
            "repair_status": repair_api.get("status"),
            "doc_rounds_used": repair_api.get("rounds_used"),
            "doc_rounds": repair_api.get("doc_rounds") or [],
            "repair_evidence": repair_api,
        })
    counts = Counter(r["status"] for r in rows)
    errors = []
    if metrics and set(metrics) - set(names):
        errors.append("metrics contain APIs outside the frozen manifest")
    complete = bool(final) and set(metrics) == set(names) and bool(fingerprint)
    complete = complete and run.get("api_count") == len(names) and run.get("max_fix_rounds") == 0
    complete = complete and bool(run.get("fingerprint_components"))
    complete = complete and not any(r["runner_category"] == "llm-error" for r in rows)
    return {
        "status": "complete" if complete else "partial" if metrics else "pending",
        "expected": len(names), "counts": dict(counts), "fingerprint": fingerprint,
        "errors": errors,
        "failure_categories": dict(Counter(r["primary_category"] for r in rows if r["status"] == "fail")),
        "recorded_provider_errors_all_fingerprints": sum(e.get("error_category") == "llm-error" for e in events),
        "observed_fingerprints": sorted({e.get("experiment_fingerprint", "") for e in events}),
        "all_checkpoint_events": events,
        "repair_summary": {k: repair.get(k) for k in (
            "attempted", "processed", "doc_fixed", "doc_rounds", "retry_rounds", "outcomes", "blocked")},
        "rows": rows,
    }


def snapshot(path: Path, out: Path) -> dict | None:
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        return None
    sha = digest(data)
    dest = out / "snapshots" / sha
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("xb") as stream:
            stream.write(data)
    return {"path": str(path), "sha256": sha, "snapshot": str(dest)}


def inspect_cell(base: Path, repo: str, cell: str, out: Path) -> dict:
    prefix, relative, docs, count = REPOS[repo]
    wt = base / f"{prefix}_{cell}"
    root = wt / relative
    manifest = root / docs / "api_manifest.json"
    if not manifest.exists():
        suffix = "setup" if repo in ("mir_eval", "thumbnailator") else "freeze"
        manifest = base / f"{prefix}_{suffix}" / relative / docs / "api_manifest.json"
    names = read_json(manifest).get("apis") or []
    if len(names) != count or len(set(names)) != count:
        raise ValueError(f"{repo}: expected {count} unique names in {manifest}")
    cell_dir = root / docs / cell
    final = read_json(cell_dir / "comprehension.json")
    if final:
        details = final.setdefault("details", {})
        for name in final.get("metrics", {}):
            detail = details.get(name)
            if not isinstance(detail, dict):
                detail = {}
                details[name] = detail
            if not detail.get("code") and "/" not in name and ".." not in name:
                script_dir = root / ".aideal_exec" / cell / f"run_{name}"
                for script_name in ("api_test.py", "ApiTest.java", "ApiTest.scala"):
                    script = script_dir / script_name
                    if script.is_file():
                        detail["code"] = script.read_text()
                        break
    repair = read_json(cell_dir / "docfix.json")
    checkpoint = root / ".aideal_exec" / cell / "comprehension_progress.jsonl"
    events, errors = read_checkpoint(checkpoint)
    report = summarize(names, events, final, repair)
    review_path = Path(__file__).resolve().parent / "failure_reviews" / f"{repo}_{cell}.json"
    review = read_json(review_path)
    result_path = cell_dir / "comprehension.json"
    if review and result_path.is_file() and review.get("result_sha256") == digest(result_path.read_bytes()):
        for row in report["rows"]:
            annotation = review.get("apis", {}).get(row["api"])
            if annotation and row["status"] == "fail":
                row["primary_category"] = annotation["primary_category"]
                row["category_reason"] = annotation["reason"]
                row["review_evidence"] = annotation
        report["failure_categories"] = dict(Counter(r["primary_category"] for r in report["rows"] if r["status"] == "fail"))
        report["manual_review"] = str(review_path)
    report["errors"].extend(errors)
    report["worktree"] = str(wt)
    report["checkpoint"] = str(checkpoint)
    report["manifest"] = str(manifest)
    report["manifest_file_sha256"] = digest(manifest.read_bytes())
    report["evidence"] = []
    for p in [cell_dir / "comprehension.json", cell_dir / "docfix.json"]:
        entry = snapshot(p, out)
        if entry:
            report["evidence"].append(entry)
    # Preserve append-only checkpoints as ledgers, rather than repeatedly
    # copying their growing prefix into quadratic-sized snapshots.
    existing = read_json(out / repo / cell / "ledger.json")
    old_events = existing.get("all_checkpoint_events") or []
    if old_events and events[:len(old_events)] != old_events:
        dump(out / repo / cell / f"previous_ledger_{digest(json.dumps(old_events).encode())}.json", existing)
    dump(out / repo / cell / "ledger.json", report)
    fields = ["api", "status", "primary_category", "runner_category", "checkpoint_attempts",
              "provider_error_attempts", "provider_internal_retries", "doc_rounds_used",
              "repair_status", "source", "error", "category_reason"]
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(report["rows"])
    atomic(out / repo / cell / "ledger.csv", stream.getvalue())
    return {k: v for k, v in report.items() if k not in ("rows", "all_checkpoint_events")}


def watchdogs(main: Path, out: Path) -> dict:
    paths = list((main / "experiments/external").glob("*watchdog.state.json"))
    paths += list(main.parent.glob("*_watchdog.state.json"))
    for prefix, relative, docs, _ in REPOS.values():
        for suffix in ("freeze", "setup"):
            paths += list((main.parent / f"{prefix}_{suffix}" / relative / docs).glob("**/*.state.json"))
    result = {}
    for path in sorted(set(paths)):
        data = read_json(path)
        if not data.get("jobs"):
            continue
        plan = Path(data.get("plan", ""))
        plan_data = yaml.safe_load(plan.read_text()) if plan.is_file() else {}
        jobs = {j["id"]: j for j in (plan_data or {}).get("jobs", [])}
        entry = {"status": data.get("status"), "plan": str(plan),
                 "plan_hash_matches": plan.is_file() and digest(plan.read_bytes()) == data.get("plan_sha256"),
                 "jobs": data["jobs"]}
        for job_id, row in entry["jobs"].items():
            spec = jobs.get(job_id) or {}
            inventory = Path(spec.get("environment_inventory", ""))
            cwd = Path(spec.get("cwd", main))
            if not inventory.is_absolute():
                inventory = cwd / inventory
            if inventory.is_file():
                row["declared_inventory_sha256"] = digest(inventory.read_bytes())
            pid = row.get("pid")
            if pid:
                try:
                    os.kill(pid, 0)
                    row["pid_exists"] = True
                except ProcessLookupError:
                    row["pid_exists"] = False
                except PermissionError:
                    row["pid_exists"] = "permission-denied"
        result[str(path)] = entry
        # Watchdog log records attempts and timestamps; heartbeat is omitted
        # from reports so a stable waiting queue does not generate commits.
        log = path.with_suffix(".log")
        if log.is_file():
            atomic(out / "watchdog_logs" / (digest(str(path).encode())[:12] + ".txt"), log.read_text())
    return result


def comparison_report(base: Path, repo: str, cells: dict, out: Path) -> None:
    prefix, relative, docs, count = REPOS[repo]
    results, evidence, problems = {}, {}, []
    for cell in CELLS:
        wt = base / f"{prefix}_{cell}"
        p = wt / relative / docs / cell / "comprehension.json"
        result = read_json(p)
        if result:
            results[cell] = result
        inventory = wt / relative / docs / "setup" / f"environment_{cell}.txt"
        evidence[cell] = {"result": str(p), "inventory": str(inventory)}
        if wt.exists():
            for key, args in [("branch", ["branch", "--show-current"]), ("commit", ["rev-parse", "HEAD"])]:
                evidence[cell][key] = subprocess.check_output(["git", "-C", str(wt), *args], text=True).strip()
        if inventory.is_file():
            raw = inventory.read_text()
            evidence[cell]["inventory_sha256"] = digest(raw.encode())
            comparable = raw
            if repo == "thumbnailator":
                # ZIP timestamps make independently built JAR byte hashes differ.
                # Verify the inventory's raw hash before comparing entry payloads.
                import zipfile
                jar = wt / relative / "source/target/thumbnailator-0.4.21.jar"
                if jar.is_file() and f"jar_sha256={digest(jar.read_bytes())}" in raw:
                    with zipfile.ZipFile(jar) as archive:
                        content_hash = hashlib.sha256()
                        for entry in sorted(archive.namelist()):
                            content_hash.update(entry.encode() + b"\0" + archive.read(entry))
                    evidence[cell]["jar_payload_sha256"] = content_hash.hexdigest()
                    comparable = re.sub(r"(?m)^jar_sha256=.*$", "jar_payload_sha256=" + content_hash.hexdigest(), raw)
            # Cell identity, experiment commit, and condition config are recorded
            # separately. Everything describing packages/runtime remains strict.
            normalized = "\n".join(line for line in comparable.replace(str(wt), "<WORKTREE>").splitlines()
                                   if not line.startswith(("cell=", "grail_commit=", "config_sha256=")))
            evidence[cell]["comparable_environment_sha256"] = digest(normalized.encode())
            if result:
                recorded = (result.get("run", {}).get("fingerprint_components", {}).get("interpreter", {})
                            .get("environment_sha256"))
                evidence[cell]["fingerprint_matches_cell_inventory"] = recorded == digest(raw.encode())
        tests = []
        for scope in [wt / relative / docs / cell, wt / relative / docs / "setup"]:
            for p2p in scope.glob("*PASS_TO_PASS*"):
                if p2p.suffix in (".md", ".json"):
                    tests.append(str(p2p))
        evidence[cell]["pass_to_pass"] = tests
        evidence[cell]["verified_test_phases"] = {}
        for phase in ("BEFORE", "AFTER"):
            evidence[cell]["verified_test_phases"][phase] = any(
                phase in Path(test).name and Path(test).suffix == ".md" and re.search(
                    r"(?m)^- (?:Exit code: 0|Result: PASS)\s*$", Path(test).read_text()) is not None
                for test in tests)
    all_complete = all(cells.get(c, {}).get("status") == "complete" for c in CELLS)
    if all_complete:
        first = results["A1"]["run"]
        for cell, result in results.items():
            run = result["run"]
            expected_doc = {"A1": "original", "A2": "aideal", "B1": "original+aideal", "B2": "aideal"}
            if result.get("doc_source") != expected_doc[cell]:
                problems.append(f"{cell}: wrong document treatment")
            for key in ("manifest_sha256", "doc_scope", "models", "max_fix_rounds", "class_context", "timeout_s"):
                if run.get(key) != first.get(key):
                    problems.append(f"{cell}: {key} differs from A1")
            for key in ("source", "fixtures", "scaffold", "engine"):
                if run.get("fingerprint_components", {}).get(key) != first.get("fingerprint_components", {}).get(key):
                    problems.append(f"{cell}: {key} differs from A1")
            def execution_spec(value):
                cfg = dict(value.get("fingerprint_components", {}).get("execute_config") or {})
                for path_key in ("work_dir", "output_dir"):
                    cfg.pop(path_key, None)
                return cfg
            if execution_spec(run) != execution_spec(first):
                problems.append(f"{cell}: execution protocol differs beyond isolated output paths")
            if set(result["metrics"]) != set(results["A1"]["metrics"]):
                problems.append(f"{cell}: API identities differ")
            if not evidence[cell].get("comparable_environment_sha256"):
                problems.append(f"{cell}: missing per-cell environment inventory")
            if not evidence[cell]["verified_test_phases"]["BEFORE"]:
                problems.append(f"{cell}: passing upstream-before evidence missing")
        envs = {e.get("comparable_environment_sha256") for e in evidence.values()}
        if len(envs) != 1:
            problems.append("per-cell dependency/runtime inventories differ after path normalization")
        # A final result alone does not establish a completed repair treatment.
        for cell in ("B1", "B2"):
            repair = read_json(out / repo / cell / "ledger.json").get("repair_summary", {})
            if repair.get("attempted") is None or repair.get("processed") != repair.get("attempted"):
                problems.append(f"{cell}: repair completion evidence missing")
            if not evidence[cell]["verified_test_phases"]["AFTER"]:
                problems.append(f"{cell}: passing upstream-after evidence missing")
    status = "PARTIAL" if not all_complete else "INVALID" if problems else "VALID WITH RECORDED LIMITATIONS"
    lines = [f"# {repo} detailed A1/A2/B1/B2 report", "", f"**Comparison status: {status}.**", "",
             f"Frozen denominator: {count} public API names. Final evaluations allow zero code-fix rounds. "
             "B cells are fresh evaluations following at most five document-repair rounds, with two stuck rounds and no separate retry rounds.", "",
             "## Reproducibility", "",
             "Exact result paths, branches, commits, environment hashes and PASS_TO_PASS evidence are recorded in provenance.json. "
             "The native result JSON retains source/fixture/scaffold/engine/model/document fingerprints. "
             "Full checkpoint and document-round histories are in each cell ledger.json; ledger.csv contains every manifest API, including pending APIs.", "",
             "## Cell results", "",
             "| Cell | State | Pass | APIs | Infra/provider excluded | Raw % | Scored % |",
             "|---|---|---:|---:|---:|---:|---:|"]
    percentages = {}
    for cell in CELLS:
        result = results.get(cell, {})
        metrics = result.get("metrics") or {}
        if not metrics or cells.get(cell, {}).get("status") != "complete":
            lines.append(f"| {cell} | pending/partial | — | {count} | — | — | — |")
            continue
        passed = sum(m.get("status") == "pass" for m in metrics.values())
        excluded = sum(m.get("status") != "pass" and m.get("error_category") in {"infra", "llm-error"} for m in metrics.values())
        raw = 100 * passed / count
        scored = 100 * passed / (count - excluded) if count > excluded else None
        percentages[cell] = raw
        lines.append(f"| {cell} | complete | {passed} | {count} | {excluded} | {raw:.2f} | {f'{scored:.2f}' if scored is not None else 'undefined'} |")
    lines += ["", "The scored column uses native infrastructure/provider labels. Secondary harness diagnoses are reported separately and do not rewrite outcomes.", "",
              "## Effects", ""]
    if all_complete and not problems:
        a1, a2, b1, b2 = [percentages[c] for c in CELLS]
        lines += [f"- Generation A2−A1: {a2-a1:+.2f} pp raw.", f"- Original repair B1−A1: {b1-a1:+.2f} pp raw.",
                  f"- Generated repair B2−A2: {b2-a2:+.2f} pp raw.", f"- Total B2−A1: {b2-a1:+.2f} pp raw.",
                  f"- Interaction: {(b2-a2)-(b1-a1):+.2f} pp raw."]
    else:
        lines += ["Effects withheld until all four matched final cells and their repair/test evidence exist."]
    lines += ["", "## Failure categories and round accounting", ""]
    for cell in CELLS:
        ledger = read_json(out / repo / cell / "ledger.json")
        lines += [f"### {cell}", "", f"Primary failure categories: {json.dumps(ledger.get('failure_categories', {}), sort_keys=True)}.", "",
                  f"Recorded provider-error attempts across all checkpoint fingerprints: {ledger.get('recorded_provider_errors_all_fingerprints', 0)}. "
                  "Provider-internal retries are not recorded by the existing client and cannot be inferred from the configured limit. "
                  "Watchdog logs retain process attempts; checkpoint attempts and document-fix rounds are separate ledger fields.", ""]
        for row in ledger.get("rows", []):
            if row["status"] != "fail" and not row.get("repair_evidence"):
                continue
            error = str(row.get("error") or "none captured").replace("`", "'").replace("\n", " ")
            lines += [f"- `{row['api']}`: {row['primary_category']}; native={row.get('runner_category')}; "
                      f"checkpoint attempts={row['checkpoint_attempts']}; provider-error attempts={row['provider_error_attempts']}; "
                      f"document rounds={row.get('doc_rounds_used')}; repair={row.get('repair_status')}. "
                      f"Source: `{row.get('source')}`. Error: `{error[:700]}`. "
                      f"Review: {row['category_reason']}"]
        lines.append("")
    lines += ["## Validity and remaining review", ""]
    lines += [f"- {p}" for p in problems]
    if any(e.get("fingerprint_matches_cell_inventory") is False for e in evidence.values()):
        lines += ["- The nested watchdog inherited the outer freeze environment fingerprint. Per-cell inventories are retained separately; "
                  "the final comparison checks their normalized runtime/dependency content. This provenance limitation must remain visible."]
    lines += ["- Recorded PASS_TO_PASS result/exit-status markers and per-cell fixture fingerprints are checked before effects are released.",
              "- Unknown primary categories require source/document review; do not relabel provider errors as documentation failures.",
              "- Report runtime from the first start through completion, including watchdog waits, rather than the last resumed invocation alone.", ""]
    dump(out / repo / "provenance.json", evidence)
    atomic(out / repo / "DETAILED_REPORT.md", "\n".join(lines))


def audit(main: Path, out: Path) -> dict:
    summary = {"deadline": DEADLINE.isoformat(), "cells": {}, "errors": []}
    for repo in REPOS:
        summary["cells"][repo] = {}
        for cell in CELLS:
            try:
                summary["cells"][repo][cell] = inspect_cell(main.parent, repo, cell, out)
            except Exception as exc:
                summary["errors"].append(f"{repo}/{cell}: {type(exc).__name__}: {exc}")
        comparison_report(main.parent, repo, summary["cells"][repo], out)
    summary["watchdogs"] = watchdogs(main, out)
    for path, state in summary["watchdogs"].items():
        if not state["plan_hash_matches"] and state["status"] == "running":
            summary["errors"].append(f"Watchdog plan drift: {path}")
        if state["status"] == "running":
            for name, row in state["jobs"].items():
                if row.get("status") == "running" and row.get("pid_exists") is False:
                    summary["errors"].append(f"Watchdog reports missing process: {name}")
    lines = ["# AIDEAL overnight evidence audit", "",
             f"Deadline: {DEADLINE.isoformat()}. This observer never starts, stops, or restarts experiment jobs.", "",
             "| Repository | Cell | State | Pass | Fail | Pending | Recorded provider-error attempts |",
             "|---|---|---|---:|---:|---:|---:|"]
    for repo, cells in summary["cells"].items():
        for cell, row in cells.items():
            c = row["counts"]
            lines.append(f"| {repo} | {cell} | {row['status']} | {c.get('pass', 0)} | {c.get('fail', 0)} | {c.get('pending', 0)} | {row['recorded_provider_errors_all_fingerprints']} |")
    lines += ["", "## Interpretation", "",
              "Partial counts are checkpoints, not final results. Provider failures remain visible and prevent completion. "
              "Per-API ledger.json/ledger.csv files include pending APIs, checkpoint attempts, errors, document rounds, and repair evidence. "
              "Provider-internal retries are unobserved in existing logs and are null, not zero. "
              "The configured retry ceiling is not an observed retry count. Unknown failure attribution requires review; execution errors alone do not prove a documentation defect.", "",
              "Raw final results are preserved unchanged. Secondary harness diagnoses do not rewrite headline scores. "
              "Runtime and usage in a resumed final JSON describe its last invocation; use checkpoint histories and watchdog start/end logs for total accounting.", "",
              "RDPro is reuse-only. Its queued entry point verifies retained evidence and exits without paid execution. "
              "Sedona preparation remains deferred until MDAnalysis has completed.", "", "## Attention", ""]
    lines += [f"- {error}" for error in summary["errors"]] or ["- No structural errors found by this observer."]
    dump(out / "status.json", summary)
    atomic(out / "STATUS.md", "\n".join(lines) + "\n")
    priorities = ("mir_eval", "thumbnailator", "tslearn")
    complete = all(summary["cells"].get(repo, {}).get(cell, {}).get("status") == "complete"
                   for repo in priorities for cell in CELLS)
    package = ["# AIDEAL Wednesday detailed priority report", "",
               f"**Status: {'All priority measurements complete; see per-repository validity decisions' if complete else 'PARTIAL — experiments are still running'}.**", "",
               f"Delivery deadline: {DEADLINE.isoformat()}.", "",
               "Scope: mir_eval (148 APIs), Thumbnailator (149 APIs), tslearn (235 APIs), each with A1/A2/B1/B2. "
               "MDAnalysis, Apache Sedona and an RDPro rerun are outside this deadline package.", "",
               "## Results, all failures, and every observed retry/repair round", ""]
    for repo in priorities:
        package += [f"- [{repo} detailed report]({repo}/DETAILED_REPORT.md): result table, effects, validity limitations and per-API failure narrative.",
                    f"  [{repo} provenance]({repo}/provenance.json): branches, commits, result and test paths, inventory hashes."]
    package += ["", "[Live status](STATUS.md) · [Machine-readable status](status.json)", "",
                "Each repository/cell directory contains ledger.csv and ledger.json covering all manifest APIs. "
                "Provider-internal retries that were never logged remain explicitly unknown. Native experiment results and scores are retained unchanged.", "",
                "The first snapshot at or after 10:45 AM Wednesday is frozen alongside this live report, "
                "including partial outcomes if provider failures remain. Missing results are never marked complete to meet the deadline.", ""]
    atomic(out / "DETAILED_PRIORITY_REPORT.md", "\n".join(package))
    cutoff = DEADLINE.timestamp() - 15 * 60
    if time.time() >= cutoff and not (out / "deadline_snapshot" / "captured.json").exists():
        # Freeze a self-contained package before 11 AM while the live report
        # continues updating; completion is never fabricated at the cutoff.
        import shutil
        destination = out / "deadline_snapshot"
        destination.mkdir(exist_ok=True)
        for filename in ("STATUS.md", "status.json", "DETAILED_PRIORITY_REPORT.md"):
            shutil.copy2(out / filename, destination / filename)
        for repo in priorities:
            shutil.copytree(out / repo, destination / repo, dirs_exist_ok=True)
        dump(destination / "captured.json", {"time": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
                                             "all_priority_measurements_complete": complete})
    atomic(out / ".gitignore", "snapshots/\nheartbeat.json\nobserver.lock\nobserver.log\n")
    dump(out / "heartbeat.json", {"pid": os.getpid(), "time": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
                                  "hours_to_deadline": (DEADLINE.timestamp() - time.time()) / 3600})
    return summary


def commit_reports(out: Path) -> None:
    root = Path(subprocess.check_output(["git", "-C", str(out), "rev-parse", "--show-toplevel"], text=True).strip())
    branch = subprocess.check_output(["git", "-C", str(root), "branch", "--show-current"], text=True).strip()
    if branch != "aideal/overnight-evidence-audit":
        raise RuntimeError(f"automatic audit commits require the isolated audit branch, got {branch}")
    # Refuse to absorb anything another process has staged.
    staged = subprocess.check_output(["git", "-C", str(root), "diff", "--cached", "--name-only"], text=True)
    if staged.strip():
        raise RuntimeError("audit index already contains staged changes")
    subprocess.run(["git", "-C", str(root), "add", "--", str(out.relative_to(root))], check=True)
    if subprocess.run(["git", "-C", str(root), "diff", "--cached", "--quiet"]).returncode:
        subprocess.run(["git", "-C", str(root), "commit", "-m", "Checkpoint overnight attempt and repair evidence"], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main-worktree", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--poll-seconds", type=int, default=60)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    with (out / "observer.lock").open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        last_commit = 0.0
        while True:
            try:
                summary = audit(args.main_worktree.resolve(), out)
                print(json.dumps({"time": time.time(), "errors": summary["errors"]}), flush=True)
                if args.commit and time.monotonic() - last_commit >= 900:
                    commit_reports(out)
                    last_commit = time.monotonic()
            except Exception as exc:
                print(f"audit error: {type(exc).__name__}: {exc}", flush=True)
                if not args.watch:
                    raise
            if not args.watch:
                return 0
            time.sleep(max(1, args.poll_seconds))


if __name__ == "__main__":
    raise SystemExit(main())
