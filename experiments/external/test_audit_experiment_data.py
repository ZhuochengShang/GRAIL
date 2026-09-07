import subprocess

from experiments.external.audit_experiment_data import fixture_evidence, snippet_evidence


def test_fixture_must_match_checked_in_bytes(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    fixture = tmp_path / "input.txt"
    fixture.write_text("1 2\n3 4\n")
    subprocess.run(["git", "-C", str(tmp_path), "add", "input.txt"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=Test", "-c",
                    "user.email=test@example.invalid", "commit", "-qm", "Pin fixture"], check=True)
    row = fixture_evidence(fixture, tmp_path)
    assert row["matches_pinned_blob"] is True
    assert row["decoded"]["data_lines"] == 2
    fixture.write_text("5 6\n")
    assert fixture_evidence(fixture, tmp_path)["matches_pinned_blob"] is False
    other = tmp_path / "untracked.txt"
    other.write_text("1 2\n")
    assert fixture_evidence(other, tmp_path)["tracked_at_pinned_commit"] is False


def test_declaring_fixture_in_scaffold_does_not_prove_snippet_uses_it():
    code = 'input_file = "checked-in.txt"\n# START\nvalue = target(values)\nassert value > 0\nprint("__CHECK__")\n# END'
    row = snippet_evidence(code, "target", ["# START", "# END"],
                           {"input_file": "checked-in.txt", "output_dir": "out"}, "values = [1, 2]")
    assert row["configured_fixture_bindings_referenced"] == []
    assert row["preloaded_bindings_referenced"] == ["values"]
    assert row["target_name_call_visible"] is True
    assert row["assertion_text_visible"] is True
    assert row["semantic_validation"].startswith("unverified")


def test_unknown_snippet_region_does_not_claim_api_was_tested():
    row = snippet_evidence("target(input_file)", "target", ["# START", "# END"], {}, "")
    assert row["snippet_region_found"] is False
    assert row["semantic_validation"] == "unverified"
