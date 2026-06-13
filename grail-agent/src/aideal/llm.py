"""Provider abstraction with author/audience role separation.

Author models WRITE documentation and tests (small/cheap is fine).
Audience models CONSUME documentation to write code (the coding agent).

Supported providers: openai, anthropic, google, ollama (for Kimi/Qwen/local
open-source models). Imports are lazy so only the used provider's package
is required.
"""

from __future__ import annotations

from .config import ModelSpec


def get_chat_model(spec: ModelSpec, temperature: float = 0.0):
    """Return a LangChain chat model for the given provider/model."""
    provider = spec.provider.lower()
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=spec.model, temperature=temperature)
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=spec.model, temperature=temperature)
    if provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=spec.model, temperature=temperature)
    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=spec.model, temperature=temperature)
    raise ValueError(f"Unknown provider: {spec.provider}")


def invoke_text(spec: ModelSpec, system: str, user: str) -> str:
    """One-shot text completion; returns the model's text content."""
    llm = get_chat_model(spec)
    resp = llm.invoke([("system", system), ("user", user)])
    return resp.content if isinstance(resp.content, str) else str(resp.content)
