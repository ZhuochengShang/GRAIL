"""Bridge from the GRAIL agent (application) to the AIDEAL error log (backend).

GRAIL imports this; AIDEAL never imports GRAIL — layering stays one-way.
Every real failure in the repair loop (validation reject, semantic reject,
compile/run failure) is appended to logs/error_log.jsonl so that
`aideal.cli notes-distill` and `aideal.cli alias-suggest` work on real data.

All functions are best-effort no-ops if AIDEAL or its config is unavailable,
so the agent never breaks because of logging.
"""

from __future__ import annotations

import re

_RUN_ID = None


def _log():
    """Lazily resolve (ErrorLog, run_id); None if AIDEAL is unavailable."""
    global _RUN_ID
    try:
        from aideal.config import load_config
        from aideal.error_log import ErrorLog, new_run_id

        cfg = load_config()
        if _RUN_ID is None:
            _RUN_ID = new_run_id()
        return ErrorLog(cfg.error_log), _RUN_ID
    except Exception:
        return None, None


_ERROR_LINE_RE = re.compile(r"(?:error|Error|ERROR|Exception)[:\]]?\s*(.{10,200})")
_CAUSE_RE = re.compile(r"((?:\w+\.)+\w*(?:Exception|Error)[^\n]{0,160})")
_FN_RE = re.compile(r"value (\w+) is not a member|not found: value (\w+)|method (\w+)")


def _first(pattern: re.Pattern, text: str) -> str:
    m = pattern.search(text or "")
    if not m:
        return ""
    return next((g for g in m.groups() if g), m.group(0))


def log_failure(
    step: str,
    section: str,
    error_text: str,
    task: str = "",
    apis: list[str] | None = None,
    fix_hint: str = "",
) -> None:
    """Append one structured failure record. Never raises."""
    log, run_id = _log()
    if log is None:
        return
    try:
        text = (error_text or "")[:4000]
        # prefer the real API in play; the hallucinated name stays in `error`
        # so that alias-suggest can mine it and map alias -> real function
        function = (apis[0] if apis else "") or _first(_FN_RE, text) or section
        log.append(
            run_id=run_id,
            step=step,
            language="Scala",
            task=task or section,
            status="fail",
            function=function,
            error=(_first(_ERROR_LINE_RE, text) or text[:200]).strip(),
            root_cause=_first(_CAUSE_RE, text).strip(),
            suggested_fix_code=(fix_hint or "")[:300].strip(),
        )
    except Exception:
        pass
