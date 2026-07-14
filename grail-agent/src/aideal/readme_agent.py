"""LLM_readme.md: find, parse, or create the LLM-facing README.

AIDEAL owns the doc format. Each API entry:

    ## API Test: `name`
    ### Goal
    ### Valid Call Patterns (or Valid Access Patterns)
    ### LLM Instruction Prompt
    ### Prompt Snippet
    ### Common Failure Modes
    ### Fix Code Hint

`find_or_create` looks for the configured LLM readme; if missing it scans the
codebase's public API surface and writes a skeleton (optionally filled by the
AUTHOR model with --generate).
"""

from __future__ import annotations

import glob as globmod
import re
from dataclasses import dataclass
from pathlib import Path

from .config import AidealConfig

API_HEADER_RE = re.compile(r"^## API Test: `([^`]+)`\s*$", re.MULTILINE)


@dataclass
class ApiEntry:
    name: str
    goal: str
    snippet: str
    body: str


def _section_between(body: str, header: str) -> str:
    m = re.search(rf"^### {re.escape(header)}\s*$(.*?)(?=^###? |\Z)", body, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def parse_readme(path: Path) -> list[ApiEntry]:
    if not path.exists():
        return []  # stage-0 codebases have no LLM readme yet
    text = path.read_text(encoding="utf-8", errors="ignore")
    matches = list(API_HEADER_RE.finditer(text))
    entries = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        entries.append(ApiEntry(
            name=m.group(1),
            goal=_section_between(body, "Goal"),
            snippet=_section_between(body, "Prompt Snippet"),
            body=body,
        ))
    return entries


def _replace_section(block: str, header: str, content: str) -> str:
    """Replace the content under `### {header}` (up to the next ### or block end).
    Appends the section if it isn't present."""
    pat = re.compile(rf"(###\s+{re.escape(header)}\s*\n)(.*?)(?=\n###\s|\Z)", re.DOTALL)
    if pat.search(block):
        return pat.sub(lambda m: m.group(1) + content.rstrip() + "\n", block, count=1)
    return block.rstrip() + f"\n\n### {header}\n{content}\n"


def _section_has_code(block: str, header: str) -> bool:
    """True if the `### {header}` section already holds a REAL fenced code example —
    a ``` block whose content isn't just the skeleton `TODO` placeholder. Drives
    augment's `only_missing` gap-fill: backfill ONLY entries lacking example/fix code,
    leaving curated or already-generated code untouched."""
    body = _section_between(block, header)
    if not body:
        return False
    for m in re.finditer(r"```[^\n]*\n(.*?)```", body, re.DOTALL):
        inner = m.group(1).strip()
        if inner and not inner.upper().startswith("TODO"):
            return True
    return False


def _recency_key(e: dict) -> str:
    """Sort key for 'newest wins'. Use run_id first: it is set on EVERY entry and
    has one consistent, lexically-sortable format (%Y%m%d-%H%M%SZ). The newer ISO
    `timestamp` field is absent on legacy rows and, being a different string shape,
    would sort inconsistently against run_id if the two were mixed — so run_id is
    the reliable ordering key and [-1] is truly the most recent."""
    return e.get("run_id") or e.get("timestamp") or ""


def _is_stale(e: dict, current_version: str) -> bool:
    """A memory entry is stale when it was recorded against a DIFFERENT code
    version than the one we're documenting now. Entries with no version tag
    (legacy rows) can't be proven stale, so they're kept."""
    v = (e.get("library_version") or "").strip()
    return bool(current_version) and bool(v) and v != current_version


def _fresh(entries: list[dict], current_version: str) -> list[dict]:
    """Drop version-mismatched entries, then sort oldest->newest so callers can
    take [-1] as the freshest trustworthy one. This is the staleness guard for
    promoting a verified example: without it, a `pass` snippet from three commits
    ago could be promoted as the current call pattern purely because it was the
    last line appended to the log."""
    return sorted((e for e in entries if not _is_stale(e, current_version)), key=_recency_key)


def _augment_block(block: str, fails: list[dict], only_missing: bool = False,
                   current_version: str = "") -> tuple[str, list[str]]:
    """Rewrite one entry from real log rows: Common Failure Modes + Fix Code Hint
    from failures, and a `Verified Example` from the latest PASSING execution — a
    compiled-and-ran snippet, the strongest possible grounding for the entry.

    `only_missing=True` = GAP-FILL: write the verified example / fix-hint code ONLY
    when the entry doesn't already have that code (so generated/curated examples are
    preserved). Common Failure Modes is always refreshed from the log either way.
    Returns (new_block, sections_added) where sections_added ⊆ {"example", "fix"}."""
    added: list[str] = []
    # verified example: the most recent snippet that compiled AND ran (status=pass
    # rows carry the working snippet in `code`). A proven example beats a written
    # one, so PROMOTE it into Valid Call Patterns.
    passed = _fresh([e for e in fails if e.get("status") == "pass" and e.get("code")], current_version)
    if passed and not (only_missing and _section_has_code(block, "Valid Call Patterns")):
        _p = passed[-1]
        _src = _p.get("library_version") or _p.get("timestamp") or "unversioned"
        block = _replace_section(
            block, "Valid Call Patterns",
            f"```\n{_p['code'].strip()}\n```\n_(verified: compiled + ran via `comprehension --execute` / probe; source @ {_src})_")
        added.append("example")
    seen: dict[tuple, int] = {}
    for e in fails:
        if e.get("status") == "fail":
            raw = (e.get("error", "") or "").strip().splitlines()[0] if e.get("error") else ""
            raw = re.sub(r"^\S+\.\w+:\d+:\s*", "", raw)   # drop "/path/File.scala:NN:"
            key = (e.get("error_category", "") or "error", raw[:200])
            seen[key] = seen.get(key, 0) + 1
    lines = [f"- **[{cat}]** {msg}" + (f" _(seen {n}x)_" if n > 1 else "")
             for (cat, msg), n in sorted(seen.items(), key=lambda kv: -kv[1])[:6]]
    cfm = "\n".join(lines) if lines else "- (no failures observed yet)"
    # prefer a real working fix (status=fixed); else fall back to any fix hint
    fixed = _fresh([e for e in fails if e.get("status") == "fixed" and e.get("suggested_fix_code")], current_version)
    real_fix = None
    if fixed:
        real_fix = ("Observed working code (from the fix loop):\n\n```scala\n"
                    + fixed[-1]["suggested_fix_code"].strip() + "\n```")
    else:
        hints = [e.get("suggested_fix_code", "").strip() for e in fails
                 if e.get("suggested_fix_code", "").strip()]
        if hints:
            real_fix = hints[-1]
    # Common Failure Modes is observational, not code — always refresh it from the log.
    block = _replace_section(block, "Common Failure Modes", cfm)
    # Fix Code Hint: in only_missing mode write ONLY real fix code into an entry that
    # lacks it (never overwrite existing code, never fill with the "no fix yet" stub).
    if only_missing:
        if real_fix and not _section_has_code(block, "Fix Code Hint"):
            block = _replace_section(block, "Fix Code Hint", real_fix)
            added.append("fix")
    else:
        block = _replace_section(
            block, "Fix Code Hint",
            real_fix or "- No confirmed fix yet; avoid the failures above.")
        if real_fix:
            added.append("fix")
    return block, added


def _grounding_tiers(cfg: AidealConfig):
    """Per readme entry, most to least trustworthy:
      verified (doc-derived code compiled AND ran) > grounded (direct test) >
      sibling (a tested method on the same class shows the pattern) > guessed.
    Returns (tiers{name->tier}, class_of{name->class}, test_index)."""
    import os as _os
    details = {d["name"]: d for d in public_api_details(cfg)}
    class_of = {n: (_os.path.basename(details[n].get("file", ""))[:-6]
                    if details[n].get("file", "").endswith(".scala") else "")
                for n in details}
    names = [e.name for e in parse_readme(cfg.llm_readme)]
    test_index = api_test_examples(cfg)
    exec_status = _exec_status_map(cfg)
    tested_classes = {class_of.get(n) for n, ex in test_index.items() if ex and class_of.get(n)}
    tiers = {}
    for n in names:
        if exec_status.get(n) == "pass":              # proven end-to-end in this harness
            tiers[n] = "verified"
        elif test_index.get(n):
            tiers[n] = "grounded"
        elif class_of.get(n) and class_of.get(n) in tested_classes:
            tiers[n] = "sibling"
        else:
            tiers[n] = "guessed"
    return tiers, class_of, test_index


def _exec_status_map(cfg: AidealConfig) -> dict:
    """function -> MOST RECENT execution outcome (pass/fail) from error_log.jsonl.

    error_log.jsonl is append-only, so file order IS chronological. Scan in that
    order and ALWAYS overwrite, so a later failure correctly downgrades an earlier
    pass.

    Fixes the sticky-pass bug: the old `setdefault` branch meant that once a
    function was marked pass, no subsequent fail could downgrade it — e.g.
    `zonalStatsLocal` stayed badged "verified" in readme_index.md while failing
    every recent run. `fixed` (a retry that produced working code) counts as pass;
    any other status does not overwrite a real pass/fail outcome."""
    from .error_log import ErrorLog
    st: dict[str, str] = {}
    for e in ErrorLog(cfg.error_log).entries():
        fn = e.get("function", "")
        if not fn:
            continue
        s = e.get("status", "")
        if s in ("pass", "fixed"):
            st[fn] = "pass"
        elif s == "fail":
            st[fn] = "fail"
    return st


def grounding_report(cfg: AidealConfig, annotate: bool = False) -> dict:
    """Which readme entries are TRUSTWORTHY vs SIBLING-backed vs GUESSED."""
    tiers, class_of, test_index = _grounding_tiers(cfg)
    if not tiers:
        return {"error": "no LLM_readme entries — run `aideal readme --generate`"}
    exec_status = _exec_status_map(cfg)
    counts = {"verified": 0, "grounded": 0, "sibling": 0, "guessed": 0}
    for t in tiers.values():
        counts[t] += 1
    total = len(tiers)
    guessed_fail = sorted(n for n, t in tiers.items() if t == "guessed" and exec_status.get(n) == "fail")
    out = {
        "total": total,
        "verified": counts["verified"], "grounded": counts["grounded"],
        "sibling_grounded": counts["sibling"], "guessed": counts["guessed"],
        "trusted_pct": round(100 * (counts["verified"] + counts["grounded"]) / total, 1),
        "guessed_that_failed_execution": guessed_fail[:40],
        "note": "verified = doc-derived code compiled AND ran (strongest); grounded = direct test; "
                "sibling = tested method on same class; guessed = signature-only (verify by execution).",
    }
    if annotate:
        badge = {"verified": "VERIFIED — doc-derived code compiled and ran via comprehension --execute.",
                 "grounded": "test-backed — usage mined from a real, passing test.",
                 "sibling": "sibling-grounded — a tested method on the same class shows the pattern.",
                 "guessed": "GUESSED — no test; generated from the signature only. Verify by execution."}
        text = cfg.llm_readme.read_text(encoding="utf-8")
        matches = list(API_HEADER_RE.finditer(text))
        parts = [text[:matches[0].start()]] if matches else [text]
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            block = text[m.start():end]
            if "_Grounding:" not in block:
                marker = f"_Grounding: {badge.get(tiers.get(m.group(1), 'guessed'))}_"
                hdr, _, rest = block.partition("\n")
                block = f"{hdr}\n{marker}\n{rest}"
            parts.append(block)
        cfg.llm_readme.write_text("".join(parts), encoding="utf-8")
        out["annotated"] = True
    return out


def organize_report(cfg: AidealConfig, write_index: bool = False) -> dict:
    """Axis 1+2 curation: group intended APIs by defining class, rank each by
    robustness (grounded > sibling > guessed, tie-broken by execution outcome),
    and mark the most robust `primary` per group so the agent reaches for it.
    Optionally writes a categorized, robust-first `docs/readme_index.md`."""
    from collections import defaultdict
    tiers, class_of, _ = _grounding_tiers(cfg)
    if not tiers:
        return {"error": "no LLM_readme entries — run `aideal readme --generate`"}
    exec_status = _exec_status_map(cfg)
    trank = {"verified": 0, "grounded": 1, "sibling": 2, "guessed": 3}
    erank = {"pass": 0, "": 1, "fail": 2}
    cats = defaultdict(list)
    for n, t in tiers.items():
        cats[class_of.get(n) or "(unknown)"].append((n, t, exec_status.get(n, "")))
    result = {}
    for cls, items in cats.items():
        items.sort(key=lambda it: (trank[it[1]], erank.get(it[2], 1), it[0]))
        result[cls] = {"primary": items[0][0], "count": len(items),
                       "apis": [{"name": n, "tier": t, "exec": ex or "not-run"} for n, t, ex in items]}
    counts = {"verified": 0, "grounded": 0, "sibling": 0, "guessed": 0}
    for t in tiers.values():
        counts[t] += 1
    summary = {"total": len(tiers), "categories": len(result), **counts}
    if write_index:
        badge = {"verified": "★", "grounded": "✅", "sibling": "🟡", "guessed": "⚠️"}
        L = [f"# {cfg.project_name} — organized API index", "",
             f"{counts['verified']} verified · {counts['grounded']} grounded · "
             f"{counts['sibling']} sibling · {counts['guessed']} guessed · {len(result)} categories", "",
             "Legend: ★ verified (compiled + ran) · ✅ grounded (direct test) · 🟡 sibling-grounded · "
             "⚠️ guessed (verify by execution). **primary** = most robust in its group.", ""]
        for cls in sorted(result):
            L.append(f"## {cls}")
            for a in result[cls]["apis"]:
                star = " **(primary)**" if a["name"] == result[cls]["primary"] else ""
                ex = f" · exec {a['exec']}" if a["exec"] != "not-run" else ""
                L.append(f"- {badge[a['tier']]} `{a['name']}` — {a['tier']}{ex}{star}")
            L.append("")
        idx = cfg.llm_readme.parent / "readme_index.md"
        idx.write_text("\n".join(L), encoding="utf-8")
        summary["index"] = str(idx)
    return {"summary": summary,
            "categories_sample": {k: {"primary": v["primary"], "count": v["count"]}
                                  for k, v in sorted(result.items())[:12]}}


_TIER_BADGE = {"verified": "★", "grounded": "✅", "sibling": "🟡", "guessed": "⚠️"}
_TIER_RANK = {"verified": 0, "grounded": 1, "sibling": 2, "guessed": 3}
_EXEC_RANK = {"pass": 0, "": 1, "fail": 2}


def _safe_filenames(gkey_label: dict[str, str]) -> dict[str, str]:
    """Map each group key -> a UNIQUE, filesystem-safe filename stem. Start from the
    human label (simple class name); when two groups sanitize to the same name (the
    general collision: same simple name in different packages, so two DISTINCT class
    files), disambiguate deterministically with trailing key segments, then a short
    stable hash as a last resort. No collision (e.g. RDPro) -> filename == label, so
    output is byte-identical to before."""
    import collections as _c
    import hashlib as _h
    san = lambda s: re.sub(r"[^\w.-]", "_", s)
    desired = {g: san(lbl) for g, lbl in gkey_label.items()}
    dup = {n for n, c in _c.Counter(desired.values()).items() if c > 1}
    out: dict[str, str] = {}
    used: set[str] = set()
    for g in sorted(gkey_label):                       # deterministic assignment order
        name = desired[g]
        if name in dup:                                # qualify with nearest parent segment(s)
            parts = [p for p in re.split(r"[/\\.]", g) if p]
            name = san(".".join(parts[-2:])) if len(parts) >= 2 else name
            while name in used:                        # last resort: stable content hash
                name = f"{desired[g]}-{_h.sha1(g.encode()).hexdigest()[:6]}"
        out[g] = name
        used.add(name)
    return out


def _catalogue_model(entries, tiers: dict, exec_status: dict, class_of: dict, owner: dict,
                     file_of: dict | None = None) -> dict:
    """Pure/testable: group README entries by defining class, rank each class's
    members the SAME way organize_report does (tier, then execution outcome, then
    name), pick the primary, and take the class purpose from the primary's Goal (no
    new LLM call). Returns {group_key: {label, safe, primary, purpose, kind,
    members:[{name,tier,exec}]}}.

    file_of {name -> source file path}: when given, classes are grouped by their
    DEFINING FILE (collision-safe: two same-named classes in different packages stay
    separate) and each group carries a human `label` + a unique `safe` filename.
    Omitted -> grouping falls back to the simple class name (back-compatible)."""
    from collections import defaultdict
    import os as _os
    by_name = {e.name: e for e in entries}
    groups: dict[str, list] = defaultdict(list)
    gkey_label: dict[str, str] = {}
    for e in entries:
        f = (file_of or {}).get(e.name, "")
        if f.endswith(".scala"):
            gkey = f[:-6]                              # path stem — unique per source file
            label = _os.path.basename(gkey)
        else:
            gkey = class_of.get(e.name) or (owner.get(e.name, ("(ungrouped)",))[0] or "(ungrouped)")
            label = gkey
        groups[gkey].append(e.name)
        gkey_label[gkey] = label
    safe_of = _safe_filenames(gkey_label)
    out: dict[str, dict] = {}
    for gkey, names in groups.items():
        ranked = sorted(names, key=lambda n: (_TIER_RANK.get(tiers.get(n, "guessed"), 3),
                                              _EXEC_RANK.get(exec_status.get(n, ""), 1), n))
        primary = ranked[0]
        pg = (by_name[primary].goal or "").strip()
        if pg and not pg.upper().startswith("TODO"):
            first = pg.splitlines()[0].strip()
            purpose = first if len(first) <= 160 else first[:160].rsplit(" ", 1)[0] + "…"
        else:
            purpose = f"{len(names)} operation(s)"
        out[gkey] = {
            "label": gkey_label[gkey], "safe": safe_of[gkey],
            "primary": primary, "purpose": purpose,
            "kind": owner.get(primary, ("", "instance"))[1],
            "members": [{"name": n, "tier": tiers.get(n, "guessed"),
                         "exec": exec_status.get(n, "")} for n in ranked],
        }
    return out


def _class_context_body(entry, model: dict, name_to_gkey: dict, by_name: dict) -> str:
    """INDEX-FIRST audience context. Prepend the target API's catalogue class header
    — how to obtain the receiver + ONE verified/grounded sibling's real call pattern —
    to the API's own doc, so the audience model stops inventing the receiver / entry
    point (the ~53% `value X is not a member` / `not found: value` failure class the
    flat per-API body can't prevent). Pure/testable; returns entry.body unchanged when
    the class isn't in the model."""
    gkey = name_to_gkey.get(entry.name)
    m = model.get(gkey) if gkey else None
    if not m:
        return entry.body
    head = [f"## Class context — `{m['label']}`", f"_{m['purpose']}_", "",
            f"**Obtaining the receiver:** {_receiver_line(m['label'], m['kind'])}", ""]
    primary = m["primary"]
    if primary != entry.name:
        ptier = next((x["tier"] for x in m["members"] if x["name"] == primary), "guessed")
        if ptier in ("verified", "grounded") and primary in by_name:
            pat = _section_between(by_name[primary].body, "Valid Call Patterns")
            if pat:
                head += [f"**Proven setup from a {ptier} sibling `{primary}` — reuse its "
                         f"receiver/imports, then call `{entry.name}` instead:**", pat, ""]
    head += ["---", ""]
    return "\n".join(head) + "\n" + entry.body


def _receiver_line(cls: str, kind: str) -> str:
    return (f"static object — call `{cls}.<method>(...)`" if kind == "static"
            else f"instance — obtain a `{cls}` value, then `<value>.<method>(...)`")


def write_catalogue(cfg: AidealConfig) -> dict:
    """ADDITIVE, non-breaking: export the flat LLM_readme into the two-level shape
    (catalogue + per-class files) WITHOUT touching LLM_readme.md or the read path.

    Writes next to LLM_readme.md:
      - LLM_readme_index.md : one section per defining class -> purpose, receiver, and
                              the class's APIs with tier badges (primary marked),
                              each linking into api/<Class>.md.
      - api/<Class>.md      : the actual entries for that class's functions, headed by
                              the class purpose + how to obtain a receiver.

    Class files are named after the source class (the defining file's stem). Reuses
    the exact ranking `organize_report` computes; the rest of the pipeline keeps
    reading the flat file until the read path is switched deliberately (a later step)."""
    from .doc_checks import _owner_map
    entries = parse_readme(cfg.llm_readme)
    if not entries:
        return {"error": "no LLM_readme.md entries — run `aideal readme --generate` first"}
    tiers, class_of, _ = _grounding_tiers(cfg)
    exec_status = _exec_status_map(cfg)
    owner = _owner_map(cfg)
    file_of = {d["name"]: d["file"] for d in public_api_details(cfg)}
    model = _catalogue_model(entries, tiers, exec_status, class_of, owner, file_of=file_of)
    by_name = {e.name: e for e in entries}
    api_dir = cfg.llm_readme.parent / "api"
    api_dir.mkdir(parents=True, exist_ok=True)

    idx = [f"# {cfg.project_name} — API catalogue", "",
           f"{len(entries)} APIs across {len(model)} classes. Scan here, then open the one "
           "class file you need (each opens with how to obtain its receiver, then its methods).", "",
           "Legend: ★ verified · ✅ grounded · 🟡 sibling · ⚠️ guessed", ""]
    files = 0
    for gkey in sorted(model, key=lambda g: (model[g]["label"], g)):
        m = model[gkey]
        label, safe = m["label"], m["safe"]
        recv = _receiver_line(label, m["kind"])
        badged = [f"{_TIER_BADGE.get(x['tier'], '⚠️')} `{x['name']}`"
                  + (" **(primary)**" if x["name"] == m["primary"] else "") for x in m["members"]]
        # per-class file: header (purpose + receiver + members) then the real entries
        body = [f"# {label}", "", f"_{m['purpose']}_", "", f"**Receiver:** {recv}", "",
                "**Members** (most robust first): " + ", ".join(badged), "", "---", ""]
        for x in m["members"]:
            body.append(by_name[x["name"]].body.strip())
            body.append("")
        (api_dir / f"{safe}.md").write_text("\n".join(body), encoding="utf-8")
        files += 1
        # catalogue section
        idx += [f"## [{label}](api/{safe}.md)", f"_{m['purpose']}_",
                f"**Receiver:** {recv}", "**APIs:** " + ", ".join(badged), ""]
    idx_path = cfg.llm_readme.parent / "LLM_readme_index.md"
    idx_path.write_text("\n".join(idx), encoding="utf-8")
    return {"action": "catalogue", "classes": len(model), "apis": len(entries),
            "index": str(idx_path), "api_dir": str(api_dir), "class_files": files,
            "note": "additive export; LLM_readme.md and the read path are untouched"}


def augment_from_log(cfg: AidealConfig, dry_run: bool = False,
                     only_missing: bool = False) -> dict:
    """Fold observed failures/fixes from error_log.jsonl into each LLM_readme
    entry's `Common Failure Modes` and `Fix Code Hint` sections, plus a verified
    `Valid Call Patterns` example from a PASSING execution (augment-from-log).
    Evidence only — never invents. Safe to re-run after more comprehension/puzzle passes.

    only_missing=True = GAP-FILL: add the verified example / fix-hint code ONLY to
    entries that don't already have that code (curated/generated code is preserved;
    Common Failure Modes is still refreshed). Use it after a full
    `comprehension --execute` to backfill exactly the entries missing a proven example."""
    from .error_log import ErrorLog, git_version
    if not cfg.llm_readme.exists():
        return {"error": "no LLM_readme.md — run `aideal readme --generate` first"}
    log = ErrorLog(cfg.error_log)
    # tag for staleness: only promote verified examples recorded against the
    # CURRENT code version (mismatched ones are dropped by _fresh). '' when the
    # target isn't a git repo -> staleness falls back to timestamp recency only.
    current_version = git_version(cfg.root)
    by_fn: dict[str, list[dict]] = {}
    for e in log.entries():
        by_fn.setdefault(e.get("function", ""), []).append(e)
    if not by_fn:
        return {"action": "noop", "note": "error_log.jsonl is empty; nothing to fold in"}

    text = cfg.llm_readme.read_text(encoding="utf-8")
    matches = list(API_HEADER_RE.finditer(text))
    parts = [text[:matches[0].start()]] if matches else [text]
    updated: list[str] = []
    example_added: list[str] = []
    fix_added: list[str] = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[m.start():end]
        fails = by_fn.get(m.group(1))
        if fails:
            block, added = _augment_block(block, fails, only_missing=only_missing,
                                          current_version=current_version)
            updated.append(m.group(1))
            if "example" in added:
                example_added.append(m.group(1))
            if "fix" in added:
                fix_added.append(m.group(1))
        parts.append(block)
    new_text = "".join(parts)
    if not dry_run:
        cfg.llm_readme.write_text(new_text, encoding="utf-8")
    return {"action": "augmented" if not dry_run else "dry-run",
            "mode": "only-missing" if only_missing else "refresh",
            "path": str(cfg.llm_readme), "entries_updated": len(updated),
            "verified_examples_added": len(example_added),
            "fix_hints_added": len(fix_added),
            "example_apis": example_added[:50],
            "fix_apis": fix_added[:50],
            "note": ("gap-fill: added verified example / fix-hint code only where missing; "
                     "Common Failure Modes refreshed") if only_missing else
                    "Common Failure Modes + Fix Code Hint + verified example rewritten from error_log"}


# --- Visibility models -------------------------------------------------------
# No single rule works across languages, so each language picks one of four
# modes. `deny`  = public by default, drop defs carrying a private marker
# (Scala/Java/C++/C#/TS/Kotlin). `allow` = private by default, keep only defs
# carrying an export marker (Rust `pub`, JS `export`). `case` = exported when
# the name starts uppercase (Go). `convention` = no keyword; the universal
# `_`-prefix rule below is the only filter (Python). Override per project with a
# `codebase.visibility` block in aideal.yaml.
_VISIBILITY_DEFAULTS: dict[str, dict] = {
    "scala":      {"mode": "deny",  "private": [r"\bprivate\b", r"\bprotected\b"]},
    "java":       {"mode": "deny",  "private": [r"\bprivate\b", r"\bprotected\b"]},
    "kotlin":     {"mode": "deny",  "private": [r"\bprivate\b", r"\bprotected\b", r"\binternal\b"]},
    "typescript": {"mode": "deny",  "private": [r"\bprivate\b", r"\bprotected\b", r"#"]},
    "c#":         {"mode": "deny",  "private": [r"\bprivate\b", r"\bprotected\b", r"\binternal\b"]},
    "csharp":     {"mode": "deny",  "private": [r"\bprivate\b", r"\bprotected\b", r"\binternal\b"]},
    "c++":        {"mode": "deny",  "private": [r"\bprivate\b", r"\bprotected\b"]},
    "cpp":        {"mode": "deny",  "private": [r"\bprivate\b", r"\bprotected\b"]},
    "rust":       {"mode": "allow", "public":  [r"\bpub\b"]},
    "go":         {"mode": "case"},
    "python":     {"mode": "convention"},
    "javascript": {"mode": "convention"},
}


def visibility_model(cfg: AidealConfig) -> dict:
    """Resolve the visibility model: explicit config overrides the language default."""
    if cfg.visibility:
        return cfg.visibility
    return _VISIBILITY_DEFAULTS.get(cfg.language.lower(), {"mode": "convention"})


def _is_public(name: str, prefix: str, model: dict) -> bool:
    """`prefix` is the text on the def line BEFORE the matched name (the modifiers),
    with any NON-PUBLIC enclosing-container modifiers prepended by `_iter_defs`
    (a def inside `private[pkg] object X` is not callable from outside either)."""
    if name.startswith("_"):          # universal convention rule (Python/JS internals)
        return False
    mode = model.get("mode", "convention")
    if mode == "deny":
        return not any(re.search(p, prefix) for p in model.get("private", []))
    if mode == "allow":
        return any(re.search(p, prefix) for p in model.get("public", []))
    if mode == "case":
        return name[:1].isupper()
    return True                       # convention: only the `_` rule applies


# Container declarations for brace-scoped languages (Scala/Java/Kotlin/C#/...).
# `mods` = everything before the container keyword on that line (modifiers).
_CONTAINER_DECL_RE = re.compile(
    r"^(?P<mods>[^={}]*?)\b(?:case\s+)?(?:class|object|trait|interface|enum|record)\s+\w+")
# Scoped Scala modifiers too: `private[raptor]`, `protected[davinci]`.
_NONPUBLIC_MOD_RE = re.compile(r"\b(?:private|protected)\b(?:\[[^\]]*\])?")


def _container_context(lines: list[str]) -> list[str]:
    """Per-line NON-PUBLIC modifier text of the enclosing containers.

    ctx[i] = space-joined private/protected modifiers of every container
    enclosing line i ('' when the whole chain is public). Members of a
    `private[pkg] object Helper { ... }` are unreachable from user code even
    when the def line itself carries no modifier — the observed leak class
    (docfix not-testable verdicts: compress protected[raptor], createRings
    private[davinci]). Heuristic brace tracking; braces inside string
    literals/comments are not parsed (acceptable for surface estimation)."""
    ctx: list[str] = [""] * len(lines)
    stack: list[tuple[int, str]] = []   # (depth after the container's `{`, mods)
    depth = 0
    pending: tuple[int, str] | None = None   # container decl awaiting its `{`
    for i, line in enumerate(lines):
        ctx[i] = " ".join(m for _, m in stack if m)
        decl = _CONTAINER_DECL_RE.match(line)
        if decl:
            mods = " ".join(_NONPUBLIC_MOD_RE.findall(decl.group("mods")))
            pending = (depth, mods)
        for ch in line:
            if ch == "{":
                if pending is not None and pending[0] == depth:
                    stack.append((depth + 1, pending[1]))
                    pending = None
                else:
                    stack.append((depth + 1, ""))   # def body / match block / ...
                depth += 1
            elif ch == "}":
                depth = max(0, depth - 1)
                while stack and stack[-1][0] > depth:
                    stack.pop()
    return ctx


def _exclude_path_patterns(cfg: AidealConfig) -> list:
    """codebase.exclude_path_patterns — regexes matched against the project-
    relative POSIX path of each source file; matches are dropped from the
    surface entirely. Use for modules that are source-visible but not user
    API (e.g. a `commontest/` test-scaffolding module)."""
    pats = (cfg.raw.get("codebase", {}) or {}).get("exclude_path_patterns", []) or []
    return [re.compile(p) for p in pats]


def _iter_defs(cfg: AidealConfig):
    """Yield (name, prefix, file_path, lineno, line) for every matched def.

    `prefix` is everything on the line BEFORE the matched NAME (so modifier
    regexes see `private`/`protected`/`override` even when the project's
    def-regex is anchored at ^), with any non-public enclosing-container
    modifiers prepended. NOTE: a lookahead like `^\\s*(?!private\\b)` in the
    def regex is NOT a reliable visibility filter — `\\s*` backtracks one
    space and the lookahead passes on any indented def; visibility belongs to
    the visibility model, not the regex."""
    pattern = re.compile(cfg.public_def_regex)
    excl = _exclude_path_patterns(cfg)
    deny_mode = visibility_model(cfg).get("mode") == "deny"
    for g in cfg.source_globs:
        for path in globmod.glob(str(cfg.root / g), recursive=True):
            rel = str(Path(path).relative_to(cfg.root)).replace("\\", "/") \
                if str(path).startswith(str(cfg.root)) else str(path).replace("\\", "/")
            if any(p.search(rel) for p in excl):
                continue
            lines = Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()
            ctx = _container_context(lines) if deny_mode else None
            for i, line in enumerate(lines):
                for m in pattern.finditer(line):
                    name = m.group(1)
                    # text before the NAME (not before the whole match): the
                    # modifiers survive even under a ^-anchored project regex.
                    prefix = line[:m.start(1)]
                    if ctx is not None and ctx[i]:
                        prefix = ctx[i] + " " + prefix
                    yield name, prefix, path, i, line


_TEST_BLOCK_RE = re.compile(r'\btest\s*\(\s*"([^"]*)"\s*\)\s*\{')
_PY_TEST_DEF_RE = re.compile(r"^([ \t]*)def\s+(test_\w+)\s*\(", re.M)


def _iter_test_blocks_py(text: str):
    """pytest style: yield (test_name, body) for each `def test_*(...)`, the body
    being every following line indented deeper than the def (indentation-scoped —
    Python has no braces). Before this, test-example mining fired 0x on Python
    codebases (_TEST_BLOCK_RE is ScalaTest-only; Sedona audit 2026-07-06)."""
    import bisect
    lines = text.splitlines()
    starts, off = [], 0
    for ln in lines:
        starts.append(off)
        off += len(ln) + 1
    for m in _PY_TEST_DEF_RE.finditer(text):
        indent = len(m.group(1).expandtabs())
        i = bisect.bisect_right(starts, m.start()) - 1
        body = [lines[i]]
        for j in range(i + 1, len(lines)):
            ln = lines[j]
            if ln.strip() and (len(ln) - len(ln.lstrip(" \t"))) <= indent:
                break
            body.append(ln)
        yield m.group(2), "\n".join(body)


_JAVA_TEST_RE = re.compile(
    r"@(?:Test|ParameterizedTest)\b[\s\S]*?\b(?:void|public\s+void)\s+(\w+)\s*\([^)]*\)\s*(?:throws\s+[\w., ]+)?\{")


def _iter_test_blocks_java(text: str):
    """JUnit style: yield (method_name, body) for each @Test/@ParameterizedTest
    method (brace-balanced from its opening `{`)."""
    for m in _JAVA_TEST_RE.finditer(text):
        open_brace = text.index("{", m.end() - 1)
        depth = 0
        for k in range(open_brace, len(text)):
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
                if depth == 0:
                    yield m.group(1), text[open_brace:k + 1]
                    break


#: per-language test-block miners; default = ScalaTest-style `test("..."){}`.
#: Extend for new languages (the `tested` intent signal + example mining
#: both flow through this table).
_TEST_MINERS = {
    "python": _iter_test_blocks_py,
    "java": _iter_test_blocks_java,
}


def _test_blocks_for(cfg: AidealConfig, text: str):
    """Language-aware test-block iterator (see _TEST_MINERS)."""
    miner = _TEST_MINERS.get(cfg.language.lower(), _iter_test_blocks)
    blocks = list(miner(text))
    # graceful fallback: a Scala repo with JUnit-style tests (or vice versa)
    # still yields examples rather than silently zero.
    if not blocks and miner is not _iter_test_blocks:
        blocks = list(_iter_test_blocks(text))
    if not blocks and miner is not _iter_test_blocks_java:
        blocks = list(_iter_test_blocks_java(text))
    return blocks


def _iter_test_blocks(text: str):
    """Yield (test_name, block_text) for each `test("...") { ... }` (brace-balanced).
    Generic for *Spec/FunSuite-style tests; falls back to nothing if none match."""
    for m in _TEST_BLOCK_RE.finditer(text):
        open_brace = text.index("{", m.end() - 1)
        depth = 0
        for k in range(open_brace, len(text)):
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
                if depth == 0:
                    yield m.group(1), text[open_brace:k + 1]
                    break


def api_test_examples(cfg: AidealConfig, max_per_api: int = 2, max_chars: int = 1400) -> dict[str, list[dict]]:
    """Search the configured test files and index real usage examples by API name.
    Returns {api_name: [{file, test, code}]}. These are compiling, ground-truth
    call patterns the generator/audience can learn from."""
    if not cfg.test_globs:
        return {}
    surface = public_api_surface(cfg)
    index: dict[str, list[dict]] = {}
    for g in cfg.test_globs:
        for path in sorted(globmod.glob(str(cfg.root / g), recursive=True)):
            text = Path(path).read_text(encoding="utf-8", errors="ignore")
            rel = str(Path(path).relative_to(cfg.root))
            for tname, block in _test_blocks_for(cfg, text):
                for name in surface:
                    if len(index.get(name, [])) >= max_per_api:
                        continue
                    # match a call/use of the name: `name(` `name[` or `.name`
                    if re.search(rf"\b{re.escape(name)}\s*[\(\[]|\.{re.escape(name)}\b", block):
                        index.setdefault(name, []).append(
                            {"file": rel, "test": tname, "code": block.strip()[:max_chars]})
    return index


_SCAFFOLD_FRAME = """// AIDEAL API-test scaffold — AUTO-GENERATED from the API surface.
// Run via: spark-shell --jars <uberjar> -i <thisfile>
// spark-shell provides `sc` (SparkContext) and `spark` (SparkSession).
// The generated snippet is spliced between API_TEST_START / END and may use
// the in-scope bindings: sc, inputA, inputB, output.

{imports}

// Compiled form (scalac + spark-submit --class GeoJobMain). This is the proven
// path: an implicit class like RaptorMixin's sc.geoTiff resolves when compiled
// inside an object, but NOT in the spark-shell -i REPL.
object GeoJob {
  def run(sc: SparkContext): Unit = {
    // Alias: LLM-authored snippets frequently reach for `sparkContext` (the
    // SparkSession accessor name) rather than the harness binding `sc`. Expose
    // both so a correct call doesn't fail on the binding name alone.
    val sparkContext = sc
    // Typed sample inputs (from comprehension.execute.sample_data). Use the
    // one(s) whose type matches the API's parameters.
    // AIDEAL_DATA_BINDINGS

    // TODO API_TEST_START
    // (generated snippet inserted here)
    // TODO API_TEST_END
  }
}

object GeoJobMain {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName("ApiTest").master("local[*]").getOrCreate()
    try {
      GeoJob.run(spark.sparkContext)
      println("__DONE__ object=GeoJob")
    } catch {
      case t: Throwable =>
        Console.err.println("__RUN_ERR__ " + t.getClass.getName + ": " + t.getMessage)
        t.printStackTrace()
    } finally {
      spark.stop()
    }
  }
}
"""

# Always-needed runtime imports the source files may not declare themselves.
_SCAFFOLD_BASE_IMPORTS = [
    "import org.apache.spark.SparkContext",
    "import org.apache.spark.sql.{SparkSession, DataFrame, Row}",
    "import org.apache.spark.rdd.RDD",
]


def _available_packages(cfg: AidealConfig) -> set[str]:
    """Packages actually present in the jars the scaffold compiles against
    (comprehension.execute.jars + uberjar). Used to drop wildcard imports for
    packages not on the classpath (e.g. internal `jhdf`) that break compilation."""
    import zipfile
    ex = (cfg.comprehension or {}).get("execute", {}) if cfg.comprehension else {}
    jar_globs = []
    if ex.get("jars"):
        jar_globs.append(str(ex["jars"]))
    if ex.get("uberjar"):
        bc = cfg.root / ex.get("build_cwd", ".")
        jar_globs.append(str(bc / ex["uberjar"]))
    jars = []
    for jg in jar_globs:
        jars += globmod.glob(jg if jg.startswith("/") else str(cfg.root / jg))
    # also the Spark jars (on the compile classpath) so org.apache.spark.* survives
    try:
        import os as _os
        import pyspark as _pyspark
        jars += globmod.glob(_os.path.join(_os.path.dirname(_pyspark.__file__), "jars", "*.jar"))
    except Exception:
        pass
    pkgs: set[str] = set()
    for jar in jars:
        try:
            for n in zipfile.ZipFile(jar).namelist():
                if n.endswith(".class") and "/" in n:
                    pkgs.add(n.rsplit("/", 1)[0].replace("/", "."))
        except Exception:
            continue
    return pkgs


def _import_package(imp: str) -> str:
    """The enclosing PACKAGE an import resolves against — i.e. exactly what must be on
    the compile classpath for it to resolve. Relies on the Scala/Java convention that
    package segments are lowercase and type/object segments are Uppercase: the package
    is the leading run of segments before the first Uppercase (type/object) segment.
    This is what makes the classpath check correct for BOTH shapes that look identical
    syntactically:
      import edu...dynoviz.raptorhunt.Rectangle          -> package edu...dynoviz.raptorhunt
      import edu...beast.cg.SpatialDataTypes.RasterRDD    -> package edu...beast.cg
        (`SpatialDataTypes` is an OBJECT, `RasterRDD` a type member — the real package
         stops at `cg`, so a member-of-object import isn't mistaken for a missing pkg)
    Wildcards and brace groups reduce to their package the same way:
      import a.b.c._            -> a.b.c
      import a.b.c.Obj._        -> a.b.c
      import a.b.{X, Y}         -> a.b
    A checker that instead accepted ANY ancestor would wrongly keep
    `org.apache.spark.test.ScalaSparkTest` (ancestor `org.apache.spark` is present) even
    though package `org.apache.spark.test` ships no classes — the bug this replaces."""
    path = imp[len("import "):].strip() if imp.startswith("import ") else imp.strip()
    if "{" in path:                       # import a.b.{X, Y} -> drop the brace group
        path = path[:path.index("{")].rstrip(".")
    elif path.endswith("._"):             # wildcard -> drop the trailing ._
        path = path[:-2]
    pkg: list[str] = []
    for seg in path.split("."):
        if seg[:1].isupper():             # first Uppercase segment = type/object -> stop
            break
        pkg.append(seg)
    return ".".join(pkg)


def _on_classpath(imp: str, avail: set[str]) -> bool:
    """True iff the import's enclosing package is present in the compile jars. `avail`
    is derived from the SAME jars scalac compiles against, so this keeps exactly the
    imports that resolve and drops exactly the ones that raise
    `object X is not a member of package Y` — e.g. source-tree-only modules (`dynoviz`,
    `test`) that are indexed from source but never shipped in the runtime jars. Callers
    skip the filter entirely when `avail` is empty (jars unresolved), so behavior is
    unchanged when the classpath can't be determined."""
    pkg = _import_package(imp)
    return bool(pkg) and pkg in avail


_TEST_FRAMEWORK_IMPORT = re.compile(
    r"scalatest|junit|scalatestplus|ScalaSparkTest|mockito|\.mock|RunWith|"
    r"AnyFunSuite|BeforeAndAfter|TestName", re.IGNORECASE)


def _imports_from_tests(cfg: AidealConfig) -> list[str]:
    """Robust import block: the SPECIFIC imports the test suite already uses to
    exercise the APIs — real, compiling, and made COLLISION-FREE. Braced imports
    are expanded to one-per-name; any simple name that resolves to two different
    paths (e.g. two `ByteArrayOutputStream`s) is DROPPED, since including both
    would make scalac ambiguous. Test-framework imports are filtered out."""
    from collections import defaultdict
    imp_re = re.compile(r"^\s*import\s+(\S.*?)\s*$", re.MULTILINE)
    raw: set[str] = set()
    for g in cfg.test_globs:
        for p in globmod.glob(str(cfg.root / g), recursive=True):
            txt = Path(p).read_text(encoding="utf-8", errors="ignore")
            for m in imp_re.finditer(txt):
                t = m.group(1).strip()
                if t and not _TEST_FRAMEWORK_IMPORT.search(t):
                    raw.add(t)
    wildcards: list[str] = []
    by_name: dict[str, set[str]] = defaultdict(set)   # simple name -> {full import}
    for t in raw:
        if t.endswith("._"):                          # package/object wildcard
            wildcards.append(f"import {t}")
        elif "{" in t and t.endswith("}"):            # expand braces to one-per-name
            pkg = t[:t.index("{")]
            for nm in t[t.index("{") + 1:t.rindex("}")].split(","):
                nm = nm.strip()
                if not nm:
                    continue
                simple = nm.split("=>")[-1].strip()   # renamed import: keep the alias
                by_name[simple].add(f"import {pkg}{nm}")
        else:
            by_name[t.rsplit('.', 1)[-1]].add(f"import {t}")
    out = list(dict.fromkeys(wildcards))
    for simple, imps in by_name.items():
        if len(imps) == 1:                            # unambiguous -> keep
            out.append(next(iter(imps)))
        # else: same simple name from >1 path -> drop (would be ambiguous)
    # drop imports whose package isn't on the compile classpath (a test-only dep
    # would fail scalac). Skipped when jars aren't configured/resolvable.
    avail = _available_packages(cfg)
    if avail:
        out = [i for i in out if _on_classpath(i, avail)]
    return sorted(set(out))


def _pkgobject_reexported_wildcards(cfg: AidealConfig) -> dict[str, set[str]]:
    """Auto-detect wildcard imports made REDUNDANT (and thus ambiguous) by a Scala
    package object. `package object X extends A with B` means `import <path>.X._`
    already brings A's/B's implicit classes into scope; a SECOND wildcard
    `import <pathA>.A._` re-introduces the same implicit at equal priority, so
    Scala can no longer disambiguate and the conversion silently stops resolving
    (the `sc.shapefile is not a member` class of bug).

    Returns `{package-object wildcard -> {redundant mixin wildcards it re-exports}}`
    so the caller can drop the mixin wildcards ONLY when the package-object
    wildcard is actually present (dropping them otherwise would delete implicits a
    codebase legitimately imports the narrow way). General: works for any codebase
    that fronts its implicits with a package object — no per-conflict config."""
    out: dict[str, set[str]] = {}
    pkg_re = re.compile(r"^\s*package\s+([\w.]+)\s*$", re.MULTILINE)
    obj_re = re.compile(r"package\s+object\s+(\w+)\s+extends\s+(.+?)(?:\{|\n\s*\n|\Z)", re.DOTALL)
    imp_named = re.compile(r"^\s*import\s+([\w.]+)\.(\w+)\s*$", re.MULTILINE)
    for g in cfg.source_globs:
        for path in globmod.glob(str(cfg.root / g), recursive=True):
            text = Path(path).read_text(encoding="utf-8", errors="ignore")
            mo = obj_re.search(text)
            if not mo:
                continue
            pm = pkg_re.search(text)
            if not pm:
                continue
            pkg_path = f"{pm.group(1)}.{mo.group(1)}"          # e.g. edu...beast
            # resolve each mixed-in trait's simple name to a full import path using
            # this file's own imports (traits with no import share the package and
            # can't collide via a *different* wildcard, so skipping them is safe).
            named = {simple: f"{owner}.{simple}" for owner, simple in imp_named.findall(text)}
            mixins: set[str] = set()
            for part in re.split(r"\bwith\b", mo.group(2)):
                m = re.match(r"\s*([\w.]+)", part)
                if not m:
                    continue
                full = named.get(m.group(1).split(".")[-1])
                if full and full != pkg_path:
                    mixins.add(f"import {full}._")
            if mixins:
                out.setdefault(f"import {pkg_path}._", set()).update(mixins)
    return out


def _source_symbol_index(cfg: AidealConfig) -> dict[str, str]:
    """Index PUBLIC, top-level type/object declarations across the source tree:
    `{SimpleName -> "import pkg.Name"}`. Top-level = declared at column 0 (Scala
    convention), which also excludes nested and private/protected declarations
    (their line starts with indentation or `private`/`protected`, so the anchored
    pattern won't match). Simple-name collisions across packages are dropped to
    avoid ambiguous imports. This is the lookup table the scaffold uses to resolve
    symbols automatically — no hand-maintained import list."""
    from collections import defaultdict
    pkg_re = re.compile(r"^\s*package\s+([\w.]+)\s*$", re.MULTILINE)
    # anchored at line start, optional benign modifiers, then the keyword + an
    # Uppercase name. `private`/`protected` are NOT in the modifier set, so a
    # `private object X` line fails to match and is skipped.
    decl_re = re.compile(
        r"^(?:(?:final|sealed|abstract|implicit|case)\s+)*(?:class|trait|object)\s+([A-Z]\w*)",
        re.MULTILINE)
    by_name: dict[str, set[str]] = defaultdict(set)
    for g in cfg.source_globs:
        for path in globmod.glob(str(cfg.root / g), recursive=True):
            text = Path(path).read_text(encoding="utf-8", errors="ignore")
            pm = pkg_re.search(text)
            if not pm:
                continue
            pkg = pm.group(1)
            for nm in decl_re.findall(text):
                by_name[nm].add(f"import {pkg}.{nm}")
    return {n: next(iter(s)) for n, s in by_name.items() if len(s) == 1}


def _defining_object_imports(cfg: AidealConfig) -> list[str]:
    """Auto-import the symbols documented APIs need — no per-object/type config:
      (a) the OBJECT that defines each API (file-stem object), so static call forms
          `RasterOperationsLocal.mapPixels(...)` / `RaptorJoin.raptorJoinFeature(...)`
          resolve — these live in the same package as their tests, so `from-tests`
          mining can't discover them; and
      (b) every TYPE a documented signature references (return + params), e.g. the
          `RaptorJoinResult` / `RaptorJoinFeature` case classes used in a raptor
          result annotation, which are also same-package and mining-invisible.
    Both are looked up in the source symbol index; anything not defined in this
    codebase (Spark's `RDD`, generic params `T`/`U`, ...) is simply absent from the
    index and ignored."""
    index = _source_symbol_index(cfg)
    if not index:
        return []
    needed: set[str] = set()
    _ident = re.compile(r"[A-Z]\w*")
    for d in public_api_details(cfg):
        if d.get("visibility") != "public":
            continue
        f = d.get("file", "")
        if f.endswith(".scala"):
            needed.add(Path(f).stem)                       # (a) defining object
        sig = d.get("signature") or ""
        ret = d.get("returns") or ""
        ptypes = " ".join(p.get("type", "") for p in (d.get("params") or []))
        for blob in (sig, ret, ptypes):                    # (b) referenced types
            needed.update(_ident.findall(blob))
    imports = {index[n] for n in needed if n in index}
    # Same compile-classpath gate the from-tests path uses: a documented API can live
    # in a source module that ISN'T on the exec classpath (e.g. `dynoviz`, or the
    # `test` helper modules under src/main/scala). Its defining-object / referenced-type
    # import is real in the source tree but `object dynoviz is not a member ...` at
    # scalac time, and — because these imports are shared by EVERY api-test — one such
    # leak fails the whole suite. Drop them here; skipped when jars are unresolved.
    avail = _available_packages(cfg)
    if avail:
        imports = {i for i in imports if _on_classpath(i, avail)}
    return sorted(imports)


def generate_scaffold(cfg: AidealConfig) -> str:
    """Build a runnable scaffold. `comprehension.execute.imports`:
      - a list      -> use that curated block verbatim,
      - "from-tests"/"auto" -> mine the SPECIFIC, compiling imports the test suite
        uses (robust; avoids the ambiguous-RasterRDD wildcard collision),
      - unset       -> auto-derive wildcard imports from source packages (best-effort)."""
    ex = (cfg.comprehension or {}).get("execute", {}) if cfg.comprehension else {}
    # the scaffold FRAME is language-specific -> a codebase adapter can override it
    # (e.g. scala-spark's GeoJobMain harness, or a Python __main__ runner). Core
    # only fills the {imports} slot + the AIDEAL_DATA_BINDINGS / API_TEST markers.
    frame = ex.get("scaffold_frame") or _SCAFFOLD_FRAME
    override = ex.get("imports")
    # project may declare must-have imports the test suite / source never writes
    # explicitly (e.g. an object like `RaptorJoin` used only inside its own
    # package, or a package-object of implicits). Honored in EVERY mode.
    extra = ex.get("extra_imports", []) or []
    # ...plus the defining OBJECT of every documented API, so static-method call
    # forms resolve even when the object lives in the same package as its tests
    # (which `from-tests` mining can't discover). Opt out with defining_object_imports: false.
    defining = _defining_object_imports(cfg) if ex.get("defining_object_imports", True) else []
    # project may drop imports that are REDUNDANT AND AMBIGUOUS: a Scala package
    # object that `extends` several mixin traits (e.g. `edu.ucr.cs.bdlab.beast._`
    # re-exports ReadWriteMixin) makes a second wildcard of the same mixin
    # (`ReadWriteMixin._`) a duplicate implicit at equal priority -> the implicit
    # conversion becomes ambiguous and silently stops resolving (`sc.shapefile`
    # "is not a member"). Listing that redundant wildcard here removes the tie.
    exclude = set(ex.get("exclude_imports", []) or [])
    # package-object re-export map: {pkgobj wildcard -> redundant mixin wildcards}.
    # Auto-drops the ambiguous duplicates so common cases need no manual
    # `exclude_imports`; config stays as an additional override.
    reexports = _pkgobject_reexported_wildcards(cfg)
    # ...and GUARANTEE the package-object umbrella wildcard(s) themselves (e.g.
    # `import edu.ucr.cs.bdlab.beast._`) — the documented entry point for the
    # sc.* implicits (shapefile/geoTiff/mapPixels-instance-form). Adding them here
    # means no manual extra_import is needed, and the reexport-drop above keeps the
    # redundant mixin wildcards from re-introducing the ambiguity.
    extra = list(extra) + defining + sorted(reexports)
    def _drop(lines: list[str]) -> list[str]:
        # remove excluded imports AND de-duplicate (a guaranteed extra_import may
        # also be mined from tests; two identical wildcards are harmless but noisy)
        present = set(lines)
        dyn = set(exclude)
        for pkgobj, mixins in reexports.items():
            if pkgobj in present:          # only redundant when the umbrella is there
                dyn |= mixins
        out: list[str] = []
        seen: set[str] = set()
        for l in lines:
            if l in dyn or l in seen:
                continue
            seen.add(l)
            out.append(l)
        return out
    if isinstance(override, list) and override:
        return frame.replace("{imports}", "\n".join(_drop(list(extra) + override)))
    if isinstance(override, str) and override.strip().lower() in ("from-tests", "auto"):
        mined = _imports_from_tests(cfg)
        return frame.replace("{imports}", "\n".join(_drop(_SCAFFOLD_BASE_IMPORTS + list(extra) + mined)))
    # Collect source packages (wildcarded) + the packages/objects the source
    # imports from. Collapse every import to a WILDCARD of its package/object so
    # the noisy per-class member lists become a short, clean set. Keep only
    # caller-facing roots — a doc-driven snippet needs the library + Spark +
    # geometry, not the library's internal deps (hadoop/geotools/kryo/jhdf).
    caller_roots = ("edu.ucr.cs.bdlab", "org.apache.spark", "org.locationtech")
    pkgs: set[str] = set()
    wilds: set[str] = set()
    pkg_re = re.compile(r"^\s*package\s+([\w.]+)", re.MULTILINE)
    imp_re = re.compile(r"^\s*import\s+(\S.*)$", re.MULTILINE)

    def _wildcard_of(target: str) -> str:
        s = target.strip()
        if s.endswith("._"):
            return s[:-2]
        if s.endswith("}"):
            return s[:s.rfind(".{")]
        return s.rsplit(".", 1)[0]            # drop the single class/member

    for g in cfg.source_globs:
        for path in globmod.glob(str(cfg.root / g), recursive=True):
            text = Path(path).read_text(encoding="utf-8", errors="ignore")
            for m in pkg_re.finditer(text):
                pkgs.add(m.group(1))
            for m in imp_re.finditer(text):
                w = _wildcard_of(m.group(1))
                if w.startswith(caller_roots) and w.count(".") >= 2:
                    wilds.add(w)
    wilds |= pkgs
    # drop accidental ancestors of a source package (e.g. edu.ucr.cs.bdlab left
    # over from `import edu.ucr.cs.bdlab.raptor`) — the specific one is kept.
    wilds = {w for w in wilds
             if w in pkgs or not any(p.startswith(w + ".") for p in pkgs)}
    # drop wildcards for packages NOT present in the compile jars (e.g. internal
    # `jhdf`) — those imports would fail to compile. Keep a wildcard if the
    # package itself, or its enclosing package (for object imports like
    # `RaptorMixin._`), has classes in the jars. Skipped if jars not configured.
    avail = _available_packages(cfg)
    if avail:
        wilds = {w for w in wilds
                 if w in avail or w.rsplit(".", 1)[0] in avail}
    # extra_imports + defining-object imports (same `extra` assembled above).
    pkg_imports = sorted(f"import {w}._" for w in wilds)
    imports = "\n".join(_drop(_SCAFFOLD_BASE_IMPORTS + list(extra) + pkg_imports))
    return frame.replace("{imports}", imports)


def public_api_surface(cfg: AidealConfig, override_filter: str | None = None) -> set[str]:
    """Public API names, optionally narrowed to the INTENDED API by a general,
    codebase-agnostic `surface_filter` (pass override_filter='all' for the raw
    discovered surface):
      all                       - every visible public def (raw surface)
      documented                - has a doc comment (author signalled intent)
      non_override              - not an `override` (excludes inherited/interface impls)
      documented_non_override   - both (tightest intended-API set)
    Default `all` (back-compat)."""
    model = visibility_model(cfg)
    flt = (override_filter or cfg.surface_filter or "all").lower()
    if flt in ("intent_score", "intent"):
        return {n for n, info in intent_scores(cfg).items() if info["selected"]}
    if flt in ("intended_llm", "intent_llm"):
        return intended_api_llm(cfg)[0]
    file_cache: dict[str, list[str]] = {}
    all_names: set[str] = set()
    documented: set[str] = set()
    non_override: set[str] = set()
    for name, prefix, path, i, _line in _iter_defs(cfg):
        if name in cfg.exclude_names or not _is_public(name, prefix, model):
            continue
        all_names.add(name)
        if not re.search(r"\boverride\b", prefix):
            non_override.add(name)
        if flt.startswith("documented"):
            lines = file_cache.setdefault(
                path, Path(path).read_text(encoding="utf-8", errors="ignore").splitlines())
            if _doc_at(cfg, lines, i).strip():
                documented.add(name)
    # Intent signals, in order of preference: documentation, then tests (a unit
    # test exercising an API is also author intent). Structural `non_override`
    # is the last resort because it's over-inclusive (can't tell API from
    # internal helper). So `documented` degrades: docs -> tested -> non_override
    # -> all, never empty.
    def _tested() -> set[str]:
        if not cfg.test_globs:
            return set()
        names = set()
        for g in cfg.test_globs:
            for p in globmod.glob(str(cfg.root / g), recursive=True):
                txt = Path(p).read_text(encoding="utf-8", errors="ignore")
                for nm in all_names:
                    if nm not in names and re.search(rf"\b{re.escape(nm)}\s*[\(\[]|\.{re.escape(nm)}\b", txt):
                        names.add(nm)
        return names

    if flt == "documented":
        return documented or _tested() or non_override or all_names
    if flt == "tested":
        return _tested() or documented or non_override or all_names
    if flt == "non_override":
        return non_override or all_names
    if flt in ("documented_non_override", "documented_and_non_override"):
        return (documented & non_override) or documented or _tested() or non_override or all_names
    if flt in ("documented_or_tested", "intended"):
        return (documented | _tested()) or non_override or all_names
    return all_names


# Generic boilerplate/lifecycle names (cross-language plumbing, not domain API).
_BOILERPLATE_NAMES = {
    "hasNext", "next", "close", "compareTo", "copy", "apply", "unapply",
    "equals", "hashCode", "toString", "iterator", "clone", "finalize",
    "productElement", "productArity", "productIterator", "productPrefix",
    "canEqual", "get", "set", "read", "write", "getClass", "wait", "notify",
}
_INTERNAL_PATH_SEGMENTS = ("/internal/", "/impl/", "/detail/", "/private/",
                           "/generated/", "/internals/")
_DEFAULT_INTENT_WEIGHTS = {
    "documented": 2, "tested": 3, "mentioned_in_docs": 4, "non_override": 1,
    "override": -3, "internal_path": -5, "boilerplate_name": -4,
    "many_impls": -3,  # interface-method detector: name defined at >= many_impls_threshold sites
    "llm_common": 0,   # off by default; >0 + intent.use_llm enables the LLM signal
}


def llm_common_apis(cfg: AidealConfig, candidates: set[str], refresh: bool = False) -> set[str]:
    """OPTIONAL LLM signal: the author model (with the role/domain persona) judges
    which candidates are commonly-used, user-facing operations. ONE call over the
    whole list, then CACHED to docs/intent_common.json so the intent score stays
    reproducible across runs (delete the cache or pass refresh to re-judge)."""
    import json as _json
    cache = cfg.llm_readme.parent / "intent_common.json"
    if cache.exists() and not refresh:
        try:
            cached = _json.loads(cache.read_text(encoding="utf-8"))
            if cached:  # an EMPTY cached list is a failed judge run, not a
                return set(cached) & candidates  # verdict — treat as a miss
        except Exception:
            pass
    from .llm import invoke_text
    from .prompts import load as load_prompt
    from .profile import require_profile
    require_profile(cfg)
    details = {d["name"]: d for d in public_api_details(cfg)}
    listing = "\n".join(f"- {n}: {details.get(n, {}).get('signature', n)}"
                        for n in sorted(candidates))
    system, user = load_prompt(cfg, "aideal/intent_common", api_list=listing)
    # dump the exact rendered prompt + raw response so the LLM step is auditable
    dump = cache.parent / "intent_common_prompt.txt"
    dump.parent.mkdir(parents=True, exist_ok=True)
    resp = invoke_text(cfg.model_for_role("author"), system, user)
    dump.write_text(
        f"MODEL: {cfg.model_for_role('author')}\n\n"
        f"===== SYSTEM =====\n{system}\n\n===== USER =====\n{user}\n\n"
        f"===== RESPONSE =====\n{resp}\n",
        encoding="utf-8")
    try:
        picked = set(_json.loads(resp[resp.index("["):resp.rindex("]") + 1]))
    except Exception:
        picked = {ln.strip("-* `").strip() for ln in resp.splitlines() if ln.strip()}
    picked &= candidates
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(_json.dumps(sorted(picked), indent=2), encoding="utf-8")
    return picked


def intended_api_llm(cfg: AidealConfig) -> tuple[set[str], dict]:
    """Token-efficient intended-API selection: STATIC evidence auto-includes the
    obvious (score >= include_threshold) and auto-excludes the clearly-internal
    (score <= exclude_threshold); the LLM adjudicates ONLY the ambiguous middle
    band, in batches, from COMPACT records (name/signature/doc/score/signals) —
    never source. Decisions are cached with provenance (`intended_api.cache`) so
    runs are reproducible. Returns (selected_names, decisions)."""
    import json as _json
    ia = (cfg.raw.get("codebase", {}) or {}).get("intended_api", {}) or {}
    inc_t = int(ia.get("static_include_threshold", 8))
    exc_t = int(ia.get("static_exclude_threshold", 1))
    batch = int(ia.get("batch_size", 25))
    refresh = bool(ia.get("refresh", False))
    cache_path = (cfg.root / ia.get("cache", "docs/intended_api_decisions.json")).resolve()

    scores = intent_scores(cfg)
    details = {d["name"]: d for d in public_api_details(cfg)}
    selected: set[str] = set()
    decisions: dict[str, dict] = {}
    ambiguous: list[str] = []
    for name, info in scores.items():
        s = info["score"]
        if s >= inc_t:
            selected.add(name); decisions[name] = {"decision": "include", "by": "static", "score": s}
        elif s <= exc_t:
            decisions[name] = {"decision": "exclude", "by": "static", "score": s}
        else:
            ambiguous.append(name)

    cache: dict = {}
    if cache_path.exists() and not refresh:
        try:
            cache = _json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            cache = {}
    todo = [n for n in ambiguous if n not in cache]
    if todo:
        try:
            from .llm import invoke_text
            from .prompts import load as load_prompt
            from .profile import require_profile
            require_profile(cfg)
            model = cfg.model_for_role("author")
            for i in range(0, len(todo), batch):
                chunk = todo[i:i + batch]
                recs = [{"name": n,
                         "signature": details.get(n, {}).get("signature", n),
                         "doc": (details.get(n, {}).get("description", "") or "")[:120],
                         "static_score": scores[n]["score"],
                         "signals": scores[n]["reasons"]} for n in chunk]
                resp = invoke_text(model, *load_prompt(cfg, "aideal/intended_review",
                                                       records=_json.dumps(recs, ensure_ascii=False, indent=2)))
                parsed = []
                try:
                    parsed = _json.loads(resp[resp.index("["):resp.rindex("]") + 1])
                except Exception:
                    parsed = []
                bydec = {d.get("name"): d for d in parsed if isinstance(d, dict)}
                for n in chunk:
                    d = bydec.get(n, {})
                    cache[n] = {"decision": d.get("decision", "uncertain"),
                                "reason": d.get("reason", ""), "by": "llm",
                                "score": scores[n]["score"], "model": model.model}
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(_json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass  # LLM unavailable -> fall back to the static threshold below

    thr = scores and next(iter(scores.values())).get("threshold", 5)
    for n in ambiguous:
        d = cache.get(n)
        if d is None:                       # LLM unavailable: fall back to intent threshold
            inc = scores[n]["score"] >= (thr or 5)
            decisions[n] = {"decision": "include" if inc else "exclude",
                            "by": "static_fallback", "score": scores[n]["score"]}
        else:
            decisions[n] = d
        if decisions[n]["decision"] == "include":
            selected.add(n)
    return selected, decisions


def _names_called_in(text: str, names: set[str]) -> set[str]:
    """Subset of `names` that appear as a call/use in `text`."""
    return {n for n in names
            if re.search(rf"\b{re.escape(n)}\s*[\(\[]|\.{re.escape(n)}\b", text)}


def _doc_code_mentions(docs_text: str, names: set[str]) -> set[str]:
    """Subset of `names` mentioned in a CODE context of the baseline docs:
    inside a fenced code block, inside inline backticks, or in call form
    (`.name` / `name(`) anywhere. A bare English-word match in prose does NOT
    count — with plain `\\b name \\b` matching, common-word APIs (RDPro:
    `run`, `this`, `close`, `write`, `read`) earned a spurious
    mentioned_in_docs(+4) just because the README uses those words in
    sentences."""
    if not docs_text or not names:
        return set()
    code = "\n".join(re.findall(r"```.*?```", docs_text, re.S))
    code += "\n" + " ".join(re.findall(r"`([^`]+)`", docs_text))
    out = set()
    for n in names:
        pat = re.escape(n)
        if re.search(rf"\b{pat}\b", code) or re.search(rf"\.{pat}\b|\b{pat}\s*\(", docs_text):
            out.add(n)
    return out


def intent_scores(cfg: AidealConfig, force_llm: bool | None = None) -> dict[str, dict]:
    """Score each public API by GENERIC evidence of user-facing intent and select
    those at/above a threshold. Codebase-agnostic: signals are documentation,
    tests, original-doc mentions, visibility/override, internal-path and
    boilerplate-name penalties. Weights/threshold/manual overrides come from
    `codebase.intent` in aideal.yaml. Returns {name: {score, reasons, selected}}
    — auditable, with per-API reasons."""
    intent = (cfg.raw.get("codebase", {}) or {}).get("intent", {}) or {}
    W = dict(_DEFAULT_INTENT_WEIGHTS); W.update(intent.get("weights", {}) or {})
    threshold = int(intent.get("threshold", 5))
    manual_inc = set(intent.get("manual_include", []) or [])
    manual_exc = set(intent.get("manual_exclude", []) or [])
    excl_pats = [re.compile(p) for p in (intent.get("exclude_name_patterns", []) or [])]
    boiler = _BOILERPLATE_NAMES | set(intent.get("boilerplate_names", []) or [])
    # interface-method detector: a name with many definition sites is (almost
    # always) a trait/interface method implemented per class, not one operation
    # (RDPro: run×29, write×27, close×27, read×24). Penalty is evidence-based
    # and auditable; strong real APIs (documented+tested+code-mentioned)
    # survive it. Tune via codebase.intent.{weights.many_impls, many_impls_threshold}.
    many_thr = int(intent.get("many_impls_threshold", 5))
    # docs_mention_mode: "code" (default) counts a doc mention only in code
    # context (fenced block / backticks / call form); "any" is the legacy
    # plain word match — kept for A/B comparison.
    mention_mode = intent.get("docs_mention_mode", "code")

    model = visibility_model(cfg)
    file_cache: dict[str, list[str]] = {}
    recs: dict[str, dict] = {}
    for name, prefix, path, i, _line in _iter_defs(cfg):
        if name in cfg.exclude_names or not _is_public(name, prefix, model):
            continue
        r = recs.setdefault(name, {"documented": False, "non_override": False,
                                   "internal": False, "sites": 0})
        r["sites"] += 1
        if not re.search(r"\boverride\b", prefix):
            r["non_override"] = True
        norm = "/" + path.replace("\\", "/").lower() + "/"
        if any(seg in norm for seg in _INTERNAL_PATH_SEGMENTS):
            r["internal"] = True
        lines = file_cache.setdefault(path, Path(path).read_text(encoding="utf-8", errors="ignore").splitlines())
        if _doc_at(cfg, lines, i).strip():
            r["documented"] = True

    names = set(recs)
    # evidence from tests and the original docs (computed once over the corpus)
    tested = set()
    for g in cfg.test_globs:
        for p in globmod.glob(str(cfg.root / g), recursive=True):
            tested |= _names_called_in(Path(p).read_text(encoding="utf-8", errors="ignore"), names - tested)
    docs_text = cfg.original_readme_text() if cfg.original_readme_files else ""
    if mention_mode == "code":
        mentioned = _doc_code_mentions(docs_text, names)
    else:  # "any" — legacy plain word match (A/B baseline)
        mentioned = {n for n in names if docs_text and re.search(rf"\b{re.escape(n)}\b", docs_text)}
    # optional LLM "commonly-used" signal (opt-in, cached for reproducibility).
    # force_llm overrides config: True = run it (default weight 4 if unset),
    # False = skip it (static-only). None = honor codebase.intent.use_llm.
    use_llm = intent.get("use_llm") if force_llm is None else force_llm
    if force_llm and not W.get("llm_common", 0):
        W["llm_common"] = 4
    common: set[str] = set()
    if W.get("llm_common", 0) and use_llm:
        # opt-in signal: degrade to static on ANY failure (missing key, profile
        # gate's SystemExit, network) so the score never crashes.
        try:
            common = llm_common_apis(cfg, names, refresh=bool(intent.get("refresh_llm")))
        except (Exception, SystemExit):
            common = set()

    out: dict[str, dict] = {}
    for name, r in recs.items():
        score = 0; reasons = []
        if r["documented"]:           score += W["documented"];      reasons.append(f"documented(+{W['documented']})")
        if name in tested:            score += W["tested"];          reasons.append(f"tested(+{W['tested']})")
        if name in mentioned:         score += W["mentioned_in_docs"]; reasons.append(f"mentioned_in_docs(+{W['mentioned_in_docs']})")
        if r["non_override"]:         score += W["non_override"];    reasons.append(f"non_override(+{W['non_override']})")
        else:                         score += W["override"];        reasons.append(f"override({W['override']})")
        if r["internal"]:             score += W["internal_path"];   reasons.append(f"internal_path({W['internal_path']})")
        if name in boiler or any(p.search(name) for p in excl_pats):
            score += W["boilerplate_name"]; reasons.append(f"boilerplate_name({W['boilerplate_name']})")
        if W.get("many_impls", 0) and r["sites"] >= many_thr:
            score += W["many_impls"]; reasons.append(f"many_impls({r['sites']} sites,{W['many_impls']})")
        if name in common:
            score += W["llm_common"]; reasons.append(f"llm_common(+{W['llm_common']})")
        selected = score >= threshold
        if name in manual_inc: selected = True;  reasons.append("manual_include")
        if name in manual_exc: selected = False; reasons.append("manual_exclude")
        out[name] = {"score": score, "reasons": reasons, "selected": selected,
                     "threshold": threshold, "sites": r["sites"]}
    return dict(sorted(out.items(), key=lambda kv: (-kv[1]["score"], kv[0])))


def intent_compare(cfg: AidealConfig) -> dict:
    """Compare intended-API selection WITHOUT the LLM signal vs WITH it.

    Runs intent twice on the same surface: static-only (force_llm=False) and
    static+LLM (force_llm=True, default weight 4). Reports counts, Jaccard
    overlap, and the APIs each side adds/drops, so the LLM signal's effect on
    the coverage denominator is auditable. `llm_signal_fired` is False when the
    LLM run silently fell back to static (no API key, unfilled profile, etc.)."""
    static = intent_scores(cfg, force_llm=False)
    llm = intent_scores(cfg, force_llm=True)
    s = {k for k, v in static.items() if v["selected"]}
    l = {k for k, v in llm.items() if v["selected"]}
    union = s | l
    jaccard = round(len(s & l) / len(union), 4) if union else 1.0
    llm_fired = any("llm_common" in "".join(v["reasons"]) for v in llm.values())
    return {
        "surface": len(static),
        "selected_static": len(s),
        "selected_llm": len(l),
        "shared": len(s & l),
        "jaccard": jaccard,
        "added_by_llm": sorted(l - s),
        "dropped_with_llm": sorted(s - l),
        "llm_signal_fired": llm_fired,
    }


def _subsume_overloads(recs: list[dict],
                       deprioritize: tuple = ()) -> tuple[list[dict], list[tuple[dict, dict]]]:
    """Telescoping-overload analysis for ONE name's definition sites.

    Same function, different parameter lists: within the SAME file (one class
    family), an overload whose parameter types are a proper prefix of a longer
    sibling's is a convenience form of that sibling (it delegates with
    defaults) — the catalog needs only the LONGEST form ("needed longest
    parameters"), e.g. `foo(x)` and `foo(x,y)` are one function documented as
    `foo(x,y)`. Cross-file same-name defs (Java facades, interface
    implementations) are never subsumed — different receiver contexts.

    Returns (maximals, subsumed): `maximals` sorted longest-params-first (then
    documented, shallowest path, line — so [0] is the canonical signature);
    `subsumed` = [(rec, subsumed_by_rec)] pointing at the LONGEST subsumer, so
    a chain foo(x) ⊂ foo(x,y) ⊂ foo(x,y,z) maps both short forms to the full one.
    """
    def _types(r: dict) -> tuple:
        return tuple((p.get("type") or "?") for p in r["params"])

    by_file: dict[str, list[dict]] = {}
    for r in recs:
        by_file.setdefault(r["file"], []).append(r)
    subsumed: list[tuple[dict, dict]] = []
    losers: set[int] = set()
    for group in by_file.values():
        for a in group:
            ta = _types(a)
            best = None
            for b in group:
                tb = _types(b)
                if b is not a and len(tb) > len(ta) and tb[:len(ta)] == ta:
                    if best is None or len(tb) > len(_types(best)):
                        best = b
            if best is not None:
                subsumed.append((a, best))
                losers.add(id(a))
    maximals = [r for r in recs if id(r) not in losers]
    # Election among the surviving maximals: within one file the longest
    # already won via subsumption; ACROSS files prefer non-deprioritized
    # paths (facade duplicates — e.g. Beast's Java* wrappers returning
    # JavaRasterRDD, the form the pipeline deliberately avoids because it
    # forced invented .toRDD adapters), then the documented context, then the
    # longest signature.
    def _depri(r: dict) -> bool:
        return any(p.search(r["file"]) for p in deprioritize)
    maximals.sort(key=lambda r: (_depri(r), not r["description"].strip(),
                                 -len(r["params"]),
                                 r["file"].count("/"), r["file"], r["line"]))
    return maximals, subsumed


def _dedup_deprioritize(cfg: AidealConfig) -> tuple:
    """Compiled `codebase.dedup.deprioritize_paths` patterns (adapter-level
    default for scala-spark: Java facade files `Java*.scala`)."""
    pats = ((cfg.raw.get("codebase", {}) or {}).get("dedup", {}) or {}).get(
        "deprioritize_paths", []) or []
    return tuple(re.compile(p) for p in pats)


def dedup_report(cfg: AidealConfig) -> dict:
    """Redundancy audit of the SELECTED surface. Deterministic (no LLM).

    Four redundancy classes, each auditable:
      1. overload collapse — one catalog entry per name; canonical site elected
         (documented > shallowest path > lowest line), others become variants;
      2. forwarder alias edges — `def a(...) = b(...)` one-liners where both
         names are selected: `a` should be catalogued as an alias of `b`, not
         documented twice;
      3. same-file same-signature twins — review list (often legitimate pairs
         like compress/decompress; never auto-dropped);
      4. alias-registry cross-check — registry aliases (aliases.json + any
         *.scala alias object using the ``(alias for `X`)`` doc convention)
         must point at a selected canonical and not shadow a surface name.
    """
    import json as _json
    det = [d for d in public_api_details(cfg) if d["visibility"] == "public"]
    scores = intent_scores(cfg)
    sel = {n for n, v in scores.items() if v["selected"]}
    by_name: dict[str, list[dict]] = {}
    for d in det:
        if d["name"] in sel:
            by_name.setdefault(d["name"], []).append(d)

    # 1. overload collapse — subsumption-aware: canonical = the maximal
    # telescoping overload ("needed longest parameters"); same-file
    # prefix-shorter forms are the SAME function with defaults, recorded under
    # subsumed_overloads, not as distinct variants.
    collapse: dict[str, dict] = {}
    subsumed_total = 0
    _depri_pats = _dedup_deprioritize(cfg)
    for n, recs in sorted(by_name.items()):
        maximals, subsumed = _subsume_overloads(recs, _depri_pats)
        canon = maximals[0]
        subsumed_total += len(subsumed)
        collapse[n] = {"sites": len(recs),
                       "canonical": f"{canon['file']}:{canon['line']}",
                       "signature": canon["signature"],
                       "subsumed_overloads": [
                           {"site": f"{a['file']}:{a['line']}",
                            "params": len(a["params"]),
                            "same_function_as": f"{b['file']}:{b['line']}"}
                           for a, b in subsumed],
                       "distinct_variants": len(maximals) - 1}

    # 2. forwarder alias edges (same-line `= callee(...)`). An edge only
    # COLLAPSES a catalog entry when EVERY def site of the name forwards to
    # the same canonical ("full"); otherwise it is "partial" — e.g. RDPro's
    # `shapefile` forwards to `spatialFile` in the Java context but is the
    # documented first-class entry point in the Scala mixin, so it stays.
    fcache: dict[str, list[str]] = {}
    forwarders: list[dict] = []
    for n, recs in sorted(by_name.items()):
        callees, sites = set(), []
        for d in recs:
            try:
                lines = fcache.setdefault(
                    d["file"], (cfg.root / d["file"]).read_text(encoding="utf-8", errors="ignore").splitlines())
                m = re.search(r"=\s*([A-Za-z_][\w.]*)\s*[\(\[]", lines[d["line"] - 1])
            except (OSError, IndexError):
                m = None
            callee = m.group(1).split(".")[-1] if m else None
            if callee in sel and callee != n:
                callees.add(callee); sites.append(f"{d['file']}:{d['line']}")
            else:
                callees.add(None)  # at least one non-forwarding site
        real = callees - {None}
        if real:
            full = None not in callees and len(real) == 1
            forwarders.append({"alias": n, "canonical": sorted(real)[0] if full else sorted(real),
                               "collapse": "full" if full else "partial",
                               "sites": sites})

    # 3. same-file same-signature twins
    twin_ix: dict[tuple, set[str]] = {}
    for n, recs in by_name.items():
        for d in recs:
            key = (d["file"], tuple((p.get("type") or "?") for p in d["params"]),
                   d["returns"] or "?")
            twin_ix.setdefault(key, set()).add(n)
    twins = [{"file": k[0], "params": list(k[1]), "returns": k[2], "names": sorted(v)}
             for k, v in sorted(twin_ix.items()) if len(v) > 1]

    # 4. alias-registry cross-check
    reg_aliases: list[dict] = []
    try:
        if cfg.aliases_file.exists():
            for r in _json.loads(cfg.aliases_file.read_text(encoding="utf-8")):
                reg_aliases.append({"alias": r["alias"], "canonical": r["canonical"],
                                    "status": r.get("status"), "source": cfg.aliases_file.name,
                                    "shadows_surface": r["alias"] in sel,
                                    "canonical_in_surface": r["canonical"] in sel})
    except Exception:
        pass
    for sf in sorted(cfg.aliases_file.parent.glob("*.scala")):
        text = sf.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"\(alias for `([\w\[\]]+)`\).*?\bdef\s+(\w+)", text, re.S):
            reg_aliases.append({"alias": m.group(2), "canonical": m.group(1),
                                "status": "added", "source": sf.name,
                                "shadows_surface": m.group(2) in sel,
                                "canonical_in_surface": m.group(1) in sel})

    sites_total = sum(c["sites"] for c in collapse.values())
    full_fwd = {f["alias"] for f in forwarders if f["collapse"] == "full"}
    return {
        "selected_names": len(by_name),
        "selected_def_sites": sites_total,
        "collapsed_variants": sites_total - len(by_name),
        "subsumed_overload_sites": subsumed_total,
        "forwarder_alias_edges": forwarders,
        "catalog_entries_after_aliasing": len(by_name) - len(full_fwd),
        "same_signature_twins": twins,
        "registry_aliases": reg_aliases,
        "collapse": collapse,
    }


def _split_top_level(inner: str) -> list[str]:
    """Split a parameter list on top-level commas (ignoring nested []/<>/()/{})."""
    out, depth, cur = [], 0, ""
    for ch in inner:
        if ch in "([{<":
            depth += 1
        elif ch in ")]}>":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def _param_record(raw: str) -> dict:
    """Parse one parameter into {name, type, default}. Splits the default on a
    top-level `=` that is NOT the `=>` of a function type (e.g. `f: Int => Int`)."""
    parts = re.split(r"=(?!>)", raw, maxsplit=1)
    left = parts[0].strip()
    default = parts[1].strip() if len(parts) > 1 else ""
    if ":" in left:
        nm, typ = left.split(":", 1)
        return {"name": nm.strip(), "type": typ.strip(), "default": default}
    return {"name": left, "type": "", "default": default}


def _signature_at(lines: list[str], idx: int, def_pos: int, name_end: int
                  ) -> tuple[str, list[dict], str]:
    """From the def line return (raw_signature, params, return_type).

    Reads a forward window so multi-line parameter lists work. A `(...)` group
    counts as the value-parameter list ONLY if it sits immediately after the
    name (after optional `[type params]`); otherwise the def is paren-less
    (`def foo: T = body(...)`) and has no value parameters — this avoids
    grabbing parentheses from the method body. params are structured dicts.
    """
    window = lines[idx][def_pos:]
    for j in range(idx + 1, min(idx + 12, len(lines))):
        window += "\n" + lines[j]

    cur = name_end - def_pos                       # index in window right after the name
    n = len(window)

    def _skip_ws(c):
        while c < n and window[c].isspace():
            c += 1
        return c

    def _skip_balanced(c, open_ch, close_ch):
        depth = 0
        while c < n:
            if window[c] == open_ch:
                depth += 1
            elif window[c] == close_ch:
                depth -= 1
                if depth == 0:
                    return c + 1
            c += 1
        return c

    cur = _skip_ws(cur)
    if cur < n and window[cur] == "[":            # generic type params, e.g. [T]
        cur = _skip_balanced(cur, "[", "]")
    cur = _skip_ws(cur)

    params: list[dict] = []
    if cur < n and window[cur] == "(":            # value parameter list
        start = cur
        cur = _skip_balanced(cur, "(", ")")
        inner = window[start + 1:cur - 1].strip()
        params = [_param_record(p) for p in _split_top_level(inner)] if inner else []

    rm = re.match(r"\s*:\s*([^\n={]+)", window[cur:])
    ret = rm.group(1).strip() if rm else ""
    sig_end = cur + (rm.end() if rm else 0)
    raw = " ".join(window[:sig_end].split())
    return raw, params, ret


def _doc_below_py(lines: list[str], idx: int) -> str:
    """Python: the docstring sits BELOW the def line. Walk past the (possibly
    multi-line) signature to the line ending with `:`, then capture a
    triple-quoted docstring if it opens there. Returns '' when absent.

    (Before this existed, the `documented` intent signal fired 0x on Python
    codebases — Sedona audit 2026-07-06 — because _doc_above looks up.)"""
    j, n = idx, len(lines)
    # end of signature: first line at/after idx whose code part ends with ':'
    while j < n:
        code = lines[j].split("#", 1)[0].rstrip()
        if code.endswith(":"):
            break
        j += 1
        if j - idx > 20:                      # runaway guard: not a normal signature
            return ""
    j += 1
    while j < n and not lines[j].strip():
        j += 1
    if j >= n:
        return ""
    m = re.match(r'^\s*[rRbBuU]{0,2}("""|\'\'\')(.*)$', lines[j])
    if not m:
        return ""
    quote, rest = m.group(1), m.group(2)
    if quote in rest:                          # one-line docstring
        return rest.split(quote, 1)[0].strip()
    parts = [rest.strip()]
    for k in range(j + 1, min(n, j + 60)):
        if quote in lines[k]:
            parts.append(lines[k].split(quote, 1)[0].strip())
            break
        parts.append(lines[k].strip())
    return " ".join(p for p in parts if p).strip()


#: where each language's API docs live relative to the definition line.
#: "above" = comment block above (Scala/Java javadoc, Kotlin KDoc, Rust ///,
#: Go doc comments, C# XML docs...); "below" = docstring under the def
#: (Python). Extend here (or teach _doc_at a new style) for new languages.
_DOC_POSITION: dict[str, str] = {"python": "below"}


def _doc_at(cfg: AidealConfig, lines: list[str], idx: int) -> str:
    """Language-aware doc extraction for the def at line idx (see _DOC_POSITION)."""
    if _DOC_POSITION.get(cfg.language.lower(), "above") == "below":
        return _doc_below_py(lines, idx) or _doc_above(lines, idx)
    return _doc_above(lines, idx)


def _doc_above(lines: list[str], idx: int) -> str:
    """Capture a doc/comment block (/** */, ///, #) immediately above line idx."""
    out, j = [], idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j >= 0 and lines[j].strip().endswith("*/"):
        while j >= 0:
            out.append(lines[j].strip());
            if lines[j].strip().startswith("/*"):
                break
            j -= 1
        out.reverse()
        txt = " ".join(l.strip("/*").strip() for l in out if l.strip("/* ").strip())
        return txt.strip()
    block = []
    while j >= 0 and re.match(r"^\s*(///|//!|#)\s?", lines[j]):
        block.append(re.sub(r"^\s*(///|//!|#)\s?", "", lines[j]).strip()); j -= 1
    block.reverse()
    return " ".join(block).strip()


def public_api_details(cfg: AidealConfig) -> list[dict]:
    """Per-definition records for the surface: name, signature, params, return,
    description, visibility, file, line. One record per definition site (not
    collapsed), so overloads across classes stay distinct."""
    model = visibility_model(cfg)
    file_cache: dict[str, list[str]] = {}
    out: list[dict] = []
    for name, prefix, path, i, line in _iter_defs(cfg):
        if name in cfg.exclude_names:
            continue
        public = _is_public(name, prefix, model)
        lines = file_cache.setdefault(
            path, Path(path).read_text(encoding="utf-8", errors="ignore").splitlines())
        m = re.compile(cfg.public_def_regex).search(line)
        raw, params, ret = _signature_at(lines, i, m.start() if m else 0,
                                         m.end() if m else 0)
        out.append({
            "name": name,
            "visibility": "public" if public else "non-public",
            "signature": raw,
            "params": params,
            "returns": ret,
            "description": _doc_at(cfg, lines, i),
            "file": str(Path(path).relative_to(cfg.root)),
            "line": i + 1,
        })
    return out


def render_api_surface(cfg: AidealConfig, include_nonpublic: bool = False) -> str:
    """Plain-text dump of the discovered API surface (Step 1 of the test plan)."""
    details = public_api_details(cfg)
    pub = [d for d in details if d["visibility"] == "public"]
    shown = details if include_nonpublic else pub
    by_name: dict[str, list[dict]] = {}
    for d in shown:
        by_name.setdefault(d["name"], []).append(d)
    lines = [
        f"API SURFACE — {cfg.project_name} ({cfg.language})",
        f"globs: {', '.join(cfg.source_globs)}",
        f"visibility model: {visibility_model(cfg).get('mode')}",
        f"public names: {len(by_name)}   public defs: {len(pub)}   "
        f"non-public defs filtered: {len(details) - len(pub)}",
        "=" * 64,
    ]
    for name in sorted(by_name):
        recs = by_name[name]
        lines.append(f"\n{name}  ({len(recs)} definition{'s' if len(recs) > 1 else ''})")
        for d in recs:
            lines.append(f"  - file   : {d['file']}:{d['line']}  [{d['visibility']}]")
            if d["params"]:
                pstr = "; ".join(
                    f"{p['name']}: {p['type']}" + (f" = {p['default']}" if p.get("default") else "")
                    if p.get("type") else p["name"]
                    for p in d["params"])
                lines.append(f"    params : {pstr}")
            else:
                lines.append("    params : (none)")
            lines.append(f"    returns: {d['returns'] or '(unspecified)'}")
            if d["description"]:
                lines.append(f"    doc    : {d['description'][:200]}")
    return "\n".join(lines)


def _params_block(params: list[dict]) -> str:
    """Pre-fill a Parameters list from the structured signature (names/types/
    defaults are facts; meanings are TODO for the author model)."""
    if not params:
        return "_None._"
    out = []
    for p in params:
        t = f" (`{p['type']}`)" if p.get("type") else ""
        d = f", default `{p['default']}`" if p.get("default") else ""
        out.append(f"- `{p['name']}`{t}{d}: TODO — what this argument means / expected values.")
    return "\n".join(out)


def _entry_skeleton(name: str, lang: str, recs: list[dict]) -> str:
    """Build a doc-entry skeleton with the factual Signature / Parameters /
    Output pre-filled from the surface; Goal / Input / examples left as TODO
    for the author model. `recs` = all definition sites for this name."""
    primary = max(recs, key=lambda r: len(r["params"]))     # richest overload
    sigs = list(dict.fromkeys((r["signature"] or name) for r in recs))
    sig_block = "\n".join(sigs)
    src = f"{primary['file']}:{primary['line']}"
    if len(recs) > 1:
        src += f"  (+{len(recs) - 1} more definition site/overload)"
    doc = primary.get("description") or ""
    doc_line = f"\n_Source doc:_ {doc}\n" if doc else ""
    ret = primary["returns"] or "unspecified"
    return f"""## API Test: `{name}`

### Signature
```{lang}
{sig_block}
```
_Source: {src}_
{doc_line}
### Goal
TODO: one sentence describing what `{name}` does, in the project's domain terms.

### Parameters
{_params_block(primary['params'])}

### Input
TODO: the data, file formats, and preconditions the caller must provide.

### Output
Returns `{ret}` — TODO: what the value represents and its format.

### Valid Call Patterns
```{lang}
TODO
```

### LLM Instruction Prompt
- TODO: rules an LLM must follow when calling `{name}`.

### Prompt Snippet
```text
TODO
```

### Common Failure Modes
- TODO

### Fix Code Hint
```{lang}
TODO
```
"""


def distilled_readme_context(cfg: AidealConfig, *, refresh: bool = False) -> str:
    """Summarize the original README ONCE into a compact, reusable context note.

    Cached next to the LLM readme; reused across every entry generation so the
    full README isn't re-sent per API (efficient + accurate). Returns a
    'generate fresh' note when the project has no original README."""
    if not cfg.original_readme_files:
        return ("No original README exists for this project — generate documentation "
                "fresh from the signature and project profile only.")
    cache = cfg.llm_readme.parent / "original_readme_notes.md"
    newest = max(p.stat().st_mtime for p in cfg.original_readme_files)
    if cache.exists() and not refresh and cache.stat().st_mtime >= newest:
        return cache.read_text(encoding="utf-8")
    from .llm import invoke_text
    from .prompts import load as load_prompt
    raw = cfg.original_readme_text(limit=150000)  # all baseline docs, summarized once
    note = invoke_text(
        cfg.model_for_role("author"),
        *load_prompt(cfg, "aideal/readme_distill", original_readme=raw),
    ).strip()
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(note, encoding="utf-8")
    return note


def _original_readme_snippets(cfg: AidealConfig, names, max_per_api: int = 2,
                              max_chars: int = 1400) -> dict[str, list[str]]:
    """Index VERBATIM code blocks from the ORIGINAL readme by the API name(s) they
    call. `distilled_readme_context` summarizes the docs ONCE and drops per-API
    snippets, so an entry never sees the project's REAL call form — e.g. the docs'
    instance-style `raster.mapPixels(f)` gets paraphrased into a non-compiling
    free-function `mapPixels(raster, f)`. Feeding the exact block back lets the
    author reproduce the true receiver/qualifier. Returns {name: [code blocks]}."""
    if not cfg.original_readme_files:
        return {}
    from collections import defaultdict
    raw = cfg.original_readme_text(limit=200000)
    # tolerant fence match: any info-string after ``` and REQUIRE the closing ```
    # to start its own line (\n```), so inline `code` / stray backticks in prose
    # don't desync the open/close pairing across the concatenated docs.
    blocks = re.findall(r"```[^\n]*\n(.*?)\n```", raw, re.DOTALL)
    idx: dict[str, list[str]] = defaultdict(list)
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        for name in names:
            if len(idx[name]) >= max_per_api:
                continue
            # a real call/use of the name: `name(`, `.name(`, `name[`
            if re.search(rf"(?:\b|\.){re.escape(name)}\s*[\(\[]", b):
                idx[name].append(b[:max_chars])
    return dict(idx)


def find_or_create(cfg: AidealConfig, generate: bool = False, max_generated: int = 10,
                   force: bool = False) -> dict:
    """Return status of the LLM readme; create a skeleton if missing.

    If the readme already exists it is returned as-is, UNLESS `force=True`
    (regenerate/overwrite) — use this to rerun `--generate` over an existing
    file instead of getting an instant "found" no-op."""
    if cfg.llm_readme.exists() and not force:
        entries = parse_readme(cfg.llm_readme)
        return {
            "action": "found",
            "path": str(cfg.llm_readme),
            "api_entries": len(entries),
            "apis": [e.name for e in entries],
            "note": "already exists; pass --force to regenerate/overwrite",
        }

    # group every definition site by name (overloads stay together), restricted
    # to the intended-API surface (cfg.surface_filter) so we document the real
    # API, not the raw regex surface.
    allowed = public_api_surface(cfg)
    by_name: dict[str, list[dict]] = {}
    for d in public_api_details(cfg):
        if d["visibility"] == "public" and d["name"] in allowed:
            by_name.setdefault(d["name"], []).append(d)
    surface = sorted(by_name)
    lang = cfg.language.lower()
    _intro = ("Generated skeleton — fill the TODOs." if not generate
              else "Generated from the API surface, project profile, and distilled docs.")
    header = f"# {cfg.project_name} — LLM_readme\n\nLLM-facing API documentation. {_intro}\n\n"
    targets = surface[:max_generated] if (generate and max_generated) else surface
    failures: list[dict] = []
    cfg.llm_readme.parent.mkdir(parents=True, exist_ok=True)

    if generate:
        # the readme is being (re)written -> invalidate readme-DERIVED caches so
        # io_hints / preamble rebuild from the NEW readme instead of a stale one.
        for _stale in ("io_hints.txt", "preamble.scala"):
            _p = cfg.llm_readme.parent / _stale
            if _p.exists():
                _p.unlink()
        import json as _json
        import sys as _sys
        from .llm import invoke_text
        from .profile import require_profile
        from .prompts import load as load_prompt

        require_profile(cfg)  # generation is domain-aware: profile must be filled
        # distil the original README ONCE; reuse the note for every entry.
        # --force also re-distils (so prompt/cap changes take effect, since the
        # mtime-based cache wouldn't otherwise notice a prompt change).
        readme_ctx = distilled_readme_context(cfg, refresh=force)
        # index real usage from the existing test suite ONCE (ground-truth examples)
        test_index = api_test_examples(cfg)
        # ...and the VERBATIM per-API code blocks from the original readme, so the
        # entry can reproduce the project's real call form (which the distilled note
        # summarizes away) instead of paraphrasing it into a non-compiling shape.
        orig_snippet_index = _original_readme_snippets(cfg, set(by_name))
        # sibling grounding: map each API to its defining class and index which
        # classes have tested methods, so an API with NO direct test can borrow
        # the tested call pattern of a sibling on the same object/class.
        import os as _os
        from collections import defaultdict as _dd
        _class_of = {n: (_os.path.basename(r[0].get("file", ""))[:-6]
                         if r and r[0].get("file", "").endswith(".scala") else "")
                     for n, r in by_name.items()}
        _sibs_by_class = _dd(list)
        for _n, _exs in test_index.items():
            if _exs and _class_of.get(_n):
                _sibs_by_class[_class_of[_n]].append((_n, _exs))
        # Version B ("try first") toggle: comprehension.execute.probe_on_missing.
        # When on, a function with no test/sibling is RUN once before its entry is
        # written, so the author grounds on real execution instead of a blind guess.
        _probe_on_missing = bool(((cfg.comprehension or {}).get("execute", {}) or {}).get("probe_on_missing"))
        total = len(targets)
        # stream each entry to disk as it completes: progress is visible and a
        # crash mid-run keeps everything generated so far (resumable by hand).
        with cfg.llm_readme.open("w", encoding="utf-8") as fh:
            fh.write(header)
            for i, name in enumerate(targets, 1):
                recs = by_name[name]
                # canonical = the maximal telescoping overload ("needed longest
                # parameters"): a same-file overload whose param types are a
                # prefix of a longer sibling's is the SAME function with
                # defaults — documented once via the longest signature and NOT
                # listed as a separate overload. Only genuinely distinct
                # signatures (different types / other receiver contexts)
                # remain in `overloads`.
                maximals, _subsumed = _subsume_overloads(recs, _dedup_deprioritize(cfg))
                primary = maximals[0]
                skeleton = _entry_skeleton(name, lang, recs)
                # Scaladoc usually sits on the SHORT base overload; if the
                # maximal form is undocumented, borrow the family's doc.
                _doc = primary["description"] or next(
                    (r["description"] for r in recs if r["description"].strip()), None)
                facts = {
                    "name": name,
                    "signature": primary["signature"] or name,
                    "params": primary["params"],           # [{name, type, default}]
                    "returns": primary["returns"] or None,
                    "source_doc": _doc,
                    "overloads": [r["signature"] for r in maximals[1:]][:5],
                }
                examples = test_index.get(name, [])
                if examples:
                    tests_text = "\n\n".join(
                        f"// from {e['file']} — test(\"{e['test']}\")\n{e['code']}" for e in examples)
                else:
                    # no direct test -> borrow the tested SIBLING pattern (same class)
                    _cls = _class_of.get(name, "")
                    _sibs = [(sn, se) for sn, se in _sibs_by_class.get(_cls, []) if sn != name][:2]
                    if _sibs:
                        _blocks = "\n\n".join(
                            f"// SIBLING `{sn}` on the same object/class `{_cls}` — mirror this call "
                            f"style (same receiver and argument order)\n// from {se[0]['file']}\n{se[0]['code']}"
                            for sn, se in _sibs)
                        tests_text = ("(no direct test for this API; use the tested SIBLING method(s) below "
                                      "as the authoritative call pattern)\n\n" + _blocks)
                    else:
                        tests_text = "(no existing test found for this API)"
                        # Version B: run the function once and ground the entry on
                        # the outcome (pass -> real call pattern; fail -> real error
                        # trace). Opt-in and fully guarded — a probe error keeps the
                        # default text so generation never breaks.
                        if _probe_on_missing:
                            try:
                                from .probe import run_probe, probe_grounding_block
                                _pr = run_probe(cfg, name, signature=primary["signature"] or "",
                                                params=primary["params"], returns=primary["returns"] or "")
                                if _pr.status in ("pass", "fail"):
                                    tests_text = probe_grounding_block(_pr, name)
                                print(f"    [probe] {name}: {_pr.status}", file=_sys.stderr)
                            except Exception as _pe:
                                print(f"    [probe] {name}: skipped ({type(_pe).__name__}: {_pe})", file=_sys.stderr)
                _orig = orig_snippet_index.get(name, [])
                orig_examples_text = ("\n\n".join(_orig) if _orig
                                      else "(no verbatim code example for this API in the original readme)")
                try:
                    entry = invoke_text(
                        cfg.model_for_role("author"),
                        *load_prompt(cfg, "aideal/readme_entry", api_name=name,
                                     api_facts=_json.dumps(facts, ensure_ascii=False, indent=2),
                                     original_readme_context=readme_ctx,
                                     original_examples=orig_examples_text,
                                     test_examples=tests_text,
                                     template=skeleton),
                    ).strip()
                    status = "ok"
                except Exception as e:  # fell back to skeleton — record why, don't hide it
                    failures.append({"api": name, "error": f"{type(e).__name__}: {e}"})
                    entry = skeleton
                    status = "FALLBACK"
                fh.write(entry + "\n\n")
                fh.flush()
                print(f"[{i}/{total}] {name} … {status}", file=_sys.stderr)
        # eager: build the readme-DERIVED io_hints / preamble now (config value
        # `auto`), so the readme bundle ships complete and in sync. Best-effort —
        # failures here never block readme generation.
        try:
            from .doc_checks import _resolve_io_hints, _resolve_preamble, _execute_sample_data
            _ex = (cfg.comprehension or {}).get("execute", {}) or {}
            _auto = lambda k: str(_ex.get(k, "")).strip().lower() == "auto"
            if _auto("io_hints") or _auto("preamble"):
                _sd, _, _ = _execute_sample_data(cfg, _ex)
                if _auto("io_hints"):
                    _resolve_io_hints(cfg, _ex, _sd)
                if _auto("preamble"):
                    _resolve_preamble(cfg, _ex, _sd)
                print("[io_hints/preamble] regenerated from the new readme", file=_sys.stderr)
        except Exception:
            pass
    else:
        with cfg.llm_readme.open("w", encoding="utf-8") as fh:
            fh.write(header)
            for name in targets:
                fh.write(_entry_skeleton(name, lang, by_name[name]) + "\n\n")

    result = {
        "action": "created_skeleton" if not generate else "created_generated",
        "path": str(cfg.llm_readme),
        "api_entries": len(targets),
        "used_original_readme": [str(p.relative_to(cfg.root)) for p in cfg.original_readme_files],
        "note": "fill TODOs or rerun with --generate (uses the author model)",
    }
    if generate:
        result["generated_ok"] = len(targets) - len(failures)
        result["fallback_to_skeleton"] = len(failures)
        if failures:
            result["failures"] = failures[:5]
            result["note"] = (f"{len(failures)}/{len(targets)} entries fell back to "
                              f"skeleton — see 'failures' for the error")
    return result


# --- surface audit: catalog vs the CURRENT visibility-correct surface --------

def surface_audit(cfg: AidealConfig) -> dict:
    """Cross-check every LLM_readme catalog entry against the current API
    surface. Catches the private-function leak class after a visibility-model
    fix: entries whose canonical definition is non-public (private/protected,
    incl. scoped `private[pkg]` and non-public enclosing containers), whose
    file is excluded by `codebase.exclude_path_patterns`, or which fell below
    the intent threshold. These entries burn fix-loop rounds and can never
    pass from an external harness — prune or exclude them instead of fixing.

    Returns counts + per-entry verdicts; CLI: `aideal surface-audit`."""
    entries = [e.name for e in parse_readme(cfg.llm_readme)]
    det = public_api_details(cfg)
    by_name: dict[str, list[dict]] = {}
    for d in det:
        by_name.setdefault(d["name"], []).append(d)
    # modifier evidence per non-public site (via the same prefix _is_public saw)
    mods_of: dict[str, list[str]] = {}
    for name, prefix, path, i, _line in _iter_defs(cfg):
        if name not in entries:
            continue
        found = _NONPUBLIC_MOD_RE.findall(prefix)
        if found:
            rel = str(Path(path).relative_to(cfg.root))
            mods_of.setdefault(name, []).append(f"{' '.join(found)} @ {rel}:{i + 1}")
    selected = public_api_surface(cfg)   # respects surface_filter (intent_score...)
    verdicts: dict[str, dict] = {}
    for n in entries:
        recs = by_name.get(n, [])
        if not recs:
            verdicts[n] = {"status": "not-on-surface",
                           "why": "no definition matched (path-excluded via "
                                  "exclude_path_patterns, moved, or renamed)"}
        elif all(r["visibility"] != "public" for r in recs):
            verdicts[n] = {"status": "non-public",
                           "why": "; ".join(mods_of.get(n, [])[:3]) or
                                  "private/protected (incl. enclosing container)",
                           "sites": [f"{r['file']}:{r['line']}" for r in recs[:3]]}
        elif n not in selected:
            verdicts[n] = {"status": "deselected",
                           "why": f"below intent threshold under surface_filter="
                                  f"{cfg.surface_filter}"}
        else:
            verdicts[n] = {"status": "ok"}
    from collections import Counter
    counts = dict(Counter(v["status"] for v in verdicts.values()))
    prune = sorted(n for n, v in verdicts.items() if v["status"] != "ok")
    return {"check": "surface-audit",
            "catalog_entries": len(entries),
            "public_names_on_surface": len({d["name"] for d in det
                                            if d["visibility"] == "public"}),
            "counts": counts,
            "prune_candidates": prune,
            "verdicts": {n: v for n, v in verdicts.items() if v["status"] != "ok"}}


# --- coverage: which APIs does each documentation set actually document? ----

def api_coverage(cfg: AidealConfig) -> dict:
    """Coverage artifact for the 2x2 experiment (design 2026-07-13):

      S = frozen runnable public surface (visibility-correct + intent filter)
      O = APIs documented in the ORIGINAL bundle (evidence-based: code block /
          backticks / call-form via _doc_code_mentions — bare prose words do
          not count), resolved against S
      G = APIs with a generated LLM_readme entry, resolved against S
      T = S ∩ O ∩ G — the SHARED manifest every pass-rate cell must consume

    Coverage (|S∩O|/|S| vs |S∩G|/|S|) is a first-class result on its own;
    pass rates are only causally comparable on T."""
    S = set(public_api_surface(cfg))
    docs_text = cfg.original_readme_text(limit=None) if cfg.original_readme_files else ""
    O = _doc_code_mentions(docs_text, S)
    G = ({e.name for e in parse_readme(cfg.llm_readme)} & S
         if cfg.llm_readme.exists() else set())
    T = S & O & G
    def pct(x):
        return round(100.0 * len(x) / len(S), 1) if S else 0.0
    return {
        "surface_S": sorted(S), "n_surface": len(S),
        "original_documented_O": sorted(O),
        "generated_documented_G": sorted(G),
        "shared_T": sorted(T),
        "coverage": {"original_pct_of_S": pct(O),
                     "generated_pct_of_S": pct(G),
                     "shared_pct_of_S": pct(T)},
        "undocumented_in_original": sorted(S - O),
        "undocumented_in_generated": sorted(S - G),
        "original_doc_files": [str(x.relative_to(cfg.root))
                               for x in cfg.original_readme_files],
        "original_doc_chars": len(docs_text),
    }
