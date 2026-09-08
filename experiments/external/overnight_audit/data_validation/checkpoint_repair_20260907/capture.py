"""Offline fingerprint capture. Never executes snippets or calls a provider."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from aideal.config import load_config
from aideal import doc_checks, llm


def digest(value):
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


def capture(config, environment, doc, timeout):
    os.environ["AIDEAL_ENV_FINGERPRINT"] = hashlib.sha256(
        Path(environment).read_bytes()).hexdigest()
    cfg = load_config(config)
    captured = {}

    def forbidden(*args, **kwargs):
        raise AssertionError("Offline capture must never invoke a provider")

    def inspect(cfg, inventory, sample, seed, doc_source, **kw):
        ex = cfg.comprehension["execute"]
        data, _, _ = doc_checks._execute_sample_data(cfg, ex)
        document = kw["shared_doc"]
        if document is None:
            document = "\n\0\n".join(f"{e.name}\n{e.body}" for e in inventory)
        args = dict(ex=ex, doc_source=doc_source, doc_scope=kw["doc_scope"],
                    max_fix_rounds=kw["max_fix_rounds"],
                    manifest_sha256=hashlib.sha256(
                        "\n".join(e.name for e in inventory).encode()).hexdigest(),
                    document_sha256=hashlib.sha256(document.encode()).hexdigest(),
                    scaffold_file=(cfg.root / ex["scaffold"]).resolve(),
                    class_context=kw["class_context"], timeout=timeout)
        for label, bindings in [("with_outputs", data), ("inputs_only", {
                k: v for k, v in data.items() if k != "output_dir"})]:
            parts = doc_checks._comprehension_fingerprint_components(
                cfg, sample_data=bindings, **args)
            captured[label] = {"fingerprint": digest(parts), "components": parts}
        ckpt = (cfg.root / ex.get("work_dir", ".aideal_exec")).resolve() / "comprehension_progress.jsonl"
        raw = ckpt.read_bytes()
        rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
        groups = list(dict.fromkeys(row["experiment_fingerprint"] for row in rows))
        candidates = {v["fingerprint"]: v for v in captured.values()}
        matching = [fp for fp in groups if fp in candidates]
        full = [fp for fp in matching if len({row["name"] for row in rows
                if row["experiment_fingerprint"] == fp}) == len(inventory)]
        selected = (full or matching)
        captured.update(checkpoint=str(ckpt), checkpoint_sha256=hashlib.sha256(raw).hexdigest(),
                        checkpoint_bytes=len(raw), groups=groups,
                        selected=candidates[selected[-1]] if selected else None,
                        selection_policy="latest fully attempted reproducible group, else latest reproducible group; never select by score or combine legacy groups",
                        config=str(Path(config).resolve()), environment=str(Path(environment).resolve()))
        return {}

    old_execute, old_invoke = doc_checks._comprehension_execute, llm.invoke_text
    try:
        doc_checks._comprehension_execute, llm.invoke_text = inspect, forbidden
        doc_checks.comprehension_check(cfg, execute=True, doc_source=doc,
                                      doc_scope="relevant", manifest="docs/eval/api_manifest.json",
                                      max_fix_rounds=0, timeout_s=timeout)
    finally:
        doc_checks._comprehension_execute, llm.invoke_text = old_execute, old_invoke
    return captured


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("config")
    p.add_argument("environment")
    p.add_argument("output")
    p.add_argument("--doc", choices=["original", "aideal"], required=True)
    p.add_argument("--timeout", type=int, required=True)
    a = p.parse_args()
    result = capture(a.config, a.environment, a.doc, a.timeout)
    with Path(a.output).open("x") as f:
        json.dump(result, f, indent=2)
    print(json.dumps({"output": a.output, "matched": bool(result["selected"]),
                      "selected": (result["selected"] or {}).get("fingerprint")}))
