from .models import AnalysisResult, PlanResult

SECTION_ORDER = [
    "LOAD_DATA",
    "TYPE_CHECK",
    "SPATIAL_CHECK",
    "TRANSFORM",
    "RASTER_VECTOR_JOIN",
    "ANALYTICS",
    "OUTPUT",
]


def _reasoning_ir(analysis: AnalysisResult) -> dict:
    return analysis.semantic_ir or {}


def infer_required_apis(analysis: AnalysisResult) -> list[str]:
    apis: list[str] = []
    ir = _reasoning_ir(analysis)
    reasoning = ir.get("reasoning", {}) if isinstance(ir, dict) else {}
    section_goals = reasoning.get("section_goals", {}) if isinstance(reasoning, dict) else {}
    intermediate_contracts = reasoning.get("intermediate_contracts", {}) if isinstance(reasoning, dict) else {}

    def add(api: str) -> None:
        if api and api not in apis:
            apis.append(api)

    if analysis.raster_inputs:
        add("geoTiff")
        add("tile metadata")
        add("pixel type")

    if analysis.requires_vector:
        add("shapefile")

    if analysis.multi_raster and analysis.needs_alignment:
        add("metadata alignment")
        add("SRID/CRS")
        add("reproject")
        add("reshape")
    if analysis.transform_family == "reshape_or_reproject" and not (
        analysis.task_type == "zonal_stats" and not analysis.multi_raster
    ):
        add("metadata alignment")
        add("SRID/CRS")
        add("reproject")
        add("reshapeNN")

    transform_goal = str(section_goals.get("TRANSFORM", "")).lower()
    analytics_goal = str(section_goals.get("ANALYTICS", "")).lower()
    transform_contract = str(intermediate_contracts.get("TRANSFORM", "")).lower()
    analytics_contract = str(intermediate_contracts.get("ANALYTICS", "")).lower()

    if (
        analysis.task_type == "zonal_stats"
        or analysis.expected_intermediate == "joined_records"
        or "joined" in transform_contract
        or "zonal" in analytics_goal
    ):
        add("raptorJoin")
    if (
        not analysis.requires_vector
        and ("transformed_raster" == transform_contract or "overlay" in transform_goal)
    ):
        add("mapPixels")
    if (
        not analysis.requires_vector
        and (
            analysis.raster_only_subtype == "categorical_summary"
            or "flat_tabular_rows" in analytics_contract
            or ("summary" in analytics_goal and analysis.raster_only_subtype != "continuous_summary")
        )
    ):
        add("flatten")

    if "mask_or_filter" in analysis.operations:
        if analysis.requires_vector:
            if analysis.expected_intermediate == "joined_records":
                add("raptorJoin")
        else:
            add("filterPixels")

    if (
        "pixel_or_summary_math" in analysis.operations
        and analysis.raster_only_subtype != "continuous_summary"
        and not analysis.requires_vector
    ):
        add("flatten")
        if analysis.final_artifact_type == "raster_file":
            add("mapPixels")
        if analysis.python_raster_load_type == "float":
            add("mapPixels cast Float")

    if analysis.multi_raster and "raster_fusion" in analysis.operations:
        add("overlay")

    if analysis.expected_intermediate == "joined_records" and "raster_vector_summary" in analysis.operations:
        add("raptorJoin")

    if analysis.final_artifact_type == "raster_file":
        add("saveAsGeoTiff")
    elif analysis.final_artifact_type == "csv_file":
        add("csv output")

    return apis


def infer_capabilities(analysis: AnalysisResult, apis: list[str]) -> list[str]:
    capabilities: list[str] = []

    def add(capability: str) -> None:
        if capability and capability not in capabilities:
            capabilities.append(capability)

    if analysis.requires_vector:
        add("vector_input")
    if analysis.multi_raster and "overlay" in apis:
        add("multi_raster_fusion")
    if (("mapPixels" in apis or "mapPixels cast Float" in apis) and not analysis.requires_vector):
        add("pixel_math")
    if "filterPixels" in apis or ("raptorJoin" in apis and analysis.requires_vector and "mask_or_filter" in analysis.operations):
        add("masking")
    if "raptorJoin" in apis and analysis.expected_intermediate == "joined_records":
        add("raster_vector_summary")
    if (
        not analysis.requires_vector
        and (
            analysis.raster_only_subtype == "categorical_summary"
            or "classification" in (analysis.task_label or "").lower()
            or "landcover" in (analysis.task_label or "").lower()
            or "land cover" in (analysis.task_label or "").lower()
        )
    ):
        add("classification_summary")
    if not analysis.requires_vector and analysis.raster_only_subtype == "continuous_summary":
        add("continuous_raster_summary")
    if "saveAsGeoTiff" in apis or analysis.final_artifact_type == "raster_file":
        add("raster_output")
    if analysis.final_artifact_type == "csv_file":
        add("tabular_output")

    return capabilities


def should_require_spatial_check(analysis: AnalysisResult, apis: list[str]) -> bool:
    if analysis.task_type == "zonal_stats" and "raptorJoin" in apis and not analysis.multi_raster:
        return False
    return analysis.multi_raster or analysis.needs_alignment or ("overlay" in apis and not analysis.requires_vector)


def map_apis_to_sections(analysis: AnalysisResult, apis: list[str]) -> dict[str, list[str]]:
    hints = {section: [] for section in SECTION_ORDER}

    for api in apis:
        if api in ("geoTiff", "shapefile"):
            hints["LOAD_DATA"].append(api)
        elif api in ("tile metadata", "pixel type"):
            hints["TYPE_CHECK"].append(api)
        elif api in ("reshape", "reproject", "metadata alignment", "SRID/CRS"):
            hints["SPATIAL_CHECK"].append(api)
        elif api == "reshapeNN":
            hints["TRANSFORM"].append(api)
        elif api in ("filterPixels", "overlay"):
            hints["TRANSFORM"].append(api)
        elif api == "raptorJoin":
            hints["RASTER_VECTOR_JOIN"].append(api)
        elif api in ("mapPixels", "mapPixels cast Float"):
            hints["TRANSFORM"].append(api)
        elif api == "flatten":
            hints["ANALYTICS"].append(api)
    if not should_require_spatial_check(analysis, apis):
        hints["SPATIAL_CHECK"] = []

    return {k: list(dict.fromkeys(v)) for k, v in hints.items()}


def should_include_section(analysis: AnalysisResult, section: str, section_apis: list[str], section_goals: dict) -> bool:
    if section_apis:
        return True
    if section == "OUTPUT":
        if analysis.task_type == "zonal_stats" and analysis.final_artifact_type == "csv_file":
            return False
        return bool(
            analysis.writes_output
            or analysis.final_artifact_type in ("csv_file", "raster_file")
        )
    if section == "RASTER_VECTOR_JOIN":
        return bool(analysis.expected_intermediate == "joined_records")
    if section == "ANALYTICS":
        analytics_goal = str(section_goals.get("ANALYTICS", "")).strip()
        if analysis.final_artifact_type == "raster_file" and analysis.expected_intermediate == "transformed_raster":
            return False
        return bool(analysis.analytics_kind or analytics_goal or analysis.expected_intermediate)
    return False


def build_plan(analysis: AnalysisResult) -> PlanResult:
    apis = infer_required_apis(analysis)
    analysis.capabilities = infer_capabilities(analysis, apis)
    section_hints = map_apis_to_sections(analysis, apis)
    reasoning = (analysis.semantic_ir or {}).get("reasoning", {}) if isinstance(analysis.semantic_ir, dict) else {}
    section_goals = reasoning.get("section_goals", {}) if isinstance(reasoning, dict) else {}
    sections = [
        section
        for section in SECTION_ORDER
        if should_include_section(analysis, section, section_hints.get(section, []), section_goals)
    ]

    reasons: dict[str, str] = {}
    for section in sections:
        section_apis = section_hints.get(section, [])
        if not section_apis and not str(section_goals.get(section, "")).strip():
            continue
        goal = str(section_goals.get(section, "")).strip()
        if goal and section_apis:
            reasons[section] = f"{goal}; selected APIs: {', '.join(section_apis)}"
        elif goal:
            reasons[section] = goal
        else:
            reasons[section] = f"selected from APIs: {', '.join(section_apis)}"
    return PlanResult(
        task_type=analysis.task_type,
        apis=apis,
        sections=sections,
        reasons=reasons,
        analysis=analysis.to_dict(),
    )
