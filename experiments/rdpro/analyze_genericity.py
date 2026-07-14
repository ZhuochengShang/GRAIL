#!/usr/bin/env python3
"""Genericity vs outcome: does the LLM fail on the CUSTOMIZED parts of the codebase?

Classifies every tested API as GENERIC / MIXED / DOMAIN-SPECIFIC using two
automatic, checkable signals (no hand labels):
  1. domain-type fraction — share of non-primitive signature types that are
     DEFINED IN THIS CODEBASE (scanned from beast sources, Scala AND Java);
  2. name domainness — camelCase tokens of the API name that never occur in
     general-purpose programming vocabulary (small fixed list) count as domain.

Then cross-tabs the buckets against real run outcomes (pass/fail + failure
category) for the two comparable full-surface runs, with examples.

Usage: python analyze_genericity.py [--json out.json] [--md docs/genericity_analysis.md]
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "grail-agent" / "src"))

from aideal.config import load_config                      # noqa: E402
from aideal.readme_agent import public_api_details          # noqa: E402

GENERIC_TOKENS = {
    # verbs / nouns any library uses — appearing in the name says nothing custom
    "get", "set", "is", "to", "add", "create", "read", "write", "load", "save",
    "open", "close", "run", "call", "make", "build", "new", "init", "initialize",
    "setup", "start", "end", "stop", "find", "check", "list", "put", "copy",
    "merge", "split", "join", "map", "filter", "reduce", "count", "sum", "size",
    "length", "num", "value", "values", "name", "names", "type", "types", "id",
    "ids", "file", "files", "path", "dir", "data", "info", "util", "utils",
    "helper", "string", "text", "index", "key", "keys", "item", "items", "empty",
    "non", "all", "any", "first", "last", "next", "prev", "min", "max", "mean",
    "avg", "average", "local", "remote", "in", "out", "input", "output", "for",
    "with", "by", "at", "of", "as", "from", "into", "compress", "decompress",
    "encode", "decode", "parse", "format", "print", "flatten", "transform",
    "select", "extract", "generate", "compute", "process", "partition",
    "partitions", "server", "options", "option", "boolean", "long", "int",
    "double", "float", "resource", "summary", "summarize", "uniform", "normal",
    "gaussian", "distribution", "using", "available", "defined", "skip",
    "retain", "seek", "bit", "part", "config", "image",
}
PRIMITIVES = {"String", "Int", "Long", "Float", "Double", "Boolean", "Unit", "Byte",
              "Short", "Char", "Any", "AnyRef", "AnyVal", "Array", "Option", "Seq",
              "List", "Map", "Set", "Iterator", "Iterable", "Class", "T", "K", "V",
              "Tuple2", "Tuple3", "ClassTag", "File", "Path", "InputStream",
              "OutputStream", "FileSystem", "Configuration", "RDD", "JavaRDD",
              "SparkContext", "SparkSession", "DataFrame", "Dataset", "JavaPairRDD"}


def camel_tokens(name: str) -> list[str]:
    return [t.lower() for t in re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])", name) if t]


def codebase_types(cfg) -> set[str]:
    """Every class/trait/object/interface NAME defined in the target sources."""
    out: set[str] = set()
    pat = re.compile(r"\b(?:case\s+class|abstract\s+class|class|trait|object|interface|enum)\s+([A-Z]\w+)")
    globs = list(cfg.source_globs) + [g.replace(".scala", ".java") for g in cfg.source_globs]
    for g in globs:
        for p in glob.glob(str(cfg.root / g), recursive=True):
            try:
                out |= set(pat.findall(Path(p).read_text(encoding="utf-8", errors="ignore")))
            except OSError:
                continue
    return out


def classify(cfg, names: list[str]) -> dict[str, dict]:
    dom_types = codebase_types(cfg)
    det: dict[str, list] = defaultdict(list)
    for d in public_api_details(cfg):
        if d["visibility"] == "public":
            det[d["name"]].append(d)
    out = {}
    for n in names:
        recs = det.get(n, [])
        sig_types = set()
        for r in recs:
            sig = " ".join([r.get("returns") or ""] + [p.get("type") or "" for p in r.get("params", [])])
            sig_types |= set(re.findall(r"\b([A-Z]\w{2,})\b", sig))
        sig_types -= PRIMITIVES
        n_dom_types = len(sig_types & dom_types)
        type_frac = n_dom_types / len(sig_types) if sig_types else 0.0
        toks = camel_tokens(n)
        dom_toks = [t for t in toks if t not in GENERIC_TOKENS]
        name_frac = len(dom_toks) / len(toks) if toks else 0.0
        score = 0.6 * type_frac + 0.4 * name_frac
        bucket = ("domain-specific" if score >= 0.5 else
                  "mixed" if score >= 0.15 else "generic")
        out[n] = {"bucket": bucket, "score": round(score, 2),
                  "domain_types": sorted(sig_types & dom_types)[:4],
                  "domain_tokens": dom_toks[:4]}
    return out


def crosstab(run_file: str, cls: dict[str, dict]) -> dict:
    d = json.loads(Path(run_file).read_text())
    m = d.get("metrics", {})
    tab: dict[str, Counter] = defaultdict(Counter)
    cats: dict[str, Counter] = defaultdict(Counter)
    examples: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for n, v in m.items():
        b = cls.get(n, {}).get("bucket", "?")
        ok = v.get("status") == "pass"
        tab[b]["pass" if ok else "fail"] += 1
        if not ok:
            cats[b][v.get("error_category") or "?"] += 1
        examples[b]["pass" if ok else "fail"].append(n)
    return {"tab": {k: dict(v) for k, v in tab.items()},
            "fail_cats": {k: dict(v) for k, v in cats.items()},
            "examples": {k: {kk: vv[:8] for kk, vv in v.items()} for k, v in examples.items()},
            "condition": Path(run_file).name,
            "audience": d.get("run", {}).get("models", {}).get("audience", "?")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="*", default=[
        "results/bench/20260707_125142_g1_codex_flat.gpt-5.3-codex.json",
        "docs/comprehension_run.json"])
    ap.add_argument("--md", default="docs/genericity_analysis.md")
    ap.add_argument("--json", dest="json_out", default="docs/genericity_analysis.json")
    args = ap.parse_args()
    cfg = load_config()
    all_names = sorted({n for f in args.runs
                        for n in json.loads(Path(f).read_text()).get("metrics", {})})
    cls = classify(cfg, all_names)
    results = [crosstab(f, cls) for f in args.runs]

    lines = ["# Generic vs customized APIs — who does the LLM actually understand?", "",
             "Buckets are AUTOMATIC: 60% weight = fraction of signature types defined in this",
             "codebase; 40% = name tokens outside general programming vocabulary. No hand labels.", ""]
    dist = Counter(v["bucket"] for v in cls.values())
    lines += [f"Surface mix: {dict(dist)}", ""]
    for r in results:
        lines += [f"## {r['condition']}  (audience: {r['audience']})", ""]
        lines += ["| bucket | pass | fail | pass rate | dominant failure |", "|---|---|---|---|---|"]
        for b in ("generic", "mixed", "domain-specific"):
            t = r["tab"].get(b, {})
            p, f = t.get("pass", 0), t.get("fail", 0)
            rate = f"{p/(p+f):.0%}" if (p + f) else "—"
            top = max(r["fail_cats"].get(b, {"—": 0}).items(), key=lambda kv: kv[1])[0]
            lines += [f"| {b} | {p} | {f} | {rate} | {top} |"]
        lines += [""]
        for b in ("generic", "domain-specific"):
            ex = r["examples"].get(b, {})
            lines += [f"- {b} PASS examples: {', '.join(ex.get('pass', [])[:6]) or '—'}",
                      f"- {b} FAIL examples: {', '.join(ex.get('fail', [])[:6]) or '—'}", ""]
    Path(args.md).write_text("\n".join(lines), encoding="utf-8")
    Path(args.json_out).write_text(json.dumps(
        {"classification": cls, "results": results}, indent=2), encoding="utf-8")
    print("\n".join(lines[:40]))
    print(f"\nwrote {args.md} and {args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
