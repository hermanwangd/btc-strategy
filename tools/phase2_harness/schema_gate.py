"""Schema gate: load versioned Phase-2 JSON schemas and validate objects."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import jsonschema
from jsonschema import ValidationError


SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "schemas" / "phase2" / "v2"

SCHEMA_NAMES = [
    "artifact",
    "result-envelope",
    "result-ready",
    "transition",
    "workflow-metrics",
    "scenario-manifest",
]


class SchemaGateError(Exception):
    """Raised when a schema cannot be loaded or an instance is invalid."""


class SchemaGate:
    """Loads the Phase-2 v2 schema bundle and validates instances."""

    def __init__(self, schema_root: os.PathLike | None = None) -> None:
        self.schema_root = Path(schema_root) if schema_root else SCHEMA_ROOT
        self._schemas: dict[str, dict[str, Any]] = {}
        self._validators: dict[str, jsonschema.Draft202012Validator] = {}
        self._load_schemas()

    def _load_schemas(self) -> None:
        for name in SCHEMA_NAMES:
            path = self.schema_root / f"{name}.schema.json"
            if not path.exists():
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    schema = json.load(f)
            except json.JSONDecodeError as exc:
                raise SchemaGateError(f"Invalid JSON in schema {path}: {exc}") from exc
            self._schemas[name] = schema
            self._validators[name] = jsonschema.Draft202012Validator(schema)
        if not self._schemas:
            raise SchemaGateError(
                f"No schema files found in schema root: {self.schema_root}"
            )

    def validate(self, name: str, instance: Any) -> None:
        """Validate an instance against the named schema.

        Raises:
            SchemaGateError: if the instance does not conform.
        """
        if name not in self._validators:
            raise SchemaGateError(f"Unknown schema: {name}")
        validator = self._validators[name]
        errors = list(validator.iter_errors(instance))
        if errors:
            messages = "; ".join(
                f"{'.'.join(str(p) for p in e.path)}: {e.message}" for e in errors
            )
            raise SchemaGateError(f"Schema validation failed for {name}: {messages}")

    def get_schema(self, name: str) -> dict[str, Any]:
        if name not in self._schemas:
            raise SchemaGateError(f"Unknown schema: {name}")
        return self._schemas[name].copy()


def validate_artifact(instance: Any) -> None:
    """Validate an object against the artifact schema."""
    SchemaGate().validate("artifact", instance)


def validate_result_envelope(instance: Any) -> None:
    """Validate an object against the result-envelope schema."""
    SchemaGate().validate("result-envelope", instance)


def validate_result_ready(instance: Any) -> None:
    """Validate an object against the result-ready schema."""
    SchemaGate().validate("result-ready", instance)


def validate_transition(instance: Any) -> None:
    """Validate an object against the transition schema."""
    SchemaGate().validate("transition", instance)


def validate_workflow_metrics(instance: Any) -> None:
    """Validate an object against the workflow-metrics schema."""
    SchemaGate().validate("workflow-metrics", instance)


def validate_scenario_manifest(instance: Any) -> None:
    """Validate an object against the scenario-manifest schema."""
    SchemaGate().validate("scenario-manifest", instance)
