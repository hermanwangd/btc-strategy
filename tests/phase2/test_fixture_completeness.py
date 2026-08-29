"""Tests for fixture completeness and scenario manifest integrity."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

from phase2_harness.cli import _load_json, _run_fixture_completeness, run


class TestFixtureCompleteness(unittest.TestCase):
    def test_manifest_is_valid(self):
        manifest_path = Path(__file__).resolve().parents[2] / "fixtures" / "phase2" / "scenario-manifest.json"
        manifest = _load_json(manifest_path)
        self.assertEqual(manifest["manifest_id"], "phase2-scenario-manifest-v2")
        self.assertGreaterEqual(len(manifest["scenarios"]), 6)

    def test_all_input_fixtures_exist(self):
        manifest_path = Path(__file__).resolve().parents[2] / "fixtures" / "phase2" / "scenario-manifest.json"
        manifest = _load_json(manifest_path)
        result = _run_fixture_completeness(manifest)
        self.assertEqual(result["status"], "PASS", result)

    def test_rejects_duplicate_ids(self):
        manifest = {
            "manifest_id": "dup-test",
            "scenarios": [
                {"scenario_id": "S1", "phase": "task_2_harness", "input_fixture": "a.json", "expected_result": "PASS", "required_evidence_fields": ["x"]},
                {"scenario_id": "S1", "phase": "task_2_harness", "input_fixture": "b.json", "expected_result": "PASS", "required_evidence_fields": ["x"]},
            ],
        }
        result = _run_fixture_completeness(manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["duplicates"], ["S1"])

    def test_rejects_missing_fixtures(self):
        manifest = {
            "manifest_id": "missing-test",
            "scenarios": [
                {"scenario_id": "S1", "phase": "task_2_harness", "input_fixture": "does-not-exist.json", "expected_result": "PASS", "required_evidence_fields": ["x"]},
            ],
        }
        result = _run_fixture_completeness(manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("does-not-exist.json", result["missing_fixtures"])

    def test_rejects_unknown_scenario_ids(self):
        manifest = {
            "manifest_id": "unknown-test",
            "scenarios": [
                {"scenario_id": "UNKNOWN-SCENARIO", "phase": "task_2_harness", "input_fixture": "fixtures/phase2/valid/artifact.json", "expected_result": "PASS", "required_evidence_fields": ["x"]},
            ],
        }
        result = _run_fixture_completeness(manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("UNKNOWN-SCENARIO", result["unknown_scenarios"])

    def test_task_3_platform_scenarios_are_skipped(self):
        manifest_path = Path(__file__).resolve().parents[2] / "fixtures" / "phase2" / "scenario-manifest.json"
        manifest = _load_json(manifest_path)
        skipped = [s for s in manifest["scenarios"] if s["phase"] == "task_3_platform_integration"]
        self.assertTrue(skipped)
        for s in skipped:
            self.assertEqual(s["expected_result"], "SKIP")


class TestHarnessCLI(unittest.TestCase):
    def test_harness_runs_successfully(self):
        manifest_path = Path(__file__).resolve().parents[2] / "fixtures" / "phase2" / "scenario-manifest.json"
        exit_code = run(manifest_path, clean_extraction=True)
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
