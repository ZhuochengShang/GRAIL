"""Build an offline evidence review and portable HTML snapshot; never call an LLM."""
import argparse
import base64
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import textwrap

from aideal.readme_agent import parse_readme

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text())


def fingerprint(parts):
    return sha(json.dumps(parts, sort_keys=True, separators=(",", ":"), default=str).encode())


def legacy_rows(project):
    directory = project / ".aideal_exec/A1"
    raw = (directory / "comprehension_progress.jsonl").read_bytes()
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    record = read(directory / "checkpoint_compatibility.json")
    selected = {r["name"]: r for r in rows if r["experiment_fingerprint"] == record["legacy_fingerprint"]}
    selected.update({r["name"]: r for r in rows if r["experiment_fingerprint"] == fingerprint(record["current_components"])})
    return selected, {"checkpoint_sha256": sha(raw), "bytes": len(raw),
                      "legacy_fingerprint": record["legacy_fingerprint"],
                      "current_fingerprint": fingerprint(record["current_components"])}


def build(a1, a2, out):
    result_path = a2 / "docs/eval/A2/comprehension.json"
    raw = result_path.read_bytes()
    result = json.loads(raw)
    docs_path = a2 / "docs/eval/A2/LLM_readme.md"
    entries = {entry.name: entry.body for entry in parse_readme(docs_path)}
    findings = read(HERE / "findings.json")
    a1rows, a1proof = legacy_rows(a1)
    metrics = result["metrics"]
    assert set(a1rows) == set(metrics)
    assert {row["api"] for row in findings} == {n for n, m in metrics.items() if m["status"] != "pass"}
    source_evidence = {}
    for row in findings:
        name = row["api"]
        entry = entries[name]
        assert sha(entry.encode()) == metrics[name]["document_sha256"], name
        row.update(native_category=metrics[name]["error_category"],
                   a1_status=a1rows[name]["status"], a1_category=a1rows[name].get("error_category"),
                   document=entry, document_sha256=sha(entry.encode()),
                   execution=result["details"][name], input_data=row.pop("input"),
                   confidence="observed failure mechanism; documentation causality not experimentally isolated",
                   proposal_status="proposed; review before application")
        retained = Path(row["execution"].get("scala_file", ""))
        if retained.is_file():
            source = retained.read_text()
            region = source.split("// TODO API_TEST_START", 1)[-1].split("// TODO API_TEST_END", 1)[0]
            region = textwrap.dedent(region).strip()
            row["retained_test"] = {"path": str(retained), "sha256": sha(retained.read_bytes()),
                "code": region, "native_code_prefix_matches": region.startswith(row["execution"].get("code", "")),
                "blank_line_normalized_prefix_matches": re.sub(r"(?m)^[ \t]+$", "", region).startswith(
                    re.sub(r"(?m)^[ \t]+$", "", row["execution"].get("code", "")))}
        for reference in row["source_refs"]:
            path, line = reference.rsplit(":", 1)
            if not path.startswith("source/"):
                path = "source/src/main/java/net/coobird/thumbnailator/" + path
            file = a2 / path
            lines = file.read_text().splitlines()
            center = int(line)
            assert 0 < center <= len(lines), reference
            source_evidence[reference] = {"path": path, "line": center, "sha256": sha(file.read_bytes()),
                "excerpt": "\n".join(f"{i+1}: {lines[i]}" for i in range(max(0, center-4), min(len(lines), center+12)))}
    apis = [{"api": name, "a1": a1rows[name]["status"], "a1_category": a1rows[name].get("error_category"),
             "a1_fingerprint": a1rows[name]["experiment_fingerprint"],
             "a2": m["status"], "a2_category": m.get("error_category"),
             "wall_s": m["wall_s"], "doc_chars": m["doc_chars"],
             "code": result["details"][name].get("code", "") if isinstance(result["details"][name], dict) else ""}
            for name, m in metrics.items()]
    paired = Counter((r["a1"] == "pass", r["a2"] == "pass") for r in apis)
    fixtures = []
    for binding, rel in [("grid_png", "Thumbnailator/grid.png"), ("grid_jpeg", "Thumbnailator/grid.jpg"),
                         ("exif_jpeg", "Exif/original.jpg"), ("diagnostic_positive_control", "Exif/orientation_6.jpg")]:
        p = a2 / "source/src/test/resources" / rel
        data = p.read_bytes()
        mime = "image/png" if p.suffix == ".png" else "image/jpeg"
        fixtures.append({"binding": binding, "path": str(p.relative_to(a2)), "sha256": sha(data),
                         "bytes": len(data), "format": mime,
                         "image": "data:" + mime + ";base64," + base64.b64encode(data).decode()})
    timeout = read(HERE / "provider_timeout_frequency.json")
    data = {"generated_at": datetime.now().astimezone().isoformat(), "title": "AIDEAL · Evidence review",
            "scope": "Thumbnailator A2 failures and A1/A2 paired recorded outcomes; Gemini timeout history covers six priority baseline cells",
            "provenance": {"a2_result": str(result_path), "a2_result_sha256": sha(raw),
                           "a2_fingerprint": result["run"]["experiment_fingerprint"],
                           "a2_document_sha256": sha(docs_path.read_bytes()), "a1": a1proof},
            "counts": {"manifest": len(metrics), "a2_pass": sum(m["status"] == "pass" for m in metrics.values()),
                       "a2_compile": sum(m.get("error_category") == "compile" for m in metrics.values()),
                       "a2_runtime": sum(m.get("error_category") == "runtime" for m in metrics.values()),
                       "groups": dict(Counter(r["group"] for r in findings)),
                       "paired": {"both_pass": paired[(True, True)], "a1_only": paired[(True, False)],
                                  "a2_only": paired[(False, True)], "neither_pass": paired[(False, False)]}},
            "assertion_false_passes": [r["api"] for r in apis if r["a2"] == "pass" and re.search(r"\bassert\s+false\b", r["code"])],
            "assertion_pass_count": sum(r["a2"] == "pass" and bool(re.search(r"\bassert\b", r["code"])) for r in apis),
            "findings": findings, "apis": apis, "source_evidence": source_evidence, "fixtures": fixtures,
            "timeout": timeout, "diagnostics": read(HERE / "isolated_contract_diagnostics.json"),
            "assertion_replays": read(HERE / "assertion_replays.json")}
    assert data["counts"]["a2_pass"] + len(findings) == len(metrics)
    out.mkdir(parents=True, exist_ok=True)
    (out / "review_data.json").write_text(json.dumps(data, indent=2) + "\n")
    html = (HERE / "dashboard.html").read_text().replace("/*__STYLE__*/", (HERE / "dashboard.css").read_text())
    html = html.replace("/*__DATA__*/", json.dumps(data).replace("<", "\\u003c"))
    html = html.replace("/*__SCRIPT__*/", (HERE / "dashboard.js").read_text())
    (out / "AIDEAL_RESULTS_REVIEW.html").write_text(html)
    write_memo(data, out)
    print(json.dumps({"out": str(out), "counts": data["counts"], "assertion_false_passes": data["assertion_false_passes"]}))


def write_memo(data, out):
    counts = data["counts"]
    lines = ["# Thumbnailator: generated README failure review", "", f"Snapshot: {data['generated_at']}", "",
        "Open `AIDEAL_RESULTS_REVIEW.html` for charts, tables, an API inspector, fixtures, and a review queue. All assets and evidence are embedded; no server or internet connection is required.", "",
        "## Readiness assessment", "",
        "The frozen A2 result records 127 passes and 22 failures across 149 names. It is not a correctness-certified readiness score. The Java command does not enable assertions; all 127 passing snippets contain assertions. Three include unconditional `assert false` (IfdStructure, getBoolean, value). Isolated replays accept these snippets without -ea and reject all three with -ea. Native results remain unchanged.", "",
        "Seven reviewed failures directly match incorrect guidance in the generated README. Seven fail on invented helper calls or wrong companion types in the audience test. Three concern receiver setup; three concern package-private APIs included in the frozen surface; two concern input/test assumptions. These are observed mechanisms, not controlled causal estimates of documentation impact or proof of 22 library defects.", "",
        "## Attempted does not mean the target API ran", "",
        "| A2 stage | Count | Interpretation |", "|---|---:|---|",
        "| API evaluation recorded | 149 | One final per-API outcome, including possible setup failures |",
        "| Test code generated | 149 | Final A2 has no provider errors and no reused rows |",
        "| Compiled and test process started | 135 | 14 tests stop at compilation |",
        "| Runtime failures | 8 | Includes setup failures and post-target failures |",
        "| Native recorded passes | 127 | Harness accepted exit status/markers with assertions disabled |",
        "| Target API reached / correctness verified | Unknown overall | Requires target-call evidence and effective checks |", "",
        "A timeout can end an evaluation before usable code exists. A compile failure means the API did not run. A runtime failure may occur before reaching the target. Calls inside disabled assertions are skipped. An API count counts distinct names; checkpoint-event counts also include repeated attempts and discarded fingerprint groups.", "",
        "## Paired recorded outcomes", "",
        "A1 is a changing checkpoint snapshot with explicit legacy compatibility; A2 is the completed native result. The original 127-versus-127 tie can change as A1 resolves provider outcomes. This snapshot uses the counts below rather than copying an earlier table.", "",
        *[f"- {key}: {value}" for key, value in counts["paired"].items()], "",
        "## Every A2 failure", "",
        "| API | Native category | Primary reviewed mechanism | A1 snapshot |", "|---|---|---|---|",
        *[f"| `{r['api']}` | {r['native_category']} | {r['group']} | {r['a1_status']} ({r['a1_category'] or 'no error'}) |" for r in data["findings"]], ""]
    for r in data["findings"]:
        lines.extend([f"### {r['api']}", "", r["finding"], "", f"Input used: {r['input_data']}", "",
                      f"Proposed improvement: {r['proposal']}", "",
                      f"Source evidence: {', '.join('`'+s+'`' for s in r['source_refs'])}. Delivered entry SHA-256: `{r['document_sha256']}`.", ""])
    lines.extend(["## Gemini timeout frequency", "", f"Separate snapshot: {data['timeout']['observed_at']}", "",
                  "| Cell | Timeout events / recorded evaluations | Percent |", "|---|---:|---:|"])
    for r in data["timeout"]["cells"]:
        lines.append(f"| {r['cell']} | {r['timeout_events']}/{r['checkpoint_events']} | {r['timeout_pct']}% |")
    lines.extend(["", "Counts include watchdog retries and historical fingerprint groups. They are not SDK request counts, independent function samples, or hourly rates. Most recorded provider failures take about 600 seconds. A1/A2 timing and documentation differ, so a lower A2 timeout rate does not establish a causal explanation. A provider outage is not a library defect.", "",
                  "## Safe fixes and remaining review", "",
                  "Implemented outside active measurement: compatibility-aware HTML counts, explicit stage labels, assertion/fixture diagnostic probes, and reporting-template validation requirements. The visual report uses 22 source- and document-bound reviews and supports local review decisions with JSON export.", "",
                  "Not changed in active runs: assertions, frozen API surface, fixture bindings, generated README, model, prompts, or budgets. Correcting those measurement settings in one condition would break comparability. A proposed matched validation revision is recorded separately; it is not an instruction to restart current workers.", "",
                  "The library developer queue should distinguish documentation correction, API usability improvements, and library behavior changes. Harness, manifest, and provider fixes belong to AIDEAL maintainers. Any source-informed diagnostic result stays separate from headline A1/A2/B1/B2 scores.", "",
                  "## Verification and limits", "",
                  "All 22 delivered README entry hashes match their native metric hashes. Source references exist and are embedded with file hashes. Contract probes confirm null ORIGINAL_FORMAT, missing EXIF in original.jpg, positive EXIF in orientation_6.jpg, maker readiness, wrong exception expectations, interface-method mismatch, and truncated-input behavior. Three native passing snippets were replayed only in temporary isolated classes with assertions off/on.", "",
                  "The DOM behavior test checks filters, all 149 API rows, paired totals, evidence inspector, local review decisions, and JSON/CSV exports. A browser was unavailable in this session, so visual rendering has not been inspected. The HTML is a timestamped snapshot and does not auto-refresh.", ""])
    (out / "REPORT.md").write_text("\n".join(lines))
    queue = [{"id": "thumbnailator-A2-"+r["api"], "status": "proposed", "api": r["api"],
              "mechanism": r["group"], "suggestion": r["proposal"], "evidence_result_sha256": data["provenance"]["a2_result_sha256"],
              "source_references": r["source_refs"], "acceptance": "Review hypothesis; validate isolated complete example with active assertions and target-call evidence before any versioned matched rerun"}
             for r in data["findings"]]
    (out / "improvement_queue.json").write_text(json.dumps(queue, indent=2)+"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a1-project", type=Path, required=True)
    parser.add_argument("--a2-project", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    build(args.a1_project.resolve(), args.a2_project.resolve(), args.out.resolve())
