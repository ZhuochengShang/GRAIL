from dataclasses import asdict, dataclass, field
from typing import Dict, List


@dataclass
class AnalysisResult:
    task_type: str
    python_raster_load_type: str
    task_label: str = ""
    capabilities: List[str] = field(default_factory=list)
    raster_inputs: List[str] = field(default_factory=list)
    vector_inputs: List[str] = field(default_factory=list)
    output_candidates: List[str] = field(default_factory=list)
    operations: List[str] = field(default_factory=list)
    requires_vector: bool = False
    multi_raster: bool = False
    needs_alignment: bool = False
    writes_output: bool = False
    analytics_output_shape: str = ""
    final_artifact_type: str = ""
    output_mode: str = ""
    output_fields: List[str] = field(default_factory=list)
    input_bindings: List[Dict[str, str]] = field(default_factory=list)
    workflow_stages: List[str] = field(default_factory=list)
    transform_family: str = ""
    analytics_kind: str = ""
    output_format: str = ""
    output_write_kind: str = ""
    expected_intermediate: str = ""
    section_intents: Dict[str, str] = field(default_factory=dict)
    workflow_goal: str = ""
    section_goals: Dict[str, str] = field(default_factory=dict)
    intermediate_contracts: Dict[str, str] = field(default_factory=dict)
    dataflow_lineage: List[str] = field(default_factory=list)
    output_intent: str = ""
    scalability_constraints: List[str] = field(default_factory=list)
    input_roles: Dict[str, str] = field(default_factory=dict)
    transform_result_shape: str = ""
    analytics_result_shape: str = ""
    output_required_input_shape: str = ""
    output_write_strategy: str = ""
    output_preconditions: Dict[str, bool] = field(default_factory=dict)
    raster_only_subtype: str = ""
    semantic_ir: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class PlanResult:
    task_type: str
    apis: List[str] = field(default_factory=list)
    sections: List[str] = field(default_factory=list)
    reasons: Dict[str, str] = field(default_factory=dict)
    analysis: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)
