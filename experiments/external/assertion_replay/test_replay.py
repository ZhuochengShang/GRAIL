import json
from pathlib import Path
import tempfile
import unittest

from .evidence import relocate, retained_source
from .execute import outcome
from .report import publish


class ReplayTests(unittest.TestCase):
    def test_native_code_recovers_case_colliding_file(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            path = project / "ApiTest.java"
            original = '// TODO API_TEST_START\nwrongLowercaseCall();\n// TODO API_TEST_END'
            path.write_text(original)
            result = retained_source(project, "A2", {"name": "Region", "status": "pass",
                "execution_evidence": {"scala_file": str(path), "code": "correctUppercaseCall();"}})
            self.assertEqual(result["binding"], "full_native_code")
            self.assertIn("correctUppercaseCall();", result["source"])
            self.assertNotIn("wrongLowercaseCall();", result["source"])
            self.assertEqual(path.read_text(), original)

    def test_provider_failure_never_replays_stale_file(self):
        result = retained_source(Path("/irrelevant"), "A1", {"name": "region", "error_category": "llm-error"})
        self.assertFalse(result["available"])

    def test_path_relocation_preserves_assertion_logic(self):
        source = 'String image = "/project/source/grid.png"; String output_dir = "/project/output"; assert false : "sentinel";'
        changed, replacements = relocate(source, Path("/project"), {"grid_png": "source/grid.png"})
        self.assertNotIn('= "/project/', changed)
        self.assertIn('assert false : "sentinel";', changed)
        self.assertEqual(len(replacements), 2)

    def test_markers_do_not_override_failed_assertion(self):
        event = {"exit_code": 1, "stdout": "__DONE__ __CHECK__", "stderr": "java.lang.AssertionError"}
        self.assertEqual(outcome(event, {}), "assertion_failure")
        event.update(exit_code=0, stderr="")
        self.assertEqual(outcome(event, {}), "pass")

    def test_java_octal_literal_is_preserved(self):
        source = r'String exif = "Exif\0\0"; String path = "/project/output";'
        changed, _ = relocate(source, Path("/project"), {})
        self.assertIn(r'"Exif\0\0"', changed)

    def test_missing_cells_and_unbound_evidence_are_explicit(self):
        with tempfile.TemporaryDirectory() as temp:
            publish(Path(temp), {"A1": {"complete": False, "source_sha256": "test", "records": [
                {"api": "test", "native": {"status": "pass"}, "binding": "retained_unbound_legacy",
                 "replay": {"variants": {"assertions_off": {"outcome": "pass"},
                                         "assertions_on": {"outcome": "assertion_failure"}}}}]}})
            summary = json.loads((Path(temp) / "summary.json").read_text())
            self.assertEqual(summary["cells"][0]["native_pass"], 1)
            self.assertEqual(summary["cells"][0]["off_pass_on_fail"], 1)
            self.assertEqual(summary["cells"][0]["unbound_retained_replays"], 1)
            self.assertNotIn("native_pass", summary["cells"][1])


if __name__ == "__main__":
    unittest.main()
