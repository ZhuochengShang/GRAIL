import hashlib
import io
import zipfile

import yaml

from aideal.config import load_config
from aideal.doc_snapshot import prepare_original_docs


def test_prepare_original_docs_from_config(tmp_path, monkeypatch):
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w") as zf:
        zf.writestr("site/index.html", "<h1>Guide</h1><p>Use Widget.run()</p>")
        zf.writestr("site/_static/x.js", "ignored")
    data = payload.getvalue()
    (tmp_path / "configs").mkdir()
    (tmp_path / "configs" / "aideal.yaml").write_text(yaml.safe_dump({
        "project": {"name": "x", "language": "Python"},
        "files": {
            "original_readme": [".docs/bundle.md"],
            "original_doc_archives": [{"label": "official", "url": "https://example/x.zip",
                                        "sha256": hashlib.sha256(data).hexdigest()}],
            "original_doc_snapshot": ".docs/bundle.md",
        },
    }), encoding="utf-8")

    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self): return data

    monkeypatch.setattr("urllib.request.urlopen", lambda *_a, **_k: Response())
    cfg = load_config(tmp_path / "configs" / "aideal.yaml")
    result = prepare_original_docs(cfg)
    text = (tmp_path / ".docs" / "bundle.md").read_text()
    assert "official: site/index.html" in text
    assert "Use Widget.run()" in text
    assert result["archives"][0]["text_files"] == 1
    assert result["bundle_sha256"]
