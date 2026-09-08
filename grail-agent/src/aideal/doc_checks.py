"""The AIDEAL check pipeline over LLM_readme.md.

1. form_check          - every API entry has the required sections
2. comprehension_check - README UNIT TEST: given ONLY the doc entry, the
                         audience model must write correct code (no other
                         source); the author model grades it against the doc
3. completeness_check  - are all public functions covered by the readme?
4. puzzle_check        - integration: runs the application-provided puzzle
                         command (GRAIL's evaluator) with a fix loop that
                         injects notes_to_self + error log on retries

Failures feed the error log; repeated failures distill into notes_to_self.
Each check returns {"check", "passed", "score", "details"}.

AIDEAL never imports the application (GRAIL) — layering is one-way.
"""

from __future__ import annotations

import random
import re
import shlex
import subprocess
import sys
from pathlib import Path

from .config import AidealConfig
from .error_log import ErrorLog, new_run_id
from .notes_to_self import NotesToSelf
from .readme_agent import parse_readme, public_api_surface, public_api_details


def _sha256_files(paths: list[Path], root: Path | None = None) -> dict:
    """Hash file names and contents deterministically for run provenance."""
    import hashlib

    digest = hashlib.sha256()
    files: list[Path] = []
    for path in paths:
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file())
    unique = sorted(set(p.resolve() for p in files), key=str)
    for path in unique:
        try:
            label = path.relative_to(root.resolve()) if root else path
        except ValueError:
            label = path
        digest.update(str(label).encode("utf-8"))
        digest.update(b"\0")
        try:
            with path.open("rb") as src:
                for chunk in iter(lambda: src.read(1024 * 1024), b""):
                    digest.update(chunk)
        except OSError as exc:
            digest.update(f"<unreadable:{type(exc).__name__}>".encode("utf-8"))
        digest.update(b"\0")
    return {"sha256": digest.hexdigest(), "file_count": len(unique)}


def _comprehension_fingerprint_components(
        cfg: AidealConfig, *, ex: dict, doc_source: str, doc_scope: str,
        max_fix_rounds: int, manifest_sha256: str, document_sha256: str,
        scaffold_file: Path, sample_data: dict, class_context: bool,
        timeout: int) -> dict:
    """Return every material input that makes a checkpoint reusable.

    A checkpoint is experimental evidence, not merely a performance cache. A
    model, YAML, scaffold, source, fixture, interpreter, or engine change must
    create a new fingerprint so an overnight watchdog cannot silently mix
    conditions after a restart.
    """
    import glob
    import os

    source_paths: list[Path] = []
    for pattern in cfg.source_globs:
        source_paths.extend(Path(p) for p in glob.glob(
            str(cfg.root / pattern), recursive=True))
    # output_dir is a writable destination supplied to snippets, not input
    # evidence. Its location remains in execute_config; its changing contents
    # must never invalidate completed API checkpoints.
    from urllib.parse import unquote, urlparse
    fixture_paths = [Path(unquote(urlparse(str(value)).path)
                          if str(value).startswith("file://") else str(value))
                     for key, value in sample_data.items() if key != "output_dir"]
    engine_dir = Path(__file__).resolve().parent
    engine_paths = [engine_dir / name for name in (
        "config.py", "doc_checks.py", "llm.py", "prompts.py", "readme_agent.py",
        "checkpoint_compatibility.py", "provider_deadline.py")]
    audience = cfg.model_for_role("audience")
    fixer = cfg.model_for_role("fixer")
    return {
        "schema": 3,
        "project": cfg.project_name,
        "language": cfg.language,
        "doc_source": doc_source,
        "doc_scope": doc_scope,
        "max_fix_rounds": max_fix_rounds,
        "manifest_sha256": manifest_sha256,
        "document_sha256": document_sha256,
        "models": {
            "audience": f"{audience.provider}:{audience.model}",
            "fixer": f"{fixer.provider}:{fixer.model}",
        },
        "class_context": bool(class_context),
        "timeout_s": timeout,
        "execute_config": ex,
        "scaffold": _sha256_files([scaffold_file], cfg.root),
        "source": _sha256_files(source_paths, cfg.root),
        "fixtures": _sha256_files(fixture_paths, cfg.root),
        "engine": _sha256_files(engine_paths, engine_dir),
        "interpreter": {
            "executable": sys.executable,
            "version": sys.version,
            "environment_sha256": os.environ.get("AIDEAL_ENV_FINGERPRINT", ""),
        },
    }


def _checkpoint_row_reusable(row: dict, experiment_fingerprint: str) -> bool:
    """Only stable terminal rows may suppress work after a restart."""
    return (row.get("experiment_fingerprint") == experiment_fingerprint
            and row.get("error_category") != "llm-error")


# ---------------------------------------------------------------------------
# 1. Form check (no LLM)
# ---------------------------------------------------------------------------

def form_check(cfg: AidealConfig) -> dict:
    inventory = parse_readme(cfg.llm_readme)
    failures: dict[str, list[str]] = {}
    for entry in inventory:
        missing = [
            req for req in cfg.required_sections
            if not any(re.search(rf"^### {re.escape(a)}\s*$", entry.body, re.MULTILINE)
                       for a in req.split("|"))
        ]
        if "TODO" in entry.body:
            missing.append("unfilled TODOs")  # a skeleton is not documentation
        if missing:
            failures[entry.name] = missing
    n = len(inventory)
    return {
        "check": "form",
        "passed": bool(n) and not failures,
        "score": round((n - len(failures)) / n, 3) if n else 0.0,
        "details": {"apis": n, "complete": n - len(failures), "missing_sections": failures},
    }


# ---------------------------------------------------------------------------
# 2. Comprehension check = README unit test
# ---------------------------------------------------------------------------

def _load_manifest(cfg: AidealConfig, manifest: str | None) -> list[str] | None:
    """Frozen API manifest: ONE list of names used by every experiment cell, so
    pass-rate deltas can never come from denominator drift (2x2 requirement).
    Accepts a JSON array or {"apis": [...]}; paths resolve against cfg.root."""
    if not manifest:
        return None
    import json as _json
    from pathlib import Path
    p = Path(manifest) if str(manifest).startswith("/") else (cfg.root / manifest)
    data = _json.loads(p.read_text(encoding="utf-8"))
    names = data["apis"] if isinstance(data, dict) else data
    if not isinstance(names, list) or not all(isinstance(n, str) and n for n in names):
        raise ValueError(f"manifest {p} must contain a non-empty-string API list")
    names = list(dict.fromkeys(names))
    unknown = sorted(set(names) - set(public_api_surface(cfg)))
    # The primary experiment remains strictly source-surface bounded. A
    # secondary artifact-scale analysis may intentionally evaluate every entry
    # emitted into a generated README, including names later rejected by the
    # surface/intent filter. Such a manifest must opt in explicitly so a typo or
    # arbitrary name can never silently enter an ordinary experiment.
    allow_artifact_entries = (
        isinstance(data, dict)
        and data.get("allow_outside_surface") == "generated_document_entries"
    )
    if unknown and not allow_artifact_entries:
        raise ValueError(f"manifest {p} contains APIs outside the configured public surface: "
                         f"{', '.join(unknown[:10])}")
    return names


def _shared_doc_text(cfg: AidealConfig, doc_source: str) -> str:
    """FULL-DOCUMENT audience context (no truncation — the experiment requires
    the audience to receive the ENTIRE selected documentation; the size is
    recorded in the run JSON so exposure is auditable).

      original         -> every configured baseline doc, whole
      aideal           -> the whole generated LLM_readme.md
      original+aideal  -> both (the B1 arm: original docs + entries the
                          doc-repair loop has created so far)
    """
    parts: list[str] = []
    if doc_source in ("original", "original+aideal"):
        parts.append(cfg.original_readme_text(limit=None))
    if doc_source in ("aideal", "original+aideal"):
        if cfg.llm_readme.exists():
            parts.append("===== GENERATED / REPAIRED API ENTRIES =====\n"
                         + cfg.llm_readme.read_text(encoding="utf-8", errors="ignore"))
        elif doc_source == "aideal":
            raise FileNotFoundError(f"{cfg.llm_readme} missing (doc_source=aideal)")
    return "\n\n".join(p for p in parts if p.strip())


def _markdown_chunks(text: str) -> list[str]:
    """Stable file/heading chunks for deterministic, non-LLM retrieval."""
    chunks: list[str] = []
    file_header = ""
    current: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        # Synthetic file boundaries are authoritative and reset malformed or
        # unclosed Markdown state from the previous source file.
        if line.startswith("===== ") and line.endswith(" ====="):
            if current:
                chunks.append("\n".join(([file_header] if file_header else []) + current).strip())
            file_header, current, fence = line, [], None
            continue
        fm = re.match(r"^(`{3,}|~{3,})", stripped)
        if fm:
            token = fm.group(1)
            marker = (token[0], len(token))
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and marker[1] >= fence[1]:
                fence = None
        if fence is None and re.match(r"^#{1,6}\s+", line) and current:
            chunks.append("\n".join(([file_header] if file_header else []) + current).strip())
            current = [line]
        else:
            current.append(line)
    if current:
        chunks.append("\n".join(([file_header] if file_header else []) + current).strip())
    return [c for c in chunks if c]


def _relevant_original_text(cfg: AidealConfig, api_name: str, limit: int) -> str:
    """Retrieve only code-evidenced Markdown sections for one API, without an LLM."""
    from .readme_agent import _doc_code_mentions
    raw = cfg.original_readme_text(limit=None)
    coverage_cfg = ((cfg.raw or {}).get("coverage") or {})
    call_patterns = coverage_cfg.get("documentation_call_patterns")
    matches: list[tuple[int, int, str]] = []
    for pos, chunk in enumerate(_markdown_chunks(raw)):
        if api_name not in _doc_code_mentions(
                chunk, {api_name}, call_patterns=call_patterns):
            continue
        # Prefer explicit calls over inline-code/name-only evidence; retain source order.
        escaped = re.escape(api_name)
        calls = len(re.findall(rf"\.{escaped}\b|\b{escaped}\s*[\(\[]", chunk))
        mentions = len(re.findall(rf"\b{escaped}\b", chunk))
        matches.append((calls * 100 + mentions, pos, chunk))
    matches.sort(key=lambda item: (-item[0], item[1]))
    selected: list[str] = []
    used = 0
    for _, _, chunk in matches:
        separator = 2 if selected else 0
        remaining = limit - used - separator
        if remaining <= 0:
            break
        selected.append(chunk[:remaining])
        used += separator + min(len(chunk), remaining)
    if not selected:
        return (f"No code-context section for `{api_name}` was found in the configured "
                "original documentation.")
    return "\n\n".join(selected)


def _relevant_original_texts(cfg: AidealConfig, names: list[str], limit: int) -> dict[str, str]:
    """Index the original bundle for every manifest API in one corpus pass.

    The old per-API implementation re-read and re-split a 15 MB Javadoc bundle
    more than a thousand times. This preserves the same deterministic ranking
    and character cap while making all-surface overnight runs practical.
    """
    from .readme_agent import _doc_code_mentions
    raw = cfg.original_readme_text(limit=None)
    coverage_cfg = ((cfg.raw or {}).get("coverage") or {})
    call_patterns = coverage_cfg.get("documentation_call_patterns")
    wanted = set(names)
    matches: dict[str, list[tuple[int, int, str]]] = {name: [] for name in names}
    for pos, chunk in enumerate(_markdown_chunks(raw)):
        for name in _doc_code_mentions(chunk, wanted, call_patterns=call_patterns):
            escaped = re.escape(name)
            calls = len(re.findall(rf"\.{escaped}\b|\b{escaped}\s*[\(\[]", chunk))
            mentions = len(re.findall(rf"\b{escaped}\b", chunk))
            matches[name].append((calls * 100 + mentions, pos, chunk))

    result: dict[str, str] = {}
    for name in names:
        ranked = sorted(matches[name], key=lambda item: (-item[0], item[1]))
        selected: list[str] = []
        used = 0
        for _, _, chunk in ranked:
            separator = 2 if selected else 0
            remaining = limit - used - separator
            if remaining <= 0:
                break
            selected.append(chunk[:remaining])
            used += separator + min(len(chunk), remaining)
        result[name] = ("\n\n".join(selected) if selected else
                        f"No code-context section for `{name}` was found in the configured "
                        "original documentation.")
    return result


def _relevant_doc_inventory(cfg: AidealConfig, doc_source: str, names: list[str]):
    """Per-API relevant documentation with one equal character ceiling per source."""
    from .readme_agent import ApiEntry
    limit = int((cfg.comprehension or {}).get("relevant_doc_chars", 12000) or 12000)
    generated = {e.name: e for e in parse_readme(cfg.llm_readme)} if cfg.llm_readme.exists() else {}
    part_limit = limit // 2 if doc_source == "original+aideal" else limit
    original = (_relevant_original_texts(cfg, names, part_limit)
                if doc_source in ("original", "original+aideal") else {})
    inventory = []
    for name in names:
        parts: list[str] = []
        if doc_source in ("original", "original+aideal"):
            parts.append(original[name])
        if doc_source in ("aideal", "original+aideal"):
            entry = generated.get(name)
            if entry:
                parts.append(entry.body[:part_limit])
        body = "\n\n===== RELATED DOCUMENTATION =====\n\n".join(parts)[:limit]
        inventory.append(ApiEntry(name=name, goal="", snippet="", body=body))
    return inventory


def _comprehension_inventory(cfg: AidealConfig, doc_source: str,
                             manifest: list[str] | None = None,
                             full_doc: bool = False,
                             doc_scope: str | None = None):
    """Build (inventory, shared_doc, error_dict). shared_doc is None unless
    full_doc — then every entry's audience context = shared_doc + target line
    (built late in the execute loop; bodies stay empty to avoid duplicating a
    multi-MB document per entry)."""
    from .readme_agent import ApiEntry
    if doc_scope == "relevant":
        names = manifest or (sorted(public_api_surface(cfg)) if doc_source.startswith("original")
                             else [e.name for e in parse_readme(cfg.llm_readme)
                                   if "TODO" not in e.body])
        return _relevant_doc_inventory(cfg, doc_source, names), None, None
    if full_doc:
        # denominator: the frozen manifest if given, else the doc's own names
        if manifest:
            names = manifest
        elif doc_source in ("original", "original+aideal"):
            names = sorted(public_api_surface(cfg))
        else:
            names = [e.name for e in parse_readme(cfg.llm_readme)
                     if "TODO" not in e.body]
        try:
            shared = _shared_doc_text(cfg, doc_source)
        except FileNotFoundError as exc:
            return None, None, {"check": "comprehension", "passed": False, "score": 0.0,
                                "details": {"error": str(exc)}}
        if not shared.strip():
            return None, None, {"check": "comprehension", "passed": False, "score": 0.0,
                                "details": {"error": f"no documentation text for "
                                            f"doc_source={doc_source}"}}
        return [ApiEntry(name=n, goal="", snippet="", body="") for n in names], \
            shared, None
    if doc_source == "original":
        if not cfg.original_readme_files:
            return None, None, {"check": "comprehension", "passed": False, "score": 0.0,
                                "details": {"error": "files.original_readme not configured or missing"}}
        text = cfg.original_readme_text(limit=12000)   # legacy (non-full-doc) mode
        names = manifest or sorted(public_api_surface(cfg))
        return [ApiEntry(name=n, goal="", snippet="",
                         body=f"(Original project README — the only documentation available)\n"
                              f"{text}\n\nTarget function: `{n}`")
                for n in names], None, None
    if doc_source == "agents":
        # BASELINE ARM: the repo's holistic agent guide (AGENTS.md) as the ONLY
        # context — the industry-standard single-file "how to work in this repo"
        # doc. Path from files.agents_doc (default AGENTS.md at project root).
        from pathlib import Path
        rel = (cfg.raw.get("files", {}) or {}).get("agents_doc", "AGENTS.md")
        p = (cfg.root / rel)
        if not p.exists():
            return None, None, {"check": "comprehension", "passed": False, "score": 0.0,
                                "details": {"error": f"agents doc not found at {rel} "
                                            "(set files.agents_doc, or drop an AGENTS.md at project root)"}}
        text = p.read_text(encoding="utf-8", errors="ignore")[:12000]
        names = manifest or sorted(public_api_surface(cfg))
        return [ApiEntry(name=n, goal="", snippet="",
                         body=f"(Project AGENTS.md — the only agent guidance available)\n"
                              f"{text}\n\nTarget function: `{n}`")
                for n in names], None, None
    inventory = [e for e in parse_readme(cfg.llm_readme) if "TODO" not in e.body]
    if manifest:
        by = {e.name: e for e in inventory}
        inventory = [by[n] for n in manifest if n in by]
    if not inventory:
        return None, None, {"check": "comprehension", "doc_source": doc_source, "passed": False,
                            "score": 0.0,
                            "details": {"error": "LLM_readme has no filled entries (skeleton TODOs "
                                                 "don't count) - run `readme --generate` or fill them"}}
    return inventory, None, None


def _build_catalogue_context(cfg: AidealConfig):
    """(model, name_to_gkey, by_name) for INDEX-FIRST comprehension, or None. Builds
    the SAME catalogue model `write_catalogue` renders, so the receiver line + the
    verified-sibling call pattern handed to the audience match the per-class files."""
    from .readme_agent import (_catalogue_model, _grounding_tiers, _exec_status_map,
                               parse_readme, public_api_details)
    entries = [e for e in parse_readme(cfg.llm_readme) if "TODO" not in e.body]
    if not entries:
        return None
    tiers, class_of, _ = _grounding_tiers(cfg)
    exec_status = _exec_status_map(cfg)
    owner = _owner_map(cfg)
    file_of = {d["name"]: d["file"] for d in public_api_details(cfg)}
    model = _catalogue_model(entries, tiers, exec_status, class_of, owner, file_of=file_of)
    name_to_gkey = {x["name"]: g for g, m in model.items() for x in m["members"]}
    return model, name_to_gkey, {e.name: e for e in entries}


def _resolve_class_context(cfg: AidealConfig, override: bool | None) -> bool:
    """CLI override wins; else the `comprehension.class_context` config flag (default off)."""
    if override is not None:
        return override
    return bool((cfg.comprehension or {}).get("class_context", False))


def comprehension_check(cfg: AidealConfig, sample: int | None = None, seed: int = 42,
                        doc_source: str = "aideal", execute: bool = False,
                        show_code: bool = False, api: str | None = None,
                        class_context: bool | None = None,
                        rerun_failed: bool = False,
                        max_fix_rounds: int | None = None,
                        resume: bool = False,
                        timeout_s: int | None = None,
                        full_doc: bool | None = None,
                        doc_scope: str | None = None,
                        manifest: str | None = None) -> dict:
    """Given only the documentation, the audience model writes code; the author
    model grades strictly against the doc. Failures go to the error log.

    rerun_failed: restrict the inventory to functions whose MOST-RECENT outcome in
             error_log is `fail` (via _exec_status_map — `fixed`/`pass` are skipped).
             Lets you re-test just the last run's failures instead of the whole
             surface. Applies to both --execute and the LLM-graded path.

    doc_source:
      "aideal"   - per-API entries from LLM_readme.md (the AIDEAL format)
      "original" - the project's ORIGINAL readme as the only context, with
                   target functions sampled from the code surface. This is
                   the baseline condition for original-vs-AIDEAL comparisons.
    execute: if True, the audience snippet is compiled/run via the configured
             `comprehension.execute` command instead of being LLM-graded —
             real execution ground truth. Defaults to ALL documented APIs.
    class_context: INDEX-FIRST read path. When on (CLI --class-context or config
             comprehension.class_context), each tested API's body is prefixed with
             its catalogue class header (how to obtain the receiver + one verified
             sibling's real call pattern) instead of the bare per-API body — the A/B
             lever against the ~53% receiver/entry-point failure class. None -> config.
    """
    from .llm import invoke_text
    from .profile import require_profile
    from .prompts import load as load_prompt
    from .readme_agent import _class_context_body

    require_profile(cfg)  # user must have entered project/target-user/domain fields
    if full_doc is None:
        full_doc = bool((cfg.comprehension or {}).get("full_doc", False))
    doc_scope = doc_scope or ("full" if full_doc else "entry")
    if doc_scope not in {"full", "relevant", "entry"}:
        raise ValueError(f"unknown doc_scope={doc_scope!r}")
    if doc_scope == "full":
        full_doc = True
    elif doc_scope == "relevant":
        full_doc = False
    manifest_names = _load_manifest(cfg, manifest)
    inventory, shared_doc, err = _comprehension_inventory(
        cfg, doc_source, manifest=manifest_names, full_doc=full_doc,
        doc_scope=doc_scope)
    if err:
        return err
    if full_doc and not execute:
        return {"check": "comprehension", "passed": False, "score": 0.0,
                "details": {"error": "--full-doc requires --execute (the LLM-graded "
                            "path would duplicate the whole document per entry)"}}
    if doc_scope == "relevant" and not execute:
        return {"check": "comprehension", "passed": False, "score": 0.0,
                "details": {"error": "--doc-scope relevant requires --execute"}}
    if api:  # test ONE specific documented API (covers both LLM-graded and --execute)
        names = [e.name for e in inventory]
        inventory = [e for e in inventory if e.name == api]
        if not inventory:
            return {"check": "comprehension", "passed": False, "error":
                    f"API '{api}' not found in {doc_source} doc. Available: "
                    f"{', '.join(sorted(names)[:40])}"}
    if rerun_failed:  # re-test ONLY functions whose most-recent error_log outcome is fail
        from .readme_agent import _exec_status_map
        failed = {fn for fn, s in _exec_status_map(cfg).items() if s == "fail"}
        inventory = [e for e in inventory if e.name in failed]
        if not inventory:
            return {"check": "comprehension", "doc_source": doc_source, "passed": True,
                    "score": 1.0, "details": {"note": "no function has a most-recent FAIL in "
                    "error_log — nothing to rerun (fixed/pass are skipped)"}}
    cc = _resolve_class_context(cfg, class_context)
    if execute:
        out = _comprehension_execute(cfg, inventory, sample, seed, doc_source,
                                     show_code=show_code, class_context=cc,
                                     max_fix_rounds=max_fix_rounds,
                                     resume=resume, timeout_s=timeout_s,
                                     shared_doc=shared_doc, doc_scope=doc_scope)
        if isinstance(out, dict) and isinstance(out.get("run"), dict):
            out["run"]["full_doc"] = bool(shared_doc is not None)
            out["run"]["doc_scope"] = doc_scope
            out["run"]["doc_chars"] = (len(shared_doc) if shared_doc else
                                         sum(len(e.body) for e in inventory))
            out["run"]["manifest"] = {"path": manifest,
                                      "apis": len(manifest_names)} if manifest_names else None
        return out
    k = len(inventory) if sample == 0 else (sample or cfg.comprehension_apis_sampled)
    if k < len(inventory):
        inventory = random.Random(seed).sample(inventory, k)

    # INDEX-FIRST: class header (receiver + verified sibling) prefixed to each body.
    # doc_source "original" has no per-class model — the flag is a no-op there.
    ctx = _build_catalogue_context(cfg) if (cc and doc_source == "aideal") else None
    body_for = (lambda e: _class_context_body(e, *ctx)) if ctx else (lambda e: e.body)

    log = ErrorLog(cfg.error_log)
    run_id = new_run_id()
    per_api: dict[str, object] = {}
    passed_n = 0
    ex = cfg.comprehension.get("execute", {}) if cfg.comprehension else {}
    _sample_data, available_inputs, _sd_warnings = _execute_sample_data(cfg, ex)
    for entry in inventory:
        code = invoke_text(
            cfg.model_for_role("audience"),
            *load_prompt(cfg, "aideal/comprehension_write",
                         api_body=body_for(entry), api_name=entry.name,
                         available_inputs=available_inputs),
        )
        verdict = invoke_text(
            cfg.model_for_role("author"),
            *load_prompt(cfg, "aideal/comprehension_grade",
                         api_body=entry.body, code=code),
        )
        if verdict.strip().upper().startswith("PASS"):
            passed_n += 1
            per_api[entry.name] = {"status": "pass", "code": code.strip()} if show_code else "pass"
        else:
            reason = verdict.split(":", 1)[-1].strip()[:200]
            per_api[entry.name] = (
                {"status": "fail", "reason": reason, "code": code.strip()}
                if show_code else f"fail: {reason}"
            )
            log.append(run_id=run_id, step="readme-unit-test", language=cfg.language,
                       task=f"comprehension_{doc_source}", status="fail",
                       function=entry.name, error=reason, root_cause="",
                       suggested_fix_code="")
    n = len(inventory)
    return {
        "check": "comprehension",
        "doc_source": doc_source,
        "passed": bool(n) and passed_n == n,
        "score": round(passed_n / n, 3) if n else 0.0,
        "details": per_api,
    }


def _fill_scaffold(scaffold: str, snippet: str, region: list[str], placeholders: dict) -> str:
    """Insert the snippet into the scaffold's API-test region and substitute
    {{KEY}} placeholders (sample-data paths). Generic: region markers and
    placeholder keys all come from config, nothing GRAIL-specific is hardcoded."""
    text = scaffold
    if region and len(region) == 2 and region[0] in text and region[1] in text:
        pre, _, rest = text.partition(region[0])
        _, _, post = rest.partition(region[1])
        # match the marker's indentation (required for Python scaffolds, where the
        # region sits inside a function body; harmless formatting for brace languages)
        indent = pre.rpartition("\n")[2]
        if indent.strip() == "":
            snippet = "\n".join((indent + l) if l.strip() else l
                                for l in snippet.splitlines())
        text = f"{pre}{region[0]}\n{snippet}\n{indent}{region[1]}{post}"
    else:                                  # no region markers: append the snippet
        text = text + "\n" + snippet
    for key, val in (placeholders or {}).items():
        text = text.replace("{{" + key + "}}", str(val))
    return text


def _strip_fences(text: str, *, strip_imports: bool = False) -> str:
    """Remove markdown code fences / language tags the model may emit despite
    instructions, so the snippet is pure code. When the scaffold owns imports,
    callers can also drop model-generated import lines to avoid stale/wrong
    imports shadowing curated scaffold imports."""
    t = text.strip()
    if "```" in t:
        # keep the content of the first fenced block if present, else strip fences
        import re as _re
        m = _re.search(r"```[a-zA-Z]*\n(.*?)```", t, _re.DOTALL)
        t = (m.group(1) if m else
             t.replace("```scala", "").replace("```python", "").replace("```", ""))
    if strip_imports:
        t = "\n".join(
            line for line in t.strip().splitlines()
            if not line.lstrip().startswith("import ")
        )
    return t.strip()


# Convention: map a fixture file's extension to a typed binding name so users
# can DROP files in a folder instead of hand-writing the sample_data catalog.
_FIXTURE_TYPES = {
    ".tif": "raster_tif", ".tiff": "raster_tif",
    ".geojson": "vector_geojson",
    ".shp": "vector_shapefile",
    ".csv": "table_csv",
    ".tsv": "table_tsv",
    ".parquet": "table_parquet",
    ".wkt": "vector_wkt",
    ".kml": "vector_kml",
    ".gpx": "vector_gpx",
    ".json": "vector_geojson",
}


def _kind_of(suffix: str) -> str | None:
    """raster / vector / table for a file extension (the *_dir kind)."""
    name = _FIXTURE_TYPES.get(suffix.lower())
    return name.split("_")[0] if name else None


# reverse of _FIXTURE_TYPES: typed binding name -> the extension(s) it should point at
# (e.g. raster_tif -> {.tif, .tiff}, vector_geojson -> {.geojson, .json}). Drives the
# type check in _validate_sample_data.
_SUFFIXES_FOR_TYPE: dict[str, set[str]] = {}
for _suf, _name in _FIXTURE_TYPES.items():
    _SUFFIXES_FOR_TYPE.setdefault(_name, set()).add(_suf)


def _validate_sample_data(sample_data: dict[str, str]) -> list[str]:
    """Sanity-check every typed input path BEFORE it is compiled into the scaffold, so a
    mis-pinned or missing `sample_data` entry fails LOUDLY and specifically here —
    `sample_data.raster_tif expects .tif/.tiff but path has '.shp'` — instead of
    surfacing many steps later as an opaque Scala runtime error the fix-loop can't parse.

    Only bindings whose NAME encodes a type (the `_FIXTURE_TYPES` convention:
    raster_tif, vector_shapefile, table_csv, ...) are type-checked; custom names and
    `output_dir` are exempt (existence-only where sensible). `*_dir` bindings must be
    directories. Returns human-readable warning lines (empty = all inputs look right)."""
    import os
    warns: list[str] = []
    for name, path in sample_data.items():
        if name == "output_dir":                       # an output target, may not exist yet
            continue
        local = str(path).split("://", 1)[-1]          # strip file:// for on-disk checks
        exists = os.path.exists(local)
        if name.endswith("_dir"):                       # folder-of-data binding
            if exists and not os.path.isdir(local):
                warns.append(f"sample_data.{name} should be a directory but is a file: {local}")
            elif not exists:
                warns.append(f"sample_data.{name} directory not found: {local}")
            continue
        expected = _SUFFIXES_FOR_TYPE.get(name)         # None -> custom name, skip type check
        if expected and not os.path.isdir(local):        # a dir dataset (parquet/, tiles/) has no file ext
            suf = os.path.splitext(local)[1].lower()
            if suf not in expected:
                warns.append(
                    f"sample_data.{name} expects {'/'.join(sorted(expected))} "
                    f"but path has '{suf or '(no extension)'}': {local}")
        if not exists:
            warns.append(f"sample_data.{name} file not found: {local}")
    return warns


def _discover_fixtures(cfg: AidealConfig, ex: dict) -> dict[str, str]:
    """Convention over config: when `sample_data` isn't set, build the typed
    catalog by scanning `fixtures_dir` (default 'fixtures/').

      top-level FILES  -> typed file bindings  (raster_tif, vector_geojson, ...)
      top-level FOLDERS -> typed *_dir bindings (raster_dir, vector_dir,
                           table_dir), keyed by the data they contain — for
                           folder-of-tiles / multi-file datasets.

    First file/folder of each type wins. Lets a user drop sample files OR data
    folders in fixtures/ instead of authoring the catalog by hand."""
    sub = ex.get("fixtures_dir", "fixtures")
    root = (cfg.root / sub)
    found: dict[str, str] = {}
    if not root.is_dir():
        return found
    for p in sorted(root.iterdir()):
        if p.is_file():                                   # single-file inputs
            name = _FIXTURE_TYPES.get(p.suffix.lower())
            if name:
                found.setdefault(name, str(p.resolve()))
        elif p.is_dir():                                  # folder-of-data inputs
            kinds = {k for f in p.rglob("*") if f.is_file()
                     for k in (_kind_of(f.suffix),) if k}
            for kind in sorted(kinds):
                found.setdefault(f"{kind}_dir", str(p.resolve()))
    return found


def _base_type(t: str) -> str:
    """Head type name, generics and package path stripped:
    'RDD[ITile[T]]' -> 'RDD', 'JavaRasterRDD[T]' -> 'JavaRasterRDD',
    'edu.ucr...cg.SpatialRDD' -> 'SpatialRDD', '' -> ''."""
    t = (t or "").strip().split("[")[0].strip()
    m = re.match(r"[A-Za-z_][\w.]*", t)
    return m.group(0).split(".")[-1] if m else ""


def _consumed_type_counts(cfg: AidealConfig) -> dict:
    """How many public defs accept each base type as a PARAMETER — i.e. what the
    library's operations actually need loaded, weighted by demand. A reader whose
    return type has count 0 feeds nothing (a shadow reader, e.g. a Java* wrapper);
    a high count means many ops consume it. Codebase-agnostic: no hardcoded names."""
    from collections import Counter
    from .readme_agent import public_api_details
    c: Counter = Counter()
    for d in public_api_details(cfg):
        if d.get("visibility") == "public":
            for p in (d.get("params") or []):
                b = _base_type(p.get("type", ""))
                if b:
                    c[b] += 1
    return dict(c)


def _useful_readers(names: list, ret_of: dict, counts: dict) -> list:
    """Order reader NAMES by how many documented ops consume each reader's return
    type (desc); drop readers whose return type is consumed by nothing. Returns []
    when there's no type signal, so the caller falls back to the raw candidates —
    this is what makes the Scala mixin reader (return feeds many ops) beat a Java
    wrapper (return feeds none) on a name collision, with no 'Java' rule."""
    scored = [(counts.get(ret_of.get(n, ""), 0), n) for n in names]
    return [n for s, n in sorted(scored, key=lambda sn: -sn[0]) if s > 0]


def _drop_unconsumed_lines(code: str, counts: dict) -> str:
    """Belt-and-suspenders: drop any generated `val x: T = ...` whose type T is
    consumed by no documented op (e.g. the model still reached for a Java wrapper)."""
    if not counts:
        return code
    kept = []
    for ln in code.splitlines():
        m = re.match(r"\s*val\s+\w+\s*:\s*([^=]+?)\s*=", ln)
        if m and _base_type(m.group(1)) and counts.get(_base_type(m.group(1)), 0) == 0:
            continue
        kept.append(ln)
    return "\n".join(kept).strip()


def _resolve_preamble(cfg: AidealConfig, ex: dict, sample_data: dict) -> str:
    """Return the typed-input preamble. `preamble: auto` LLM-generates it ONCE
    (cached to docs/preamble.scala) from the codebase's own documented reader
    APIs — so NO human writes Scala. A literal string is used as-is (still
    supported). Any failure (no key/profile) degrades to '' so the model just
    writes its own I/O guided by io_hints.

    Hardened grounding: readers are ranked by how many documented ops CONSUME their
    return type, shadow readers (return type consumed by nothing — the classic
    JavaRasterRDD/JavaSpatialRDD wrappers) are dropped, the model is told the target
    consumed types explicitly, and any generated line binding to an unconsumed type
    is filtered out. This is the general fix for the reader name-collision that made
    `auto` load Java wrappers and force snippets to invent .toRDD/.toRasterRDD."""
    raw = (ex.get("preamble", "") or "")
    if raw.strip().lower() != "auto":
        return raw.strip()
    cache = cfg.llm_readme.parent / "preamble.scala"
    if cache.exists():
        return cache.read_text(encoding="utf-8").strip()
    try:
        from .llm import invoke_text
        from .readme_agent import parse_readme, public_api_details
        from .profile import require_profile
        require_profile(cfg)
        counts = _consumed_type_counts(cfg)
        ret_of = {d["name"]: _base_type(d.get("returns", "")) for d in public_api_details(cfg)}
        cands = [e for e in parse_readme(cfg.llm_readme)
                 if re.search(r"read|geoTiff|geojson|load|shapefile|spatialFile|wkt|import", e.name, re.I)]
        useful_names = _useful_readers([e.name for e in cands], ret_of, counts)
        by_name = {e.name: e for e in cands}
        readers = ([by_name[n] for n in useful_names] or cands)[:8]
        target_set = sorted({ret_of.get(e.name, "") for e in readers if ret_of.get(e.name)})
        targets = ", ".join(target_set) or "the library's core input types"
        kinds = ", ".join(sorted(sample_data))
        system = (f"You write {cfg.language} that loads sample inputs into typed variables, "
                  "using ONLY the reader APIs documented below. Output only code, no fences, "
                  "one `val <name>: <Type> = <reader>(<pathVar>)` per usable input. Load into the "
                  f"types the library's operations CONSUME ({targets}); do NOT use a reader that "
                  "returns a type not in that list (e.g. a Java* wrapper the operations don't accept).")
        user = (f"Path variables in scope: {kinds}\n\nTarget consumed types: {targets}\n\n"
                "Documented reader APIs:\n" + "\n\n".join(e.body for e in readers)
                + "\n\nWrite the load statements.")
        code = invoke_text(cfg.model_for_role("author"), system, user).strip()
        code = re.sub(r"^```\w*\n?|```$", "", code, flags=re.MULTILINE).strip()
        code = _drop_unconsumed_lines(code, counts)
        if code:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(code, encoding="utf-8")
        return code
    except Exception:
        return ""


def _resolve_io_hints(cfg: AidealConfig, ex: dict, sample_data: dict) -> str:
    """Return the I/O cheat-sheet. `io_hints: auto` LLM-generates it ONCE (cached
    to docs/io_hints.txt) from the codebase's own documented reader/writer APIs —
    so NO human writes it. A literal string is used as-is. Degrades to '' on any
    failure (no key/profile)."""
    raw = (ex.get("io_hints", "") or "")
    if raw.strip().lower() != "auto":
        return raw.strip()
    cache = cfg.llm_readme.parent / "io_hints.txt"
    if cache.exists():
        return cache.read_text(encoding="utf-8").strip()
    try:
        from .llm import invoke_text
        from .readme_agent import parse_readme, public_api_details
        from .profile import require_profile
        require_profile(cfg)
        # rank reader/writer entries by how many documented ops consume their return
        # type (central readers like `shapefile` float up) BEFORE the cap, so a
        # high-index-but-central reader isn't truncated away — the bug that made
        # io_hints miss `shapefile` (past the first 12) and always suggest geojson.
        counts = _consumed_type_counts(cfg)
        ret_of = {d["name"]: _base_type(d.get("returns", "")) for d in public_api_details(cfg)}
        cand = [e for e in parse_readme(cfg.llm_readme)
                if re.search(r"read|write|save|load|geoTiff|geojson|shapefile|join", e.name, re.I)]
        cand.sort(key=lambda e: -counts.get(ret_of.get(e.name, ""), 0))
        entries = [e.body for e in cand[:12]]
        system = (f"From the documented APIs below, write a SHORT I/O cheat-sheet for a coder using this "
                  f"{cfg.language} library: how to load each input type, how to write output, and any "
                  "static-object-vs-instance-method gotchas. 4-6 concrete lines with real call forms. No fences.")
        user = "Documented APIs:\n\n" + "\n\n".join(entries)
        txt = invoke_text(cfg.model_for_role("author"), system, user).strip()
        if txt:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(txt, encoding="utf-8")
        return txt
    except Exception:
        return ""


def _execute_sample_data(cfg: AidealConfig, ex: dict) -> tuple[dict[str, str], str, list[str]]:
    """Resolve sample-data bindings for prompts/scaffolds. Uses the configured
    `sample_data` if present; otherwise auto-discovers a `fixtures/` folder.
    Always provides an `output_dir` binding so write APIs have a target.

    Returns (sample_data, available_inputs, warnings). `warnings` flags typed inputs
    whose path is missing or whose extension contradicts the binding's declared type
    (see _validate_sample_data); they're also echoed to stderr so a mis-pinned input is
    obvious on the console, not buried in a downstream compile/runtime failure."""
    def _resolve(v):
        if isinstance(v, dict):
            package = v.get("package")
            resource = v.get("resource")
            if not package or not resource:
                raise ValueError("sample_data mapping requires both 'package' and 'resource'")
            from importlib.resources import files
            target = files(str(package)).joinpath(str(resource))
            if not target.is_file():
                raise FileNotFoundError(
                    f"package resource not found: {package}:{resource}")
            return str(target)
        v = str(v)
        return str((cfg.root / v).resolve()) if (not v.startswith("/") and "/" in v) else v

    use_uri = ex.get("local_uris", True)

    def _as_uri(p):
        p = str(p)
        if "://" in p:
            return p
        return f"file://{p}" if (use_uri and p.startswith("/")) else p

    # fixtures auto-discovery is the base; explicit `sample_data` entries OVERRIDE
    # per binding — so you can pin just raster_tif and let geojson/csv auto-fill.
    configured = dict(_discover_fixtures(cfg, ex))
    configured.update(ex.get("sample_data", {}) or {})
    configured.setdefault("output_dir", ex.get("output_dir", "/tmp/aideal_apitest_out"))
    sample_data = {k: _as_uri(_resolve(v)) for k, v in configured.items()}
    available_inputs = "\n".join(f"- {k} = {p}" for k, p in sample_data.items()) or "(none configured)"
    # type/existence check on the input paths (raster_tif must be a .tif, etc.) so a
    # bad binding is caught here, not as an opaque Scala error deep in the run.
    warnings = _validate_sample_data(sample_data)
    if warnings:
        import sys
        for w in warnings:
            sys.stderr.write(f"  [sample_data] WARNING: {w}\n")
        sys.stderr.flush()
    return sample_data, available_inputs, warnings


def _classify_error_py(merged: str, rc: int, error_marker: str) -> tuple[str, str, str]:
    """Python flavor of _classify_error. compile = SyntaxError/IndentationError
    (the file never ran); infra = missing third-party module (env problem, not a
    doc problem — excluded from the doc-quality denominator like JVM
    NoClassDefFoundError); runtime = everything raised while running."""
    import re as _re
    m = _re.search(r"(?:ModuleNotFoundError|ImportError)[:\s]+(.+)", merged)
    if m:
        return "infra", f"missing module/import: {m.group(1).strip()[:200]}", ""
    m = _re.search(r"^(?:SyntaxError|IndentationError|TabError)[:\s]+(.+)$", merged, _re.M)
    if m:
        loc = _re.search(r'File "([^"]+)", line (\d+)', merged)
        return "compile", m.group(0).strip()[:300], (f"{loc.group(1)}:{loc.group(2)}" if loc else "")
    if error_marker and error_marker in merged:
        line = next((l for l in merged.splitlines() if error_marker in l), "").strip()
        msg = line.split(error_marker, 1)[-1].strip()
        frames = _re.findall(r'File "([^"]+\.py)", line (\d+)', merged)
        locus = f"{frames[-1][0]}:{frames[-1][1]}" if frames else ""
        return "runtime", msg or "runtime error", locus
    m = _re.search(r"^(\w*(?:Error|Exception)\b.*)$", merged, _re.M)
    if m:
        return "runtime", m.group(1).strip()[:300], ""
    return "unknown", (merged.strip()[-300:] or f"exit {rc}"), ""


def _classify_error_java(merged: str, rc: int, error_marker: str) -> tuple[str, str, str]:
    """Java flavor: distinguish javac diagnostics, missing classpath entries,
    and exceptions raised by an otherwise runnable harness."""
    import re as _re
    im = _re.search(
        r"(?:NoClassDefFoundError|ClassNotFoundException)[:\s]+([\w/.$]+)", merged)
    if im:
        return "infra", f"missing dependency on classpath: {im.group(1)}", ""
    cm = _re.search(r"^([^\n]+\.java):(\d+): error: (.+)$", merged, _re.M)
    if cm:
        return "compile", cm.group(0).strip()[:300], f"{cm.group(1)}:{cm.group(2)}"
    if error_marker and error_marker in merged:
        line = next((line for line in merged.splitlines() if error_marker in line), "").strip()
        msg = line.split(error_marker, 1)[-1].strip()
        frame = _re.search(r"\bat [\w.$]+\(([^:()]+\.java):(\d+)\)", merged)
        locus = f"{frame.group(1)}:{frame.group(2)}" if frame else ""
        return "runtime", msg or "runtime exception", locus
    exc = _re.search(r"^(?:Exception in thread \"[^\"]+\" )?([\w.$]+(?:Exception|Error): .+)$",
                     merged, _re.M)
    if exc:
        return "runtime", exc.group(1).strip()[:300], ""
    return "unknown", (merged.strip()[-300:] or f"exit {rc}"), ""


def _classify_error(merged: str, rc: int, error_marker: str,
                    language: str = "scala") -> tuple[str, str, str]:
    """Return (category, message, locus) from the run output.
    category: compile | runtime | timeout | infra | unknown; locus = the failing call."""
    import re as _re
    if rc == 124:
        return "timeout", "execution timed out", ""
    if language.lower() == "python":
        return _classify_error_py(merged, rc, error_marker)
    if language.lower() == "java":
        return _classify_error_java(merged, rc, error_marker)
    # infra/environment: a dependency missing from the HARNESS classpath (the real
    # test suite has it; spark-submit local[*] may not). NoClassDefFoundError /
    # ClassNotFoundException are never a documentation problem — no doc fix resolves
    # a missing jar — so they get their own category and are excluded from the
    # doc-quality denominator. Matches ONLY the explicit JVM class-loading errors,
    # NOT scalac "not found: type X" (which IS a real snippet/doc problem).
    im = _re.search(r"(?:NoClassDefFoundError|ClassNotFoundException)[:\s]+([\w/.$]+)", merged)
    if im:
        return "infra", f"missing dependency on classpath: {im.group(1)}", ""
    # compile-time classpath gap: scalac can't read a referenced class from the jars
    # (inner-class / version mismatch, e.g. a protobuf ExtendableMessage). Also infra,
    # not a doc problem — this is the `build` "Unable to locate class..." failure.
    if _re.search(r"Unable to locate class corresponding to inner class|"
                  r"class file needed by .* is missing|missing or invalid dependency detected", merged):
        return "infra", "compile-time classpath/version gap (missing or mismatched jar)", ""
    # runtime: the scaffold prints __RUN_ERR__ <Class>: <msg>
    if error_marker and error_marker in merged:
        line = next((l for l in merged.splitlines() if error_marker in l), "").strip()
        msg = line.split(error_marker, 1)[-1].strip()
        # first app stack frame = the failing call site
        frame = next((l.strip() for l in merged.splitlines()
                      if l.strip().startswith("at ") and ".scala" in l), "")
        return "runtime", msg or "runtime error", frame
    # compile: scalac prints `<file>.scala:NN: error: <msg>`
    cm = _re.search(r"^(.*\.scala:\d+: error: .*)$", merged, _re.MULTILINE)
    if cm:
        return "compile", cm.group(1).strip(), cm.group(1).split(":")[0:2] and cm.group(1).split(" error:")[0].strip()
    return "unknown", (merged.strip()[-300:] or f"exit {rc}"), ""


def _owner_map(cfg: AidealConfig) -> dict:
    """name -> (owner_type, kind). owner_type is the class/object that DEFINES the
    function (Scala's one-top-level-type-per-file convention: the source file stem).
    kind is 'static' when that type is declared `object <stem>` and NOT also a
    class/trait (call as `Owner.method(...)`), else 'instance' (needs a receiver of
    type Owner: `val r: Owner = ...; r.method(...)`).

    This is the receiver TYPE the flat doc erases into a bare `value.method`, which
    is what sends a snippet calling the method on the wrong type (e.g. `area` on
    IFeature instead of its owner LiteGeometry). Same class grouping `organize`
    already uses — reused here to type the receiver."""
    import os
    from .readme_agent import public_api_details
    file_kind: dict[str, str] = {}
    owners: dict[str, tuple] = {}
    for d in public_api_details(cfg):
        f = d.get("file", "")
        if not f.endswith(".scala"):
            continue
        stem = os.path.basename(f)[:-6]
        if f not in file_kind:
            try:
                txt = (cfg.root / f).read_text(encoding="utf-8", errors="ignore")
            except Exception:
                txt = ""
            has_object = bool(re.search(rf"^\s*(?:final\s+|case\s+)?object\s+{re.escape(stem)}\b", txt, re.M))
            has_type = bool(re.search(
                rf"^\s*(?:final\s+|sealed\s+|abstract\s+|case\s+)?(?:class|trait)\s+{re.escape(stem)}\b", txt, re.M))
            file_kind[f] = "static" if (has_object and not has_type) else "instance"
        owners[d["name"]] = (stem, file_kind[f])
    return owners


def _receiver_hint(entry_name: str, owner_map: dict) -> str:
    """Render the receiver-typing instruction for the snippet-writer, from _owner_map."""
    own = owner_map.get(entry_name)
    if not own:
        return ""
    typ, kind = own
    if kind == "static":
        return f"`{entry_name}` is a STATIC method on object `{typ}` — call it as `{typ}.{entry_name}(...)`."
    return (f"`{entry_name}` is an INSTANCE method on `{typ}` — you need a value of type `{typ}` to "
            f"call it on (obtain one from a preloaded input, or from a sibling method that returns / "
            f"constructs a `{typ}`), then call `.{entry_name}` on it. Do NOT call it on an unrelated type.")


_FRAME_RE = re.compile(r"\(([A-Za-z0-9_$]+\.(?:scala|java)):(\d+)\)"
                       r"|File \"[^\"]*?([A-Za-z0-9_]+\.py)\", line (\d+)")


def _codebase_frames(merged: str, file_index: dict[str, str], limit: int = 5) -> list[str]:
    """Extract the CODEBASE source lines exercised by a failing run: JVM stack
    frames `at pkg.Cls.m(File.scala:123)` whose file basename belongs to the
    target repo (via `file_index` basename→relative-path). Answers "which
    RDPro line did the snippet actually reach" for runtime failures."""
    out: list[str] = []
    seen: set[str] = set()
    for m in _FRAME_RE.finditer(merged):
        base, ln = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        rel = file_index.get(base)
        if not rel:
            continue
        key = f"{rel}:{ln}"
        if key not in seen:
            seen.add(key)
            out.append(key)
            if len(out) >= limit:
                break
    return out


def _comprehension_execute(cfg: AidealConfig, inventory, sample, seed, doc_source: str,
                           show_code: bool = False, class_context: bool = False,
                           max_fix_rounds: int | None = None,
                           resume: bool = False, timeout_s: int | None = None,
                           shared_doc: str | None = None,
                           doc_scope: str = "entry") -> dict:
    """Compile/run each API's audience snippet via the configured command.
    PASS = the program runs (success_marker present, exit 0). Real failures
    (compile/runtime) are logged with the actual error text.

    class_context: INDEX-FIRST — prefix each API's body with its catalogue class
    header (receiver + a verified sibling's real call pattern) so the snippet writer
    stops inventing the receiver/entry point. Complements the existing `{receiver}`
    TYPE hint with a proven, compiled example. Off -> bare per-API body (baseline)."""
    import os
    import shlex
    import subprocess
    import tempfile
    from pathlib import Path
    from .llm import invoke_text
    from .prompts import load as load_prompt

    from .llm import usage_snapshot, usage_delta
    import time as _time

    ex = cfg.comprehension.get("execute", {}) if cfg.comprehension else {}
    manifest_inventory_n = len(inventory)
    cmd_template = ex.get("command", "")
    scaffold_path = ex.get("scaffold", "")
    if not cmd_template or not scaffold_path:
        return {"check": "comprehension", "mode": "execute", "passed": False, "score": 0.0,
                "details": {"error": "configure comprehension.execute.{command,scaffold} in aideal.yaml"}}
    scaffold_file = (cfg.root / scaffold_path).resolve()
    if not scaffold_file.exists():
        return {"check": "comprehension", "mode": "execute", "passed": False, "score": 0.0,
                "details": {"error": f"scaffold not found: {scaffold_file}"}}
    scaffold = scaffold_file.read_text(encoding="utf-8", errors="ignore")
    region = ex.get("region", ["// TODO API_TEST_START", "// TODO API_TEST_END"])

    # Build the project's own uberjar ONCE, then run snippets against that single
    # jar (no hand-listed dependency jars). build runs in build_cwd; {uberjar}
    # in the command is replaced with the resolved jar path.
    import glob as _glob
    build_cwd = (cfg.root / ex.get("build_cwd", ".")).resolve()
    build_cmd = ex.get("build", "")
    build_info = None
    if build_cmd:
        try:
            bp = subprocess.run(shlex.split(build_cmd), cwd=build_cwd, capture_output=True,
                                text=True, timeout=int(ex.get("build_timeout_seconds", 1800) or 1800))
        except FileNotFoundError as e:
            return {"check": "comprehension", "mode": "execute", "passed": False, "score": 0.0,
                    "details": {"error": f"build tool not found ({e.filename}). Install Maven on "
                                "PATH, or set comprehension.execute.build: '' and point `uberjar` "
                                "at a prebuilt jar."}}
        except subprocess.TimeoutExpired:
            return {"check": "comprehension", "mode": "execute", "passed": False, "score": 0.0,
                    "details": {"error": "project build timed out"}}
        build_info = {"exit_code": bp.returncode, "stderr_tail": bp.stderr[-400:]}
        if bp.returncode != 0:
            return {"check": "comprehension", "mode": "execute", "passed": False, "score": 0.0,
                    "details": {"error": "project build failed", "build": build_info}}
    uberjar = ""
    uber_list: list[str] = []
    if ex.get("uberjar"):
        uber_list = sorted(_glob.glob(str(build_cwd / ex["uberjar"])))
        uberjar = uber_list[-1] if uber_list else ""
    # A glob of a prebuilt distribution's lib/*.jar — comma-joined as {jars}
    # (spark-submit --jars), colon-joined into {classpath} (scalac) below.
    jars = ""
    beast_jars_list: list[str] = []
    if ex.get("jars"):
        jg = str(ex["jars"])
        beast_jars_list = sorted(_glob.glob(jg if jg.startswith("/") else str(cfg.root / jg)))
        if not beast_jars_list:
            return {"check": "comprehension", "mode": "execute", "passed": False, "score": 0.0,
                    "details": {"error": f"no jars matched comprehension.execute.jars: {jg}"}}
        jars = ",".join(beast_jars_list)

    # {classpath} for scalac (COLON-separated): Spark jars + beast jars + the
    # uber jar (the uber carries JTS/GeoTools types so generated snippets that
    # reference them still compile). Runtime deps come from --packages.
    spark_jars: list[str] = []
    spark_jars_glob = ex.get("spark_jars", "")
    if spark_jars_glob:
        sjg = str(spark_jars_glob)
        spark_jars = sorted(_glob.glob(
            sjg if sjg.startswith("/") else str(cfg.root / sjg)))
        if not spark_jars:
            return {"check": "comprehension", "mode": "execute", "passed": False,
                    "score": 0.0, "details": {
                        "error": f"no Spark jars matched comprehension.execute.spark_jars: {sjg}"}}
    else:
        try:
            import pyspark as _pyspark
            _sj = os.path.join(os.path.dirname(_pyspark.__file__), "jars")
            spark_jars = sorted(_glob.glob(os.path.join(_sj, "*.jar")))
        except Exception:
            pass
    classpath = ":".join(beast_jars_list + spark_jars + uber_list)

    def _resolve(v):
        v = str(v)
        return str((cfg.root / v).resolve()) if (not v.startswith("/") and "/" in v) else v

    # Typed sample-data catalog: name -> resolved path. Each becomes a `val` in
    # the scaffold; the model picks the one(s) matching the API's param types.
    sample_data, available_inputs, sample_data_warnings = _execute_sample_data(cfg, ex)
    _lang = cfg.language.lower()
    _is_py = _lang == "python"
    _is_java = _lang == "java"
    bindings = "\n    ".join(
        (f'{k} = r"{p}"' if _is_py else
         f'String {k} = "{p}";' if _is_java else
         f'val {k} = "{p}"')
        for k, p in sample_data.items())
    # Option-2 isolation: a codebase-specific `preamble` pre-loads typed inputs
    # (e.g. rasterRDD, featuresRDD) right after the path vals, so a per-API test
    # writes ONLY the API call — I/O can no longer fail the test. The model is
    # then shown the pre-loaded typed vars instead of raw paths.
    preamble = _resolve_preamble(cfg, ex, sample_data)   # 'auto' -> LLM-generated, cached
    if preamble:
        _cmt = "#" if _is_py else "//"
        bindings += (f"\n\n    {_cmt} pre-loaded typed inputs (comprehension.execute.preamble)\n    "
                     + "\n    ".join(preamble.splitlines()))
        if _is_py:
            preloaded = re.findall(
                r"^\s*(\w+)\s*(?::\s*\w+)?\s*=\s*(?:.*?#\s*type:\s*(.+))?",
                preamble, re.M)
        elif _is_java:
            preloaded = [(name, typ) for typ, name in re.findall(
                r"^\s*(?:final\s+)?([\w.$<>?, \[\]]+)\s+(\w+)\s*=", preamble, re.M)]
        else:
            preloaded = re.findall(r"val\s+(\w+)\s*:\s*([^=]+?)\s*=", preamble)
        preloaded = [(n, (t or "(see preamble)").strip()) for n, t in preloaded if n]
        if preloaded:
            available_inputs = (
                "Pre-loaded and already in scope — use these directly, do NOT re-load:\n"
                + "\n".join(f"- {n}: {t.strip()}" for n, t in preloaded)
                + "\n(raw input path strings also in scope if needed: "
                + ", ".join(sample_data) + ")")
    # legacy {{KEY}} placeholders still supported
    placeholders = {k: _resolve(v) for k, v in (ex.get("placeholders", {}) or {}).items()}
    success_marker = ex.get("success_marker", "")
    error_marker = ex.get("error_marker", "")
    # Phase-A correctness gate: when require_correctness is on, a run only PASSES if
    # it emitted the structured witness (check_marker) — i.e. the snippet actually
    # ran the require(...) correctness assertion and produced a non-degenerate
    # result. Catches a wrong pixel TYPE that reads garbage without throwing, which
    # a plain "it ran" (success_marker) check would let through. Default off.
    check_marker = ex.get("check_marker", "__CHECK__")
    require_correctness = bool(ex.get("require_correctness", False))
    timeout = int(timeout_s or ex.get("timeout_seconds", 600) or 600)
    strip_snippet_imports = bool(ex.get("strip_snippet_imports", False))
    output_tail_chars = int(ex.get("output_tail_chars", 2000) or 2000)
    if max_fix_rounds is None:                                # CLI/bench override wins
        max_fix_rounds = int(ex.get("max_fix_rounds", 3) or 0)   # default 3 fixes (4 attempts)
    # stuck detector: N CONSECUTIVE identical errors -> stop this API's loop.
    # Evidence (g4 fix-all, gemini-2.5-pro, 2026-07-07): every fixable API
    # fixed within 12 rounds; unfixable ones repeated the SAME compile error
    # to the 100-round cap (addTile: 368K output tokens on one API). 0 disables.
    stuck_repeats = int(ex.get("stuck_repeats", 3) or 0)
    work_dir = (cfg.root / ex.get("work_dir", ".aideal_exec")).resolve()
    work_dir.mkdir(parents=True, exist_ok=True)

    # A resume checkpoint is valid only for the exact experimental treatment.
    # Hash both the ordered denominator and the delivered document so A2 rows
    # can never leak into a repaired B2 run merely because both say "aideal".
    import hashlib as _hashlib
    import json as _json
    _manifest_payload = "\n".join(e.name for e in inventory).encode("utf-8")
    manifest_sha256 = _hashlib.sha256(_manifest_payload).hexdigest()
    _doc_payload = (shared_doc if shared_doc is not None else
                    "\n\0\n".join(f"{e.name}\n{e.body}" for e in inventory))
    doc_sha256 = _hashlib.sha256(_doc_payload.encode("utf-8")).hexdigest()
    fingerprint_components = _comprehension_fingerprint_components(
        cfg, ex=ex, doc_source=doc_source, doc_scope=doc_scope,
        max_fix_rounds=max_fix_rounds, manifest_sha256=manifest_sha256,
        document_sha256=doc_sha256, scaffold_file=scaffold_file,
        sample_data=sample_data, class_context=class_context, timeout=timeout)
    _fp_payload = _json.dumps(
        fingerprint_components, sort_keys=True, separators=(",", ":"),
        default=str).encode("utf-8")
    experiment_fingerprint = _hashlib.sha256(_fp_payload).hexdigest()

    # Crash-proof progress: one JSONL row per finished API, flushed as it
    # completes. A killed/crashed full run loses NOTHING: rerun with --resume
    # and already-finished APIs are skipped and pre-filled into the results
    # (the 2026-07-01 all-API run died ~120/218 in and lost every result).
    # Without --resume the checkpoint restarts with the run.
    ckpt = work_dir / "comprehension_progress.jsonl"
    from .checkpoint_compatibility import load_compatibility
    reuse = load_compatibility(ckpt, fingerprint_components) if resume else {}
    legacy_fingerprint = reuse.get("legacy_fingerprint")
    done_rows: dict[str, dict] = {}
    if resume and ckpt.exists():
        for line in ckpt.read_text(encoding="utf-8").splitlines():
            try:
                row = _json.loads(line)
                # Provider/network failures are transient evidence, not a
                # completed API. An overnight restart must retry them instead
                # of silently preserving a quota outage in the final table.
                if (_checkpoint_row_reusable(row, experiment_fingerprint)
                        or (legacy_fingerprint and
                            _checkpoint_row_reusable(row, legacy_fingerprint))):
                    # Native current evidence takes precedence over legacy
                    # rows even when both versions append to the same journal.
                    previous = done_rows.get(row["name"], {})
                    if (previous.get("experiment_fingerprint") == experiment_fingerprint
                            and row.get("experiment_fingerprint") != experiment_fingerprint):
                        continue
                    done_rows[row["name"]] = row
            except Exception:
                continue
    elif ckpt.exists():
        try:
            ckpt.unlink()
        except OSError:          # e.g. cross-mount permission mismatch —
            try:                 # truncating is just as good as deleting
                ckpt.write_text("")
            except OSError:
                pass             # worst case: stale rows only matter under --resume

    # Scope execution to user-facing, runnable APIs. Most of the public surface
    # is internal/utility defs (close, copy, compareTo, hasNext, ...) that aren't
    # standalone-runnable — completeness covers all of them; execution shouldn't.
    include = set(ex.get("include", []) or [])
    exclude = set(ex.get("exclude", []) or [])
    # Reproducible alternative to a hand-list: select by DEFINING CLASS. User-
    # facing ops live in entrypoint classes (the SparkContext/RasterRDD mixin and
    # the operation objects); internal helpers live in tile/reader/serializer
    # classes. Derived from the `file` of each API — no manual judgment.
    entry_classes = set(ex.get("entrypoint_classes", []) or [])
    if entry_classes and not include:
        import os as _os
        include = {d["name"] for d in public_api_details(cfg)
                   if d["visibility"] == "public"
                   and _os.path.basename(d["file"])[:-6] in entry_classes}
    if include:
        inventory = [e for e in inventory if e.name in include]
    if exclude:
        inventory = [e for e in inventory if e.name not in exclude]
    if sample and sample < len(inventory):
        inventory = random.Random(seed).sample(inventory, sample)
    import sys as _count_sys
    _count_sys.stderr.write(
        f"[comprehension] APIs to execute: {len(inventory)} of "
        f"{manifest_inventory_n} (doc_source={doc_source}, doc_scope={doc_scope})\n"
    )
    _count_sys.stderr.flush()

    io_hints_text = _resolve_io_hints(cfg, ex, sample_data)   # 'auto' -> LLM-generated, cached

    # Build the Ivy --packages / --repositories flags from list config so the
    # generic spark-submit command can live in the scala-spark adapter and a
    # project only supplies its `packages:`/`repositories:` lists (empty -> the
    # flag disappears entirely).
    pkgs = ex.get("packages") or []
    repos = ex.get("repositories") or []
    packages_flag = ("--packages " + ",".join(pkgs)) if pkgs else ""
    repositories_flag = ("--repositories " + ",".join(repos)) if repos else ""

    log = ErrorLog(cfg.error_log)
    run_id = new_run_id()
    task = f"comprehension_exec_{doc_source}"
    per_api: dict[str, object] = {}
    passed_n = 0
    infra_n = 0            # runs that failed only on a missing dependency (infra);
                           # excluded from the doc-quality denominator in the result
    # receiver typing: the flat doc renders `value.method`; hand the snippet-writer
    # the DEFINING type per function so it calls the method on the right receiver.
    owner_map = _owner_map(cfg)
    # INDEX-FIRST: build the catalogue model once; prefix each body with its class
    # header (receiver + a verified sibling's proven call pattern). Off -> bare body.
    from .readme_agent import _class_context_body
    if shared_doc is not None:
        # FULL-DOCUMENT mode (2x2 experiment): every audience attempt receives
        # the ENTIRE selected documentation; only the target line differs.
        # No truncation — exposure is total and identical across the manifest.
        import sys as _s
        _s.stderr.write(f"[full-doc] audience context = {len(shared_doc):,} chars "
                        f"per API x {len(inventory)} APIs "
                        f"(~{len(shared_doc) // 4:,} tokens/call)\n")
        body_for = (lambda e: shared_doc
                    + f"\n\n===== TARGET =====\nWrite a snippet that calls `{e.name}`.")
        ctx = None
    else:
        ctx = _build_catalogue_context(cfg) if class_context else None
        body_for = (lambda e: _class_context_body(e, *ctx)) if ctx else (lambda e: e.body)
    # source attribution: which codebase definition each tested name targets
    # (canonical site = same election as `aideal dedup`), plus a basename→path
    # index so runtime stack frames can be mapped back to repo source lines.
    from .readme_agent import _subsume_overloads, _dedup_deprioritize
    import glob as _globmod
    _pub_details = [d for d in public_api_details(cfg) if d["visibility"] == "public"]
    _by_name_det: dict[str, list] = {}
    for _d in _pub_details:
        _by_name_det.setdefault(_d["name"], []).append(_d)
    _depri = _dedup_deprioritize(cfg)
    site_of: dict[str, dict] = {}
    for _n, _recs in _by_name_det.items():
        _mx, _ = _subsume_overloads(_recs, _depri)
        site_of[_n] = {"source": f"{_mx[0]['file']}:{_mx[0]['line']}",
                       "other_sites": len(_recs) - 1}
    file_index: dict[str, str] = {}
    for _g in list(cfg.source_globs) + [g.replace(".scala", ".java")
                                        for g in cfg.source_globs]:
        for _p in _globmod.glob(str(cfg.root / _g), recursive=True):
            file_index.setdefault(os.path.basename(_p),
                                  str(Path(_p).relative_to(cfg.root)))

    # micro-benchmark accounting (per API and per run): wall time + provider-
    # reported tokens + which model wrote/fixed. `fixer` role (fallback:
    # audience) handles attempts >0 — map `roles: fixer` (or CLI --role
    # fixer=google:gemini-2.5-pro) to benchmark a different fixer model.
    metrics: dict[str, dict] = {}
    run_t0 = _time.time()
    run_u0 = usage_snapshot()
    writer_spec = cfg.model_for_role("audience")
    fixer_spec = cfg.model_for_role("fixer")
    for entry in inventory:
        if entry.name in done_rows:      # --resume: finished in a previous run
            row = done_rows[entry.name]
            metrics[entry.name] = {k: row.get(k) for k in (
                "status", "attempts", "pass_round", "wall_s", "llm_calls",
                "input_tokens", "output_tokens", "by_model", "error_category",
                "error", "locus", "doc_chars", "document_sha256", "source",
                "source_other_sites", "codebase_frames")}
            metrics[entry.name]["evidence_fingerprint"] = row.get("experiment_fingerprint")
            per_api[entry.name] = row.get("execution_evidence") or f"resumed: {row.get('status')}"
            if row.get("status") == "pass":
                passed_n += 1
            if row.get("error_category") == "infra":
                infra_n += 1
            continue
        api_t0 = _time.time()
        api_u0 = usage_snapshot()
        work_api = work_dir / f"run_{entry.name}"
        (work_api / "classes").mkdir(parents=True, exist_ok=True)
        scala_file = work_api / str(ex.get("test_filename", "ApiTest.scala"))
        cmd = (cmd_template.replace("{scala_file}", str(scala_file))
               .replace("{test_file}", str(scala_file))
               .replace("{root}", str(cfg.root))
               .replace("{uberjar}", uberjar).replace("{jars}", jars)
               .replace("{classpath}", classpath).replace("{work}", str(work_api))
               .replace("{packages}", packages_flag)
               .replace("{repositories}", repositories_flag))

        ran = False
        last = {}
        last_run = {"stdout": "", "stderr": "", "exit_code": None}
        rounds_trace: list[dict] = []
        prev_sig, same_sig = None, 0   # stuck detector state (per API)
        import sys as _sys
        receiver = _receiver_hint(entry.name, owner_map)
        for attempt in range(1 + max_fix_rounds):
            # A condition's first attempt must be documentation-only. Historical
            # error-log feedback would leak earlier treatments into A1/A2 even
            # with max_fix_rounds=0. Only an actual retry may see failures.
            known = [] if attempt == 0 else log.failures_for(entry.name)
            try:
                snippet = _strip_fences(invoke_text(
                    writer_spec if attempt == 0 else fixer_spec,
                    *load_prompt(cfg, "aideal/comprehension_write_exec",
                                 api_body=body_for(entry), api_name=entry.name,
                                 available_inputs=available_inputs,
                                 receiver=receiver or "(receiver type not resolved)",
                                 known_failures=known or "(none yet)",
                                 execution_context=ex.get("execution_context", ""),
                                 exec_hints=ex.get("exec_hints", ""),
                                 io_hints=io_hints_text),
                ), strip_imports=strip_snippet_imports)
            except Exception as llm_exc:
                # provider error (quota/network/bad model id) must not kill a
                # 200-API run — record it as this API's failure and move on.
                cat = "llm-error"
                msg = f"{type(llm_exc).__name__}: {llm_exc}"
                last = {"cat": cat, "msg": msg, "locus": "", "code": ""}
                rounds_trace.append({"round": attempt, "status": "fail",
                                     "category": cat, "error": msg[:160]})
                _sys.stderr.write(f"  [{entry.name}] round {attempt}: FAIL [{cat}] {msg[:90]}\n")
                _sys.stderr.flush()
                log.append(run_id=run_id, step="readme-exec-test", language=cfg.language,
                           task=task, status="fail", function=entry.name,
                           error_category=cat, error=msg[:500], round=attempt)
                break
            scala = _fill_scaffold(scaffold.replace("// AIDEAL_DATA_BINDINGS", bindings)
                                   .replace("# AIDEAL_DATA_BINDINGS", bindings),
                                   snippet, region, placeholders)
            scala_file.write_text(scala, encoding="utf-8")
            try:
                # shell=True so the `scalac && jar && spark-submit` pipeline runs
                proc = subprocess.run(cmd, shell=True, cwd=work_dir, capture_output=True,
                                      text=True, timeout=timeout, env=dict(os.environ))
                out, err_out, rc = proc.stdout, proc.stderr, proc.returncode
            except subprocess.TimeoutExpired as e:
                # TimeoutExpired carries the captured streams as BYTES even with
                # text=True — concatenating raw killed the 2026-07-01 full run
                # ("can't concat str to bytes" at plotImage, ~120 APIs in).
                def _txt(b):
                    return b.decode("utf-8", "ignore") if isinstance(b, (bytes, bytearray)) else (b or "")
                out, err_out, rc = _txt(e.stdout), _txt(e.stderr) + "\n[timeout]", 124
            last_run = {"stdout": out or "", "stderr": err_out or "", "exit_code": rc}
            merged = (out or "") + "\n" + (err_out or "")
            ran = (rc == 0) and (success_marker in merged if success_marker else True) \
                and not (error_marker and error_marker in merged) \
                and (check_marker in merged if require_correctness else True)
            if ran:
                rounds_trace.append({"round": attempt, "status": "pass"})
                _sys.stderr.write(f"  [{entry.name}] round {attempt}: PASS\n"); _sys.stderr.flush()
                # record the PASSING snippet: a compiled-and-ran example is the
                # strongest grounding -> `aideal augment` folds it into the entry.
                log.append(run_id=run_id, step="readme-exec-test", language=cfg.language,
                           task=task, status="pass", function=entry.name,
                           code=snippet.strip()[:1500], round=attempt)
                # if this took a retry, also log the fix (error -> working code)
                if attempt > 0 and last:
                    log.append(run_id=run_id, step="readme-exec-test", language=cfg.language,
                               task=task, status="fixed", function=entry.name,
                               error_category=last.get("cat", ""), error=last.get("msg", ""),
                               root_cause=last.get("locus", ""), code=last.get("code", ""),
                               suggested_fix_code=snippet.strip()[:1000], round=attempt)
                break
            cat, msg, locus = _classify_error(merged, rc, error_marker,
                                              language=cfg.language)
            # coarse cat (compile/runtime/timeout) drives metrics/report; the shared
            # FIX_GUIDE adds a FINER, actionable hint (e.g. type-mismatch -> "pick the
            # geoTiff[T] that matches the raster"). Stored so failures_for replays it
            # into the next round, the same way the demo agent converges.
            from .fix_guide import classify as _classify_fix
            _, fix_hint = _classify_fix(merged)
            # ran clean but omitted the correctness witness -> tell the model exactly
            # what's missing instead of a vague "unknown" (Phase-A gate).
            if (require_correctness and rc == 0 and check_marker not in merged
                    and not (error_marker and error_marker in merged)):
                cat = "no-correctness-check"
                msg = (f"ran without a correctness check: no '{check_marker}' witness printed. "
                       f"End the snippet with require(<result non-degenerate>, ...) then "
                       f"println(\"{check_marker} {entry.name} \" + <witness>).")
                fix_hint = msg
            frames = _codebase_frames(merged, file_index)
            last = {"cat": cat, "msg": msg, "locus": locus,
                    "code": snippet.strip()[:1000], "frames": frames}
            rounds_trace.append({"round": attempt, "status": "fail", "category": cat,
                                 "error": msg[:160],
                                 **({"codebase_frames": frames} if frames else {})})
            _sys.stderr.write(f"  [{entry.name}] round {attempt}: FAIL [{cat}] {msg[:90]}\n"); _sys.stderr.flush()
            log.append(run_id=run_id, step="readme-exec-test", language=cfg.language,
                       task=task, status="fail", function=entry.name,
                       error_category=cat, error=msg, root_cause=locus,
                       code=snippet.strip()[:1000], suggested_fix_code=fix_hint,
                       round=attempt)
            # infra (missing jar) won't be fixed by rewriting the snippet — stop
            # retrying and don't spam the log with identical dependency failures.
            if cat == "infra":
                break
            sig = (cat, (msg or "")[:120])
            same_sig = same_sig + 1 if sig == prev_sig else 1
            prev_sig = sig
            if stuck_repeats and same_sig >= stuck_repeats:
                rounds_trace.append({"round": attempt, "status": "stuck-stop",
                                     "note": f"same error {same_sig}x consecutively"})
                _sys.stderr.write(f"  [{entry.name}] STUCK: same error {same_sig}x — "
                                  f"stopping fix loop\n"); _sys.stderr.flush()
                break
        if ran:
            passed_n += 1
            status = "pass" if not last else "pass (after fix)"
            per_api[entry.name] = (
                {"status": status, "rounds": rounds_trace, "code": snippet.strip(),
                 "scala_file": str(scala_file), "exit_code": last_run["exit_code"],
                 "stdout_tail": last_run["stdout"][-output_tail_chars:],
                 "stderr_tail": last_run["stderr"][-output_tail_chars:]}
                if show_code else
                ({"status": status, "rounds": rounds_trace} if len(rounds_trace) > 1 else status)
            )
        else:
            status = f"fail [{last.get('cat','?')}]: {last.get('msg','')[:140]}"
            if last.get("cat") == "infra":
                infra_n += 1
            per_api[entry.name] = (
                {"status": "fail", "rounds": rounds_trace, "error_category": last.get("cat", ""),
                 "error": last.get("msg", ""), "code": last.get("code", ""),
                 "scala_file": str(scala_file), "exit_code": last_run["exit_code"],
                 "stdout_tail": last_run["stdout"][-output_tail_chars:],
                 "stderr_tail": last_run["stderr"][-output_tail_chars:]}
                if show_code else
                ({"status": status, "rounds": rounds_trace} if len(rounds_trace) > 1 else status)
            )
        u = usage_delta(api_u0)
        metrics[entry.name] = {
            "status": "pass" if ran else "fail",
            "attempts": len(rounds_trace),
            "pass_round": next((r["round"] for r in rounds_trace
                                if r["status"] == "pass"), None),
            "wall_s": round(_time.time() - api_t0, 1),
            "llm_calls": u["calls"],
            "input_tokens": u["input_tokens"],
            "output_tokens": u["output_tokens"],
            "by_model": u["by_model"],
            "error_category": None if ran else last.get("cat", ""),
            "error": None if ran else last.get("msg", ""),
            "locus": None if ran else last.get("locus", ""),
            "doc_chars": len(shared_doc if shared_doc is not None else entry.body),
            "document_sha256": _hashlib.sha256(
                (shared_doc if shared_doc is not None else entry.body).encode("utf-8")
            ).hexdigest(),
            # which RDPro definition this API targets (canonical file:line,
            # same election as `aideal dedup`) …
            "source": site_of.get(entry.name, {}).get("source"),
            "source_other_sites": site_of.get(entry.name, {}).get("other_sites"),
            # … and which codebase lines the run actually REACHED (JVM stack
            # frames from the last failing round; empty for compile failures
            # — those never enter rdpro code; None for passes — no trace).
            "codebase_frames": (last.get("frames") or None) if not ran else None,
        }
        with ckpt.open("a", encoding="utf-8") as _ck:   # flush per API — crash-safe
            _ck.write(_json.dumps({"name": entry.name, "doc_source": doc_source,
                                   "experiment_fingerprint": experiment_fingerprint,
                                   "execution_evidence": per_api[entry.name],
                                   **metrics[entry.name]}, ensure_ascii=False) + "\n")
    n = len(inventory)
    # Doc-quality denominator excludes infra-only failures (missing-dependency runs
    # are environment noise, not documentation failures — see _classify_error). The
    # raw pass/n is kept as `score_with_infra` for transparency.
    scored_n = n - infra_n
    # Report all three denominators explicitly (no ambiguity):
    #   raw_surface       = every visible public def (regex surface)
    #   intended_surface  = surface_filter set (what gets documented)
    #   executed          = the runnable subset actually compiled/run here
    raw = public_api_surface(cfg, override_filter="all")
    intended = public_api_surface(cfg)
    covered = {e.name for e in inventory}
    return {
        "check": "comprehension",
        "mode": "execute",
        "doc_source": doc_source,
        "run": {   # micro-benchmark header: everything a condition needs to be comparable
            "run_id": run_id,
            "api_count": n,
            "manifest_api_count": manifest_inventory_n,
            "models": {"audience": f"{writer_spec.provider}:{writer_spec.model}",
                       "fixer": f"{fixer_spec.provider}:{fixer_spec.model}"},
            "max_fix_rounds": max_fix_rounds,
            "class_context": bool(class_context),
            "timeout_s": timeout,
            "wall_s": round(_time.time() - run_t0, 1),
            "usage": usage_delta(run_u0),
            "checkpoint": str(ckpt),
            "resumed_apis": len([k for k in done_rows if k in metrics]),
            "manifest_sha256": manifest_sha256,
            "document_sha256": doc_sha256,
            "experiment_fingerprint": experiment_fingerprint,
            "fingerprint_components": fingerprint_components,
            "checkpoint_reuse": reuse,
            "doc_scope": doc_scope,
        },
        "passed": bool(scored_n) and passed_n == scored_n,
        "score": round(passed_n / scored_n, 3) if scored_n else 0.0,
        "score_with_infra": round(passed_n / n, 3) if n else 0.0,
        "infra_excluded": infra_n,
        "coverage": {
            "raw_surface": len(raw),
            "intended_surface": len(intended),
            "surface_filter": cfg.surface_filter,
            "executed": n,
            "scored": scored_n,
            "infra_excluded": infra_n,
            "untested_intended": sorted(intended - covered)[:20],
        },
        # surfaced (not fatal): typed inputs whose path is missing or the wrong type.
        # A non-empty list here usually explains a run of runtime I/O failures.
        "sample_data_warnings": sample_data_warnings,
        "metrics": metrics,   # per-API: status, attempts, pass_round, wall_s, tokens, by_model
        "details": per_api,
    }


# ---------------------------------------------------------------------------
# 3. Completeness check (no LLM)
# ---------------------------------------------------------------------------

def _normalize(name: str) -> str:
    return re.sub(r"\[.*\]$", "", name).strip("`")


def completeness_check(cfg: AidealConfig) -> dict:
    surface = public_api_surface(cfg)                       # intended-API set
    raw = public_api_surface(cfg, override_filter="all")    # raw discovered surface
    documented = {_normalize(e.name) for e in parse_readme(cfg.llm_readme)}
    undocumented = sorted(surface - documented)
    n = len(surface)
    return {
        "check": "completeness",
        "passed": not undocumented,
        "score": round((n - len(undocumented)) / n, 3) if n else 0.0,
        "details": {
            "raw_surface": len(raw),               # every visible public def
            "intended_surface": n,                 # surface_filter set = denominator
            "surface_filter": cfg.surface_filter,
            "public_functions": n,                 # (= intended_surface; kept for back-compat)
            "documented": len(documented),
            "undocumented": undocumented,
            "orphan_doc_entries": sorted(documented - surface),
        },
    }


# ---------------------------------------------------------------------------
# 4. Puzzle check with fix loop
# ---------------------------------------------------------------------------

def puzzle_check(
    cfg: AidealConfig,
    dry_run: bool = False,
    *,
    doc_source: str = "aideal",
    api_doc: str | None = None,
    bank: str | None = None,
    sample_data: str | None = None,
    plan_path: str | None = None,
    plan_out: str | None = None,
    mode: str | None = None,
    case_ids: list[str] | None = None,
    sample: int | None = None,
    seed: int | None = None,
    tag: str | None = None,
    memory: str | None = None,
) -> dict:
    """Run an application-provided puzzle evaluator on a frozen AIDEAL plan.

    The runner remains application-owned, but AIDEAL owns the experimental
    controls: documentation arm, stable case selection, fixture hashes, model,
    and run label.  Legacy projects with only ``puzzle.command`` continue to
    work without a bank or plan.
    """
    import hashlib
    import json as _json
    import os
    from pathlib import Path

    from .puzzle_bank import (
        freeze_puzzle_plan,
        load_structured,
        verify_plan_inputs,
        write_plan,
    )

    def _path(value: str) -> Path:
        p = Path(value)
        return p.resolve() if p.is_absolute() else (cfg.root / p).resolve()

    def _doc_path() -> Path:
        if api_doc:
            result = _path(api_doc)
            if not result.is_file():
                raise FileNotFoundError(f"puzzle documentation not found: {result}")
            return result
        if doc_source == "aideal":
            if not cfg.llm_readme.is_file():
                raise FileNotFoundError(f"generated documentation not found: {cfg.llm_readme}")
            return cfg.llm_readme
        parts: list[str] = []
        if doc_source in ("original", "original+aideal"):
            original = cfg.original_readme_text(limit=None)
            if not original.strip():
                raise FileNotFoundError("no configured original documentation for puzzle arm")
            parts.append(original)
        if doc_source == "original+aideal":
            parts.append("===== GENERATED AIDEAL DOCUMENTATION =====\n"
                         + cfg.llm_readme.read_text(encoding="utf-8", errors="ignore"))
        destination = cfg.root / ".aideal_exec" / "puzzle_docs" / f"{doc_source}.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("\n\n".join(parts), encoding="utf-8")
        return destination

    def _sha(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    pz = cfg.puzzle
    cmd_template = pz.get("command", "")
    if not cmd_template:
        return {"check": "puzzle", "passed": False, "score": 0.0,
                "details": {"error": "no puzzle.command configured"}}
    selected_seed = int(seed if seed is not None else pz.get("seed", 42))
    selected_doc = _doc_path()
    frozen_plan: dict | None = None
    selected_plan: Path | None = None
    selected_mode = mode or "composition"
    if plan_path:
        selected_plan = _path(plan_path)
        frozen_plan = load_structured(selected_plan)
        plan_mode = str(frozen_plan.get("mode", "composition"))
        if mode is not None and mode != plan_mode:
            return {"check": "puzzle", "passed": False, "score": 0.0,
                    "details": {"error": f"--mode {mode} disagrees with frozen plan mode {plan_mode}",
                                "plan": str(selected_plan)}}
        selected_mode = plan_mode
        drift = verify_plan_inputs(frozen_plan)
        if drift:
            return {"check": "puzzle", "passed": False, "score": 0.0,
                    "details": {"error": "frozen plan input drift", "issues": drift,
                                "plan": str(selected_plan)}}
    else:
        bank_value = bank or pz.get("test_bank")
        data_value = sample_data or pz.get("sample_data")
        if bank_value or data_value:
            if not bank_value or not data_value:
                return {"check": "puzzle", "passed": False, "score": 0.0,
                        "details": {"error": "both puzzle test bank and sample data are required"}}
            from .readme_agent import parse_readme
            frozen_plan = freeze_puzzle_plan(
                root=cfg.root,
                bank_path=_path(str(bank_value)),
                sample_data_path=_path(str(data_value)),
                mode=selected_mode,
                case_ids=case_ids,
                sample=sample,
                seed=selected_seed,
                documented_apis={entry.name for entry in parse_readme(cfg.llm_readme)},
            )
            selected_plan = (_path(plan_out) if plan_out else
                             cfg.root / ".aideal_exec" / "puzzle_plans" /
                             f"{selected_mode}_seed{selected_seed}.json")
            write_plan(frozen_plan, selected_plan)

    model = cfg.model_for_role("audience")
    run_tag = tag or f"{doc_source}_{selected_mode}"
    work_dir = _path(str(pz.get("work_dir", "results/puzzle_runs")))
    runner_args = pz.get("runner_args") or []
    if isinstance(runner_args, str):
        runner_args = shlex.split(runner_args)
    rendered_runner_args = " ".join(shlex.quote(str(item)) for item in runner_args)
    scaffold = _path(str(pz.get("scaffold", "../../grail-agent/outputs/generated_scala/job_scaffold.scala")))
    guide_value = str(pz.get("guide", "")).strip()
    guide = _path(guide_value) if guide_value else None
    values = {
        "python": shlex.quote(sys.executable),
        "llm_readme": shlex.quote(str(cfg.llm_readme)),
        "api_doc": shlex.quote(str(selected_doc)),
        "test_bank": shlex.quote(str(_path(str(bank or pz.get('test_bank', '.'))))),
        "sample_data": shlex.quote(str(_path(str(sample_data or pz.get('sample_data', '.'))))),
        "plan": shlex.quote(str(selected_plan)) if selected_plan else "",
        "work_dir": shlex.quote(str(work_dir)),
        "mode": shlex.quote(selected_mode),
        "tag": shlex.quote(run_tag),
        "provider": shlex.quote(model.provider),
        "model": shlex.quote(model.model),
        "scaffold": shlex.quote(str(scaffold)),
        "guide": shlex.quote(str(guide)) if guide else "",
        "runner_args": rendered_runner_args,
        "max_retries_per_section": int(pz.get("max_retries_per_section", 2)),
        "dry_run": "--dry-run" if dry_run else "",
        "n": pz.get("num_puzzles", 3),
        "k": pz.get("num_functions", 5),
        "seed": selected_seed,
    }
    cmd = cmd_template.format(**values)
    if dry_run and "{dry_run}" not in cmd_template:
        cmd += " --dry-run"

    notes = NotesToSelf(cfg.notes_to_self)
    log = ErrorLog(cfg.error_log)
    rounds = []
    max_rounds = 1 if dry_run else 1 + int(pz.get("max_fix_rounds", 0))
    memory_enabled = (memory or str(pz.get("memory", "on"))).lower() == "on"
    for rnd in range(max_rounds):
        env = dict(os.environ)
        env.pop("PUZZLE_HINTS", None)
        hints = ("\n\n".join(x for x in (notes.to_prompt(), log.to_prompt()) if x)
                 if memory_enabled else "")
        if hints:
            hint_path = cfg.error_log.parent / "puzzle_hints.txt"
            hint_path.parent.mkdir(parents=True, exist_ok=True)
            hint_path.write_text(hints, encoding="utf-8")
            env["PUZZLE_HINTS"] = str(hint_path)
        run_cwd = (cfg.root / pz.get("cwd", ".")).resolve()
        proc = subprocess.run(shlex.split(cmd), cwd=run_cwd,
                              capture_output=True, text=True, env=env)
        report_summary = None
        report_match = re.search(r"^report:\s*(.+puzzle_report\.json)\s*$", proc.stdout, re.M)
        if report_match:
            report_file = Path(report_match.group(1).strip())
            try:
                report_summary = _json.loads(report_file.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                report_summary = None
        rounds.append({"round": rnd, "exit_code": proc.returncode,
                       "stdout_tail": proc.stdout[-2000:],
                       "stderr_tail": proc.stderr[-2000:],
                       "report": report_summary})
        if proc.returncode == 0:
            break
        notes.distill(log)  # consolidate before the next fix round
    ok = rounds[-1]["exit_code"] == 0
    scored = [round_["report"].get("readiness_score") for round_ in rounds
              if isinstance(round_.get("report"), dict)
              and round_["report"].get("readiness_score") is not None]
    return {"check": "puzzle", "passed": ok,
            "score": (None if dry_run else
                      (scored[-1] if scored else (1.0 if ok else 0.0))),
            "details": {
                "dry_run": dry_run,
                "command": cmd,
                "rounds": rounds,
                "doc_source": doc_source,
                "api_doc": str(selected_doc),
                "api_doc_sha256": _sha(selected_doc),
                "api_doc_bytes": selected_doc.stat().st_size,
                "plan": str(selected_plan) if selected_plan else None,
                "case_ids": frozen_plan.get("case_ids", []) if frozen_plan else [],
                "mode": selected_mode,
                "tag": run_tag,
                "memory": "on" if memory_enabled else "off",
                "model": {"provider": model.provider, "model": model.model},
            }}
