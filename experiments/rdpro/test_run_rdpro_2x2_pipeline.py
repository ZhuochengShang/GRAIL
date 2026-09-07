import json
from pathlib import Path
import tempfile
import unittest

from experiments.rdpro import run_rdpro_2x2_pipeline as pipeline


class RDProPipelineTests(unittest.TestCase):
    def make_result(self, path: Path, **changes):
        result = {
            "check": "comprehension", "mode": "execute", "doc_source": "aideal",
            "run": {"api_count": 88, "manifest_api_count": 88,
                    "manifest_sha256": pipeline.MANIFEST_SHA256,
                    "doc_scope": "relevant", "max_fix_rounds": 0},
            "coverage": {"executed": 88}, "metrics": {
                f"api{i}": {"status": "pass", "error_category": None} for i in range(88)},
            "sample_data_warnings": [],
        }
        result.update(changes)
        path.write_text(json.dumps(result), encoding="utf-8")

    def test_inventory_hash_matches_frozen_protocol(self):
        manifest = pipeline.HISTORICAL_A1 / "experiments/rdpro/docs/api_manifest_shared.json"
        data = pipeline.validate_manifest(manifest)
        self.assertEqual(len(data["apis"]), 88)

    def test_result_validation_accepts_exact_protocol(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.json"
            self.make_result(path)
            self.assertEqual(len(pipeline.validate_result(path, "aideal")["metrics"]), 88)

    def test_result_validation_rejects_wrong_scope(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.json"
            self.make_result(path)
            data = json.loads(path.read_text())
            data["run"]["doc_scope"] = "full"
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(RuntimeError, "doc_scope"):
                pipeline.validate_result(path, "aideal")

    def test_dependency_graph_enforces_matched_b2_baseline(self):
        jobs = {job["id"]: job for job in pipeline.build_plan()["jobs"]}
        self.assertIn("rdpro_a2_zero", jobs["rdpro_b2_sync"]["depends_on"])
        self.assertIn("rdpro_b2_repair_checkpoint", jobs["rdpro_b2_zero"]["depends_on"])
        self.assertEqual(pipeline.build_plan()["max_parallel"], 2)

    def test_every_comprehension_is_shared_relevant_zero(self):
        for job in pipeline.build_plan()["jobs"]:
            if not job["id"].endswith("_zero"):
                continue
            command = job["command"]
            self.assertEqual(command[command.index("--doc-scope") + 1], "relevant")
            self.assertEqual(command[command.index("--max-fix-rounds") + 1], "0")
            self.assertEqual(command[command.index("--manifest") + 1],
                             "docs/api_manifest_shared.json")
            self.assertIn("--resume", command)

    def test_docfix_outputs_are_rooted_from_worker_cwd(self):
        jobs = {job["id"]: job for job in pipeline.build_plan()["jobs"]}
        for cell in ("b1", "b2"):
            command = jobs[f"rdpro_{cell}_repair"]["command"]
            for option in ("--from-results", "--report", "--deep-dive-out"):
                value = command[command.index(option) + 1]
                self.assertTrue(value.startswith("experiments/rdpro/"), (option, value))

    def test_run_requires_explicit_paid_confirmation(self):
        with self.assertRaisesRegex(SystemExit, "confirm-paid-llm"):
            pipeline.run_watchdog(Path("unused.yaml"), False)


if __name__ == "__main__":
    unittest.main()
