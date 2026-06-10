PIPELINE_CONTRACT = {
    "LOAD_DATA": {
        "stage_role": "load_source_data",
        "required_calls": ["geoTiff"],
        "invariants": ["load_data_from_injected_paths"],
    },
    "TYPE_CHECK": {
        "stage_role": "inspect_loaded_types",
        "required_tokens": ["pixelType"],
    },
    "SPATIAL_CHECK": {
        "stage_role": "align_spatial_inputs",
        "required_tokens": ["rasterMetadata"],
        "invariants": ["spatial_check_only_when_required"],
    },
    "TRANSFORM": {
        "stage_role": "process_raster_or_raster_vector_inputs",
        "invariants": ["result_should_be_typed", "prepare_analysis_ready_intermediate"],
    },
    "RASTER_VECTOR_JOIN": {
        "stage_role": "materialize_raster_vector_join",
        "invariants": ["result_should_be_typed", "prepare_analysis_ready_intermediate"],
    },
    "ANALYTICS": {
        "stage_role": "aggregate_transformed_outputs",
        "invariants": ["analytics_should_aggregate_intermediate"],
    },
}

CAPABILITY_CONTRACTS = {
    "vector_input": {
        "LOAD_DATA": {
            "required_calls": ["shapefile"],
        }
    },
    "multi_raster_fusion": {
        "TRANSFORM": {
            "invariants": ["multi_source_inputs_must_be_materialized_before_reduction"],
        }
    },
    "pixel_math": {
        "TRANSFORM": {
            "invariants": ["final_result_must_be_typed"],
            "produces_shape": "transformed_raster",
        }
    },
    "masking": {
        "TRANSFORM": {
            "invariants": ["mask_or_filter_logic"],
            "produces_shape": "transformed_raster",
        }
    },
    "raster_vector_summary": {
        "RASTER_VECTOR_JOIN": {
            "required_calls": ["raptorJoin"],
            "invariants": ["raster_vector_summary"],
            "produces_shape": "joined_records",
        },
        "ANALYTICS": {
            "required_inputs": ["joined_records"],
            "invariants": ["aggregate_joined_values", "use_spark_groupby_aggregate", "must_assign_reusable_result", "must_produce_flat_tabular_rows", "must_compute_zone_level_percentages"],
            "produces_shape": "flat_tabular_rows",
        },
    },
    "classification_summary": {
        "ANALYTICS": {
            "required_inputs": ["raster_or_transformed_raster"],
            "invariants": ["classification_or_summary", "use_spark_groupby_aggregate", "must_assign_reusable_result"],
        }
    },
    "continuous_raster_summary": {
        "ANALYTICS": {
            "required_inputs": ["raster_or_transformed_raster"],
            "invariants": ["continuous_summary_or_stats", "must_assign_reusable_result"],
        }
    },
}


def _workflow_contracts(analysis: dict | None) -> dict[str, dict]:
    info = analysis or {}
    analytics_output_shape = info.get("analytics_output_shape", "")
    final_artifact_type = info.get("final_artifact_type", "")
    output_mode = info.get("output_mode", "")
    output_fields = list(info.get("output_fields", []) or [])
    requires_vector = bool(info.get("requires_vector"))

    contracts: dict[str, dict] = {}

    if requires_vector:
        expected_intermediate = str(info.get("expected_intermediate", "") or "")
        contracts.setdefault("TRANSFORM", {}).update({"produces_shape": "raster_or_transformed_raster"})
        transform_contract = contracts.setdefault("TRANSFORM", {})
        required_calls = list(transform_contract.get("required_calls", []) or [])
        transform_contract["required_calls"] = [call for call in required_calls if call != "mapPixels"]
        if expected_intermediate == "joined_records":
            contracts.setdefault("RASTER_VECTOR_JOIN", {}).update(
                {
                    "required_inputs": ["raster_or_transformed_raster"],
                    "required_calls": ["raptorJoin"],
                    "produces_shape": "joined_records",
                    "invariants": ["raster_vector_summary", "must_assign_reusable_result"],
                }
            )
    elif analytics_output_shape in ("tabular_rows", "summary_map") or final_artifact_type == "csv_file":
        contracts.setdefault("TRANSFORM", {}).update({"produces_shape": "raster_or_transformed_raster"})

    if analytics_output_shape:
        contracts.setdefault("ANALYTICS", {})
        produces_shape = analytics_output_shape
        if requires_vector and analytics_output_shape == "tabular_rows":
            produces_shape = "flat_tabular_rows"
        elif not requires_vector and final_artifact_type == "csv_file" and analytics_output_shape in ("tabular_rows", "summary_map"):
            produces_shape = "flat_tabular_rows"
        contracts["ANALYTICS"]["produces_shape"] = produces_shape
        if requires_vector and str(info.get("expected_intermediate", "") or "") == "joined_records":
            contracts["ANALYTICS"]["required_inputs"] = ["joined_records"]
        elif info.get("multi_raster"):
            contracts["ANALYTICS"]["required_inputs"] = ["transformed_raster"]
        else:
            contracts["ANALYTICS"]["required_inputs"] = ["raster_or_transformed_raster"]
        contracts["ANALYTICS"]["invariants"] = list(contracts["ANALYTICS"].get("invariants", []))
        if analytics_output_shape in ("tabular_rows", "summary_map"):
            contracts["ANALYTICS"]["invariants"].append("must_assign_reusable_result")
        if final_artifact_type == "csv_file":
            contracts["ANALYTICS"]["invariants"].append("derive_tabular_or_summary_output")
        if not requires_vector and final_artifact_type == "csv_file":
            contracts["ANALYTICS"]["invariants"].append("must_produce_flat_tabular_rows")
        if requires_vector and str(info.get("expected_intermediate", "") or "") == "joined_records" and analytics_output_shape == "tabular_rows":
            contracts["ANALYTICS"]["invariants"].append("must_produce_flat_tabular_rows")
            contracts["ANALYTICS"]["invariants"].append("must_compute_zone_level_percentages")
            if final_artifact_type == "csv_file":
                contracts["ANALYTICS"]["invariants"].append("must_persist_final_artifact")
                contracts["ANALYTICS"]["invariants"].append("must_write_tabular_output")
            else:
                contracts["ANALYTICS"]["invariants"].append("must_assign_output_rows_variable")
                contracts.setdefault("OUTPUT", {})
                contracts["OUTPUT"]["required_inputs"] = ["flat_tabular_rows"]
                contracts["OUTPUT"]["expected_fields"] = ["outputRows"]
                contracts["OUTPUT"]["invariants"] = list(contracts["OUTPUT"].get("invariants", []))
                contracts["OUTPUT"]["invariants"].append("must_consume_output_rows_variable")
                contracts["OUTPUT"]["invariants"].append("must_write_tabular_output")

    return contracts


def merge_contract_dict(base: dict, extra: dict) -> dict:
    out = dict(base or {})
    for key, value in (extra or {}).items():
        if isinstance(value, list):
            out[key] = list(out.get(key, []))
            for item in value:
                if item not in out[key]:
                    out[key].append(item)
        else:
            out[key] = value
    return out


def build_section_contract(section: str, task_type: str, capabilities: list[str] | None = None, analysis: dict | None = None) -> dict:
    contract = dict(PIPELINE_CONTRACT.get(section, {}))
    for capability in (capabilities or []):
        contract = merge_contract_dict(contract, CAPABILITY_CONTRACTS.get(capability, {}).get(section, {}))
    contract = merge_contract_dict(contract, _workflow_contracts(analysis).get(section, {}))
    contract["task_type"] = task_type
    contract["capabilities"] = list(capabilities or [])
    return contract


def render_section_contract(section: str, task_type: str, capabilities: list[str] | None = None, analysis: dict | None = None) -> str:
    contract = build_section_contract(section, task_type, capabilities=capabilities, analysis=analysis)
    lines = [f"SECTION_{section} contract:"]
    lines.append(f"- task_type: {task_type}")
    if contract.get("capabilities"):
        lines.append("- capabilities: " + ", ".join(contract["capabilities"]))
    for key in (
        "stage_role",
        "required_calls",
        "required_tokens",
        "required_inputs",
        "required_outputs",
        "produces_shape",
        "expected_fields",
        "invariants",
    ):
        value = contract.get(key, [])
        if isinstance(value, list) and value:
            lines.append(f"- {key}: " + ", ".join(value))
        elif isinstance(value, str) and value:
            lines.append(f"- {key}: {value}")
    return "\n".join(lines)
