import re
from typing import Dict, List

from .contracts import build_section_contract
from .models import AnalysisResult, PlanResult
from .planner import SECTION_ORDER, map_apis_to_sections

SECTION_PATTERN = re.compile(
    r"(?ms)^(\s*// TODO SECTION_([A-Z_]+)_START\s*$)(.*?)(^\s*// TODO SECTION_\2_END\s*$)"
)


def _extract_scaffold_sections(scaffold_text: str) -> Dict[str, Dict[str, str]]:
    sections: Dict[str, Dict[str, str]] = {}
    for match in SECTION_PATTERN.finditer(scaffold_text or ""):
        start_marker, name, body, end_marker = match.group(1), match.group(2), match.group(3), match.group(4)
        sections[name] = {
            "start_marker": start_marker.strip(),
            "end_marker": end_marker.strip(),
            "body": body.strip("\n"),
            "body_is_placeholder": "TODO" in body or not body.strip(),
        }
    return sections


def _canonical_inputs(analysis: AnalysisResult) -> Dict[str, object]:
    return {
        "raster_inputs": list(analysis.raster_inputs),
        "vector_inputs": list(analysis.vector_inputs),
        "output_candidates": list(analysis.output_candidates),
        "requires_vector": analysis.requires_vector,
        "multi_raster": analysis.multi_raster,
        "needs_alignment": analysis.needs_alignment,
        "operations": list(analysis.operations),
    }


def _section_notes(section: str, analysis: AnalysisResult, apis: List[str]) -> List[str]:
    notes: List[str] = []

    if section == "LOAD_DATA":
        if analysis.raster_inputs:
            notes.append("Load raster inputs with geoTiff using the injected raster path variables.")
        if analysis.requires_vector:
            notes.append("Load vector inputs with shapefile using the injected vector path variables.")
        notes.append("For sanity checks, prefer take(1) or one sampled tile/feature instead of count().")
    elif section == "TYPE_CHECK":
        notes.append("Inspect runtime Spark SQL pixelType and raster metadata; expect IntegerType for class rasters, "
          "FloatType or DoubleType for continuous rasters, and array-valued pixel types for multi-band or "
          "overlay outputs.")
        if analysis.requires_vector:
            notes.append("Confirm the vector RDD is non-empty before downstream spatial work.")
        notes.append("Reuse sampled records or metadata for validation; avoid count() as a type-check action.")
    elif section == "SPATIAL_CHECK":
        if analysis.requires_vector and analysis.needs_alignment:
            notes.append("Validate vector and raster CRS compatibility before clipping or zonal work.")
        if analysis.multi_raster:
            notes.append("Align raster metadata before overlay or any per-pixel fusion.")
    elif section == "TRANSFORM":
        if "filterPixels" in apis:
            notes.append("Implement value-based raster filtering in this section.")
        if "mapPixels" in apis:
            notes.append("Keep transformed raster outputs explicitly typed.")
        if analysis.requires_vector and analysis.expected_intermediate == "joined_records":
            notes.append("Keep this section focused on raster preparation before the explicit raster-vector join stage.")
        elif analysis.requires_vector:
            notes.append("Use this section for vector-boundary reprojection, clipping, masking, or reshape logic without forcing a join result.")
    elif section == "RASTER_VECTOR_JOIN":
        if analysis.requires_vector and analysis.expected_intermediate == "joined_records":
            notes.append("Materialize raster-vector pairing here with raptorJoin so analytics can aggregate by feature.")
            if "mask_or_filter" in analysis.operations:
                notes.append("Use the join stage, not a later analytics stage, to establish geometry-aware raster membership.")
    elif section == "ANALYTICS":
        if "raptorJoin" in apis:
            notes.append("Aggregate joined raster values into per-feature summary statistics with Spark groupBy or other aggregate operations.")
        if "flatten" in apis:
            notes.append("Use flatten when analytics needs raster values materialized as pixel-level tuples before aggregation.")
        if "mapPixels" in apis and analysis.raster_only_subtype == "categorical_summary":
            notes.append("Convert class counts into percentages or summary values if the task requires it.")
        notes.append("Use expensive actions only when analytics actually requires them; avoid count() for logging.")
    elif section == "OUTPUT":
        if "saveAsGeoTiff" in apis:
            notes.append("Persist the final raster output with saveAsGeoTiff.")
        elif analysis.final_artifact_type == "csv_file":
            notes.append("Persist the final tabular output using standard Scala or Spark file-writing logic.")
        else:
            notes.append("No raster output API was inferred; this section may remain a no-op or log-only step.")

    if not notes:
        notes.append("No additional section-specific notes inferred.")

    return notes


def build_section_specs(
    analysis: AnalysisResult,
    plan: PlanResult,
    scaffold_text: str = "",
) -> Dict[str, object]:
    scaffold_sections = _extract_scaffold_sections(scaffold_text)
    section_api_map = map_apis_to_sections(analysis, plan.apis)
    selected_sections = set(plan.sections)
    specs: List[Dict[str, object]] = []

    for section in SECTION_ORDER:
        apis = section_api_map.get(section, [])
        scaffold_info = scaffold_sections.get(section, {})
        selected = section in selected_sections or bool(apis)
        contract = build_section_contract(section, plan.task_type, capabilities=analysis.capabilities, analysis=analysis.to_dict())
        specs.append(
            {
                "section": section,
                "selected": selected,
                "reason": plan.reasons.get(section, ""),
                "apis": apis,
                "contract": contract,
                "scaffold": {
                    "start_marker": scaffold_info.get("start_marker", f"// TODO SECTION_{section}_START"),
                    "end_marker": scaffold_info.get("end_marker", f"// TODO SECTION_{section}_END"),
                    "existing_body": scaffold_info.get("body", ""),
                    "body_is_placeholder": scaffold_info.get("body_is_placeholder", True),
                },
                "implementation_notes": _section_notes(section, analysis, apis),
            }
        )

    return {
        "task_type": plan.task_type,
        "task_label": analysis.task_label,
        "apis": list(plan.apis),
        "sections": list(plan.sections),
        "section_api_map": section_api_map,
        "inputs": _canonical_inputs(analysis),
        "scaffold_has_markers": bool(scaffold_sections),
        "section_specs": specs,
    }
