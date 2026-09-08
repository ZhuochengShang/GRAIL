"""Separate native and assertion-enabled replay reporting, with explicit evidence gaps."""
from collections import Counter
from datetime import datetime
import html
import json


def atomic(path, text):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text)
    temp.replace(path)


def publish(out, cells):
    now = datetime.now().astimezone().isoformat()
    summaries, rows = [], []
    for cell in ("A1", "A2", "B1", "B2"):
        current = cells.get(cell)
        if current is None:
            summaries.append({"cell": cell, "state": "awaiting native evidence"})
            continue
        records = current["records"]
        categories = Counter(r.get("replay", {}).get("variants", {}).get("assertions_on", {}).get("outcome", "not_replayed") for r in records)
        control = Counter(r.get("replay", {}).get("variants", {}).get("assertions_off", {}).get("outcome", "not_replayed") for r in records)
        native_pass = sum(r["native"]["status"] == "pass" for r in records)
        replayed = sum("replay" in r for r in records)
        changed = [r for r in records if r.get("replay", {}).get("variants", {}).get("assertions_off", {}).get("outcome") == "pass"
                   and r["replay"]["variants"]["assertions_on"]["outcome"] != "pass"]
        summaries.append({"cell": cell, "state": "native complete" if current["complete"] else "native partial",
                          "native_apis": len(records), "native_pass": native_pass, "replayed": replayed,
                          "assertions_on": dict(categories), "assertions_off": dict(control), "off_pass_on_fail": len(changed),
                          "unbound_retained_replays": sum(r.get("binding") == "retained_unbound_legacy" and "replay" in r for r in records),
                          "native_source_sha256": current["source_sha256"]})
        for r in records:
            variants = r.get("replay", {}).get("variants", {})
            rows.append({"cell": cell, "api": r["api"], "native": r["native"]["status"],
                         "native_category": r["native"].get("error_category"), "binding": r.get("binding", r.get("reason", "pending")),
                         "off": variants.get("assertions_off", {}).get("outcome", "not_replayed"),
                         "on": variants.get("assertions_on", {}).get("outcome", "not_replayed"),
                         "evidence": r.get("evidence_file"),
                         "error": variants.get("assertions_on", {}).get("stderr", r.get("replay", {}).get("compile", {}).get("stderr", ""))})
    data = {"updated_at": now, "scope": "isolated execution replay; zero LLM calls; zero code fixes",
            "limitations": ["Assertion-enabled acceptance is not an independently validated correctness oracle.",
                "This replay cannot certify the entire documentation-repair pipeline; it does not rerun repair decisions.",
                "Native results remain unchanged. Isolation and fresh per-test outputs may change outcomes; the assertions-off control exposes this.",
                "Legacy retained snippets without full native code or a matching failure prefix are unbound diagnostic evidence.",
                "B cells are processed automatically when final native results appear; absence is pending, not zero success."],
            "cells": summaries, "apis": rows}
    atomic(out / "summary.json", json.dumps(data, indent=2) + "\n")
    lines = ["# Thumbnailator native outcomes and isolated assertion replay", "", "Updated: " + now, "",
             "No native score is replaced. Both replay variants use identical code, copied fixture bytes, a fresh output root and Java 8 isolation; only `-da` versus `-ea` differs.", "",
             "| Cell | Native state | Native pass / API outcomes | Replayed | Off pass | On pass | Off pass → on fail | Unbound retained replays |",
             "|---|---|---:|---:|---:|---:|---:|---:|"]
    for s in summaries:
        if "native_apis" not in s:
            lines.append(f"| {s['cell']} | {s['state']} | — | — | — | — | — | — |")
        else:
            lines.append(f"| {s['cell']} | {s['state']} | {s['native_pass']}/{s['native_apis']} | {s['replayed']} | {s['assertions_off'].get('pass', 0)} | {s['assertions_on'].get('pass', 0)} | {s['off_pass_on_fail']} | {s['unbound_retained_replays']} |")
    lines += ["", "## Interpretation", "", *["- " + s for s in data["limitations"]], "",
              "## API outcomes", "", "| Cell | API | Native | Off replay | On replay | Evidence binding |", "|---|---|---|---|---|---|"]
    lines += [f"| {r['cell']} | `{r['api']}` | {r['native']} | {r['off']} | {r['on']} | {r['binding']} |" for r in rows]
    atomic(out / "REPORT.md", "\n".join(lines) + "\n")
    table = "".join("<tr>" + "".join("<td>" + html.escape(str(r[k])) + "</td>" for k in ("cell", "api", "native", "off", "on", "binding")) + "</tr>" for r in rows)
    cards = "".join(f"<article><h2>{s['cell']}</h2><p>{s['state']}</p>" +
                    (f"<b>{s['native_pass']}/{s['native_apis']}</b> native passes<br><b>{s['assertions_off'].get('pass', 0)}/{s['replayed']}</b> off-control passes<br><b>{s['assertions_on'].get('pass', 0)}/{s['replayed']}</b> on-replay passes<br><span>{s['off_pass_on_fail']} off-pass → on-fail</span>" if "native_apis" in s else "Pending") + "</article>" for s in summaries)
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AIDEAL assertion replay</title>
<style>body{font:16px system-ui;margin:30px auto;padding:0 20px;max-width:1250px;color:#183044;background:#f3f6fa}h1{font-size:32px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px}article{background:white;border-radius:12px;padding:20px;border-top:5px solid #137e8d}b{font-size:23px}span{color:#a32d34}aside{padding:18px;background:#fff0d7;border-left:5px solid #b4780a;margin:20px 0}table{border-collapse:collapse;width:100%;background:white}td,th{text-align:left;padding:10px;border-bottom:1px solid #d5dfe8}input{padding:12px;width:70%;margin:16px 0}.scroll{overflow:auto}tr:has(td:nth-child(5):empty){opacity:.5}a{color:#075c80}</style>
<h1>AIDEAL · Native outcomes and assertion replay</h1><p>__DATE__ · Offline snapshot · No Gemini calls</p><div class="cards">__CARDS__</div>
<aside><strong>Validation boundary:</strong> assertions-on replay acceptance does not independently certify API correctness or the documentation-repair pipeline. Native scores remain unchanged. Unbound legacy snippets are diagnostic evidence. Pending cells are not completed results.</aside>
<p>Native run → snapshot retained evidence → copy fixtures and isolate writes → assertions-off control / assertions-on replay → separate evidence review</p>
<p><a href="REPORT.md">Detailed memo</a> · <a href="summary.json">JSON summary</a> · <a href="preflight.json">Assertion and isolation preflight</a></p>
<label for="search">Filter cell, API, outcome or evidence binding</label><br><input id="search" type="search" placeholder="e.g. assertion_failure, A2, Region"><div class="scroll"><table><thead><tr><th>Cell</th><th>API</th><th>Native</th><th>Assertions off</th><th>Assertions on</th><th>Evidence binding</th></tr></thead><tbody>__TABLE__</tbody></table></div>
<script>document.querySelector('#search').addEventListener('input',e=>{const q=e.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q));});</script></html>'''
    atomic(out / "REPLAY.html", page.replace("__DATE__", html.escape(now)).replace("__CARDS__", cards).replace("__TABLE__", table))
