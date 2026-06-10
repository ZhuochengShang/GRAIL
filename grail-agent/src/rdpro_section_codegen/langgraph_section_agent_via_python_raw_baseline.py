from __future__ import annotations

import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PACKAGE_PARENT = PACKAGE_DIR.parent
if str(PACKAGE_PARENT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_PARENT))

from rdpro_section_codegen import langgraph_section_agent as base
from rdpro_section_codegen.section_text import extract_section_body, set_section_body, strip_fences


def _baseline_parse_args():
    args = _original_parse_args()
    if args.translation_mode != "via-python-raw":
        raise ValueError(
            "This baseline script is only for --translation-mode via-python-raw."
        )
    return args


def _baseline_normalize_candidate_scala(candidate_text: str, current_scala: str, section: str) -> str:
    candidate = strip_fences(candidate_text)
    if f"// TODO SECTION_{section}_START" in candidate and f"// TODO SECTION_{section}_END" in candidate:
        candidate_body = extract_section_body(candidate, section)
        return set_section_body(current_scala, section, candidate_body)
    return set_section_body(current_scala, section, candidate)


def _baseline_find_relevant_api_doc_sections(api_doc_text: str, section: str, section_apis: list[str], python_analysis: dict) -> str:
    return api_doc_text or ""


def _baseline_render_scala_context(current_scala: str, section: str, planned_sections: list[str]) -> str:
    return current_scala or ""


def _baseline_find_symbol_scope_issues(full_scala_text: str, section: str, section_body: str, planned_sections: list[str], analysis=None, contract=None) -> list[str]:
    return []


_original_parse_args = base.parse_args

base.parse_args = _baseline_parse_args
base._normalize_candidate_scala = _baseline_normalize_candidate_scala
base.find_relevant_api_doc_sections = _baseline_find_relevant_api_doc_sections
base.render_active_section_ir = base.render_analysis_ir
base._render_scala_context = _baseline_render_scala_context
base.find_symbol_scope_issues = _baseline_find_symbol_scope_issues


if __name__ == "__main__":
    base.main()
