from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import TypedDict
from urllib.parse import unquote, urlparse

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langchain_core.runnables import RunnableConfig

# Allow running this file directly from inside the package directory.
PACKAGE_DIR = Path(__file__).resolve().parent
PACKAGE_PARENT = PACKAGE_DIR.parent
if str(PACKAGE_PARENT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_PARENT))

from rdpro_section_codegen.analyzer import analyze_python_script
from rdpro_section_codegen import AnalysisResult, build_plan, extract_called_apis, render_api_fix_guides
from rdpro_section_codegen.compile_runner import run_compile_package_submit
from rdpro_section_codegen.contracts import build_section_contract, render_section_contract
from rdpro_section_codegen.file_utils import read_text, to_uri, write_text
from rdpro_section_codegen.section_text import (
    contains_placeholder_paths,
    edited_outside_active_section,
    error_excerpt,
    extract_section_body,
    set_section_body,
    strip_fences,
)
from rdpro_section_codegen.validation_checks import (
    build_final_review_prompt,
    build_run_failure_feedback,
    build_semantic_feedback,
    build_semantic_prompt,
    find_contract_shape_issues,
    find_full_program_issues,
    find_missing_required_calls,
    find_lineage_issues,
    find_relevant_api_doc_sections,
    find_symbol_scope_issues,
    parse_semantic_verdict,
    section_is_effectively_placeholder,
    validate_candidate_scope,
)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except Exception:
    ChatGoogleGenerativeAI = None

SECTIONS = [
    "LOAD_DATA",
    "TYPE_CHECK",
    "SPATIAL_CHECK",
    "TRANSFORM",
    "RASTER_VECTOR_JOIN",
    "ANALYTICS",
    "OUTPUT",
]


class AgentState(TypedDict, total=False):
    section_idx: int
    retries_in_section: int
    total_turns: int
    done: bool
    success: bool
    fail_reason: str

    guide_text: str
    api_doc_text: str
    python_source_text: str
    input_mode: str
    problem_text: str
    analysis: dict
    current_scala: str

    prompt: str
    feedback: str
    candidate_scala: str
    validation_ok: bool
    semantic_ok: bool
    final_review_ok: bool

    run_ok: bool
    run_report_path: str
    run_merged_path: str
    run_stdout_tail: str
    run_stderr_tail: str
    run_compile_seconds: float
    run_jar_seconds: float
    run_submit_seconds: float
    run_total_seconds: float

    llm_prompt_tokens: int
    llm_completion_tokens: int
    llm_total_tokens: int
    llm_seconds: float

    metrics_events: list[dict]
    trace_events: list[dict]
    active_section_apis: list[str]
    active_api_fix_guides: str
    planned_sections: list[str]


class Config(TypedDict):
    scaffold_path: str
    python_input_path: str
    output_scala_path: str
    work_dir: str
    provider: str
    model: str
    max_retries_per_section: int
    max_total_turns: int

    spark_submit: str
    env_bin: str
    rdpro_lib_dir: str
    spark_packages: str
    spark_repositories: str
    compile_timeout_seconds: int
    jar_timeout_seconds: int
    submit_timeout_seconds: int


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def current_sections(state: AgentState) -> list[str]:
    return list(state.get("planned_sections", SECTIONS))


def _analysis_from_state(state: AgentState) -> AnalysisResult:
    analysis_dict = state.get("analysis") or {}
    if analysis_dict:
        return AnalysisResult(**analysis_dict)
    return analyze_python_script(state.get("python_source_text", "") or "", task_label="")


def _analysis_from_free_text(problem_text: str, task_type: str, task_label: str) -> AnalysisResult:
    return analyze_python_script(problem_text or "", task_type=task_type, task_label=task_label)


def _extract_paths_for_raw_mode(text: str, exts: tuple[str, ...]) -> list[str]:
    pattern = r'(?:(?:file://)?/[^\s,"\')]+(?:' + "|".join(re.escape(ext) for ext in exts) + r'))'
    matches = re.findall(pattern, text or "", flags=re.IGNORECASE)
    cleaned: list[str] = []
    for value in matches:
        path = value.rstrip(".,;:")
        if path not in cleaned:
            cleaned.append(path)
    return cleaned


def _build_raw_python_mode_analysis(problem_text: str, python_source_text: str) -> AnalysisResult:
    combined = "\n".join(part for part in [python_source_text or "", problem_text or ""] if part)
    raster_inputs = _extract_paths_for_raw_mode(combined, (".tif", ".tiff", ".img", ".vrt", ".jp2", ".asc"))
    vector_inputs = _extract_paths_for_raw_mode(combined, (".shp", ".geojson", ".gpkg", ".json", ".kml"))
    final_artifact_type = "csv_file" if re.search(r"\bcsv\b", combined, flags=re.IGNORECASE) else ""
    return AnalysisResult(
        task_type="generic",
        python_raster_load_type="implicit",
        task_label="",
        raster_inputs=raster_inputs,
        vector_inputs=vector_inputs,
        output_candidates=[],
        requires_vector=bool(vector_inputs),
        final_artifact_type=final_artifact_type,
        output_mode="persisted_file" if final_artifact_type else "",
        workflow_goal="",
        analytics_kind="",
        semantic_ir={},
    )


def _infer_free_text_task(problem_text: str, cfg: Config) -> dict:
    allowed = ["generic", "raster_only", "raster_vector", "zonal_stats"]
    prompt = "\n".join(
        [
            "Read the geospatial task description and classify the dominant workflow shape.",
            f"Example task_type values: {allowed}",
            "Use task_type as a coarse routing label only.",
            "Use task_label for the specific domain description such as landcover, NDVI, change detection, or zonal statistics.",
            "Return valid JSON only:",
            '{"task_type":"...","task_label":"...","reason":"..."}',
            "",
            "Task description:",
            problem_text or "",
        ]
    )
    resp = _invoke_llm(
        system="You are a geospatial task classifier. Return one JSON object only.",
        user=prompt,
        cfg=cfg,
    )
    raw = strip_fences(resp.content if hasattr(resp, "content") else str(resp)).strip()
    match = re.search(r"\{.*\}", raw, flags=re.S)
    payload = json.loads(match.group(0) if match else raw)
    task_type = str(payload.get("task_type", "generic") or "").strip().lower()
    if task_type not in allowed:
        task_type = "generic"
    return {
        "task_type": task_type,
        "task_label": str(payload.get("task_label", "") or "").strip(),
        "reason": str(payload.get("reason", "") or "").strip(),
    }


def _generate_python_reference(problem_text: str, cfg: Config) -> str:
    prompt = "\n".join(
        [
            "Write a Python reference implementation for the geospatial task description below.",
            "Requirements:",
            "- Return Python code only, no markdown.",
            "- Prefer a clear single-file script shape with functions when useful.",
            "- Use explicit file path variables if paths are present in the task description.",
            "- If exact library behavior is unknown, keep the code conservative and readable.",
            "",
            "Task description:",
            problem_text or "",
        ]
    )
    resp = _invoke_llm(
        system="You are a strict Python geospatial code generator.",
        user=prompt,
        cfg=cfg,
    )
    return strip_fences(resp.content if hasattr(resp, "content") else str(resp))


def _build_task_section_hint(section: str, problem_text: str, analysis: AnalysisResult) -> str:
    lines = [
        f"task_type={analysis.task_type}",
        f"task_label={analysis.task_label}",
        f"operations={analysis.operations}",
        f"requires_vector={analysis.requires_vector}",
        f"transform_family={analysis.transform_family}",
        f"analytics_kind={analysis.analytics_kind}",
        f"expected_intermediate={analysis.expected_intermediate}",
    ]
    section_rules = {
        "INPUTS": "Define canonical input and output path variables only. Reuse task-provided paths, do not invent placeholder paths, and do not load raster or vector data in this section.",
        "LOAD_DATA": "Load only the datasets needed for the workflow. Reuse injected path variables; do not invent file paths.",
        "TYPE_CHECK": "Validate runtime type assumptions and cheap metadata assumptions without reshaping the pipeline.",
        "SPATIAL_CHECK": "Only add alignment logic when the workflow truly needs multi-raster spatial alignment.",
        "TRANSFORM": "Implement raster preparation before analytics. Keep whole-raster reshaping, rescaling, reprojecting, filtering, or pixel transforms here.",
        "RASTER_VECTOR_JOIN": "Implement the explicit raster-vector join stage for zonal or per-feature workflows. Materialize joinedRecords with raptorJoin here.",
        "ANALYTICS": "Aggregate the transformed result into the requested metrics. Avoid global raster summaries when the task is per-feature or zonal.",
    }
    if problem_text:
        lines.append("task_description_excerpt=" + _trim_block(problem_text, 1200).replace("\n", " "))
    lines.append(section_rules.get(section, "Implement the section contract faithfully."))
    return "\n".join(lines)


def render_analysis_ir(analysis: AnalysisResult, section: str | None = None) -> str:
    semantic_ir = dict(analysis.semantic_ir or {})
    if section:
        semantic_ir["active_section"] = {
            "section": section,
            "intent": analysis.section_intents.get(section, ""),
        }
    return json.dumps(semantic_ir, indent=2, sort_keys=True)


def render_active_section_ir(analysis: AnalysisResult, section: str) -> str:
    relevant_lineage = [
        edge for edge in (analysis.dataflow_lineage or [])
        if section.lower() in edge.lower()
        or (analysis.intermediate_contracts.get(section, "") and analysis.intermediate_contracts.get(section, "") in edge)
    ]
    payload = {
        "workflow_goal": analysis.workflow_goal,
        "task_type": analysis.task_type,
        "task_label": analysis.task_label,
        "active_section": {
            "section": section,
            "goal": analysis.section_goals.get(section, ""),
            "contract": analysis.intermediate_contracts.get(section, ""),
        },
        "shapes": {
            "expected_intermediate": analysis.expected_intermediate,
            "transform_result_shape": analysis.transform_result_shape,
            "analytics_result_shape": analysis.analytics_result_shape,
            "output_required_input_shape": analysis.output_required_input_shape,
        },
        "constraints": {
            "operations": analysis.operations,
            "transform_family": analysis.transform_family,
            "analytics_kind": analysis.analytics_kind,
            "scalability_constraints": analysis.scalability_constraints,
        },
        "relevant_lineage": relevant_lineage,
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def _extract_assigned_variables(scala_section_body: str) -> list[str]:
    return re.findall(r"(?m)\bval\s+([A-Za-z_][A-Za-z0-9_]*)\b", scala_section_body or "")


def _redact_prompt_only_helpers(section_body: str) -> str:
    body = section_body or ""
    body = re.sub(
        r'(?m)^\s*val\s+primaryVectorPath\s*=\s*primaryVectorPathOpt\.getOrElse\(throw new IllegalArgumentException\("Vector path is not defined"\)\)\s*\n?',
        "",
        body,
    )
    return body


def _render_scala_context(current_scala: str, section: str, planned_sections: list[str]) -> str:
    active_body = extract_section_body(current_scala, section)
    inputs_body = extract_section_body(current_scala, "INPUTS").strip()
    blocks = []
    if inputs_body:
        if section == "INPUTS":
            blocks.append(f"SECTION_INPUTS:\n{inputs_body}")
        else:
            input_vars = _extract_assigned_variables(inputs_body)
            blocks.append(
                "SECTION_INPUTS_VARS:\n"
                + "// Available scaffold vars: "
                + ", ".join(input_vars if input_vars else ["(none)"])
                + "\n// Reuse these variables; do not redeclare scaffold inputs in later sections."
            )
    blocks.append(f"SECTION_{section}:\n{active_body.strip() or '(empty)'}")

    try:
        idx = planned_sections.index(section)
    except ValueError:
        idx = -1

    previous_sections = planned_sections[max(0, idx - 2):idx] if idx >= 0 else []
    for prev in previous_sections:
        prev_body = extract_section_body(current_scala, prev).strip()
        prev_body = _redact_prompt_only_helpers(prev_body)
        if prev_body and not section_is_effectively_placeholder(prev_body, prev):
            prev_vars = _extract_assigned_variables(prev_body)
            blocks.append(
                f"SECTION_{prev}_SUMMARY:\n"
                + "// Assigned vars: "
                + ", ".join(prev_vars if prev_vars else ["(none)"])
            )
    return "\n\n".join(blocks)


def _render_in_scope_variables(current_scala: str, section: str, planned_sections: list[str]) -> str:
    vars_in_scope: list[str] = []

    def add_vars(section_body: str) -> None:
        for name in _extract_assigned_variables(section_body):
            if name == "primaryVectorPath":
                continue
            if name not in vars_in_scope:
                vars_in_scope.append(name)

    inputs_body = extract_section_body(current_scala or "", "INPUTS")
    add_vars(inputs_body)

    try:
        idx = planned_sections.index(section)
    except ValueError:
        idx = -1

    if idx >= 0:
        for prev in planned_sections[:idx]:
            prev_body = extract_section_body(current_scala or "", prev)
            if prev_body and not section_is_effectively_placeholder(prev_body, prev):
                add_vars(prev_body)

    return ", ".join(vars_in_scope) if vars_in_scope else "(none)"


def _render_reuse_variables(current_scala: str, section: str, planned_sections: list[str]) -> str:
    preferred: list[str] = []

    def maybe_add(name: str) -> None:
        if name and name not in preferred:
            preferred.append(name)

    vars_in_scope = _render_in_scope_variables(current_scala, section, planned_sections)
    available = [v.strip() for v in vars_in_scope.split(",") if v.strip() and v.strip() != "(none)"]
    for name in ("raster", "vector", "joinedRecords", "transformedRaster", "maskedRaster", "outputPath", "primaryRasterPath", "primaryVectorPathOpt"):
        if name in available:
            maybe_add(name)
    for name in available:
        maybe_add(name)
    return ", ".join(preferred) if preferred else "(none)"


def _infer_final_repair_section(issues: list[str], planned_sections: list[str]) -> str:
    issue_text = "\n".join(issues or [])
    ordered_sections = [section for section in planned_sections if section in SECTIONS]
    for section in ordered_sections:
        if f"SECTION_{section}" in issue_text:
            return section
    if "saveAsGeoTiff" in issue_text or "output" in issue_text.lower():
        return "OUTPUT" if "OUTPUT" in ordered_sections else (ordered_sections[-1] if ordered_sections else "OUTPUT")
    if "joined result" in issue_text or "flatten" in issue_text:
        return "ANALYTICS" if "ANALYTICS" in ordered_sections else (ordered_sections[-1] if ordered_sections else "OUTPUT")
    return ordered_sections[-1] if ordered_sections else "OUTPUT"


def _file_uri_to_path(uri: str) -> Path:
    parsed = urlparse(uri)
    if parsed.scheme and parsed.scheme != "file":
        raise ValueError(f"Unsupported output URI scheme: {parsed.scheme}")
    return Path(unquote(parsed.path))


def build_inputs_section_body(analysis: AnalysisResult, work_dir: Path) -> str:
    raster_uris = [to_uri(path) for path in analysis.raster_inputs]
    vector_uris = [to_uri(path) for path in analysis.vector_inputs]

    output_seed = analysis.output_candidates[0] if analysis.output_candidates else ""
    if output_seed:
        output_uri = to_uri(output_seed)
    else:
        default_suffix = ".csv" if analysis.final_artifact_type == "csv_file" else ".tif"
        output_uri = (work_dir / "generated_output" / f"output{default_suffix}").resolve().as_uri()

    output_seed_path = _file_uri_to_path(output_uri)
    output_dir_uri = output_seed_path.parent.resolve().as_uri()
    output_basename = output_seed_path.stem or "output"
    output_extension = output_seed_path.suffix

    raster_seq = ", ".join(f'"{path}"' for path in raster_uris)
    vector_seq = ", ".join(f'"{path}"' for path in vector_uris)

    lines = [
        f"    val rasterPaths: Seq[String] = Seq({raster_seq})",
        f"    val vectorPaths: Seq[String] = Seq({vector_seq})" if vector_uris else "    val vectorPaths: Seq[String] = Seq.empty[String]",
        '    val primaryRasterPath: String = rasterPaths.headOption.getOrElse(throw new IllegalArgumentException("rasterPaths is empty"))',
        "    val primaryVectorPathOpt: Option[String] = vectorPaths.headOption",
        f'    val outputDir: String = "{output_dir_uri}"',
        f'    val outputBasename: String = "{output_basename}"',
        f'    val outputExtension: String = "{output_extension}"',
        '    val outputRunTag: String = java.util.UUID.randomUUID().toString.replace("-", "")',
        '    val outputPath: String = s"${outputDir}/${outputBasename}_${outputRunTag}${outputExtension}"',
    ]
    return "\n".join(lines)


def _extract_token_usage(resp) -> tuple[int, int, int]:
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0

    usage_meta = getattr(resp, "usage_metadata", None) or {}
    if usage_meta:
        prompt_tokens = int(usage_meta.get("input_tokens", 0) or 0)
        completion_tokens = int(usage_meta.get("output_tokens", 0) or 0)
        total_tokens = int(usage_meta.get("total_tokens", 0) or 0)

    if total_tokens == 0:
        rm = getattr(resp, "response_metadata", None) or {}
        tk = rm.get("token_usage", {}) if isinstance(rm, dict) else {}
        prompt_tokens = int(tk.get("prompt_tokens", prompt_tokens) or prompt_tokens)
        completion_tokens = int(tk.get("completion_tokens", completion_tokens) or completion_tokens)
        total_tokens = int(tk.get("total_tokens", total_tokens) or total_tokens)

    return prompt_tokens, completion_tokens, total_tokens


def _metrics_with_event(state: AgentState, event: dict) -> list[dict]:
    events = list(state.get("metrics_events", []))
    events.append(event)
    return events


def _trace_with_event(state: AgentState, event: dict) -> list[dict]:
    traces = list(state.get("trace_events", []))
    section = str(event.get("section") or "")
    analysis = _analysis_from_state(state)
    contract = {}
    section_goal = ""
    section_contract_hint = ""
    if section and section in SECTIONS:
        contract = build_section_contract(
            section,
            analysis.task_type,
            capabilities=analysis.capabilities,
            analysis=analysis.to_dict(),
        )
        section_goal = str(analysis.section_goals.get(section, "") or "")
        section_contract_hint = str(analysis.intermediate_contracts.get(section, "") or "")
    trace = {
        "turn": event.get("turn", state.get("total_turns", 0)),
        "section": section,
        "result": event.get("result", ""),
        "reason": event.get("reason", ""),
        "retries_in_section": state.get("retries_in_section", 0),
        "section_goal": section_goal,
        "section_contract_hint": section_contract_hint,
        "section_contract": contract,
        "active_section_apis": list(state.get("active_section_apis", []) or []),
        "planned_sections": list(state.get("planned_sections", []) or []),
        "feedback_in": state.get("feedback", ""),
        "workflow_goal": analysis.workflow_goal,
        "output_intent": analysis.output_intent,
    }
    traces.append(trace)
    return traces


def _cfg(config: RunnableConfig) -> Config:
    return config.get("configurable", {}).get("cfg", {})


def _invoke_llm(system: str, user: str, cfg: Config):
    provider = cfg.get("provider", "openai")
    model = cfg["model"]
    if provider == "google":
        if ChatGoogleGenerativeAI is None:
            raise ImportError(
                "langchain_google_genai is not installed. "
                "Install with: pip install langchain-google-genai"
            )
        llm = ChatGoogleGenerativeAI(model=model, temperature=0)
    else:
        llm = ChatOpenAI(model=model, temperature=0)
    return llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])


def _trim_block(text: str, max_chars: int) -> str:
    value = (text or "").strip()
    if len(value) <= max_chars:
        return value
    return value[:max_chars] + "\n...[truncated]..."


def _cleanup_section_body(candidate_body: str, section: str) -> str:
    body = candidate_body or ""
    body = re.sub(r"(?m)^\s*(?://\s*)?SECTION_[A-Z_]+\s*:?\s*$\n?", "", body)
    body = re.sub(r"(?m)^\s*SECTION_INPUTS_VARS:\s*$\n?", "", body)
    body = re.sub(r"(?m)^\s*//\s*Available scaffold vars:\s*.*\n?", "", body)
    body = re.sub(r"(?m)^\s*//\s*Do not redeclare these variables in SECTION_LOAD_DATA\.\s*$\n?", "", body)
    body = re.sub(r"(?m)^\s*Do not redeclare these variables in SECTION_LOAD_DATA\.\s*$\n?", "", body)
    body = re.sub(r"(?m)^\s*//\s*Reuse these variables; do not redeclare scaffold inputs in later sections\.\s*$\n?", "", body)
    body = re.sub(r"(?m)^\s*import\s+.+\n?", "", body)
    wrapped = re.match(
        r"(?s)^\s*try\s*\{\s*(.*?)\s*\}\s*catch\s*\{\s*.*?\s*\}\s*$",
        body,
    )
    if wrapped:
        body = wrapped.group(1).strip() + "\n"
    return body


def _apply_scaffold_variable_normalization(candidate_body: str, current_scala: str) -> str:
    body = candidate_body or ""
    inputs_body = extract_section_body(current_scala or "", "INPUTS")
    has_primary_vector_opt = bool(re.search(r"\bprimaryVectorPathOpt\b", inputs_body or ""))
    if has_primary_vector_opt:
        body = re.sub(
            r"\bsc\.shapefile\(\s*primaryVectorPath\s*\)",
            'sc.shapefile(primaryVectorPathOpt.getOrElse(throw new IllegalArgumentException("Vector path is not defined")))',
            body,
        )
        body = re.sub(
            r"\bsc\.shapefile\(\s*primaryVectorPathOpt\s*\)",
            'sc.shapefile(primaryVectorPathOpt.getOrElse(throw new IllegalArgumentException("Vector path is not defined")))',
            body,
        )
        body = re.sub(
            r'(?m)^\s*val\s+primaryVectorPath\s*=\s*primaryVectorPathOpt\.getOrElse\(throw new IllegalArgumentException\("Vector path is not defined"\)\)\s*\n?',
            "",
            body,
        )
    return body


def _normalize_candidate_scala(candidate_text: str, current_scala: str, section: str) -> str:
    candidate = strip_fences(candidate_text)
    if f"// TODO SECTION_{section}_START" in candidate and f"// TODO SECTION_{section}_END" in candidate:
        candidate_body = extract_section_body(candidate, section)
        candidate_body = _cleanup_section_body(candidate_body, section)
        candidate_body = _apply_scaffold_variable_normalization(candidate_body, current_scala)
        return set_section_body(current_scala, section, candidate_body)
    candidate = _cleanup_section_body(candidate, section)
    candidate = _apply_scaffold_variable_normalization(candidate, current_scala)
    return set_section_body(current_scala, section, candidate)


def _infer_section_apis_for_prompt(section: str, section_body: str, analysis: AnalysisResult) -> list[str]:
    section_apis = extract_called_apis(section_body)
    if section_apis:
        return section_apis
    if section == "TYPE_CHECK" and analysis.raster_inputs:
        return ["geoTiff"]
    if section == "OUTPUT":
        if analysis.final_artifact_type == "csv_file":
            return ["csv output"]
        if analysis.final_artifact_type == "raster_file":
            return ["saveAsGeoTiff"]
    if section == "RASTER_VECTOR_JOIN" and (analysis.requires_vector or analysis.task_type == "zonal_stats"):
        return ["raptorJoin"]
    if section == "ANALYTICS":
        if analysis.requires_vector or analysis.task_type == "zonal_stats":
            return ["raptorJoin"]
        if analysis.raster_only_subtype == "categorical_summary" or (analysis.raster_inputs and not analysis.requires_vector):
            return ["flatten"]
    return []


def _build_retry_hint(section: str, current_scala: str, analysis: AnalysisResult) -> str:
    if section == "TYPE_CHECK":
        in_scope = _render_in_scope_variables(current_scala, section, SECTIONS)
        available = {v.strip() for v in in_scope.split(",") if v.strip() and v.strip() != "(none)"}
        sampled_name = ""
        for candidate in ("firstRasterTile", "firstRaster", "sampleTile", "sampleRasterTile"):
            if candidate in available:
                sampled_name = candidate
                break
        sample_line = (
            f"- Reuse `{sampled_name}` for `pixelType` inspection instead of creating a new sampled helper."
            if sampled_name
            else "- If no sampled raster variable exists yet, sample once with `raster.first()` and reuse that value locally."
        )
        return (
            "RETRY_HINT:\n"
            "- Reuse the loaded raster variable from CURRENT_SCALA.\n"
            f"{sample_line}\n"
            "- Compare against Spark SQL type objects like `IntegerType`, `FloatType`, or `DoubleType`.\n"
            "- Do not use `raster.first()._1` or `getDataType` on a tile."
        )
    if section == "OUTPUT" and analysis.final_artifact_type == "csv_file":
        return (
            "RETRY_HINT:\n"
            "- Reuse the analytics result already assigned in CURRENT_SCALA.\n"
            "- Keep OUTPUT focused on final persistence only; do not recompute analytics here.\n"
            "- Do not leave OUTPUT as comments only."
        )
    return ""


def _build_compact_analysis_block(section: str, analysis: AnalysisResult, input_mode: str, python_source_text: str) -> str:
    if input_mode == "via-python-raw":
        return "\n".join(
            [
                "PYTHON_SOURCE_TO_TRANSLATE:",
                _trim_block(python_source_text or "", 3500) or "(none)",
            ]
        )
    lines = [
        "TASK_CONTEXT:",
        f"- task_type: {analysis.task_type}",
        f"- requires_vector: {analysis.requires_vector}",
        f"- final_artifact_type: {analysis.final_artifact_type}",
        f"- analytics_kind: {analysis.analytics_kind}",
        f"- active_section_goal: {analysis.section_goals.get(section, '')}",
        f"- active_section_contract: {analysis.intermediate_contracts.get(section, '')}",
    ]
    if analysis.raster_only_subtype:
        lines.append(f"- raster_only_subtype: {analysis.raster_only_subtype}")
    lines.extend(
        [
            "",
            "STRUCTURED_ANALYSIS_IR:",
            _trim_block(render_active_section_ir(analysis, section), 1800),
        ]
    )
    return "\n".join(lines)


def _build_section_prompt_rules(section: str, analysis: AnalysisResult) -> str:
    rules = {
        "LOAD_DATA": [
            "Treat `primaryRasterPath`, `primaryVectorPathOpt`, and `outputPath` as already defined by SECTION_INPUTS.",
            "Do not redeclare scaffold input variables.",
            "Keep the load simple; use `sc.geoTiff(...)` and `sc.shapefile(primaryVectorPathOpt.getOrElse(...))` only to materialize the core inputs.",
            "Do not branch on runtime pixelType here.",
            "Do not create sampled raster helper variables such as `firstRaster` in this section.",
        ],
        "TYPE_CHECK": [
            "Validate runtime pixelType here, not in LOAD_DATA.",
            "Reuse sampled records or metadata; avoid `count()`.",
            "Do not treat `raster.first()` as a tuple or call `getDataType` on a tile.",
            "Do not declare or redefine path variables, output variables, or scaffold input variables in this section.",
            "Do not reload raster or vector data in this section; reuse `raster`, `vector`, and existing sampled values from earlier sections.",
            "If a sampled raster variable such as `firstRaster` or `firstRasterTile` already exists, reuse it instead of creating another sampled helper with the same role.",
        ],
        "TRANSFORM": [
            "Keep this section to raster preparation only.",
            "Do not perform final aggregation here.",
            "Do not place `raptorJoin` here when SECTION_RASTER_VECTOR_JOIN exists.",
            "Prefer a reusable intermediate such as `transformedRaster`, `maskedRaster`, or `validPixels`.",
        ],
        "RASTER_VECTOR_JOIN": [
            "This section should materialize the explicit raster-vector pairing.",
            "Prefer one reusable assignment such as `val joinedRecords = raster.raptorJoin(vector)`.",
            "Do not perform final grouped analytics here.",
        ],
        "ANALYTICS": [
            "Compute summaries from the upstream intermediate, not from invented helpers.",
            "For categorical raster summaries, prefer `flatten.map(_._4)` followed by Spark aggregation.",
            "Do not use `groupByKey()` for large keyed aggregation when `reduceByKey`, `aggregateByKey`, or `combineByKey` can produce the same result more scalably.",
            "Do not assign Spark numeric `sum()` directly to `Long` without conversion.",
            "Avoid invented feature accessors or guessed schema fields.",
            "Produce reusable analytics rows or summary values only.",
        ],
        "OUTPUT": [
            "Persist the final artifact through `outputPath`.",
            "Keep this section focused on final persistence only.",
            "Do not assemble large tabular outputs on the driver with `collect()` or `FileWriter`.",
        ],
    }
    section_rules = list(rules.get(section, []))
    if section == "ANALYTICS" and not analysis.requires_vector and analysis.final_artifact_type == "csv_file":
        section_rules.append("For raster-only tabular summaries, assign reusable flat rows such as `(class_value, count, percentage)`.")
    if section == "ANALYTICS" and analysis.task_type == "zonal_stats":
        section_rules.extend(
            [
                "This is zonal analytics; consume the raster-vector join result.",
                "Emit reusable flat rows such as `(zone_key, class_value, count, percentage)`.",
                "For zonal CSV workflows, persist the final tabular artifact directly in SECTION_ANALYTICS.",
            ]
        )
    if section == "OUTPUT" and analysis.task_type == "zonal_stats":
        section_rules.append("If OUTPUT is present for zonal workflows, keep it minimal and do not recompute analytics here.")
    return "\n".join(f"- {rule}" for rule in section_rules)


def node_prepare_prompt(state: AgentState, config: RunnableConfig) -> AgentState:
    section = current_sections(state)[state["section_idx"]]
    input_mode = state.get("input_mode", "")
    feedback = _trim_block(state.get("feedback") or "", 2500)
    feedback_block = f"\n\nFIX_CONTEXT:\n{feedback}\n" if feedback else ""
    section_body = extract_section_body(state.get("current_scala", ""), section)
    analysis = _analysis_from_state(state)
    section_apis = _infer_section_apis_for_prompt(section, section_body, analysis)
    api_fix_guides = render_api_fix_guides(section_apis)
    api_fix_guides_block = f"\nAPI_FIX_GUIDES:\n{api_fix_guides}\n" if api_fix_guides else ""
    section_contract_text = render_section_contract(
        section,
        analysis.task_type,
        capabilities=analysis.capabilities,
        analysis=analysis.to_dict(),
    )
    relevant_api_doc = find_relevant_api_doc_sections(
        state.get("api_doc_text", ""),
        section,
        section_apis,
        analysis.to_dict(),
    )
    prompt_task_text = _trim_block(state.get("problem_text", ""), 2500)
    prompt_current_scala = _trim_block(
        _render_scala_context(state.get("current_scala", ""), section, current_sections(state)),
        5000,
    )
    prompt_in_scope_vars = _trim_block(
        _render_in_scope_variables(state.get("current_scala", ""), section, current_sections(state)),
        1500,
    )
    prompt_reuse_vars = _trim_block(
        _render_reuse_variables(state.get("current_scala", ""), section, current_sections(state)),
        1500,
    )
    prompt_api_doc = _trim_block(relevant_api_doc, 3000)
    analysis_block = _build_compact_analysis_block(section, analysis, input_mode, state.get("python_source_text", ""))
    retry_hint_block = _build_retry_hint(section, state.get("current_scala", ""), analysis)
    retry_hint_append = f"\n\n{retry_hint_block}" if retry_hint_block else ""
    section_rules_block = _build_section_prompt_rules(section, analysis)
    if input_mode == "via-python-raw":
        section_contract_text = "Use the scaffold, in-scope variables, raw Python source, and API_DOC to fill this section."
        prompt_task_text = ""
        section_focus_text = "Translate the raw Python workflow into this Scala section without adding extra task interpretation."
    else:
        section_focus_text = _build_task_section_hint(section, state.get("problem_text", ""), analysis)
    prompt = f"""Task: Fill only SECTION_{section} in the Scala scaffold.

Hard constraints:
- Do not modify any other section.
- Keep all markers unchanged.
- Do not add `import` statements inside section bodies; imports are scaffold-owned.
- Use only methods/patterns from API_DOC.
- Must print exactly: __STEP__ {section}_done
- Return full Scala code only (no markdown).
- Treat CURRENT_SCALA as the source of truth for all existing variables and scaffold state.
- Reuse variables already defined in SECTION_INPUTS or earlier sections; do not redeclare them.
- Prefer reusing variables listed in REUSE_THESE_VARIABLES before introducing any new local helper.
- Never declare a new `val` with the same name as any variable shown in IN_SCOPE_VARIABLES or REUSE_THESE_VARIABLES.
- Only introduce a new helper variable when no existing variable already provides that value.
- Prefer cheap sanity checks like `take(1)` or metadata inspection.
- Do not use `count()` on RasterRDD or large RDDs just for logging or validation.
- Prefer distributed Spark/RDPro operations over driver-heavy `collect()` logic.
- Treat scalability as a whole-program requirement, not a per-section preference.
- Preserve reusable distributed intermediates across sections instead of recomputing them.
- Analyze the input data with your knowledge and reason about the case to choose the right scalable code.

Section order context:
{", ".join(current_sections(state))}

API_DOC:
{prompt_api_doc or "(no section-specific API doc extracted)"}

SECTION_CONTRACT:
{section_contract_text}

ACTIVE_SECTION_APIS:
{", ".join(section_apis) if section_apis else "(none yet)"}
{api_fix_guides_block}

IN_SCOPE_VARIABLES:
{prompt_in_scope_vars}

REUSE_THESE_VARIABLES:
{prompt_reuse_vars}

TASK_DESCRIPTION:
{prompt_task_text or "(none)"}

SECTION_FOCUS:
{section_focus_text}

{analysis_block}

SECTION_RULES:
{section_rules_block or "- Implement the section contract faithfully."}
{retry_hint_append}

CURRENT_SCALA:
{prompt_current_scala}
{feedback_block}
"""
    return {
        "prompt": prompt,
        "total_turns": state["total_turns"] + 1,
        "active_section_apis": section_apis,
        "active_api_fix_guides": api_fix_guides,
    }


def node_generate_candidate(state: AgentState, config: RunnableConfig) -> AgentState:
    cfg = _cfg(config)
    t0 = time.perf_counter()
    resp = _invoke_llm(
        system=(
            "You are a senior geospatial Scala engineer working with RDPro, Spark, raster, "
            "and vector analytics. Write valid production-style Scala code using only "
            "documented APIs from the provided context."
        ),
        user=state["prompt"],
        cfg=cfg,
    )
    llm_seconds = round(time.perf_counter() - t0, 4)
    pt, ct, tt = _extract_token_usage(resp)
    candidate = _normalize_candidate_scala(
        resp.content if hasattr(resp, "content") else str(resp),
        state["current_scala"],
        current_sections(state)[state["section_idx"]],
    )
    return {
        "candidate_scala": candidate,
        "llm_prompt_tokens": pt,
        "llm_completion_tokens": ct,
        "llm_total_tokens": tt,
        "llm_seconds": llm_seconds,
    }


def node_validate_scope(state: AgentState, config: RunnableConfig) -> AgentState:
    cfg = _cfg(config)
    section = current_sections(state)[state["section_idx"]]
    ok, feedback = validate_candidate_scope(
        state["candidate_scala"],
        state["current_scala"],
        section,
        edited_outside_active_section,
        contains_placeholder_paths,
    )
    if not ok:
        retries = state["retries_in_section"] + 1
        too_many = retries >= cfg["max_retries_per_section"]
        events = _metrics_with_event(
            state,
            {
                "section": section,
                "turn": state.get("total_turns", 0),
                "result": "validation_reject",
                "reason": feedback,
                "llm_prompt_tokens": state.get("llm_prompt_tokens", 0),
                "llm_completion_tokens": state.get("llm_completion_tokens", 0),
                "llm_total_tokens": state.get("llm_total_tokens", 0),
                "llm_seconds": state.get("llm_seconds", 0.0),
            },
        )
        traces = _trace_with_event(state, events[-1])
        return {
            "validation_ok": False,
            "retries_in_section": retries,
            "feedback": feedback,
            "done": too_many,
            "success": False if too_many else state.get("success", False),
            "fail_reason": f"Section {section} failed validation {retries} times" if too_many else "",
            "metrics_events": events,
            "trace_events": traces,
        }
    return {"validation_ok": True}


def node_semantic_check(state: AgentState, config: RunnableConfig) -> AgentState:
    cfg = _cfg(config)
    section = current_sections(state)[state["section_idx"]]
    candidate_body = extract_section_body(state["candidate_scala"], section)
    analysis = _analysis_from_state(state)
    python_plan = build_plan(analysis)
    contract = build_section_contract(
        section,
        python_plan.task_type,
        capabilities=analysis.capabilities,
        analysis=analysis.to_dict(),
    )
    required_calls = list(contract.get("required_calls", []) or [])
    missing_calls = find_missing_required_calls(candidate_body, required_calls)
    lineage_issues = find_lineage_issues(
        state["candidate_scala"],
        section,
        candidate_body,
        python_plan.task_type,
        required_calls,
    )
    symbol_scope_issues = find_symbol_scope_issues(
        state["candidate_scala"],
        section,
        candidate_body,
        current_sections(state),
        analysis.to_dict(),
        contract,
    )
    contract_shape_issues = find_contract_shape_issues(
        state["candidate_scala"],
        section,
        candidate_body,
        contract,
    )

    if missing_calls or lineage_issues or symbol_scope_issues or contract_shape_issues or (required_calls and section_is_effectively_placeholder(candidate_body, section)):
        retries = state["retries_in_section"] + 1
        too_many = retries >= cfg["max_retries_per_section"]
        issues: list[str] = []
        if missing_calls:
            issues.append(f"Missing required API calls for SECTION_{section}: {', '.join(missing_calls)}")
        issues.extend(lineage_issues)
        issues.extend(symbol_scope_issues)
        issues.extend(contract_shape_issues)
        if required_calls and section_is_effectively_placeholder(candidate_body, section):
            issues.append(f"SECTION_{section} is still effectively placeholder/no-op")
        fix = (
            f"Implement SECTION_{section} with the planned contract.\n"
            f"Required calls: {', '.join(required_calls) if required_calls else '(none)'}\n"
            f"Required inputs: {', '.join(contract.get('required_inputs', []) or ['(none)'])}\n"
            f"Expected output shape: {contract.get('produces_shape', '(unspecified)')}\n"
            "Do not leave the section as only comments plus the step marker."
        )
        feedback = build_semantic_feedback(section, {"issues": issues, "fix": fix})
        events = _metrics_with_event(
            state,
            {
                "section": section,
                "turn": state.get("total_turns", 0),
                "result": "semantic_reject",
                "reason": feedback,
                "llm_prompt_tokens": 0,
                "llm_completion_tokens": 0,
                "llm_total_tokens": 0,
                "llm_seconds": 0.0,
            },
        )
        traces = _trace_with_event(state, events[-1])
        return {
            "semantic_ok": False,
            "retries_in_section": retries,
            "feedback": feedback,
            "done": too_many,
            "success": False if too_many else state.get("success", False),
            "fail_reason": f"Section {section} failed semantic check after {retries} attempts" if too_many else "",
            "metrics_events": events,
            "trace_events": traces,
        }

    section_apis = extract_called_apis(candidate_body)
    api_fix_guides = render_api_fix_guides(section_apis)
    relevant_api_doc = find_relevant_api_doc_sections(
        state.get("api_doc_text", ""),
        section,
        section_apis,
        analysis.to_dict(),
    )
    prompt = build_semantic_prompt(
        section,
        candidate_body,
        relevant_api_doc,
        section_apis,
        api_fix_guides + (
            f"\n\nTASK_ANALYSIS:\n"
            f"- task_type: {analysis.task_type}\n"
            f"- task_label: {analysis.task_label}\n"
            f"- operations: {analysis.operations}\n"
            f"- raster_inputs: {analysis.raster_inputs}\n"
            f"- vector_inputs: {analysis.vector_inputs}\n"
            f"- transform_family: {analysis.transform_family}\n"
            f"- analytics_kind: {analysis.analytics_kind}\n"
            f"- expected_intermediate: {analysis.expected_intermediate}\n"
            f"\nSTRUCTURED_ANALYSIS_IR:\n{render_active_section_ir(analysis, section)}\n"
        ),
    )
    t0 = time.perf_counter()
    resp = _invoke_llm(
        system=(
            "You are a senior geospatial Scala engineer reviewing RDPro and Spark code for "
            "API correctness and workflow validity. Return JSON only."
        ),
        user=prompt,
        cfg=cfg,
    )
    llm_seconds = round(time.perf_counter() - t0, 4)
    pt, ct, tt = _extract_token_usage(resp)
    raw = strip_fences(resp.content if hasattr(resp, "content") else str(resp)).strip()
    verdict = parse_semantic_verdict(raw)

    ok = bool(verdict.get("ok"))
    if ok:
        events = _metrics_with_event(
            state,
            {
                "section": section,
                "turn": state.get("total_turns", 0),
                "result": "semantic_pass",
                "reason": "",
                "llm_prompt_tokens": pt,
                "llm_completion_tokens": ct,
                "llm_total_tokens": tt,
                "llm_seconds": llm_seconds,
            },
        )
        traces = _trace_with_event(state, events[-1])
        return {"semantic_ok": True, "metrics_events": events, "trace_events": traces}

    retries = state["retries_in_section"] + 1
    too_many = retries >= cfg["max_retries_per_section"]
    feedback = build_semantic_feedback(section, verdict)
    events = _metrics_with_event(
        state,
        {
            "section": section,
            "turn": state.get("total_turns", 0),
            "result": "semantic_reject",
            "reason": feedback,
            "llm_prompt_tokens": pt,
            "llm_completion_tokens": ct,
            "llm_total_tokens": tt,
            "llm_seconds": llm_seconds,
        },
    )
    traces = _trace_with_event(state, events[-1])
    return {
        "semantic_ok": False,
        "retries_in_section": retries,
        "feedback": feedback,
        "done": too_many,
        "success": False if too_many else state.get("success", False),
        "fail_reason": f"Section {section} failed semantic check after {retries} attempts" if too_many else "",
        "metrics_events": events,
        "trace_events": traces,
    }


def node_compile_submit(state: AgentState, config: RunnableConfig) -> AgentState:
    cfg = _cfg(config)
    section = current_sections(state)[state["section_idx"]]
    out_path = Path(cfg["output_scala_path"]).resolve()
    write_text(out_path, state["candidate_scala"])
    result = run_compile_package_submit(state["candidate_scala"], section, state["total_turns"], cfg, now_stamp)
    return {
        "run_ok": result["run_ok"],
        "run_report_path": result["report_log"],
        "run_merged_path": result["merged_log"],
        "run_stdout_tail": result["stdout_tail"],
        "run_stderr_tail": result["stderr_tail"],
        "run_compile_seconds": result["compile_seconds"],
        "run_jar_seconds": result["jar_seconds"],
        "run_submit_seconds": result["submit_seconds"],
        "run_total_seconds": result["total_seconds"],
    }


def node_evaluate(state: AgentState, config: RunnableConfig) -> AgentState:
    cfg = _cfg(config)
    section = current_sections(state)[state["section_idx"]]

    if state.get("total_turns", 0) >= cfg["max_total_turns"]:
        return {
            "done": True,
            "success": False,
            "fail_reason": f"Reached max_total_turns={cfg['max_total_turns']}",
        }

    if state.get("run_ok"):
        next_idx = state["section_idx"] + 1
        out_path = Path(cfg["output_scala_path"]).resolve()
        write_text(out_path, state["candidate_scala"])
        events = _metrics_with_event(
            state,
            {
                "section": section,
                "turn": state.get("total_turns", 0),
                "result": "success",
                "llm_prompt_tokens": state.get("llm_prompt_tokens", 0),
                "llm_completion_tokens": state.get("llm_completion_tokens", 0),
                "llm_total_tokens": state.get("llm_total_tokens", 0),
                "llm_seconds": state.get("llm_seconds", 0.0),
                "compile_seconds": state.get("run_compile_seconds", 0.0),
                "jar_seconds": state.get("run_jar_seconds", 0.0),
                "submit_seconds": state.get("run_submit_seconds", 0.0),
                "run_total_seconds": state.get("run_total_seconds", 0.0),
            },
        )
        traces = _trace_with_event(state, events[-1])

        if next_idx >= len(current_sections(state)):
            return {
                "current_scala": state["candidate_scala"],
                "section_idx": next_idx,
                "retries_in_section": 0,
                "feedback": "",
                "metrics_events": events,
                "trace_events": traces,
            }
        return {
            "current_scala": state["candidate_scala"],
            "section_idx": next_idx,
            "retries_in_section": 0,
            "feedback": "",
            "metrics_events": events,
            "trace_events": traces,
        }

    retries = state["retries_in_section"] + 1
    too_many = retries >= cfg["max_retries_per_section"]
    err_tail = (state.get("run_stderr_tail") or "")[-4000:]
    out_tail = (state.get("run_stdout_tail") or "")[-4000:]
    failed_section_body = extract_section_body(state.get("candidate_scala", ""), section)
    failed_section_apis = extract_called_apis(failed_section_body)
    api_fix_guides = render_api_fix_guides(failed_section_apis)
    failure_excerpt = error_excerpt(err_tail, out_tail, max_chars=3500)
    events = _metrics_with_event(
        state,
        {
            "section": section,
            "turn": state.get("total_turns", 0),
            "result": "run_failed",
            "llm_prompt_tokens": state.get("llm_prompt_tokens", 0),
            "llm_completion_tokens": state.get("llm_completion_tokens", 0),
            "llm_total_tokens": state.get("llm_total_tokens", 0),
            "llm_seconds": state.get("llm_seconds", 0.0),
            "compile_seconds": state.get("run_compile_seconds", 0.0),
            "jar_seconds": state.get("run_jar_seconds", 0.0),
            "submit_seconds": state.get("run_submit_seconds", 0.0),
            "run_total_seconds": state.get("run_total_seconds", 0.0),
        },
    )
    traces = _trace_with_event(state, events[-1])
    return {
        "retries_in_section": retries,
        "feedback": build_run_failure_feedback(section, failure_excerpt, failed_section_apis, api_fix_guides),
        "done": too_many,
        "success": False if too_many else state.get("success", False),
        "fail_reason": f"Section {section} failed after {retries} attempts" if too_many else "",
        "metrics_events": events,
        "trace_events": traces,
        "active_section_apis": failed_section_apis,
        "active_api_fix_guides": api_fix_guides,
    }


def route_after_validate(state: AgentState) -> str:
    if state.get("done"):
        return "end"
    if not state.get("validation_ok"):
        return "prepare_prompt"
    return "semantic_check"


def route_after_semantic(state: AgentState) -> str:
    if state.get("done"):
        return "end"
    if not state.get("semantic_ok"):
        return "prepare_prompt"
    return "compile_submit"


def route_after_evaluate(state: AgentState) -> str:
    if state.get("done"):
        return "end"
    if state.get("section_idx", 0) >= len(current_sections(state)):
        return "final_review"
    return "prepare_prompt"


def route_after_final_review(state: AgentState) -> str:
    if state.get("done"):
        return "end"
    return "prepare_prompt"


def node_final_review(state: AgentState, config: RunnableConfig) -> AgentState:
    cfg = _cfg(config)
    full_scala = state.get("current_scala", "")
    analysis = _analysis_from_state(state)
    deterministic_issues = find_full_program_issues(full_scala, analysis.to_dict())
    if deterministic_issues:
        target_section = _infer_final_repair_section(deterministic_issues, current_sections(state))
        retries = 1 if state.get("section_idx") != current_sections(state).index(target_section) else state.get("retries_in_section", 0) + 1
        too_many = retries >= cfg["max_retries_per_section"]
        feedback = build_semantic_feedback(
            "FINAL",
            {
                "issues": deterministic_issues,
                "fix": "Repair the full program so end-to-end logic matches the source workflow.",
            },
        )
        feedback += (
            f"\n\nTARGET_REPAIR_SECTION:\nSECTION_{target_section}\n"
            f"Edit SECTION_{target_section} next to address the earliest whole-program mismatch."
        )
        return {
            "final_review_ok": False,
            "done": too_many,
            "success": False if too_many else state.get("success", False),
            "fail_reason": "Final whole-program review failed" if too_many else "",
            "feedback": feedback,
            "section_idx": current_sections(state).index(target_section),
            "retries_in_section": retries,
        }

    prompt = build_final_review_prompt(
        full_scala,
        analysis.to_dict(),
        _trim_block(state.get("api_doc_text", ""), 12000),
    )
    t0 = time.perf_counter()
    resp = _invoke_llm(
        system="You are a strict Scala end-to-end translation reviewer. Return JSON only.",
        user=prompt,
        cfg=cfg,
    )
    llm_seconds = round(time.perf_counter() - t0, 4)
    pt, ct, tt = _extract_token_usage(resp)
    raw = strip_fences(resp.content if hasattr(resp, "content") else str(resp)).strip()
    verdict = parse_semantic_verdict(raw)
    ok = bool(verdict.get("ok"))
    events = _metrics_with_event(
        state,
        {
            "section": "FINAL",
            "turn": state.get("total_turns", 0),
            "result": "final_review_pass" if ok else "final_review_reject",
            "reason": "" if ok else ((str(verdict)[:500] + "...") if len(str(verdict)) > 500 else str(verdict)),
            "llm_prompt_tokens": pt,
            "llm_completion_tokens": ct,
            "llm_total_tokens": tt,
            "llm_seconds": llm_seconds,
        },
    )
    traces = _trace_with_event(state, events[-1])
    if ok:
        return {
            "final_review_ok": True,
            "done": True,
            "success": True,
            "fail_reason": "",
            "metrics_events": events,
            "trace_events": traces,
        }
    feedback = build_semantic_feedback("FINAL", verdict)
    target_section = _infer_final_repair_section(list(verdict.get("issues", []) or []), current_sections(state))
    retries = 1 if state.get("section_idx") != current_sections(state).index(target_section) else state.get("retries_in_section", 0) + 1
    too_many = retries >= cfg["max_retries_per_section"]
    feedback += (
        f"\n\nTARGET_REPAIR_SECTION:\nSECTION_{target_section}\n"
        f"Edit SECTION_{target_section} next to address the earliest whole-program mismatch."
    )
    return {
        "final_review_ok": False,
        "done": too_many,
        "success": False if too_many else state.get("success", False),
        "fail_reason": "Final whole-program review failed" if too_many else "",
        "feedback": feedback,
        "metrics_events": events,
        "trace_events": traces,
        "section_idx": current_sections(state).index(target_section),
        "retries_in_section": retries,
    }


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("prepare_prompt", node_prepare_prompt)
    g.add_node("generate_candidate", node_generate_candidate)
    g.add_node("validate_scope", node_validate_scope)
    g.add_node("semantic_check", node_semantic_check)
    g.add_node("compile_submit", node_compile_submit)
    g.add_node("evaluate", node_evaluate)
    g.add_node("final_review", node_final_review)

    g.add_edge(START, "prepare_prompt")
    g.add_edge("prepare_prompt", "generate_candidate")
    g.add_edge("generate_candidate", "validate_scope")
    g.add_conditional_edges(
        "validate_scope",
        route_after_validate,
        {
            "prepare_prompt": "prepare_prompt",
            "semantic_check": "semantic_check",
            "compile_submit": "compile_submit",
            "end": END,
        },
    )
    g.add_conditional_edges(
        "semantic_check",
        route_after_semantic,
        {
            "prepare_prompt": "prepare_prompt",
            "compile_submit": "compile_submit",
            "end": END,
        },
    )
    g.add_edge("compile_submit", "evaluate")
    g.add_conditional_edges(
        "evaluate",
        route_after_evaluate,
        {
            "prepare_prompt": "prepare_prompt",
            "final_review": "final_review",
            "end": END,
        },
    )
    g.add_conditional_edges(
        "final_review",
        route_after_final_review,
        {
            "prepare_prompt": "prepare_prompt",
            "end": END,
        },
    )
    return g.compile()


def parse_args() -> argparse.Namespace:
    default_root = Path("/Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook")
    doc_root = Path("/Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Doc")
    default_scaffold = default_root / "rdpro_section_codegen" / "job_scaffold.scala"
    default_output_scala = default_root / "rdpro_section_codegen" / "one_shot_output_sectional.scala"
    parser = argparse.ArgumentParser(description="Section-by-section Scala migration agent with LangGraph")
    parser.add_argument("--guide", default=str(default_root / "RDProAgentLoop_perAPI_fix_migration_guide.md"))
    parser.add_argument("--api-doc", default=str(doc_root / "rdpro_api_doc_combined.md"))
    parser.add_argument("--scaffold", default=str(default_scaffold))
    parser.add_argument("--python-input", default=str(default_root / "../python/ndvi.py"))
    parser.add_argument("--output-scala", default=str(default_output_scala))
    parser.add_argument("--work-dir", default=str(default_root / "agent_runs"))
    parser.add_argument("--provider", choices=["openai", "google"], default="openai")
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument(
        "--translation-mode",
        choices=["python-script", "direct", "via-python", "via-python-raw"],
        default="python-script",
    )
    parser.add_argument("--free-text", default="")
    parser.add_argument("--max-retries-per-section", type=int, default=5)
    parser.add_argument("--max-total-turns", type=int, default=40)
    parser.add_argument("--compile-timeout-seconds", type=int, default=120)
    parser.add_argument("--jar-timeout-seconds", type=int, default=60)
    parser.add_argument("--submit-timeout-seconds", type=int, default=900)

    parser.add_argument("--spark-submit", default="/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/spark-submit")
    parser.add_argument("--env-bin", default="/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin")
    parser.add_argument(
        "--rdpro-lib-dir",
        default="/Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/beast-0.10.2-SNAPSHOT-bin/beast-0.10.2-SNAPSHOT/lib",
    )
    parser.add_argument(
        "--spark-packages",
        default=(
            "org.locationtech.jts:jts-core:1.19.0,"
            "org.geotools:gt-referencing:24.1,"
            "org.geotools:gt-epsg-hsql:24.1,"
            "org.geotools:gt-geotiff:24.1,"
            "org.geotools:gt-coverage:24.1,"
            "it.geosolutions.imageio-ext:imageio-ext-tiff:1.4.14"
        ),
    )
    parser.add_argument(
        "--spark-repositories",
        default="https://repo.osgeo.org/repository/geotools-releases/,https://repo.osgeo.org/repository/release/",
    )
    return parser.parse_args()


def write_metrics_csv(path: Path, events: list[dict]) -> None:
    fields = [
        "section",
        "turn",
        "result",
        "reason",
        "llm_prompt_tokens",
        "llm_completion_tokens",
        "llm_total_tokens",
        "llm_seconds",
        "compile_seconds",
        "jar_seconds",
        "submit_seconds",
        "run_total_seconds",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for ev in events:
            w.writerow({k: ev.get(k, "") for k in fields})


def main() -> None:
    args = parse_args()

    guide_path = Path(args.guide).resolve()
    api_doc_path = Path(args.api_doc).resolve()
    scaffold_path = Path(args.scaffold).resolve()
    output_scala_path = Path(args.output_scala).resolve()
    if output_scala_path == scaffold_path:
        raise ValueError("--output-scala must be a separate file and cannot equal --scaffold")
    work_dir = Path(args.work_dir).resolve()
    work_dir.mkdir(parents=True, exist_ok=True)

    cfg: Config = {
        "scaffold_path": str(scaffold_path),
        "python_input_path": str(Path(args.python_input).resolve()),
        "output_scala_path": str(output_scala_path),
        "work_dir": str(work_dir),
        "provider": args.provider,
        "model": args.model,
        "max_retries_per_section": args.max_retries_per_section,
        "max_total_turns": args.max_total_turns,
        "spark_submit": args.spark_submit,
        "env_bin": args.env_bin,
        "rdpro_lib_dir": args.rdpro_lib_dir,
        "spark_packages": args.spark_packages,
        "spark_repositories": args.spark_repositories,
        "compile_timeout_seconds": args.compile_timeout_seconds,
        "jar_timeout_seconds": args.jar_timeout_seconds,
        "submit_timeout_seconds": args.submit_timeout_seconds,
    }

    if args.translation_mode != "python-script" and not args.free_text.strip():
        raise ValueError("--free-text is required when --translation-mode is direct, via-python, or via-python-raw")

    python_source_text = ""
    problem_text = (args.free_text or "").strip()
    input_mode = args.translation_mode
    generated_python_path = ""

    if args.translation_mode == "python-script":
        python_input_path = Path(args.python_input).resolve()
        python_source_text = read_text(python_input_path) if python_input_path.exists() else ""
        analysis = analyze_python_script(python_source_text)
    else:
        task_info = None
        if args.translation_mode in {"direct", "via-python"}:
            task_info = _infer_free_text_task(problem_text, cfg)
        if args.translation_mode in {"via-python", "via-python-raw"}:
            python_source_text = _generate_python_reference(problem_text, cfg)
            compile(python_source_text, "<generated_python_reference>", "exec")
            if args.translation_mode == "via-python":
                analysis = analyze_python_script(
                    python_source_text,
                    task_type=task_info["task_type"],
                    task_label=task_info["task_label"],
                )
            else:
                analysis = _build_raw_python_mode_analysis(problem_text, python_source_text)
            generated_python_path = str((work_dir / f"generated_python_reference_{now_stamp()}.py").resolve())
            write_text(Path(generated_python_path), python_source_text)
        else:
            analysis = _analysis_from_free_text(problem_text, task_info["task_type"], task_info["task_label"])

    planned_sections = list(SECTIONS if args.translation_mode == "via-python-raw" else (build_plan(analysis).sections or SECTIONS))

    init_state: AgentState = {
        "section_idx": 0,
        "retries_in_section": 0,
        "total_turns": 0,
        "done": False,
        "success": False,
        "fail_reason": "",
        "guide_text": read_text(guide_path) if guide_path.exists() else "",
        "api_doc_text": read_text(api_doc_path) if api_doc_path.exists() else "",
        "python_source_text": python_source_text,
        "input_mode": input_mode,
        "problem_text": problem_text,
        "analysis": analysis.to_dict(),
        "current_scala": read_text(scaffold_path),
        "feedback": "",
        "metrics_events": [],
        "trace_events": [],
        "planned_sections": planned_sections,
    }
    init_state["current_scala"] = set_section_body(
        init_state["current_scala"],
        "INPUTS",
        build_inputs_section_body(analysis, work_dir),
    )
    write_text(output_scala_path, init_state["current_scala"])

    app = build_graph()
    final_state = app.invoke(init_state, config={"configurable": {"cfg": cfg}})

    events = list(final_state.get("metrics_events", []))
    trace_events = list(final_state.get("trace_events", []))
    total_prompt_tokens = sum(int(ev.get("llm_prompt_tokens", 0) or 0) for ev in events)
    total_completion_tokens = sum(int(ev.get("llm_completion_tokens", 0) or 0) for ev in events)
    total_tokens = sum(int(ev.get("llm_total_tokens", 0) or 0) for ev in events)
    total_llm_seconds = round(sum(float(ev.get("llm_seconds", 0.0) or 0.0) for ev in events), 4)
    total_run_seconds = round(sum(float(ev.get("run_total_seconds", 0.0) or 0.0) for ev in events), 4)

    summary = {
        "success": final_state.get("success", False),
        "done": final_state.get("done", False),
        "input_mode": input_mode,
        "generated_python_reference": generated_python_path,
        "section_idx": final_state.get("section_idx", 0),
        "planned_sections": planned_sections,
        "completed_sections": planned_sections[: final_state.get("section_idx", 0)],
        "fail_reason": final_state.get("fail_reason", ""),
        "output_scala": str(output_scala_path),
        "last_report": final_state.get("run_report_path", ""),
        "last_merged": final_state.get("run_merged_path", ""),
        "last_feedback": final_state.get("feedback", ""),
        "metrics": {
            "events_count": len(events),
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "total_tokens": total_tokens,
            "total_llm_seconds": total_llm_seconds,
            "total_compile_jar_submit_seconds": total_run_seconds,
        },
        "trace_events_count": len(trace_events),
    }

    stamp = now_stamp()
    summary_path = work_dir / f"summary_{stamp}.json"
    metrics_json_path = work_dir / f"metrics_{stamp}.json"
    trace_json_path = work_dir / f"trace_{stamp}.json"
    metrics_csv_path = work_dir / f"metrics_{stamp}.csv"
    write_text(summary_path, json.dumps(summary, indent=2))
    write_text(metrics_json_path, json.dumps(events, indent=2))
    write_text(trace_json_path, json.dumps(trace_events, indent=2))
    write_metrics_csv(metrics_csv_path, events)
    print(json.dumps(summary, indent=2))
    print(f"summary_path={summary_path}")
    print(f"metrics_json_path={metrics_json_path}")
    print(f"trace_json_path={trace_json_path}")
    print(f"metrics_csv_path={metrics_csv_path}")


if __name__ == "__main__":
    main()
