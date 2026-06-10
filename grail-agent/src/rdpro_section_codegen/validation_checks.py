from __future__ import annotations

import json
import re

from .section_text import extract_section_body


def validate_candidate_scope(candidate_scala: str, current_scala: str, section: str, edited_outside_active_section, contains_placeholder_paths) -> tuple[bool, str]:
    bad, reason = edited_outside_active_section(current_scala, candidate_scala, section)
    if bad:
        return False, f"Rejected: {reason}. Edit only SECTION_{section}."
    if contains_placeholder_paths(candidate_scala):
        return False, (
            f"Rejected: SECTION_{section} candidate contains placeholder file paths.\n"
            "Do not invent /path/to literals. Reuse the injected SECTION_INPUTS variables only."
        )
    candidate_body = extract_section_body(candidate_scala, section)
    inputs_body = extract_section_body(current_scala, "INPUTS")
    scaffold_vars = set(re.findall(r"(?m)^\s*val\s+([A-Za-z_][A-Za-z0-9_]*)\b", inputs_body or ""))
    protected_vars = set(scaffold_vars)
    section_markers = ["LOAD_DATA", "TYPE_CHECK", "SPATIAL_CHECK", "TRANSFORM", "RASTER_VECTOR_JOIN", "ANALYTICS", "OUTPUT"]
    for prev_section in section_markers:
        if prev_section == section:
            break
        prev_body = extract_section_body(current_scala, prev_section)
        protected_vars.update(re.findall(r"(?m)^\s*val\s+([A-Za-z_][A-Za-z0-9_]*)\b", prev_body or ""))
    if re.search(r"(?m)^\s*SECTION_[A-Z_]+\s*:?\s*$", candidate_body or ""):
        return False, (
            f"Rejected: SECTION_{section} candidate contains a stray `SECTION_*:` label inside the section body.\n"
            "Write plain Scala statements only between the existing TODO markers."
        )
    if re.search(r"(?m)^\s*import\s+.+$", candidate_body or ""):
        return False, (
            f"Rejected: SECTION_{section} adds `import` statements inside the section body.\n"
            "Imports belong in the scaffold header only. Reuse the scaffold imports instead of adding new ones."
        )
    if section != "INPUTS":
        for protected_var in sorted(protected_vars):
            if re.search(rf"(?m)^\s*val\s+{re.escape(protected_var)}\b", candidate_body or ""):
                return False, (
                    f"Rejected: SECTION_{section} redeclares upstream variable `{protected_var}`.\n"
                    "Reuse variables already defined in SECTION_INPUTS or earlier sections instead of redefining them."
                )
    if section == "LOAD_DATA":
        if re.search(r"\bprimaryVectorPathOpt\b", inputs_body or "") and not re.search(r"\bprimaryVectorPath\b", inputs_body or ""):
            if re.search(r"\bsc\.shapefile\(\s*primaryVectorPathOpt\s*\)", candidate_body or ""):
                return False, (
                    "Rejected: SECTION_LOAD_DATA passes `primaryVectorPathOpt` directly to `sc.shapefile(...)`.\n"
                    "Use the canonical inline unwrap pattern:\n"
                    'val vector: RDD[IFeature] = sc.shapefile(primaryVectorPathOpt.getOrElse(throw new IllegalArgumentException("Vector path is not defined")))'
                )
            if "primaryVectorPathOpt.getOrElse" in (candidate_body or "") and "sc.shapefile(primaryVectorPathOpt.getOrElse" not in (candidate_body or ""):
                return False, (
                    "Rejected: SECTION_LOAD_DATA should use one canonical vector-load shape.\n"
                    "Call `sc.shapefile(primaryVectorPathOpt.getOrElse(...))` directly."
                )
            if re.search(r"(?m)^\s*val\s+primaryVectorPathOpt\b", candidate_body or ""):
                return False, (
                    "Rejected: SECTION_LOAD_DATA redeclares scaffold variable `primaryVectorPathOpt`.\n"
                    "Reuse scaffold inputs instead of redefining them."
                )
    return True, ""


def build_semantic_prompt(section: str, candidate_body: str, api_doc_text: str, section_apis: list[str], api_fix_guides: str) -> str:
    section_specific_rules = ""
    if section == "LOAD_DATA":
        section_specific_rules = """

Section-specific guidance for LOAD_DATA:
- It is valid to load both raster and vector inputs here.
- Do not reject shapefile/vector loading just because the section also loads a raster.
- The section should establish the core input datasets used by later sections.
- Treat scaffold-provided variables such as `primaryRasterPath`, `primaryVectorPathOpt`, and `outputPath` as valid in this section.
- Prefer `sc.shapefile(primaryVectorPathOpt.getOrElse(...))` directly instead of introducing a separate `primaryVectorPath` helper variable.
- Do not require runtime pixel-type branching in LOAD_DATA; that belongs in TYPE_CHECK when needed.
- Prefer not to create sampled raster helper variables such as `firstRaster` in LOAD_DATA when TYPE_CHECK can own that sample later.
- Do reject invented loader option variables like `loadOpts` when they are not already defined in the scaffold or API context.
- If a cheap load sanity check is present, prefer it to reuse existing values and avoid introducing new sample helpers that later sections will need again.
"""
    elif section == "TYPE_CHECK":
        section_specific_rules = """

Section-specific guidance for TYPE_CHECK:
- This section may use previously imported Scala or Spark SQL symbols such as IntegerType, FloatType, and DoubleType.
- Do not reject code just because a symbol is not documented in API_DOC if it is a standard imported Scala/Spark symbol.
- This section does not need to call a new RDPro API if it is validating types, schema, pixel type, or assumptions established in LOAD_DATA.
- Accept direct checks, assertions, and guard clauses when they are consistent with earlier loaded variables.
- Prefer reusing an existing sampled raster variable from earlier sections rather than creating another same-role sample helper.
- Reuse sampled records or metadata for validation; avoid `count()` unless the workflow explicitly needs total size.
- Reject `raster.first()._1` or similar tuple-style assumptions unless API_DOC explicitly shows the raster returns tuples here.
- Reject `getDataType` called on raster tiles; prefer `pixelType` or other documented tile metadata instead.
"""
    elif section == "TRANSFORM":
        section_specific_rules = """

Section-specific guidance for TRANSFORM:
- TRANSFORM means raster preparation that produces an intermediate for later analysis or for a later explicit raster-vector join stage.
- Valid RDPro transform families here include mapPixels, filterPixels, overlay, reshape/rescale/reproject.
- Choose the transform family from the Python intent, not by defaulting to mapPixels.
- If a separate RASTER_VECTOR_JOIN section exists, keep raster-vector pairing APIs there instead of using them in TRANSFORM.
- Prefer not to use mapPixels for geometry-driven masking unless the Python source is explicitly remapping pixel values.
- TRANSFORM may produce a transformed raster or filtered raster.
- TRANSFORM should not perform the final histogram, count, percentage, or grouped summary aggregation when a later ANALYTICS section is available.
- Examples of TRANSFORM operations: mapPixels, filterPixels, overlay, reshape.
- Flag invented tile inspection patterns such as `tile.metadata`, `firstTile.metadata`, or `tile.get(x, y)` when they are not documented in API_DOC.
"""
    elif section == "RASTER_VECTOR_JOIN":
        section_specific_rules = """

Section-specific guidance for RASTER_VECTOR_JOIN:
- This section is the explicit raster-vector pairing stage.
- Prefer one concrete reusable assignment such as `val joinedRecords = raster.raptorJoin(vector)` or another documented raster-vector pairing call such as `mask(...)`.
- The goal is to produce `joined_records` for downstream analytics, not to perform final aggregations here.
- Do not skip the join when vector data is required for zonal or per-feature analytics.
- Do not replace the join with raster-only logic like flatten or whole-raster histogramming.
"""
    elif section == "ANALYTICS":
        section_specific_rules = """

Section-specific guidance for ANALYTICS:
- ANALYTICS means computing summary values, percentages, histograms, counts, or grouped aggregate outputs from the intermediate produced by TRANSFORM.
- If the workflow needs pixel-level samples, prefer raster.flatten to materialize `(x, y, RasterMetadata, value)` tuples.
- flatten is a good fit for class histograms, frequency counts, land-use percentages, and similar summaries.
- Do not invent tile helpers like `tile.toArray()` when pixel-level rows are already available through flatten.
- ANALYTICS should usually consume the transformed raster produced earlier, e.g. `maskedRaster` or another prior raster variable.
- Flag invented feature accessors such as `getAttribute(...)` or `getID(...)` unless API_DOC explicitly shows them.
- Prefer using only field names that are explicitly available in the prompt context; do not reward guessed schema names.
- If analytics is skipped or only validating pipeline wiring, keep it minimal and avoid expensive full-data actions.
"""
    elif section == "OUTPUT":
        section_specific_rules = """

Section-specific guidance for OUTPUT:
- Treat `outputPath` as valid when it comes from the scaffold.
- If local file IO is used, reject direct use of `file:/...` URIs with `FileWriter` or similar APIs unless the URI is converted to a filesystem path first.
- If Spark CSV output is used, prefer overwrite mode and directory-style output semantics.
- Reject direct CSV writes of nested `array` or `struct` columns unless the code flattens or serializes them first.
"""

    return f"""Review SECTION_{section} for semantic correctness.

Judge only the following:
- invented RDPro symbols
- wrong RDPro parameter counts
- wrong RDPro parameter order
- section logic that clearly contradicts the intended workflow

Do not require an exact match to examples. Alternative implementations are allowed if they are valid.
Do not comment on ordinary Scala, Spark, or local validation logic unless it directly breaks the intended workflow.
Do flag obviously expensive validation-only actions on large raster data, such as `count()` used just for logging or sanity checks.
Prefer false negatives over false positives: if a section is unusual but still plausibly valid and consistent with the workflow, mark it as ok.

Strict checks:
- RDPro API names, constants, sentinels, and method names must match the provided API context exactly.
- Each RDPro API call must use a valid parameter count and parameter order for a real callable shape from the provided context.
- Reject invented RDPro config/constants/options names even if they sound plausible.

Allowed without complaint:
- local variables
- assertions and guard clauses
- standard Scala or Spark SQL symbols such as IntegerType, FloatType, and DoubleType
- control-flow differences from examples
- helper logic around valid RDPro calls
- different but valid Spark/Scala aggregation shapes
- different variable names as long as referenced values are defined in the section or earlier sections
- reusing previously defined variables instead of recreating them
{section_specific_rules}

Return JSON only:
{{
  "ok": true,
  "issues": [],
  "fix": ""
}}

API_DOC:
{api_doc_text}

ACTIVE_SECTION_APIS:
{", ".join(section_apis) if section_apis else "(none detected)"}

API_FIX_GUIDES:
{api_fix_guides}

SECTION_CODE:
{candidate_body}
"""


def extract_api_test_block(api_doc_text: str, api_name: str) -> str:
    pattern = rf"(?ms)^## API Test: `{re.escape(api_name)}`\s*$\n(.*?)(?=^## API Test: |\Z)"
    match = re.search(pattern, api_doc_text or "")
    if not match:
        return ""
    return f"## API Test: `{api_name}`\n\n" + match.group(1).strip()


def find_relevant_api_doc_sections(api_doc_text: str, section: str, section_apis: list[str], python_analysis: dict) -> str:
    analysis = python_analysis or {}
    operations = set(analysis.get("operations", []) or [])
    relevant_apis = list(section_apis)

    if section == "LOAD_DATA" and "geoTiff" not in relevant_apis:
        relevant_apis.append("geoTiff")
    if section == "TYPE_CHECK" and "geoTiff" not in relevant_apis and analysis.get("raster_inputs"):
        relevant_apis.append("geoTiff")
    if analysis.get("requires_vector") and "IFeature" not in relevant_apis:
        relevant_apis.append("IFeature")
    if section == "TRANSFORM":
        if "mask_or_filter" in operations:
            transform_apis = ("mapPixels",) if analysis.get("requires_vector") else ("filterPixels", "mapPixels")
            for api in transform_apis:
                if api not in relevant_apis:
                    relevant_apis.append(api)
        if analysis.get("multi_raster"):
            if "overlay" not in relevant_apis:
                relevant_apis.append("overlay")
    if section == "RASTER_VECTOR_JOIN":
        if "raptorJoin" not in relevant_apis:
            relevant_apis.append("raptorJoin")
    if section == "ANALYTICS":
        for api in ("flatten", "raptorJoin"):
            if api not in relevant_apis:
                relevant_apis.append(api)
    if section == "OUTPUT" and analysis.get("final_artifact_type") == "raster_file" and "saveAsGeoTiff" not in relevant_apis:
        relevant_apis.append("saveAsGeoTiff")

    blocks = [extract_api_test_block(api_doc_text, api) for api in relevant_apis]
    blocks = [block for block in blocks if block.strip()]
    return "\n\n".join(blocks)


def parse_semantic_verdict(raw: str) -> dict:
    cleaned = (raw or "").strip()
    cleaned = re.sub(r"^json\s*", "", cleaned, flags=re.IGNORECASE)
    try:
        return json.loads(cleaned)
    except Exception:
        return {
            "ok": False,
            "issues": [f"Semantic checker returned invalid JSON: {cleaned[:500]}"],
            "fix": "Return valid JSON only.",
        }


def find_missing_required_calls(section_body: str, required_calls: list[str]) -> list[str]:
    body = section_body or ""
    patterns = {
        "geoTiff": [r"\.geoTiff(?:\[[^\]]+\])?\("],
        "shapefile": [r"\.shapefile\("],
        "filterPixels": [r"\.filterPixels\("],
        "mapPixels": [r"\.mapPixels\("],
        "flatten": [r"\.flatten\b"],
        "overlay": [r"\.overlay\("],
        "raptorJoin": [r"\.raptorJoin\(", r"\.mask\("],
        "saveAsGeoTiff": [r"\.saveAsGeoTiff\("],
    }
    missing: list[str] = []
    for api in required_calls or []:
        api_patterns = patterns.get(api, [])
        if api_patterns and not any(re.search(pattern, body) for pattern in api_patterns):
            missing.append(api)
    return missing


def section_is_effectively_placeholder(section_body: str, section: str) -> bool:
    body = (section_body or "").strip()
    if not body:
        return True

    lines = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("//"):
            continue
        if line == f'println("__STEP__ {section}_done")':
            continue
        lines.append(line)

    return len(lines) == 0


def _extract_assigned_variables(section_body: str) -> list[str]:
    return re.findall(r"(?m)\bval\s+([A-Za-z_][A-Za-z0-9_]*)\b", section_body or "")


def find_contract_shape_issues(
    full_scala_text: str,
    section: str,
    section_body: str,
    contract: dict,
) -> list[str]:
    issues: list[str] = []
    body = section_body or ""
    invariants = set(contract.get("invariants", []) or [])
    required_inputs = set(contract.get("required_inputs", []) or [])
    produces_shape = contract.get("produces_shape", "")
    assigned_vars = _extract_assigned_variables(body)

    if section == "TYPE_CHECK" and section_is_effectively_placeholder(body, "TYPE_CHECK"):
        issues.append("SECTION_TYPE_CHECK is effectively placeholder-only, but the workflow requires a real pixelType validation step.")

    if section == "ANALYTICS" and produces_shape in ("tabular_rows", "summary_map"):
        if "countByValue(" in body and not assigned_vars:
            issues.append("SECTION_ANALYTICS computes a count map but does not assign a reusable analytics result.")
        if re.search(r"(?m)^\s*println\(", body) and len([line for line in body.splitlines() if line.strip() and not line.strip().startswith("//")]) <= 2:
            issues.append("SECTION_ANALYTICS is effectively console-only, but the workflow expects reusable analytics output.")
        if re.search(r"(?m)\bval\s+\w+\s*:\s*Long\s*=\s*.+\.sum\(\)", body):
            issues.append("SECTION_ANALYTICS assigns `.sum()` directly to `Long`, but Spark numeric `sum()` commonly yields `Double` here.")
    if section == "ANALYTICS" and "must_assign_output_rows_variable" in invariants:
        if "outputRows" not in assigned_vars:
            issues.append("SECTION_ANALYTICS must assign the final flat rows to a canonical variable named `outputRows` for SECTION_OUTPUT.")
    if section == "ANALYTICS":
        if re.search(r"\bFiles\.write\(", body) or re.search(r"\.saveAsTextFile\(", body) or re.search(r"\.write(?:\.[A-Za-z_][A-Za-z0-9_]*)*\.csv\(", body) or re.search(r"\bFileWriter\s*\(", body):
            if "must_persist_final_artifact" not in invariants and "must_write_tabular_output" not in invariants:
                issues.append("SECTION_ANALYTICS persists output directly, but file writing belongs in SECTION_OUTPUT.")

    if section in ("TRANSFORM", "RASTER_VECTOR_JOIN"):
        if "prepare_analysis_ready_intermediate" in invariants and not assigned_vars:
            issues.append(f"SECTION_{section} does not assign an intermediate result for downstream analytics.")
        if "analytics_should_aggregate_intermediate" not in invariants and produces_shape not in ("joined_records", "transformed_raster", "raster_or_transformed_raster"):
            pass

    if section == "RASTER_VECTOR_JOIN":
        if "raster_vector_summary" in invariants and not re.search(r"\.raptorJoin\(", body):
            issues.append("SECTION_RASTER_VECTOR_JOIN does not call raptorJoin even though the contract requires explicit raster-vector pairing.")

    if section in ("TRANSFORM", "RASTER_VECTOR_JOIN"):
        if re.search(r"\b(?:firstTile|tile)\.metadata\b", body):
            issues.append(f"SECTION_{section} uses tile.metadata, which is not a documented tile access pattern here.")
        if re.search(r"\b(?:firstTile|tile)\.get\(\s*[^,)]+\s*,\s*[^)]+\)", body):
            issues.append(f"SECTION_{section} uses tile.get(x, y), which is not a valid documented tile access pattern here.")

    if section == "TYPE_CHECK":
        if re.search(r"\braster(?:Float)?\.first\(\)\s*\._1\b", body):
            issues.append("SECTION_TYPE_CHECK treats raster.first() as a tuple, but the sampled raster tile should be used directly.")
        if re.search(r"\b(?:firstRaster|firstRasterTile|sampleTile|sampleRasterTile)\.getDataType\b", body):
            issues.append("SECTION_TYPE_CHECK calls getDataType on a raster tile, but pixelType should be used instead.")

    if section == "ANALYTICS":
        if re.search(r"\.getAttribute\(", body):
            issues.append("SECTION_ANALYTICS uses invented feature accessor getAttribute(...).")
        if re.search(r"\.getID\(", body):
            issues.append("SECTION_ANALYTICS uses invented feature accessor getID(...).")
        if re.search(r"""\.getAs\[[^\]]+\]\(\s*["'](?:neighborhood|neighborhood_name|dominant_category|zone_name)["']\s*\)""", body):
            issues.append("SECTION_ANALYTICS uses a guessed feature field name that is not grounded in API_DOC or CURRENT_SCALA.")

    if section == "OUTPUT":
        if section_is_effectively_placeholder(body, "OUTPUT") and (
            "must_persist_final_artifact" in invariants
            or "must_write_tabular_output" in invariants
            or "must_use_distributed_csv_output" in invariants
        ):
            issues.append("SECTION_OUTPUT is effectively placeholder-only, but the workflow contract requires a real persisted artifact.")
        if "must_persist_final_artifact" in invariants:
            if not re.search(r"\.saveAsGeoTiff\(|csv|writerows\(|writeheader\(|open\(|Files\.write\(|saveAsTextFile\(", body, flags=re.IGNORECASE):
                issues.append("SECTION_OUTPUT does not appear to persist a final artifact.")
        if "must_write_tabular_output" in invariants:
            if ".saveAsGeoTiff(" in body:
                issues.append("SECTION_OUTPUT writes a raster artifact even though the workflow expects tabular output.")
            if not re.search(r"csv|writerows\(|writeheader\(|open\(|Files\.write\(|saveAsTextFile\(", body, flags=re.IGNORECASE):
                issues.append("SECTION_OUTPUT does not include tabular/file-writing logic for the planned output artifact.")
        if re.search(r"FileWriter\s*\(\s*\"file:/", body):
            issues.append("SECTION_OUTPUT passes a file: URI directly to FileWriter instead of converting it to a local filesystem path.")
        if re.search(r"\bFiles\.write\(\s*Paths\.get\(outputPath\)", body):
            issues.append("SECTION_OUTPUT passes the URI-style `outputPath` directly into `Paths.get(...)`; convert it to a local filesystem path first or use a distributed writer.")
        if re.search(r"\.write(?:\.[A-Za-z_][A-Za-z0-9_]*)*\.csv\(", body) and ".mode(\"overwrite\")" not in body and ".mode('overwrite')" not in body:
            issues.append("SECTION_OUTPUT uses Spark CSV output without overwrite mode, which is brittle across benchmark reruns.")
        if re.search(r"\.write(?:\.[A-Za-z_][A-Za-z0-9_]*)*\.csv\(", body) and re.search(r"\barray<|\bstruct<|ArrayType|StructType|StructField|\bRow\b", body):
            issues.append("SECTION_OUTPUT appears to send nested schema data directly to CSV instead of flattening or serializing it first.")
        if "must_consume_output_rows_variable" in invariants:
            if not re.search(r"\boutputRows\b", body):
                issues.append("SECTION_OUTPUT must consume the canonical `outputRows` variable from SECTION_ANALYTICS.")
            if re.search(r"\bzonalStats\b", body):
                issues.append("SECTION_OUTPUT should persist `outputRows` directly instead of reinterpreting raw `zonalStats` tuples.")

    return issues


def extract_assigned_api_variables(scala_text: str) -> dict[str, str]:
    assignments: dict[str, str] = {}
    pattern = re.compile(r"(?m)\bval\s+([A-Za-z_][A-Za-z0-9_]*)\b[^=]*=\s*(.+)$")
    api_patterns = [
        ("raptorJoin", re.compile(r"\.(?:raptorJoin|mask)\(")),
        ("mapPixels", re.compile(r"\.mapPixels\(")),
        ("flatten", re.compile(r"\.flatten\b")),
        ("saveAsGeoTiff", re.compile(r"\.saveAsGeoTiff\(")),
        ("geoTiff", re.compile(r"\.geoTiff(?:\[[^\]]+\])?\(")),
        ("shapefile", re.compile(r"\.shapefile\(")),
    ]
    for match in pattern.finditer(scala_text or ""):
        var_name = match.group(1)
        rhs = match.group(2)
        for api_name, api_pattern in api_patterns:
            if api_pattern.search(rhs):
                assignments[var_name] = api_name
                break
    return assignments


def find_lineage_issues(
    full_scala_text: str,
    section: str,
    section_body: str,
    task_type: str,
    required_calls: list[str],
) -> list[str]:
    issues: list[str] = []
    assignments = extract_assigned_api_variables(full_scala_text)

    if section == "ANALYTICS" and task_type == "zonal_stats" and "raptorJoin" in required_calls:
        joined_vars = [name for name, api in assignments.items() if api == "raptorJoin"]
        if joined_vars:
            if re.search(r"\b(?:raster|rasterFloat)\.flatten\b", section_body or ""):
                issues.append("SECTION_ANALYTICS uses raw raster flatten instead of consuming the joined raster-vector result.")
            if not any(re.search(rf"\b{re.escape(var_name)}\b", section_body or "") for var_name in joined_vars):
                issues.append("SECTION_ANALYTICS does not consume the joined result produced earlier in the pipeline.")

    return issues


def find_symbol_scope_issues(
    full_scala_text: str,
    section: str,
    section_body: str,
    planned_sections: list[str],
    analysis: dict | None = None,
    contract: dict | None = None,
) -> list[str]:
    current_body = section_body or ""
    if not current_body.strip():
        return []

    analysis_info = analysis or {}
    contract_info = contract or {}
    known_symbols = {"sc", "spark"}
    inputs_body = extract_section_body(full_scala_text or "", "INPUTS")
    known_symbols.update(_extract_assigned_variables(inputs_body))

    try:
        section_idx = planned_sections.index(section)
    except ValueError:
        section_idx = -1

    current_assigned = set(_extract_assigned_variables(current_body))
    known_symbols.update(current_assigned)

    if section_idx >= 0:
        for prev in planned_sections[:section_idx]:
            prev_body = extract_section_body(full_scala_text or "", prev)
            known_symbols.update(_extract_assigned_variables(prev_body))

    intermediate_contracts = dict(analysis_info.get("intermediate_contracts", {}) or {})
    expected_symbol_map = {
        "loaded_raster_and_vector_inputs": {"raster", "vector"},
        "loaded_raster_inputs": {"raster"},
        "validated_type_assumptions": {"raster"},
        "validated_spatial_compatibility": {"raster"},
        "raster_or_transformed_raster": {"raster", "transformedRaster", "maskedRaster"},
        "transformed_raster": {"transformedRaster", "maskedRaster"},
        "joined_records": {"joinedRecords"},
        "flat_tabular_rows": {"summaryRows", "summaryDf"},
        "analysis_result": {"summaryRows", "summaryDf"},
    }
    expected_symbols: set[str] = set()
    for prev in planned_sections[:section_idx] if section_idx >= 0 else []:
        expected_symbols.update(expected_symbol_map.get(intermediate_contracts.get(prev, ""), set()))
    expected_symbols.update(expected_symbol_map.get(contract_info.get("produces_shape", ""), set()))
    expected_symbols.update(expected_symbol_map.get(intermediate_contracts.get(section, ""), set()))
    required_inputs = contract_info.get("required_inputs", []) or []
    for required_input in required_inputs:
        expected_symbols.update(expected_symbol_map.get(required_input, set()))

    fallback_symbols = {
        "raster",
        "vector",
        "joinedRecords",
    }
    watched_symbols = expected_symbols or fallback_symbols
    referenced = {
        name
        for name in watched_symbols
        if re.search(rf"\b{re.escape(name)}\b", current_body)
    }
    missing = sorted(name for name in referenced if name not in known_symbols)
    return [
        f"SECTION_{section} references `{name}` but that variable is not assigned in SECTION_INPUTS, an earlier section, or the current section."
        for name in missing
    ]


def build_semantic_feedback(section: str, verdict: dict) -> str:
    issues = verdict.get("issues", [])
    fix = verdict.get("fix", "")
    section_hint = ""

    if section == "OUTPUT":
        joined_issues = "\n".join(issues)
        if (
            "distributed Spark-style text/CSV output path" in joined_issues
            or "concrete distributed output call" in joined_issues
            or "placeholder-only" in joined_issues
        ):
            section_hint = (
                "\n- Consume the assigned analytics result directly in the write step.\n"
                "- Keep OUTPUT focused on persistence instead of recomputing analytics.\n"
                "- Do not leave OUTPUT as comments plus the step marker.\n"
            )
    elif section == "ANALYTICS":
        joined_issues = "\n".join(issues)
        if (
            "flat tabular rows" in joined_issues
            or "Window-based analytics" in joined_issues
            or "struct-based nested analytics" in joined_issues
        ):
            section_hint = (
                "\n- Prefer a direct flat-row aggregation pattern:\n"
                "  `joinedRecords.map(... => ((zoneKey, classValue), 1L)).reduceByKey(_ + _)`\n"
                "  then derive per-zone totals and emit `(zone_key, class_value, count, percentage)` rows.\n"
                "- Avoid `Window.partitionBy(...)` and nested `struct(...)` output when the contract requires flat rows.\n"
            )

    if section == "FINAL":
        return (
            "Semantic check failed for FINAL whole-program review.\n\n"
            f"ISSUES:\n" + "\n".join(f"- {issue}" for issue in issues) + "\n\n"
            f"FIX:\n{fix}\n\n"
            "REPAIR_INSTRUCTION:\n"
            "- This is a whole-program mismatch across multiple sections, not a single-section repair.\n"
            "- Review SECTION_TRANSFORM, SECTION_ANALYTICS, and SECTION_OUTPUT together.\n"
            "- Ensure analytics consumes the joined or masked raster-vector result when the task is zonal statistics.\n"
            "- Ensure the output format matches the Python workflow intent."
        )
    return (
        f"Semantic check failed for SECTION_{section}.\n\n"
        f"ISSUES:\n" + "\n".join(f"- {issue}" for issue in issues) + "\n\n"
        f"FIX:\n{fix}\n\n"
        f"REPAIR_INSTRUCTION:\n"
        f"- Keep all repairs inside SECTION_{section}.\n"
        f"- Use exact API symbols and valid parameter lists from the provided context.\n"
        f"- Do not invent constants, option objects, or overloads.\n"
        f"- Prefer cheap sanity checks like `take(1)` or metadata reuse over `count()` on large raster data."
        f"{section_hint}"
    )


def build_run_failure_feedback(section: str, failure_excerpt: str, failed_section_apis: list[str], api_fix_guides: str) -> str:
    api_fix_guides_block = f"\n\n{api_fix_guides}\n" if api_fix_guides else ""
    extra_hints = []
    if "filealreadyexistsexception" in failure_excerpt.lower() or "already exists" in failure_excerpt.lower():
        extra_hints.append("- If the failure is an output-path collision, use overwrite mode or a unique `outputPath` per run.")
    if ".sum()" in failure_excerpt and "found   : double" in failure_excerpt.lower() and "required: long" in failure_excerpt.lower():
        extra_hints.append("- If the failing expression is `sum()`, treat it as `Double` unless you explicitly convert it.")
    extra_hint_block = ("\n" + "\n".join(extra_hints)) if extra_hints else ""
    return (
        f"Run failed for SECTION_{section}.\n\n"
        f"COMPILE_AND_RUNTIME_ERRORS:\n{failure_excerpt}\n\n"
        f"FAILED_SECTION_APIS:\n{', '.join(failed_section_apis) if failed_section_apis else '(none detected)'}"
        f"{api_fix_guides_block}\n\n"
        f"REPAIR_INSTRUCTION:\n"
        f"- Use the error excerpt to identify the exact failing symbol, type, or call.\n"
        f"- Use the API fix guide snippet only as the local repair pattern.\n"
        f"- Keep all repairs inside SECTION_{section}.\n"
        f"- Prefer the smallest code change that resolves the compile failure.\n"
        f"- When repairing validation or logging code, prefer `take(1)` over `count()` on large raster data."
        f"{extra_hint_block}"
    )


def find_full_program_issues(full_scala_text: str, python_analysis: dict) -> list[str]:
    issues: list[str] = []
    analysis = python_analysis or {}
    task_type = analysis.get("task_type", "")
    final_artifact_type = analysis.get("final_artifact_type", "")
    output_mode = analysis.get("output_mode", "")
    analytics_output_shape = analysis.get("analytics_output_shape", "")

    analytics_body_match = re.search(
        r"(?ms)// TODO SECTION_ANALYTICS_START\s*(.*?)^\s*// TODO SECTION_ANALYTICS_END\s*$",
        full_scala_text or "",
    )
    analytics_body = analytics_body_match.group(1).strip() if analytics_body_match else ""
    output_body_match = re.search(
        r"(?ms)// TODO SECTION_OUTPUT_START\s*(.*?)^\s*// TODO SECTION_OUTPUT_END\s*$",
        full_scala_text or "",
    )
    output_body = output_body_match.group(1).strip() if output_body_match else ""

    if task_type == "zonal_stats":
        issues.extend(find_lineage_issues(full_scala_text, "ANALYTICS", analytics_body, task_type, ["raptorJoin"]))

    if analytics_output_shape in ("tabular_rows", "summary_map"):
        if re.search(r"(?m)^\s*println\(", analytics_body) and not re.search(r"(?m)\bval\s+[A-Za-z_][A-Za-z0-9_]*\b", analytics_body):
            issues.append("Whole-program analytics is console-only, but the workflow contract expects reusable analytics results.")

    return list(dict.fromkeys(issues))


def build_final_review_prompt(full_scala_text: str, python_analysis: dict, api_doc_text: str) -> str:
    analysis = python_analysis or {}
    return f"""Review the full generated Scala program against the source workflow intent.

Judge only end-to-end translation correctness:
- whether later sections consume the right variables from earlier sections
- whether the full pipeline preserves the source task semantics

Do not focus on style.
Return JSON only:
{{
  "ok": true,
  "issues": [],
  "fix": ""
}}

TASK_ANALYSIS:
- task_type: {analysis.get("task_type", "")}
- task_label: {analysis.get("task_label", "")}
- operations: {analysis.get("operations", [])}
- raster_inputs: {analysis.get("raster_inputs", [])}
- vector_inputs: {analysis.get("vector_inputs", [])}
- output_candidates: {analysis.get("output_candidates", [])}
- analytics_output_shape: {analysis.get("analytics_output_shape", "")}
- final_artifact_type: {analysis.get("final_artifact_type", "")}
- output_mode: {analysis.get("output_mode", "")}
- output_fields: {analysis.get("output_fields", [])}
- workflow_stages: {analysis.get("workflow_stages", [])}
- transform_family: {analysis.get("transform_family", "")}
- analytics_kind: {analysis.get("analytics_kind", "")}
- expected_intermediate: {analysis.get("expected_intermediate", "")}

STRUCTURED_ANALYSIS_IR:
{json.dumps(analysis.get("semantic_ir", {}), indent=2, sort_keys=True)}

API_DOC:
{api_doc_text}

FULL_SCALA:
{full_scala_text}
"""
