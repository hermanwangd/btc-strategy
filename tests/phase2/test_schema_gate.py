"""Tests for phase2_harness.schema_gate."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

from phase2_harness.schema_gate import SchemaGate, SchemaGateError


class TestSchemaGate(unittest.TestCase):
    def setUp(self):
        self.gate = SchemaGate()

    def test_load_all_schemas(self):
        for name in [
            "artifact",
            "result-envelope",
            "result-ready",
            "transition",
            "workflow-metrics",
            "scenario-manifest",
        ]:
            schema = self.gate.get_schema(name)
            self.assertIsInstance(schema, dict)
            self.assertIn("$schema", schema)

    def test_artifact_valid(self):
        self.gate.validate(
            "artifact",
            {
                "artifact_id": "artifact-1",
                "sha256": "0" * 64,
            },
        )

    def test_artifact_missing_sha256(self):
        with self.assertRaises(SchemaGateError):
            self.gate.validate("artifact", {"artifact_id": "artifact-1"})

    def test_artifact_uppercase_sha256_rejected(self):
        with self.assertRaises(SchemaGateError):
            self.gate.validate(
                "artifact",
                {"artifact_id": "artifact-1", "sha256": "0" * 63 + "A"},
            )

    def test_artifact_sha256_wrong_length(self):
        with self.assertRaises(SchemaGateError):
            self.gate.validate(
                "artifact",
                {"artifact_id": "artifact-1", "sha256": "abc"},
            )

    def test_result_envelope_dispositions(self):
        for disp in ("PASS", "REJECTED", "BLOCKED", "FAILED"):
            self.gate.validate(
                "result-envelope",
                {
                    "event_type": "RESULT_ENVELOPE_V1",
                    "result_identity": "r1",
                    "state": "completed",
                    "result_disposition": disp,
                    "artifact_id": "a1",
                    "artifact_sha256": "0" * 64,
                    "producer_run_id": "run-1",
                },
            )

    def test_result_envelope_invalid_disposition(self):
        with self.assertRaises(SchemaGateError):
            self.gate.validate(
                "result-envelope",
                {
                    "event_type": "RESULT_ENVELOPE_V1",
                    "result_identity": "r1",
                    "state": "completed",
                    "result_disposition": "APPROVED",
                    "artifact_id": "a1",
                    "artifact_sha256": "0" * 64,
                    "producer_run_id": "run-1",
                },
            )

    def test_workflow_metrics_negative_rejected(self):
        with self.assertRaises(SchemaGateError):
            self.gate.validate(
                "workflow-metrics",
                {
                    "read_invocations": -1,
                    "sealed_rows_observed": 0,
                    "holdout_access_incidents": 0,
                },
            )

    def test_scenario_manifest_valid(self):
        self.gate.validate(
            "scenario-manifest",
            {
                "manifest_id": "m1",
                "scenarios": [
                    {
                        "scenario_id": "s1",
                        "phase": "task_2_harness",
                        "input_fixture": "fixtures/phase2/valid/foo.json",
                        "expected_result": "PASS",
                        "required_evidence_fields": ["artifact_sha256"],
                    }
                ],
            },
        )

    def test_unknown_schema(self):
        with self.assertRaises(SchemaGateError):
            self.gate.validate("not-a-schema", {})

    def test_missing_schema_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SchemaGateError):
                SchemaGate(tmp)

    def test_schema_root_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            schema = {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {"x": {"type": "integer"}},
                "required": ["x"],
            }
            with open(os.path.join(tmp, "artifact.schema.json"), "w") as f:
                json.dump(schema, f)
            gate = SchemaGate(tmp)
            with self.assertRaises(SchemaGateError):
                gate.validate("artifact", {})
            gate.validate("artifact", {"x": 1})


if __name__ == "__main__":
    unittest.main()
