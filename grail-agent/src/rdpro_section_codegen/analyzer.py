import json
import re
from pathlib import Path
from typing import List, Tuple

from .models import AnalysisResult

try:
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI
except Exception:
    HumanMessage = None
    SystemMessage = None
    ChatOpenAI = None

RASTER_EXTS = {".tif", ".tiff", ".img", ".vrt", ".jp2", ".asc"}
VECTOR_EXTS = {".shp", ".geojson", ".gpkg", ".json", ".kml"}


def _looks_like_path(value: str) -> bool:
    v = (value or "").strip()
    return "/" in v or v.startswith("file:") or Path(v).suffix.lower() in (RASTER_EXTS | VECTOR_EXTS)


def _strip_paths_for_semantics(text: str) -> str:
    return re.sub(
        r"(?:file://|/)[^\s,;:()]+?\.(?:tif|tiff|img|vrt|jp2|asc|shp|geojson|gpkg|json|kml)",
        " ",
        text or "",
        flags=re.IGNORECASE,
    )


def _extract_assignment_paths(py_text: str) -> List[Tuple[str, str]]:
    items: List[Tuple[str, str]] = []
    for match in re.finditer(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*Path\((['\"])(.+?)\2\)", py_text or ""):
        items.append((match.group(1), match.group(3)))
    for match in re.finditer(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(['\"])(.+?)\2", py_text or ""):
        value = match.group(3)
        if _looks_like_path(value):
            items.append((match.group(1), value))
    return items


def _extract_inline_paths(text: str) -> List[Tuple[str, str]]:
    items: List[Tuple[str, str]] = []
    pattern = re.compile(
        r"(?P<path>(?:file://|/)[^\s,;:()]+?\.(?:tif|tiff|img|vrt|jp2|asc|shp|geojson|gpkg|json|kml))",
        flags=re.IGNORECASE,
    )
    for match in pattern.finditer(text or ""):
        value = match.group("path").strip().rstrip(".")
        prefix = (text[max(0, match.start() - 80):match.start()] or "").lower()
        nearby = (text[max(0, match.start() - 40):min(len(text), match.end() + 40)] or "").lower()
        if any(token in nearby for token in ("input raster path", "raster path", "input raster")):
            label = "raster_path"
        elif any(token in nearby for token in ("input vector path", "vector path", "shapefile path")):
            label = "vector_path"
        elif any(token in nearby for token in ("output csv", "output path", "save to", "write to", "export to")):
            label = "output_path"
        elif any(token in prefix for token in ("vector", "shapefile", "polygon", "boundary", "neighborhood")):
            label = "vector_path"
        elif any(token in prefix for token in ("raster", "geotiff", "tiff", "nlcd")):
            label = "raster_path"
        elif any(token in prefix for token in ("output", "out", "result", "save", "write", "export")):
            label = "output_path"
        else:
            label = "path"
        items.append((label, value))
    return items


def _classify_paths(items: List[Tuple[str, str]], py_text: str) -> Tuple[List[str], List[str], List[str]]:
    rasters: List[str] = []
    vectors: List[str] = []
    outputs: List[str] = []

    all_items = list(items) + _extract_inline_paths(py_text)

    for var, value in all_items:
        ext = Path(value).suffix.lower()
        is_output = bool(re.search(r"(?i)out|output|result|save", var))
        if ext in RASTER_EXTS:
            (outputs if is_output else rasters).append(value)
        elif ext in VECTOR_EXTS:
            (outputs if is_output else vectors).append(value)
        elif is_output and _looks_like_path(value):
            outputs.append(value)

    for match in re.finditer(r"['\"]([^'\"]+)['\"]", py_text or ""):
        value = match.group(1).strip()
        if not _looks_like_path(value):
            continue
        ext = Path(value).suffix.lower()
        if ext in RASTER_EXTS and value not in rasters and value not in outputs:
            rasters.append(value)
        if ext in VECTOR_EXTS and value not in vectors and value not in outputs:
            vectors.append(value)

    return list(dict.fromkeys(rasters)), list(dict.fromkeys(vectors)), list(dict.fromkeys(outputs))


def _build_input_bindings(items: List[Tuple[str, str]], rasters: List[str], vectors: List[str], outputs: List[str]) -> List[dict]:
    bindings: List[dict] = []
    seen: set[tuple[str, str, str]] = set()
    ordered_paths = [("raster", path) for path in rasters] + [("vector", path) for path in vectors] + [("output", path) for path in outputs]
    item_lookup = list(items)

    for kind, path in ordered_paths:
        variable = ""
        role = "auxiliary"
        for name, value in item_lookup:
            if value == path:
                variable = name
                lower_name = name.lower()
                if any(token in lower_name for token in ("primary", "main", "input", "raster", "vector", "output")):
                    role = "primary"
                break
        key = (kind, path, variable)
        if key in seen:
            continue
        seen.add(key)
        bindings.append(
            {
                "kind": kind,
                "path": path,
                "variable": variable,
                "role": role if bindings else "primary",
            }
        )
    return bindings


def _infer_task_type(text: str) -> str:
    t = _strip_paths_for_semantics(text).lower()
    if "raster-only" in t or "whole raster" in t or "no polygon overlay" in t:
        return "raster_only"
    if "zonal" in t or "polygon" in t or "raptorjoin" in t:
        return "zonal_stats"
    if "change detection" in t or "changedetection" in t or "temporal change" in t:
        return "raster_vector" if any(token in t for token in ("polygon", "vector", "boundary", "shapefile")) else "raster_only"
    if "land cover" in t or "landcover" in t or "classification" in t:
        return "raster_only"
    if "ndvi" in t or ("nir" in t and "red" in t):
        return "raster_only"
    if "clip" in t or "mask" in t or "crop" in t:
        return "raster_vector" if any(token in t for token in ("polygon", "vector", "boundary", "shapefile", "geometry")) else "raster_only"
    return "generic"


def _parse_json_object(text: str) -> dict:
    s = (text or "").strip()
    if not s:
        raise ValueError("empty LLM response")
    try:
        return json.loads(s)
    except Exception:
        match = re.search(r"\{.*\}", s, flags=re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def llm_infer_task_type(py_text: str, provider: str = "openai", model: str = "gpt-4o") -> dict:
    if provider != "openai":
        raise ValueError(f"Unsupported provider for llm_infer_task_type: {provider}")
    if ChatOpenAI is None or SystemMessage is None or HumanMessage is None:
        raise ImportError("langchain_openai/langchain_core is required for llm_infer_task_type")

    allowed = ["generic", "raster_only", "raster_vector", "zonal_stats"]
    system = "You are a geospatial task classifier. Return exactly one JSON object and nothing else."
    user = "\n".join(
        [
            "Read the Python geospatial script and classify the dominant workflow shape.",
            f"Example task_type values: {allowed}",
            "Return valid JSON only in the form: {\"task_type\": \"...\", \"task_label\": \"...\", \"reason\": \"...\"}",
            "Use task_type for coarse routing and task_label for a concise specific description such as landcover, NDVI, clip, or zonal class summary.",
            "Prefer the dominant end-to-end task, not every sub-operation.",
            "",
            "Python script:",
            py_text or "",
        ]
    )

    llm = ChatOpenAI(model=model, temperature=0)
    response = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])
    raw = response.content if hasattr(response, "content") else str(response)
    parsed = _parse_json_object(raw)
    task_type = str(parsed.get("task_type", "") or "").strip().lower()
    if task_type not in allowed:
        raise ValueError(f"Invalid task_type from LLM: {task_type}")
    return {
        "task_type": task_type,
        "task_label": str(parsed.get("task_label", "") or "").strip(),
        "reason": str(parsed.get("reason", "") or "").strip(),
    }


def _infer_python_raster_load_type(text: str) -> str:
    t = (text or "").lower()
    if any(k in t for k in ["astype(np.float32", 'astype("float32"', "astype('float32'", "float32", "float64"]):
        return "float"
    if any(k in t for k in ["astype(np.int", 'astype("int', "astype('int", "uint8", "uint16", "int16", "int32", "int64"]):
        return "int"
    return "implicit"


def _infer_operations(text: str, multi_raster: bool, has_vector: bool) -> List[str]:
    t = _strip_paths_for_semantics(text).lower()
    ops: List[str] = []

    if any(k in t for k in ["rasterio", "geotiff", ".tif", ".tiff", "raster"]):
        ops.append("load_raster")
    if has_vector:
        ops.append("load_vector")
    if any(k in t for k in ["to_crs", "reproject", "set_crs", "epsg", "crs"]):
        ops.append("check_alignment")
    if any(k in t for k in ["mask", "clip", "crop", "filter", "where", "nodata"]):
        ops.append("mask_or_filter")
    if has_vector and any(k in t for k in ["geometry_mask", "unary_union", "mask", "clip", "crop"]):
        ops.append("vector_boundary_overlay")
    if multi_raster and any(k in t for k in ["overlay", "stack", "band", "bands"]):
        ops.append("raster_fusion")
    if any(k in t for k in ["map", "astype", "sum(", "mean(", "count(", "unique", "value_counts", "percentage", "percent"]):
        ops.append("pixel_or_summary_math")
    if has_vector and any(k in t for k in ["zonal", "per-feature", "groupby", "join", "intersect", "extract"]):
        ops.append("raster_vector_summary")
    if any(k in t for k in ["write(", "save", "output", "result", "export", "to_file"]):
        ops.append("write_output")

    return list(dict.fromkeys(ops))


def _infer_output_fields(text: str) -> List[str]:
    match = re.search(r"(?ms)writer\s*=\s*csv\.DictWriter\([^)]*fieldnames\s*=\s*list\(rows\[0\]\.keys\(\)\)", text or "")
    if match:
        dict_keys = re.findall(r'["\']([A-Za-z_][A-Za-z0-9_]*)["\']\s*:', text or "")
        return list(dict.fromkeys(dict_keys))
    dict_keys = re.findall(r'["\']([A-Za-z_][A-Za-z0-9_]*)["\']\s*:', text or "")
    return list(dict.fromkeys(dict_keys))


def _infer_transform_family(text: str, task_type: str, has_vector: bool, multi_raster: bool) -> str:
    t = _strip_paths_for_semantics(text).lower()
    if has_vector and any(token in t for token in ("zonal", "per-feature", "groupby", "raptorjoin", "join", "intersect", "extract")):
        return "raster_vector_join"
    if any(token in t for token in ("to_crs", "reproject", "warp", "resample", "geometry_mask")):
        return "reshape_or_reproject"
    if any(token in t for token in ("mask", "clip", "crop")):
        return "mask_or_clip"
    if multi_raster and any(token in t for token in ("overlay", "stack", "band", "bands")):
        return "multi_raster_overlay"
    if any(token in t for token in ("astype", "where", "map", "ndvi")):
        return "pixel_math"
    if task_type == "raster_only" and any(token in t for token in ("land cover", "landcover", "classification")):
        return "classification_summary_prep"
    return "generic_transform"


def _infer_analytics_kind(text: str, task_type: str, has_vector: bool, analytics_output_shape: str) -> str:
    t = _strip_paths_for_semantics(text).lower()
    if has_vector and any(token in t for token in ("percent", "percentage", "dominant", "groupby", "summary", "zonal")):
        return "per_feature_tabular_summary"
    if any(token in t for token in ("countbyvalue", "value_counts", "np.unique", "histogram")):
        return "class_histogram"
    if any(token in t for token in ("percent", "percentage")) and any(
        token in t for token in ("land cover", "landcover", "classification")
    ):
        return "class_percentage_summary"
    if analytics_output_shape == "raster":
        return "raster_derived_output"
    return "generic_analytics"


def _infer_raster_only_subtype(
    text: str,
    task_type: str,
    has_vector: bool,
    analytics_output_shape: str,
    final_artifact_type: str,
) -> str:
    if has_vector:
        return ""
    t = _strip_paths_for_semantics(text).lower()
    if final_artifact_type == "raster_file" or analytics_output_shape == "raster":
        return "raster_transform_output"
    if any(token in t for token in ("land cover", "landcover", "classification", "class count", "histogram")):
        return "categorical_summary"
    if any(token in t for token in ("mean", "average", "min", "max", "continuous", "interpolate", "upsample", "resample")):
        return "continuous_summary"
    if analytics_output_shape in ("tabular_rows", "summary_map"):
        return "categorical_summary"
    return "generic_raster"


def _infer_workflow_stages(
    operations: List[str],
    has_vector: bool,
    needs_alignment: bool,
    writes_output: bool,
    analytics_output_shape: str,
) -> List[str]:
    stages = ["load"]
    stages.append("type_check")
    if needs_alignment:
        stages.append("spatial_check")
    if any(op in operations for op in ("mask_or_filter", "vector_boundary_overlay", "raster_fusion", "raster_vector_summary")):
        stages.append("transform")
    if has_vector and "raster_vector_summary" in operations:
        stages.append("raster_vector_join")
    if analytics_output_shape or "pixel_or_summary_math" in operations:
        stages.append("analytics")
    if writes_output:
        stages.append("output")
    if has_vector and "transform" not in stages:
        stages.append("transform")
    return list(dict.fromkeys(stages))


def _infer_output_format(outputs: List[str], final_artifact_type: str) -> str:
    if outputs:
        first_ext = Path(outputs[0]).suffix.lower()
        if first_ext:
            return first_ext.lstrip(".")
    mapping = {
        "csv_file": "csv",
        "raster_file": "geotiff",
        "console_output": "console",
        "in_memory_result": "memory",
    }
    return mapping.get(final_artifact_type, "unknown")


def _infer_output_write_kind(text: str, final_artifact_type: str) -> str:
    t = (text or "").lower()
    if final_artifact_type == "csv_file":
        if "dictwriter" in t:
            return "csv_dict_writer"
        return "tabular_file_write"
    if final_artifact_type == "raster_file":
        if "saveasgeotiff" in t:
            return "rdpro_raster_writer"
        if "rasterio.open" in t and ("'w'" in t or '"w"' in t):
            return "rasterio_writer"
        return "raster_file_write"
    if final_artifact_type == "console_output":
        return "console_print"
    return "in_memory"


def _infer_expected_intermediate(has_vector: bool, multi_raster: bool, analytics_output_shape: str, transform_family: str) -> str:
    if transform_family == "raster_vector_join":
        return "joined_records"
    if has_vector and analytics_output_shape in ("tabular_rows", "summary_map"):
        return "joined_records"
    if multi_raster or transform_family in ("multi_raster_overlay", "pixel_math", "mask_or_clip", "reshape_or_reproject"):
        return "transformed_raster"
    if analytics_output_shape in ("tabular_rows", "summary_map"):
        return "raster_values_or_summary_source"
    return "generic_intermediate"


def _build_section_intents(
    task_type: str,
    transform_family: str,
    analytics_kind: str,
    expected_intermediate: str,
    final_artifact_type: str,
    output_format: str,
    has_vector: bool,
) -> dict[str, str]:
    output_intent = "persist final artifact"
    if final_artifact_type == "csv_file":
        output_intent = f"persist tabular output as {output_format or 'csv'}"
    elif final_artifact_type == "raster_file":
        output_intent = f"persist raster output as {output_format or 'geotiff'}"

    analytics_source = expected_intermediate or "analysis_ready_intermediate"
    if has_vector and transform_family == "raster_vector_join":
        analytics_source = "joined_records"

    intents = {
        "LOAD_DATA": "materialize configured raster/vector inputs from bound paths",
        "TYPE_CHECK": "validate pixel/data assumptions introduced during load",
        "SPATIAL_CHECK": "verify CRS/alignment requirements only when spatial compatibility matters",
        "TRANSFORM": f"build the main {transform_family or 'workflow'} intermediate for task_type={task_type}",
        "ANALYTICS": f"derive {analytics_kind or 'summary results'} from {analytics_source}",
        "OUTPUT": output_intent,
    }
    if has_vector and transform_family == "raster_vector_join":
        intents["RASTER_VECTOR_JOIN"] = "materialize the explicit raster-vector join as joined_records"
        intents["TRANSFORM"] = f"prepare raster inputs for the explicit {transform_family or 'workflow'} join stage"
    elif has_vector:
        intents["TRANSFORM"] = "prepare raster inputs with vector boundary alignment, reprojection, clipping, or masking before downstream analysis"
    return intents


def _build_workflow_goal(
    task_type: str,
    task_label: str,
    has_vector: bool,
    multi_raster: bool,
    analytics_output_shape: str,
    final_artifact_type: str,
) -> str:
    parts: list[str] = []
    if task_label:
        parts.append(task_label)
    else:
        parts.append(task_type or "geospatial workflow")

    if has_vector:
        parts.append("using raster and vector inputs")
    elif multi_raster:
        parts.append("using multiple raster inputs")
    else:
        parts.append("using raster inputs")

    if analytics_output_shape == "tabular_rows":
        parts.append("to produce tabular summary rows")
    elif analytics_output_shape == "summary_map":
        parts.append("to produce aggregated summary values")
    elif final_artifact_type == "raster_file":
        parts.append("to produce a raster artifact")

    return " ".join(parts).strip()


def _build_intermediate_contracts(
    has_vector: bool,
    multi_raster: bool,
    expected_intermediate: str,
    analytics_output_shape: str,
    final_artifact_type: str,
    transform_family: str,
) -> dict[str, str]:
    load_result = "loaded_raster_and_vector_inputs" if has_vector else "loaded_raster_inputs"
    if multi_raster:
        load_result = "loaded_multi_raster_inputs"
    transform_result = expected_intermediate or "analysis_ready_intermediate"
    join_result = "joined_records" if expected_intermediate == "joined_records" else ""
    if has_vector:
        transform_result = "raster_or_transformed_raster"
    if analytics_output_shape == "tabular_rows":
        analytics_result = "flat_tabular_rows"
    elif analytics_output_shape == "summary_map":
        analytics_result = "summary_aggregates"
    elif final_artifact_type == "raster_file":
        analytics_result = "raster_ready_result"
    else:
        analytics_result = "analysis_result"
    if final_artifact_type == "csv_file":
        output_result = "persisted_tabular_artifact"
    elif final_artifact_type == "raster_file":
        output_result = "persisted_raster_artifact"
    else:
        output_result = "materialized_final_result"
    contracts = {
        "LOAD_DATA": load_result,
        "TYPE_CHECK": "validated_type_assumptions",
        "SPATIAL_CHECK": "validated_spatial_compatibility",
        "TRANSFORM": transform_result,
        "ANALYTICS": analytics_result,
        "OUTPUT": output_result,
    }
    if has_vector and transform_family == "raster_vector_join":
        contracts["RASTER_VECTOR_JOIN"] = join_result
    return contracts


def _build_dataflow_lineage(
    has_vector: bool,
    transform_result: str,
    join_result: str,
    analytics_result: str,
    output_result: str,
) -> list[str]:
    source = "raster and vector inputs" if has_vector else "raster inputs"
    steps = [
        f"{source} -> loaded datasets",
        f"loaded datasets -> {transform_result}",
    ]
    if has_vector and join_result:
        steps.append(f"{transform_result} -> {join_result}")
        steps.append(f"{join_result} -> {analytics_result}")
    else:
        steps.append(f"{transform_result} -> {analytics_result}")
    steps.append(f"{analytics_result} -> {output_result}")
    return steps


def _build_input_roles(rasters: List[str], vectors: List[str], outputs: List[str]) -> dict[str, str]:
    roles: dict[str, str] = {}
    if rasters:
        roles["primary_raster"] = rasters[0]
    if len(rasters) > 1:
        for idx, path in enumerate(rasters[1:], start=2):
            roles[f"secondary_raster_{idx-1}"] = path
    if vectors:
        roles["vector_context"] = vectors[0]
    if outputs:
        roles["output_target"] = outputs[0]
    return roles


def _infer_transform_result_shape(has_vector: bool, multi_raster: bool, transform_family: str, expected_intermediate: str) -> str:
    if expected_intermediate == "joined_records":
        return "joined_records"
    if multi_raster and transform_family in ("multi_raster_overlay", "pixel_math"):
        return "fused_raster"
    if transform_family in ("mask_or_clip", "reshape_or_reproject"):
        return "transformed_raster"
    return "analysis_ready_intermediate"


def _infer_analytics_result_shape(analytics_output_shape: str, final_artifact_type: str) -> str:
    if analytics_output_shape == "tabular_rows":
        return "flat_tabular_rows"
    if analytics_output_shape == "summary_map":
        return "summary_map"
    if final_artifact_type == "raster_file":
        return "raster_result"
    return "generic_result"


def _build_output_preconditions(
    analytics_result_shape: str,
    final_artifact_type: str,
    output_mode: str,
) -> dict[str, bool]:
    return {
        "requires_flattening": analytics_result_shape == "nested_rows",
        "requires_overwrite": output_mode == "persisted_file",
        "requires_distributed_write": final_artifact_type in ("csv_file", "raster_file"),
    }


def _infer_output_required_input_shape(
    analytics_result_shape: str,
    final_artifact_type: str,
) -> str:
    if final_artifact_type == "csv_file":
        return "flat_tabular_rows"
    if final_artifact_type == "raster_file":
        return "raster_result"
    return analytics_result_shape or "generic_result"


def _infer_output_write_strategy(
    final_artifact_type: str,
    output_mode: str,
    requires_vector: bool,
) -> str:
    if final_artifact_type == "csv_file":
        return "distributed_csv" if requires_vector or output_mode == "persisted_file" else "tabular_csv"
    if final_artifact_type == "raster_file":
        return "geotiff_writer"
    if output_mode == "console_only":
        return "console_only"
    return "in_memory_or_deferred"


def _build_output_intent(final_artifact_type: str, output_format: str, output_mode: str) -> str:
    if final_artifact_type == "csv_file":
        return f"write distributed tabular output as {output_format or 'csv'} with {output_mode or 'persisted_file'} semantics"
    if final_artifact_type == "raster_file":
        return f"write raster output as {output_format or 'geotiff'} with {output_mode or 'persisted_file'} semantics"
    if output_mode == "console_only":
        return "emit summary to console only"
    return "materialize final result for downstream use"


def _build_scalability_constraints(
    has_vector: bool,
    analytics_output_shape: str,
    final_artifact_type: str,
    output_mode: str,
) -> list[str]:
    constraints = [
        "avoid collect() and other driver-heavy materialization",
        "avoid validation-only count() on large datasets",
        "preserve reusable distributed intermediates across sections",
    ]
    if has_vector:
        constraints.append("prefer distributed raster-vector operations over local geometry loops")
    if analytics_output_shape in ("tabular_rows", "summary_map"):
        constraints.append("keep analytics in distributed aggregations until final output")
    if final_artifact_type == "csv_file" or output_mode == "persisted_file":
        constraints.append("prefer distributed, overwrite-safe output behavior")
    return constraints


def _build_semantic_ir(
    task_type: str,
    task_label: str,
    python_raster_load_type: str,
    rasters: List[str],
    vectors: List[str],
    outputs: List[str],
    input_bindings: List[dict],
    operations: List[str],
    workflow_stages: List[str],
    transform_family: str,
    analytics_kind: str,
    analytics_output_shape: str,
    final_artifact_type: str,
    output_mode: str,
    output_format: str,
    output_write_kind: str,
    output_fields: List[str],
    expected_intermediate: str,
    requires_vector: bool,
    multi_raster: bool,
    needs_alignment: bool,
    section_intents: dict[str, str],
    workflow_goal: str,
    section_goals: dict[str, str],
    intermediate_contracts: dict[str, str],
    dataflow_lineage: List[str],
    output_intent: str,
    scalability_constraints: List[str],
    input_roles: dict[str, str],
    transform_result_shape: str,
    analytics_result_shape: str,
    output_required_input_shape: str,
    output_write_strategy: str,
    output_preconditions: dict[str, bool],
    raster_only_subtype: str,
) -> dict:
    return {
        "ir_version": "reasoning_v1",
        "task": {
            "task_type": task_type,
            "task_label": task_label,
            "workflow_goal": workflow_goal,
        },
        "inputs": {
            "bindings": input_bindings,
            "raster_inputs": list(rasters),
            "vector_inputs": list(vectors),
            "output_candidates": list(outputs),
            "input_roles": dict(input_roles),
            "requires_vector": requires_vector,
            "multi_raster": multi_raster,
            "needs_alignment": needs_alignment,
        },
        "workflow": {
            "stages": workflow_stages,
            "operations": list(operations),
            "python_raster_load_type": python_raster_load_type,
            "transform_family": transform_family,
            "analytics_kind": analytics_kind,
            "raster_only_subtype": raster_only_subtype,
            "expected_intermediate": expected_intermediate,
            "transform_result_shape": transform_result_shape,
            "analytics_result_shape": analytics_result_shape,
            "dataflow_lineage": list(dataflow_lineage),
        },
        "output": {
            "analytics_output_shape": analytics_output_shape,
            "final_artifact_type": final_artifact_type,
            "output_mode": output_mode,
            "output_format": output_format,
            "output_write_kind": output_write_kind,
            "output_required_input_shape": output_required_input_shape,
            "output_write_strategy": output_write_strategy,
            "output_fields": list(output_fields),
            "output_intent": output_intent,
            "output_preconditions": dict(output_preconditions),
        },
        "reasoning": {
            "section_goals": dict(section_goals),
            "intermediate_contracts": dict(intermediate_contracts),
            "scalability_constraints": list(scalability_constraints),
        },
        "section_intents": dict(section_intents),
    }


def _infer_workflow_shapes(text: str, outputs: List[str], task_type: str) -> tuple[str, str, str]:
    t = (text or "").lower()
    output_exts = {Path(path).suffix.lower() for path in outputs if path}
    writes_csv = (
        ".csv" in output_exts
        or "csv.dictwriter" in t
        or "write_csv(" in t
        or bool(
            re.search(
                r"\b(write|save|export|produce|output|persist)\b[^\n.]{0,40}\bcsv\b",
                t,
            )
        )
        or "csv output" in t
        or "csv outputs" in t
        or "tabular csv output" in t
        or "tabular csv outputs" in t
        or ("tabular" in t and "csv" in t)
    )
    writes_raster = bool(output_exts & RASTER_EXTS) or "saveasgeotiff" in t or ("rasterio.open" in t and ("'w'" in t or '"w"' in t))
    returns_rows = bool(re.search(r"\breturn\s+[A-Za-z_][A-Za-z0-9_]*\s*,\s*[A-Za-z_][A-Za-z0-9_]*", text or ""))
    builds_rows = any(token in t for token in ["output_rows", "summary_rows", "writerows(", "dictwriter", "append(build_", "rows.append("])

    if writes_csv:
        final_artifact_type = "csv_file"
        output_mode = "persisted_file"
    elif writes_raster:
        final_artifact_type = "raster_file"
        output_mode = "persisted_file"
    elif "print(" in t or "logger." in t:
        final_artifact_type = "console_output"
        output_mode = "console_only"
    else:
        final_artifact_type = "in_memory_result"
        output_mode = "in_memory"

    if task_type == "zonal_stats" and writes_csv:
        analytics_output_shape = "tabular_rows"
    elif writes_raster and any(
        token in t for token in ("clip", "mask", "crop", "reproject", "geometry_mask")
    ):
        analytics_output_shape = "raster"
    elif builds_rows or returns_rows:
        analytics_output_shape = "tabular_rows"
    elif "countbyvalue(" in t or "value_counts" in t or "np.unique" in t:
        analytics_output_shape = "summary_map"
    elif task_type == "raster_vector" and any(
        token in t for token in ("clip", "mask", "crop", "reproject", "geometry_mask")
    ):
        analytics_output_shape = "raster"
    elif any(
        token in t for token in ("ndvi", "clip", "mask", "crop", "reproject", "geometry_mask")
    ):
        analytics_output_shape = "raster"
    else:
        analytics_output_shape = "generic_result"

    return analytics_output_shape, final_artifact_type, output_mode


def analyze_python_script(py_text: str, task_type: str | None = None, task_label: str = "") -> AnalysisResult:
    items = _extract_assignment_paths(py_text)
    raster_inputs, vector_inputs, output_candidates = _classify_paths(items, py_text)
    resolved_task_type = task_type or _infer_task_type(py_text)
    multi_raster = len(raster_inputs) > 1
    operations = _infer_operations(py_text, multi_raster=multi_raster, has_vector=bool(vector_inputs))
    needs_alignment = "check_alignment" in operations
    writes_output = "write_output" in operations or bool(output_candidates)
    output_fields = _infer_output_fields(py_text)
    analytics_output_shape, final_artifact_type, output_mode = _infer_workflow_shapes(
        py_text,
        output_candidates,
        resolved_task_type,
    )
    input_bindings = _build_input_bindings(items, raster_inputs, vector_inputs, output_candidates)
    transform_family = _infer_transform_family(py_text, resolved_task_type, bool(vector_inputs), multi_raster)
    analytics_kind = _infer_analytics_kind(py_text, resolved_task_type, bool(vector_inputs), analytics_output_shape)
    raster_only_subtype = _infer_raster_only_subtype(
        py_text,
        resolved_task_type,
        bool(vector_inputs),
        analytics_output_shape,
        final_artifact_type,
    )
    workflow_stages = _infer_workflow_stages(
        operations,
        has_vector=bool(vector_inputs),
        needs_alignment=needs_alignment,
        writes_output=writes_output,
        analytics_output_shape=analytics_output_shape,
    )
    output_format = _infer_output_format(output_candidates, final_artifact_type)
    output_write_kind = _infer_output_write_kind(py_text, final_artifact_type)
    expected_intermediate = _infer_expected_intermediate(
        has_vector=bool(vector_inputs),
        multi_raster=multi_raster,
        analytics_output_shape=analytics_output_shape,
        transform_family=transform_family,
    )
    section_intents = _build_section_intents(
        resolved_task_type,
        transform_family,
        analytics_kind,
        expected_intermediate,
        final_artifact_type,
        output_format,
        bool(vector_inputs),
    )
    workflow_goal = _build_workflow_goal(
        resolved_task_type,
        task_label,
        bool(vector_inputs),
        multi_raster,
        analytics_output_shape,
        final_artifact_type,
    )
    section_goals = dict(section_intents)
    intermediate_contracts = _build_intermediate_contracts(
        has_vector=bool(vector_inputs),
        multi_raster=multi_raster,
        expected_intermediate=expected_intermediate,
        analytics_output_shape=analytics_output_shape,
        final_artifact_type=final_artifact_type,
        transform_family=transform_family,
    )
    input_roles = _build_input_roles(raster_inputs, vector_inputs, output_candidates)
    transform_result_shape = _infer_transform_result_shape(
        has_vector=bool(vector_inputs),
        multi_raster=multi_raster,
        transform_family=transform_family,
        expected_intermediate=expected_intermediate,
    )
    analytics_result_shape = _infer_analytics_result_shape(
        analytics_output_shape=analytics_output_shape,
        final_artifact_type=final_artifact_type,
    )
    output_required_input_shape = _infer_output_required_input_shape(
        analytics_result_shape=analytics_result_shape,
        final_artifact_type=final_artifact_type,
    )
    output_write_strategy = _infer_output_write_strategy(
        final_artifact_type=final_artifact_type,
        output_mode=output_mode,
        requires_vector=bool(vector_inputs),
    )
    dataflow_lineage = _build_dataflow_lineage(
        has_vector=bool(vector_inputs),
        transform_result=intermediate_contracts["TRANSFORM"],
        join_result=intermediate_contracts.get("RASTER_VECTOR_JOIN", ""),
        analytics_result=intermediate_contracts["ANALYTICS"],
        output_result=intermediate_contracts["OUTPUT"],
    )
    output_intent = _build_output_intent(final_artifact_type, output_format, output_mode)
    output_preconditions = _build_output_preconditions(
        analytics_result_shape=analytics_result_shape,
        final_artifact_type=final_artifact_type,
        output_mode=output_mode,
    )
    scalability_constraints = _build_scalability_constraints(
        has_vector=bool(vector_inputs),
        analytics_output_shape=analytics_output_shape,
        final_artifact_type=final_artifact_type,
        output_mode=output_mode,
    )
    semantic_ir = _build_semantic_ir(
        task_type=resolved_task_type,
        task_label=task_label,
        python_raster_load_type=_infer_python_raster_load_type(py_text),
        rasters=raster_inputs,
        vectors=vector_inputs,
        outputs=output_candidates,
        input_bindings=input_bindings,
        operations=operations,
        workflow_stages=workflow_stages,
        transform_family=transform_family,
        analytics_kind=analytics_kind,
        analytics_output_shape=analytics_output_shape,
        final_artifact_type=final_artifact_type,
        output_mode=output_mode,
        output_format=output_format,
        output_write_kind=output_write_kind,
        output_fields=output_fields,
        expected_intermediate=expected_intermediate,
        requires_vector=bool(vector_inputs),
        multi_raster=multi_raster,
        needs_alignment=needs_alignment,
        section_intents=section_intents,
        workflow_goal=workflow_goal,
        section_goals=section_goals,
        intermediate_contracts=intermediate_contracts,
        dataflow_lineage=dataflow_lineage,
        output_intent=output_intent,
        scalability_constraints=scalability_constraints,
        input_roles=input_roles,
        transform_result_shape=transform_result_shape,
        analytics_result_shape=analytics_result_shape,
        output_required_input_shape=output_required_input_shape,
        output_write_strategy=output_write_strategy,
        output_preconditions=output_preconditions,
        raster_only_subtype=raster_only_subtype,
    )
    python_raster_load_type = _infer_python_raster_load_type(py_text)

    return AnalysisResult(
        task_type=resolved_task_type,
        task_label=task_label,
        python_raster_load_type=python_raster_load_type,
        raster_inputs=raster_inputs,
        vector_inputs=vector_inputs,
        output_candidates=output_candidates,
        operations=operations,
        requires_vector=bool(vector_inputs),
        multi_raster=multi_raster,
        needs_alignment=needs_alignment,
        writes_output=writes_output,
        analytics_output_shape=analytics_output_shape,
        final_artifact_type=final_artifact_type,
        output_mode=output_mode,
        output_fields=output_fields,
        input_bindings=input_bindings,
        workflow_stages=workflow_stages,
        transform_family=transform_family,
        analytics_kind=analytics_kind,
        output_format=output_format,
        output_write_kind=output_write_kind,
        expected_intermediate=expected_intermediate,
        section_intents=section_intents,
        workflow_goal=workflow_goal,
        section_goals=section_goals,
        intermediate_contracts=intermediate_contracts,
        dataflow_lineage=dataflow_lineage,
        output_intent=output_intent,
        scalability_constraints=scalability_constraints,
        input_roles=input_roles,
        transform_result_shape=transform_result_shape,
        analytics_result_shape=analytics_result_shape,
        output_required_input_shape=output_required_input_shape,
        output_write_strategy=output_write_strategy,
        output_preconditions=output_preconditions,
        raster_only_subtype=raster_only_subtype,
        semantic_ir=semantic_ir,
    )
