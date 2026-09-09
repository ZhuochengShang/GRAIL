import json

from experiments.mdanalysis import run_full_2x2_pipeline as pipeline


def test_mdanalysis_waits_for_all_priority_repositories(tmp_path, monkeypatch):
    def mark(repo, job):
        (tmp_path / f"{repo}_pipeline_watchdog.state.json").write_text(
            json.dumps({"jobs": {job: {"status": "succeeded"}}}))

    mark("tslearn", "tslearn_complete_full235")
    sleeps = []

    def finish_others(seconds):
        sleeps.append(seconds)
        mark("mir_eval", "mir_eval_complete_2x2")
        mark("thumbnailator", "thumbnailator_complete_2x2")

    monkeypatch.setattr(pipeline.time, "sleep", finish_others)
    pipeline.wait_for_priority_repositories(tmp_path)
    assert sleeps == [30]
    pipeline.wait_for_priority_repositories(tmp_path)
    assert sleeps == [30]
