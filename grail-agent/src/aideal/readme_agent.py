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
    """`prefix` is the text on the def line BEFORE the matched name (the modifiers)."""
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


def _iter_defs(cfg: AidealConfig):
    """Yield (name, prefix, file_path, lineno, line) for every matched def."""
    pattern = re.compile(cfg.public_def_regex)
    for g in cfg.source_globs:
        for path in globmod.glob(str(cfg.root / g), recursive=True):
            lines = Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()
            for i, line in enumerate(lines):
                for m in pattern.finditer(line):
                    yield m.group(1), line[:m.start()], path, i, line


_TEST_BLOCK_RE = re.compile(r'\btest\s*\(\s*"([^"]*)"\s*\)\s*\{')


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
            for tname, block in _iter_test_blocks(text):
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
object GeoJob {{
  def run(sc: SparkContext): Unit = {{
    // Typed sample inputs (from comprehension.execute.sample_data). Use the
    // one(s) whose type matches the API's parameters.
    // AIDEAL_DATA_BINDINGS

    // TODO API_TEST_START
    // (generated snippet inserted here)
    // TODO API_TEST_END
  }}
}}

object GeoJobMain {{
  def main(args: Array[String]): Unit = {{
    val spark = SparkSession.builder().appName("ApiTest").master("local[*]").getOrCreate()
    try {{
      GeoJob.run(spark.sparkContext)
      println("__DONE__ object=GeoJob")
    }} catch {{
      case t: Throwable =>
        Console.err.println("__RUN_ERR__ " + t.getClass.getName + ": " + t.getMessage)
        t.printStackTrace()
    }} finally {{
      spark.stop()
    }}
  }}
}}
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


def generate_scaffold(cfg: AidealConfig) -> str:
    """Build a runnable scaffold. If comprehension.execute.imports is set, use
    that curated import block verbatim (avoids wildcard collisions like an
    ambiguous RasterRDD); otherwise auto-derive wildcard imports from the source
    packages (best-effort, may need curation for collision-prone codebases)."""
    ex = (cfg.comprehension or {}).get("execute", {}) if cfg.comprehension else {}
    override = ex.get("imports")
    if override:
        return _SCAFFOLD_FRAME.format(imports="\n".join(override))
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
    # project may declare must-have imports a sub-package source never imports
    # (e.g. the `edu.ucr.cs.bdlab.beast._` package-object implicits).
    extra = (cfg.comprehension.get("execute", {}) or {}).get("extra_imports", []) or []
    pkg_imports = sorted(f"import {w}._" for w in wilds)
    imports = "\n".join(_SCAFFOLD_BASE_IMPORTS + list(extra) + pkg_imports)
    return _SCAFFOLD_FRAME.format(imports=imports)


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
            if _doc_above(lines, i).strip():
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
            return set(_json.loads(cache.read_text(encoding="utf-8"))) & candidates
        except Exception:
            pass
    from .llm import invoke_text
    from .prompts import load as load_prompt
    from .profile import require_profile
    require_profile(cfg)
    details = {d["name"]: d for d in public_api_details(cfg)}
    listing = "\n".join(f"- {n}: {details.get(n, {}).get('signature', n)}"
                        for n in sorted(candidates))
    resp = invoke_text(cfg.model_for_role("author"),
                       *load_prompt(cfg, "aideal/intent_common", api_list=listing))
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


def intent_scores(cfg: AidealConfig) -> dict[str, dict]:
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

    model = visibility_model(cfg)
    file_cache: dict[str, list[str]] = {}
    recs: dict[str, dict] = {}
    for name, prefix, path, i, _line in _iter_defs(cfg):
        if name in cfg.exclude_names or not _is_public(name, prefix, model):
            continue
        r = recs.setdefault(name, {"documented": False, "non_override": False, "internal": False})
        if not re.search(r"\boverride\b", prefix):
            r["non_override"] = True
        norm = "/" + path.replace("\\", "/").lower() + "/"
        if any(seg in norm for seg in _INTERNAL_PATH_SEGMENTS):
            r["internal"] = True
        lines = file_cache.setdefault(path, Path(path).read_text(encoding="utf-8", errors="ignore").splitlines())
        if _doc_above(lines, i).strip():
            r["documented"] = True

    names = set(recs)
    # evidence from tests and the original docs (computed once over the corpus)
    tested = set()
    for g in cfg.test_globs:
        for p in globmod.glob(str(cfg.root / g), recursive=True):
            tested |= _names_called_in(Path(p).read_text(encoding="utf-8", errors="ignore"), names - tested)
    docs_text = cfg.original_readme_text() if cfg.original_readme_files else ""
    mentioned = {n for n in names if docs_text and re.search(rf"\b{re.escape(n)}\b", docs_text)}
    # optional LLM "commonly-used" signal (opt-in, cached for reproducibility)
    common: set[str] = set()
    if W.get("llm_common", 0) and intent.get("use_llm"):
        try:
            common = llm_common_apis(cfg, names, refresh=bool(intent.get("refresh_llm")))
        except Exception:
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
        if name in common:
            score += W["llm_common"]; reasons.append(f"llm_common(+{W['llm_common']})")
        selected = score >= threshold
        if name in manual_inc: selected = True;  reasons.append("manual_include")
        if name in manual_exc: selected = False; reasons.append("manual_exclude")
        out[name] = {"score": score, "reasons": reasons, "selected": selected, "threshold": threshold}
    return dict(sorted(out.items(), key=lambda kv: (-kv[1]["score"], kv[0])))


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
            "description": _doc_above(lines, i),
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
        total = len(targets)
        # stream each entry to disk as it completes: progress is visible and a
        # crash mid-run keeps everything generated so far (resumable by hand).
        with cfg.llm_readme.open("w", encoding="utf-8") as fh:
            fh.write(header)
            for i, name in enumerate(targets, 1):
                recs = by_name[name]
                primary = max(recs, key=lambda r: len(r["params"]))
                skeleton = _entry_skeleton(name, lang, recs)
                facts = {
                    "name": name,
                    "signature": primary["signature"] or name,
                    "params": primary["params"],           # [{name, type, default}]
                    "returns": primary["returns"] or None,
                    "source_doc": primary["description"] or None,
                    "overloads": [r["signature"] for r in recs if r is not primary][:5],
                }
                examples = test_index.get(name, [])
                if examples:
                    tests_text = "\n\n".join(
                        f"// from {e['file']} — test(\"{e['test']}\")\n{e['code']}" for e in examples)
                else:
                    tests_text = "(no existing test found for this API)"
                try:
                    entry = invoke_text(
                        cfg.model_for_role("author"),
                        *load_prompt(cfg, "aideal/readme_entry", api_name=name,
                                     api_facts=_json.dumps(facts, ensure_ascii=False, indent=2),
                                     original_readme_context=readme_ctx,
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
