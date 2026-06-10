from __future__ import annotations

import re


def strip_fences(text: str) -> str:
    s = (text or "").strip()
    s = re.sub(r"^```(?:scala)?\s*", "", s)
    s = re.sub(r"\s*```$", "", s)
    return s.strip() + "\n"


def section_bounds(text: str, section: str) -> tuple[tuple[int, int], tuple[int, int]] | None:
    start_pat = f"// TODO SECTION_{section}_START"
    end_pat = f"// TODO SECTION_{section}_END"
    a = text.find(start_pat)
    b = text.find(end_pat)
    if a < 0 or b < 0 or b <= a:
        return None
    body_start = a + len(start_pat)
    body_end = b
    return (a, body_start), (body_end, b + len(end_pat))


def edited_outside_active_section(old_text: str, new_text: str, section: str) -> tuple[bool, str]:
    old_bounds = section_bounds(old_text, section)
    new_bounds = section_bounds(new_text, section)
    if not old_bounds or not new_bounds:
        return True, f"Missing markers for SECTION_{section}"

    old_prefix = old_text[: old_bounds[0][0]]
    old_suffix = old_text[old_bounds[1][1] :]
    new_prefix = new_text[: new_bounds[0][0]]
    new_suffix = new_text[new_bounds[1][1] :]

    if old_prefix != new_prefix or old_suffix != new_suffix:
        return True, "Candidate modified content outside active section"

    return False, ""


def extract_section_body(text: str, section: str) -> str:
    bounds = section_bounds(text, section)
    if not bounds:
        return ""
    return text[bounds[0][1] : bounds[1][0]].strip()


def set_section_body(text: str, section: str, body: str) -> str:
    bounds = section_bounds(text, section)
    if not bounds:
        raise ValueError(f"Missing markers for SECTION_{section}")
    start = text[: bounds[0][1]]
    end = text[bounds[1][0] :]
    return start + "\n" + body.rstrip() + "\n" + end


def contains_placeholder_paths(text: str) -> bool:
    tokens = ["file:///path/to/", "/path/to/"]
    return any(token in (text or "") for token in tokens)


def error_excerpt(stderr_text: str, stdout_text: str, max_chars: int = 5000) -> str:
    parts = []
    stderr = (stderr_text or "").strip()
    stdout = (stdout_text or "").strip()
    if stderr:
        parts.append("STDERR_EXCERPT:\n" + stderr[-max_chars:])
    if stdout:
        parts.append("STDOUT_EXCERPT:\n" + stdout[-max_chars:])
    return "\n\n".join(parts)
