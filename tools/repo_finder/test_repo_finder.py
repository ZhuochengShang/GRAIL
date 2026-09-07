from tools.repo_finder.sedona_shape_repo_finder import (
    detect_docs_tests,
    score_candidate,
)


def test_published_score_formula_has_no_hidden_library_or_pypi_bonus():
    repo = {"stargazers_count": 1000, "forks_count": 150}
    structure = {"has_tests": True, "has_docs": True, "has_examples": True}
    score, _ = score_candidate(
        repo, paths=["src/api.py"], src=["src/api.py"],
        api_info={"public_api_count": 80},
        activity={"active": True, "days": 20}, structure=structure,
        lib_score=100, pypi={"pypi_found": True, "downloads_total": 99_000_000},
        issue_info={"usage_issue_hits": 50})
    # 10 stars + 7.5 forks + 20 API + 15 activity + 8 tests + 4 docs
    # + 4 examples + 8 issue-confusion.
    assert score == 76.5


def test_checked_in_sample_data_detection_is_path_and_extension_based():
    result = detect_docs_tests([
        "README.md", "tests/test_audio.py", "tests/data/example.wav",
        "src/package.py",
    ])
    assert result["has_tests"]
    assert result["has_sample_data"]
    assert result["sample_data_file_count"] == 1
    assert result["sample_data_files"] == ["tests/data/example.wav"]


def test_source_code_in_fixture_directory_is_not_counted_as_sample_data():
    result = detect_docs_tests(["tests/fixtures/generator.py", "tests/test_api.py"])
    assert not result["has_sample_data"]
