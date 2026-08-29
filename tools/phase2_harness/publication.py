"""Publication wrapper enforcing one-artifact/one-envelope and Gate independence."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

from phase2_harness.schema_gate import SchemaGate, SchemaGateError


@dataclass(frozen=True)
class Artifact:
    """An artifact with its canonical bytes and declared metadata."""

    artifact_id: str
    sha256: str
    bytes_: bytes


class PublicationError(Exception):
    """Raised when publication cannot produce a terminal result."""


class PublicationWrapper:
    """Validate terminal artifact publication before it becomes a result.

    The wrapper enforces:
      - exactly one terminal producer artifact;
      - at most one independent Gate validation artifact;
      - recomputed SHA-256 matches declared metadata;
      - producer and Gate artifacts are distinct identities;
      - producer PASS is never treated as independent Gate approval;
      - a PASS envelope requires an independent Gate artifact;
      - invalid publication produces no terminal result.
    """

    def __init__(self, schema_gate: SchemaGate | None = None) -> None:
        self.schema_gate = schema_gate or SchemaGate()

    def _hash(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _validate_artifact(self, artifact: Artifact, context: str) -> None:
        meta = {"artifact_id": artifact.artifact_id, "sha256": artifact.sha256}
        try:
            self.schema_gate.validate("artifact", meta)
        except SchemaGateError as exc:
            raise PublicationError(f"{context} metadata invalid: {exc}") from exc
        canonical = self._hash(artifact.bytes_)
        if canonical != artifact.sha256:
            raise PublicationError(
                f"{context} hash mismatch: declared={artifact.sha256} canonical={canonical}"
            )

    def publish(
        self,
        producer_artifacts: list[Artifact],
        gate_artifacts: list[Artifact],
        envelope: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Attempt to publish a terminal result.

        Args:
            producer_artifacts: Terminal artifacts produced by the worker.
            gate_artifacts: Independent Gate validation artifacts.
            envelope: Optional pre-declared envelope to validate and seal.

        Returns:
            A validated result envelope when all checks pass.

        Raises:
            PublicationError: on any invalid condition; no terminal result is produced.
        """
        # Cardinality checks on producer artifacts
        if not producer_artifacts:
            raise PublicationError("No terminal producer artifact.")
        if len(producer_artifacts) > 1:
            raise PublicationError("Multiple terminal producer artifacts.")
        producer = producer_artifacts[0]

        # Cardinality checks on Gate artifacts
        if len(gate_artifacts) > 1:
            raise PublicationError("Multiple independent Gate artifacts.")
        gate = gate_artifacts[0] if gate_artifacts else None

        # Validate artifact hashes
        self._validate_artifact(producer, "producer artifact")
        if gate:
            self._validate_artifact(gate, "independent Gate artifact")

        # Distinctness between producer and Gate artifacts
        if gate and producer.artifact_id == gate.artifact_id:
            raise PublicationError("Producer artifact ID collides with Gate artifact ID.")
        if gate and producer.sha256 == gate.sha256:
            raise PublicationError("Producer artifact hash collides with Gate artifact hash.")

        # Validate envelope if supplied, otherwise build a minimal envelope.
        if envelope is None:
            if gate:
                raise PublicationError("Gate artifact present but no envelope.")
            raise PublicationError("No terminal envelope.")

        try:
            self.schema_gate.validate("result-envelope", envelope)
        except SchemaGateError as exc:
            raise PublicationError(f"Envelope schema invalid: {exc}") from exc

        # Envelope must reference the producer artifact
        if envelope.get("artifact_id") != producer.artifact_id:
            raise PublicationError(
                f"Envelope artifact_id {envelope.get('artifact_id')} does not match "
                f"producer {producer.artifact_id}."
            )
        if envelope.get("artifact_sha256") != producer.sha256:
            raise PublicationError("Envelope artifact_sha256 does not match producer hash.")

        # Disposition-specific rules
        disposition = envelope.get("result_disposition")
        if disposition == "PASS":
            if not gate:
                raise PublicationError(
                    "Producer PASS cannot be published without independent Gate artifact."
                )
        else:
            # Non-PASS dispositions must not carry a Gate artifact
            if gate:
                raise PublicationError(
                    f"Gate artifact present for non-PASS disposition {disposition}."
                )

        return envelope
