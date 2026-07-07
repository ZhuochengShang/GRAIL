#!/usr/bin/env python3
"""Pre-flight for bench_conditions.py — run on the Mac BEFORE benching.

1. Lists which codex / gemini model IDs YOUR accounts actually offer
   (so BENCH_CODEX_MODEL / BENCH_GEMINI_MODEL are set to real IDs, not guesses).
2. Sends ONE tiny request through each provider path the harness uses
   (openai chat, codex/Responses, google) to prove keys + plumbing end-to-end.

Needs: OPENAI_API_KEY, GOOGLE_API_KEY in env. Never prints keys.
Usage:  python bench_check.py            # list + smoke test
        python bench_check.py --list     # list models only (no test calls)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve()
                       .parents[2] / "grail-agent" / "src"))


def list_models() -> tuple[list[str], list[str]]:
    codex, gemini = [], []
    try:
        from openai import OpenAI
        ids = [m.id for m in OpenAI().models.list().data]
        codex = sorted(i for i in ids if "codex" in i)
        print("OpenAI codex-capable models on this account:")
        print("  " + ("\n  ".join(codex) if codex else "(none visible — use a gpt chat model?)"))
    except Exception as e:
        print(f"OpenAI model list FAILED: {type(e).__name__}: {str(e)[:200]}")
    try:
        from google import genai
        names = [m.name.split("/")[-1] for m in genai.Client().models.list()]
        gemini = sorted(n for n in names if n.startswith(("gemini-2", "gemini-3")))
        code_named = [n for n in names if "code" in n.lower()]
        print("Gemini models on this account (2.x/3.x):")
        print("  " + "\n  ".join(gemini[:20]))
        print("Gemini code-named models:",
              code_named or "(none — Gemini has no separate code API; "
                            "pick a strong general model, e.g. the newest pro)")
    except Exception as e:
        print(f"Gemini model list FAILED: {type(e).__name__}: {str(e)[:200]}")
    return codex, gemini


def smoke(codex_ids: list[str], gemini_ids: list[str]) -> None:
    from aideal.config import ModelSpec
    from aideal.llm import invoke_text, usage_snapshot, reset_usage

    def one(provider: str, model: str) -> None:
        try:
            reset_usage()
            out = invoke_text(ModelSpec(provider=provider, model=model),
                              "Reply with exactly: OK", "ping")
            u = usage_snapshot()
            print(f"  {provider}:{model:34} -> {out.strip()[:20]!r}  "
                  f"(in={u['input_tokens']} out={u['output_tokens']} tokens)")
        except Exception as e:
            print(f"  {provider}:{model:34} -> FAILED {type(e).__name__}: {str(e)[:140]}")

    print("\nSmoke test (1 tiny call per provider path):")
    one("openai", os.environ.get("BENCH_OPENAI_MODEL", "gpt-4o"))
    cx = os.environ.get("BENCH_CODEX_MODEL") or (codex_ids[-1] if codex_ids else None)
    if cx:
        one("codex", cx)
        print(f"    -> export BENCH_CODEX_MODEL={cx}")
    else:
        print("  codex: no codex model found; set BENCH_CODEX_MODEL manually")
    gm = os.environ.get("BENCH_GEMINI_MODEL") or \
        next((g for g in reversed(gemini_ids) if "pro" in g), None)
    if gm:
        one("google", gm)
        print(f"    -> export BENCH_GEMINI_MODEL={gm}")
    else:
        print("  google: set BENCH_GEMINI_MODEL manually")


if __name__ == "__main__":
    missing = [k for k in ("OPENAI_API_KEY", "GOOGLE_API_KEY") if not os.environ.get(k)]
    if missing:
        print("missing env:", ", ".join(missing))
        raise SystemExit(2)
    c, g = list_models()
    if "--list" not in sys.argv:
        smoke(c, g)
