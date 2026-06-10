import json
import sys
from pathlib import Path

from .analyzer import analyze_python_script
from .planner import build_plan


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m rdpro_section_codegen.cli <python_script>", file=sys.stderr)
        return 2

    script_path = Path(sys.argv[1]).expanduser().resolve()
    py_text = script_path.read_text(encoding="utf-8", errors="ignore")
    analysis = analyze_python_script(py_text)
    plan = build_plan(analysis)
    print(json.dumps(plan.to_dict(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
