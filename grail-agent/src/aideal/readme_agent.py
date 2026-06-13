"""LLM_readme.md: find, parse, or create the LLM-facing README.

AIDEAL owns the doc format. Each API entry:

    ## API Test: `name`
    ### Goal
    ### Valid Call Patterns (or Valid Access Patterns)
    ### LLM Instruction Prompt
    ### Prompt Snippet
    ### Common Failure Modes
    ### Fix Code Hint

`find_or_create` looks for the configured LLM readme; if missing it scans the
codebase's public API surface and writes a skeleton (optionally filled by the
AUTHOR model with --generate).
"""

from __future__ import annotations

import glob as globmod
import re
from dataclasses import dataclass
from pathlib import Path

from .config import AidealConfig

API_HEADER_RE = re.compile(r"^## API Test: `([^`]+)`\s*$", re.MULTILINE)


@dataclass
class ApiEntry:
    name: str
    goal: str
    snippet: str
    body: str


def _section_between(body: str, header: str) -> str:
    m = re.search(rf"^### {re.escape(header)}\s*$(.*?)(?=^###? |\Z)", body, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def parse_readme(path: Path) -> list[ApiEntry]:
    if not path.exists():
        return []  # stage-0 codebases have no LLM readme yet
    text = path.read_text(encoding="utf-8", errors="ignore")
    matches = list(API_HEADER_RE.finditer(text))
    entries = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        entries.append(ApiEntry(
            name=m.group(1),
            goal=_section_between(body, "Goal"),
            snippet=_section_between(body, "Prompt Snippet"),
            body=body,
        ))
    return entries


def public_api_surface(cfg: AidealConfig) -> set[str]:
    names: set[str] = set()
    pattern = re.compile(cfg.public_def_regex)
    for g in cfg.source_globs:
        for path in globmod.glob(str(cfg.root / g), recursive=True):
            text = Path(path).read_text(encoding="utf-8", errors="ignore")
            for m in pattern.finditer(text):
                name = m.group(1)
                if name not in cfg.exclude_names and not name.startswith("_"):
                    names.add(name)
    return names


SKELETON_ENTRY = """## API Test: `{name}`

### Goal
TODO: one sentence describing what this API does.

### Valid Call Patterns
```{lang}
TODO
```

### LLM Instruction Prompt
- TODO: rules an LLM must follow when calling `{name}`.

### Prompt Snippet
```text
TODO
```

### Common Failure Modes
- TODO

### Fix Code Hint
```{lang}
TODO
```
"""


def find_or_create(cfg: AidealConfig, generate: bool = False, max_generated: int = 10) -> dict:
    """Return status of the LLM readme; create a skeleton if missing."""
    if cfg.llm_readme.exists():
        entries = parse_readme(cfg.llm_readme)
        return {
            "action": "found",
            "path": str(cfg.llm_readme),
            "api_entries": len(entries),
            "apis": [e.name for e in entries],
        }

    surface = sorted(public_api_surface(cfg))
    lang = cfg.language.lower()
    parts = [f"# {cfg.project_name} — LLM_readme\n",
             "LLM-facing API documentation. Generated skeleton; fill the TODOs.\n"]
    targets = surface[:max_generated] if generate else surface
    if generate:
        from .llm import invoke_text
        from .profile import require_profile
        from .prompts import load as load_prompt

        require_profile(cfg)  # generation is domain-aware: profile must be filled
        for name in targets:
            try:
                entry = invoke_text(
                    cfg.model_for_role("author"),
                    *load_prompt(cfg, "aideal/readme_entry", name=name,
                                 template=SKELETON_ENTRY.format(name=name, lang=lang)),
                )
                parts.append(entry.strip() + "\n")
            except Exception:
                parts.append(SKELETON_ENTRY.format(name=name, lang=lang))
    else:
        for name in targets:
            parts.append(SKELETON_ENTRY.format(name=name, lang=lang))

    cfg.llm_readme.parent.mkdir(parents=True, exist_ok=True)
    cfg.llm_readme.write_text("\n".join(parts), encoding="utf-8")
    return {
        "action": "created_skeleton" if not generate else "created_generated",
        "path": str(cfg.llm_readme),
        "api_entries": len(targets),
        "note": "fill TODOs or rerun with --generate (uses the author model)",
    }
