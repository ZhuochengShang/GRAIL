"""Read native evidence without importing the experiment runner or provider."""
import hashlib
import json
from pathlib import Path
import re
import textwrap


def digest(value):
    if not isinstance(value, bytes):
        value = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(value).hexdigest()


def read(path):
    return json.loads(path.read_text())


def collect(project, cell):
    """Final result wins; incomplete A1 uses its explicitly approved legacy group."""
    final = project / f"docs/eval/{cell}/comprehension.json"
    if final.exists():
        raw = final.read_bytes()
        data = json.loads(raw)
        rows = {n: dict(m, name=n, execution_evidence=data["details"].get(n),
                       experiment_fingerprint=m.get("evidence_fingerprint") or data["run"]["experiment_fingerprint"])
                for n, m in data["metrics"].items()}
        components = data["run"]["fingerprint_components"]
        source = final
        complete = True
    else:
        checkpoint = project / f".aideal_exec/{cell}/comprehension_progress.jsonl"
        compatibility = checkpoint.parent / "checkpoint_compatibility.json"
        if not checkpoint.exists() or not compatibility.exists():
            return None
        proof = read(compatibility)
        components = proof["current_components"]
        raw = checkpoint.read_bytes()
        # A writer may be appending its final line. Ignore only that incomplete line.
        lines = raw.splitlines(keepends=True)
        journal = [json.loads(line) for line in lines if line.endswith(b"\n")]
        rows = {r["name"]: r for r in journal if r["experiment_fingerprint"] == proof["legacy_fingerprint"]}
        rows.update({r["name"]: r for r in journal if r["experiment_fingerprint"] == digest(components)})
        source, complete = checkpoint, False
    # Older retries saved complete detail for a few rows. Bind only matching fingerprints.
    for archived in sorted((project / f"docs/eval/{cell}/retry_attempts").glob("*.json")):
        old = read(archived)
        fp = old.get("run", {}).get("experiment_fingerprint")
        for name, detail in old.get("details", {}).items():
            row = rows.get(name)
            if row and row["experiment_fingerprint"] == fp and not isinstance(row.get("execution_evidence"), dict):
                row["execution_evidence"] = detail
    return {"cell": cell, "project": str(project), "complete": complete, "rows": rows,
            "components": components, "source_path": str(source), "source_sha256": digest(raw)}


def retained_source(project, cell, row):
    detail = row.get("execution_evidence")
    detail = detail if isinstance(detail, dict) else {}
    path = Path(detail.get("scala_file") or project / f".aideal_exec/{cell}/run_{row['name']}/ApiTest.java")
    if row.get("error_category") == "llm-error":
        return {"available": False, "reason": "provider failure; stale retained files are not this attempt"}
    if not path.is_file():
        return {"available": False, "reason": "retained full harness unavailable"}
    raw = path.read_bytes()
    source = raw.decode()
    start, end = "// TODO API_TEST_START", "// TODO API_TEST_END"
    prefix, body = source.split(start, 1)
    snippet, suffix = body.split(end, 1)
    norm = lambda s: re.sub(r"(?m)^[ \t]+$", "", textwrap.dedent(s).strip())
    native = detail.get("code", "")
    binding = "retained_unbound_legacy"
    if row["status"] == "pass" and native:
        # Passing code in native JSON is complete, including case-colliding file recovery.
        source = prefix + start + "\n" + textwrap.indent(native, "            ") + "\n            " + end + suffix
        binding = "full_native_code"
    elif native and norm(snippet).startswith(norm(native)):
        binding = "retained_matches_native_failure_prefix"
    elif native:
        return {"available": False, "reason": "retained source does not match recorded failure prefix"}
    return {"available": True, "source": source, "binding": binding,
            "retained_path": str(path), "retained_sha256": digest(raw),
            "native_code_sha256": digest(native.encode()) if native else None,
            "recovered_from_native_code": bool(native and norm(snippet) != norm(native) and row["status"] == "pass")}


def relocate(source, project, fixtures):
    """Rebase path literals only; preserve generated test logic and fixture bytes."""
    replacements = []
    for name, relative in fixtures.items():
        original = str((project / relative).resolve())
        replacement = 'System.getProperty("aideal.replay.root") + ' + json.dumps("/fixtures/" + name + Path(relative).suffix)
        quoted = json.dumps(original)
        if quoted in source:
            source = source.replace(quoted, replacement)
            replacements.append({"from": original, "to": "fixtures/" + name + Path(relative).suffix})
    # Output bindings, including any other project-local absolute path literals.
    def replace(match):
        value = json.loads(match.group())
        if value.startswith(str(project) + "/"):
            relative = "project/" + value[len(str(project)) + 1:]
            replacements.append({"from": value, "to": relative})
            return 'System.getProperty("aideal.replay.root") + ' + json.dumps("/" + relative)
        return match.group()
    source = re.sub(r'"(?:[^"\\]|\\.)*"', replace, source)
    return source, replacements
