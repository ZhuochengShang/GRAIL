"""AIDEAL configuration: one YAML file controls models, paths, languages,
tasks, and run settings."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise ImportError("AIDEAL needs PyYAML: pip install pyyaml") from exc


@dataclass
class ModelSpec:
    provider: str
    model: str


@dataclass
class AidealConfig:
    root: Path
    project_name: str
    language: str
    source_globs: list[str]
    public_def_regex: str
    exclude_names: list[str]
    visibility: dict          # optional override of the per-language visibility model
    test_globs: list[str]     # where existing unit tests live (real usage examples)
    surface_filter: str       # intended-API filter: all|documented|non_override|documented_non_override
    # workspace files
    llm_readme: Path
    original_readme: Path | None            # first baseline doc (back-compat / existence check)
    original_readme_files: list[Path]       # all baseline docs (files/dirs/globs expanded)
    notes_to_self: Path
    integration_tasks: Path
    aliases_file: Path
    error_log: Path
    # models
    registry: dict[str, ModelSpec]
    roles: dict[str, str]            # role -> registry key
    # runtime
    runtime_target: str
    runtime: dict
    # checks
    required_sections: list[str]
    comprehension_apis_sampled: int
    comprehension: dict           # optional execute-mode config (scaffold, command, sample data)
    # puzzle
    puzzle: dict
    raw: dict = field(default_factory=dict)

    def original_readme_text(self, limit: int | None = None) -> str:
        """Concatenate all baseline docs (README + extra docs/dirs) with file
        headers. `limit` caps the total characters."""
        parts: list[str] = []
        for p in self.original_readme_files:
            try:
                t = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            parts.append(f"===== {p.relative_to(self.root)} =====\n{t}")
        text = "\n\n".join(parts)
        return text[:limit] if limit else text

    def model_for_role(self, role: str) -> ModelSpec:
        key = self.roles.get(role)
        if key is None or key not in self.registry:
            raise KeyError(f"role '{role}' is not mapped to a registry model (have: {list(self.registry)})")
        return self.registry[key]

    def model_by_name(self, name: str) -> ModelSpec:
        return self.registry[name]


def _resolve_readme_sources(root: Path, sources: list[str]) -> list[Path]:
    """Expand each baseline-doc source (a file, a directory, or a glob) into a
    sorted, de-duplicated list of files. Directories pull in their *.md."""
    import glob as _glob
    found: list[Path] = []
    seen: set[Path] = set()
    for src in sources:
        base = (root / src)
        if base.is_dir():
            matches = sorted(_glob.glob(str(base / "**" / "*.md"), recursive=True))
        elif any(ch in src for ch in "*?["):
            matches = sorted(_glob.glob(str(base), recursive=True))
        else:
            matches = [str(base)]
        for m in matches:
            p = Path(m).resolve()
            if p.is_file() and p not in seen:
                seen.add(p); found.append(p)
    return found


def find_config(start: Path | None = None) -> Path | None:
    """Search cwd and up to 3 parents for configs/aideal.yaml."""
    cur = (start or Path.cwd()).resolve()
    for d in [cur, *cur.parents[:3]]:
        cand = d / "configs" / "aideal.yaml"
        if cand.exists():
            return cand
    return None


def load_config(config_path: str | Path | None = None) -> AidealConfig:
    if config_path is None:
        config_path = find_config()
        if config_path is None:
            raise FileNotFoundError(
                "No configs/aideal.yaml found in this directory or its parents. "
                "Run from a project root, pass --config <path>, or run "
                "`python -m aideal.cli init` to scaffold a new project here."
            )
    config_path = Path(config_path).resolve()
    root = config_path.parent.parent  # configs/ -> project root (grail-agent/)
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    project = raw.get("project", {})
    cb = raw.get("codebase", {})
    files = raw.get("files", {})
    models = raw.get("models", {})
    runtime = raw.get("runtime", {})
    checks = raw.get("checks", {})

    registry = {
        name: ModelSpec(provider=m["provider"], model=m["model"])
        for name, m in models.get("registry", {}).items()
    }

    def _file(key: str, default: str) -> Path:
        return (root / files.get(key, default)).resolve()

    # baseline docs: accept a single string or a list of files/dirs/globs
    _orig_raw = files.get("original_readme")
    _orig_sources = ([_orig_raw] if isinstance(_orig_raw, str)
                     else list(_orig_raw) if _orig_raw else [])
    _orig_files = _resolve_readme_sources(root, _orig_sources)

    return AidealConfig(
        root=root,
        project_name=project.get("name", "unknown"),
        language=project.get("language", "Scala"),
        source_globs=cb.get("source_globs", []),
        public_def_regex=cb.get("public_def_regex", r"def\s+([A-Za-z][A-Za-z0-9_]*)"),
        exclude_names=cb.get("exclude_names", []),
        visibility=cb.get("visibility", {}) or {},
        test_globs=cb.get("test_globs", []) or [],
        surface_filter=cb.get("surface_filter", "all") or "all",
        llm_readme=_file("llm_readme", "docs/LLM_readme.md"),
        original_readme=_orig_files[0] if _orig_files else None,
        original_readme_files=_orig_files,
        notes_to_self=_file("notes_to_self", "docs/notes_to_self.md"),
        integration_tasks=_file("integration_tasks", "configs/integration_tasks.yaml"),
        aliases_file=_file("aliases", "aliases/aliases.json"),
        error_log=_file("error_log", "logs/error_log.jsonl"),
        registry=registry,
        roles=models.get("roles", {}),
        runtime_target=runtime.get("target", "local"),
        runtime=runtime,
        required_sections=checks.get("required_sections", ["Goal"]),
        comprehension_apis_sampled=int(checks.get("comprehension_apis_sampled", 5)),
        comprehension=raw.get("comprehension", {}) or {},
        puzzle=raw.get("puzzle", {}),
        raw=raw,
    )


CONFIG_TEMPLATE = """\
# AIDEAL config - scaffolded by `aideal init`. Fill the TODOs.
project:
  name: TODO
  language: TODO        # e.g. Python, Scala

codebase:
  source_globs:
    - "TODO/**/*.py"    # where the public API lives
  public_def_regex: "def\\\\s+([a-zA-Z][A-Za-z0-9_]*)"
  exclude_names: []

files:
  project_profile: configs/project_profile.yaml
  prompts_dir: prompts            # optional overrides; package defaults used if absent
  original_readme: README.md      # baseline doc(s): a path, or a list of files/dirs/globs
  llm_readme: docs/LLM_readme.md
  notes_to_self: docs/notes_to_self.md
  integration_tasks: configs/integration_tasks.yaml
  aliases: aliases/aliases.json
  error_log: logs/error_log.jsonl

models:
  registry:
    gpt-4o:      { provider: openai, model: gpt-4o }
    gpt-4o-mini: { provider: openai, model: gpt-4o-mini }
  roles:
    author: gpt-4o-mini
    audience: gpt-4o

runtime:
  target: local
  local: {}

checks:
  required_sections:
    - "Goal"
    - "Valid Call Patterns|Valid Access Patterns"
    - "LLM Instruction Prompt"
    - "Prompt Snippet"
    - "Common Failure Modes"
    - "Fix Code Hint"
  comprehension_apis_sampled: 5

puzzle:
  cwd: .
  command: ""           # application-provided runner, see experiments/testbed/runner
  num_puzzles: 5
  num_functions: 4
  seed: 42
  max_fix_rounds: 2
"""


def init_config(directory: Path | None = None) -> Path:
    """Scaffold configs/aideal.yaml in `directory` (default cwd)."""
    root = (directory or Path.cwd()).resolve()
    path = root / "configs" / "aideal.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(CONFIG_TEMPLATE, encoding="utf-8")
    return path


def load_tasks(cfg: AidealConfig) -> list[dict]:
    """Read integration_tasks.yaml -> list of {id, language, goal, apis}."""
    if not cfg.integration_tasks.exists():
        return []
    data = yaml.safe_load(cfg.integration_tasks.read_text(encoding="utf-8")) or {}
    return data.get("tasks", [])
