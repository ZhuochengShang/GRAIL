from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from rdpro_section_codegen.analyzer import analyze_python_script
from rdpro_section_codegen.file_utils import read_text, to_uri, write_text
from rdpro_section_codegen.langgraph_section_agent import build_inputs_section_body
from rdpro_section_codegen.section_text import extract_section_body, set_section_body

SECTIONS = [
    "LOAD_DATA",
    "TYPE_CHECK",
    "SPATIAL_CHECK",
    "TRANSFORM",
    "ANALYTICS",
    "OUTPUT",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rewrite a successful sample Scala job into a cluster-ready Scala job.")
    parser.add_argument("--input-scala", required=True)
    parser.add_argument("--output-scala", required=True)
    parser.add_argument("--raster-path", action="append", default=[])
    parser.add_argument("--vector-path", action="append", default=[])
    parser.add_argument("--output-path", default="")
    parser.add_argument("--master", default="")
    parser.add_argument("--keep-step-markers", action="store_true")
    return parser.parse_args()


def _replace_master(scala_text: str, master: str) -> str:
    if master:
        if re.search(r'\.master\(".*?"\)', scala_text):
            return re.sub(r'\.master\(".*?"\)', f'.master("{master}")', scala_text)
        return scala_text.replace('.appName("GeoJobMain")', f'.appName("GeoJobMain")\n      .master("{master}")')
    return re.sub(r'(?m)^\s*\.master\("local\[\*\]"\)\s*\n', "", scala_text)


def _rewrite_inputs(
    scala_text: str,
    raster_paths: list[str],
    vector_paths: list[str],
    output_path: str | None,
) -> str:
    if not output_path:
        inputs_body = extract_section_body(scala_text, "INPUTS")
        if not inputs_body:
            raise ValueError("SECTION_INPUTS is missing, so raster/vector paths cannot be rewritten in place.")
        raster_seq = ", ".join(f'"{path}"' for path in raster_paths)
        vector_seq = ", ".join(f'"{path}"' for path in vector_paths)
        vector_line = (
            f"    val vectorPaths: Seq[String] = Seq({vector_seq})"
            if vector_paths
            else "    val vectorPaths: Seq[String] = Seq.empty[String]"
        )
        updated_body = re.sub(
            r'(?m)^\s*val\s+rasterPaths:\s+Seq\[String\]\s*=\s*Seq\([^\n]*\)\s*$',
            f'    val rasterPaths: Seq[String] = Seq({raster_seq})',
            inputs_body,
        )
        updated_body = re.sub(
            r'(?m)^\s*val\s+vectorPaths:\s+Seq\[String\]\s*=\s*(?:Seq\([^\n]*\)|Seq\.empty\[String\])\s*$',
            vector_line,
            updated_body,
        )
        return set_section_body(scala_text, "INPUTS", updated_body)

    pseudo_python = "\n".join(
        [*(f'raster_path_{idx} = "{path}"' for idx, path in enumerate(raster_paths, start=1)),
         *(f'vector_path_{idx} = "{path}"' for idx, path in enumerate(vector_paths, start=1)),
         f'output_path = "{output_path}"']
    )
    analysis = analyze_python_script(pseudo_python, task_type="generic", task_label="cluster_rewrite")
    analysis.raster_inputs = list(raster_paths)
    analysis.vector_inputs = list(vector_paths)
    analysis.output_candidates = [output_path]
    new_inputs = build_inputs_section_body(analysis, Path(output_path).resolve().parent)
    return set_section_body(scala_text, "INPUTS", new_inputs)


def _strip_debug_lines(section_body: str, keep_step_markers: bool) -> tuple[str, list[str]]:
    lines = section_body.splitlines()
    kept: list[str] = []
    removed: list[str] = []
    skip_until_paren_balance = 0
    skip_until_block_close = 0

    for line in lines:
        stripped = line.strip()
        if skip_until_paren_balance > 0:
            removed.append(stripped or line)
            skip_until_paren_balance += line.count("(") - line.count(")")
            continue
        if skip_until_block_close > 0:
            removed.append(stripped or line)
            skip_until_block_close += line.count("{") - line.count("}")
            continue
        if not stripped:
            kept.append(line)
            continue
        if ".show(" in stripped or ".printSchema(" in stripped:
            removed.append(stripped)
            continue
        if "println(" in stripped and "__STEP__" not in stripped and "__DONE__" not in stripped:
            removed.append(stripped)
            continue
        if ".take(1)" in stripped and stripped.startswith(("val ", "if ", "assert", "require")):
            removed.append(stripped)
            paren_delta = line.count("(") - line.count(")")
            if stripped.startswith("if ") and "{" in line:
                skip_until_block_close = line.count("{") - line.count("}")
            elif paren_delta > 0:
                skip_until_paren_balance = paren_delta
            continue
        if not keep_step_markers and "__STEP__" in stripped:
            removed.append(stripped)
            continue
        kept.append(line)
    cleaned = "\n".join(kept).strip()
    if not cleaned:
        cleaned = "// clusterized: removed sample/debug actions"
    return cleaned, removed


def _clusterize_sections(scala_text: str, keep_step_markers: bool) -> tuple[str, dict[str, list[str]]]:
    removed_by_section: dict[str, list[str]] = {}
    updated = scala_text
    for section in SECTIONS:
        body = extract_section_body(updated, section)
        if not body:
            continue
        cleaned, removed = _strip_debug_lines(body, keep_step_markers)
        if removed:
            removed_by_section[section] = removed
            updated = set_section_body(updated, section, cleaned)
    return updated, removed_by_section


def clusterize_scala_text(
    scala_text: str,
    raster_paths: list[str],
    vector_paths: list[str],
    output_path: str | None = None,
    master: str = "",
    keep_step_markers: bool = False,
) -> tuple[str, dict]:
    if not raster_paths:
        raise ValueError("At least one raster path is required for cluster rewrite.")

    rewritten = _rewrite_inputs(
        scala_text,
        [to_uri(path) for path in raster_paths],
        [to_uri(path) for path in vector_paths],
        to_uri(output_path) if output_path else None,
    )
    rewritten = _replace_master(rewritten, master.strip())
    rewritten, removed = _clusterize_sections(rewritten, keep_step_markers=keep_step_markers)
    summary = {
        "raster_paths": raster_paths,
        "vector_paths": vector_paths,
        "output_path_override": output_path or "(preserved from input scala)",
        "master": master.strip() or "(removed local master)",
        "removed_actions": removed,
    }
    return rewritten, summary


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_scala).resolve()
    output_path = Path(args.output_scala).resolve()
    scala_text = read_text(input_path)
    rewritten, summary = clusterize_scala_text(
        scala_text=scala_text,
        raster_paths=args.raster_path,
        vector_paths=args.vector_path,
        output_path=args.output_path.strip() or None,
        master=args.master.strip(),
        keep_step_markers=args.keep_step_markers,
    )

    write_text(output_path, rewritten)
    summary = {
        "input_scala": str(input_path),
        "output_scala": str(output_path),
        **summary,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
