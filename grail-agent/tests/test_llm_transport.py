import sys
import types
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from aideal.config import ModelSpec  # noqa: E402
from aideal.llm import get_chat_model  # noqa: E402


def test_google_transport_is_bounded_and_configurable(monkeypatch):
    captured = {}

    class FakeGoogleModel:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setitem(
        sys.modules,
        "langchain_google_genai",
        types.SimpleNamespace(ChatGoogleGenerativeAI=FakeGoogleModel),
    )
    monkeypatch.setenv("AIDEAL_GOOGLE_REQUEST_TIMEOUT_S", "123")
    monkeypatch.setenv("AIDEAL_GOOGLE_MAX_RETRIES", "1")

    get_chat_model(ModelSpec(provider="google", model="gemini-test"))

    assert captured["request_timeout"] == 123.0
    assert captured["retries"] == 1
    assert captured["model"] == "gemini-test"

