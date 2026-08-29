"""Tests for phase2_harness.publication."""

import hashlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

from phase2_harness.publication import Artifact, PublicationError, PublicationWrapper


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class TestPublicationWrapper(unittest.TestCase):
    def setUp(self):
        self.pub = PublicationWrapper()
        self.producer_bytes = b"producer-payload"
        self.producer_hash = _hash(self.producer_bytes)
        self.gate_bytes = b"gate-payload"
        self.gate_hash = _hash(self.gate_bytes)

    def _valid_envelope(self, disposition: str = "PASS") -> dict:
        return {
            "event_type": "RESULT_ENVELOPE_V1",
            "result_identity": "result-1",
            "state": "completed",
            "result_disposition": disposition,
            "artifact_id": "producer-artifact",
            "artifact_sha256": self.producer_hash,
            "producer_run_id": "run-1",
            "task_id": "task-1",
        }

    def test_pass_with_gate_returns_envelope(self):
        producer = Artifact("producer-artifact", self.producer_hash, self.producer_bytes)
        gate = Artifact("gate-artifact", self.gate_hash, self.gate_bytes)
        envelope = self._valid_envelope("PASS")
        result = self.pub.publish([producer], [gate], envelope)
        self.assertEqual(result["result_disposition"], "PASS")

    def test_rejected_without_gate(self):
        producer = Artifact("producer-artifact", self.producer_hash, self.producer_bytes)
        envelope = self._valid_envelope("REJECTED")
        result = self.pub.publish([producer], [], envelope)
        self.assertEqual(result["result_disposition"], "REJECTED")

    def test_zero_producer_artifacts(self):
        with self.assertRaises(PublicationError):
            self.pub.publish([], [], self._valid_envelope())

    def test_multiple_producer_artifacts(self):
        producer = Artifact("producer-artifact", self.producer_hash, self.producer_bytes)
        with self.assertRaises(PublicationError):
            self.pub.publish([producer, producer], [], self._valid_envelope())

    def test_multiple_gate_artifacts(self):
        producer = Artifact("producer-artifact", self.producer_hash, self.producer_bytes)
        gate = Artifact("gate-artifact", self.gate_hash, self.gate_bytes)
        with self.assertRaises(PublicationError):
            self.pub.publish([producer], [gate, gate], self._valid_envelope())

    def test_pass_without_gate_rejected(self):
        producer = Artifact("producer-artifact", self.producer_hash, self.producer_bytes)
        with self.assertRaises(PublicationError) as ctx:
            self.pub.publish([producer], [], self._valid_envelope("PASS"))
        self.assertIn("independent Gate artifact", str(ctx.exception))

    def test_pass_with_same_artifact_id(self):
        producer = Artifact("shared-id", self.producer_hash, self.producer_bytes)
        gate = Artifact("shared-id", self.gate_hash, self.gate_bytes)
        with self.assertRaises(PublicationError) as ctx:
            self.pub.publish([producer], [gate], self._valid_envelope())
        self.assertIn("collides", str(ctx.exception))

    def test_pass_with_same_hash(self):
        producer = Artifact("producer-artifact", self.producer_hash, self.producer_bytes)
        gate = Artifact("gate-artifact", self.producer_hash, self.producer_bytes)
        with self.assertRaises(PublicationError) as ctx:
            self.pub.publish([producer], [gate], self._valid_envelope())
        self.assertIn("collides", str(ctx.exception))

    def test_hash_mismatch_producer(self):
        producer = Artifact("producer-artifact", "0" * 64, self.producer_bytes)
        gate = Artifact("gate-artifact", self.gate_hash, self.gate_bytes)
        with self.assertRaises(PublicationError) as ctx:
            self.pub.publish([producer], [gate], self._valid_envelope())
        self.assertIn("hash mismatch", str(ctx.exception))

    def test_envelope_artifact_id_mismatch(self):
        producer = Artifact("producer-artifact", self.producer_hash, self.producer_bytes)
        gate = Artifact("gate-artifact", self.gate_hash, self.gate_bytes)
        envelope = self._valid_envelope()
        envelope["artifact_id"] = "other-artifact"
        with self.assertRaises(PublicationError) as ctx:
            self.pub.publish([producer], [gate], envelope)
        self.assertIn("does not match producer", str(ctx.exception))

    def test_invalid_envelope_schema(self):
        producer = Artifact("producer-artifact", self.producer_hash, self.producer_bytes)
        gate = Artifact("gate-artifact", self.gate_hash, self.gate_bytes)
        envelope = {"event_type": "RESULT_ENVELOPE_V1"}
        with self.assertRaises(PublicationError):
            self.pub.publish([producer], [gate], envelope)

    def test_no_envelope(self):
        producer = Artifact("producer-artifact", self.producer_hash, self.producer_bytes)
        with self.assertRaises(PublicationError):
            self.pub.publish([producer], [], None)


if __name__ == "__main__":
    unittest.main()
