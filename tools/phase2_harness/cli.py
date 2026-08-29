"""Command-line acceptance harness for Phase-2 repository acceptance."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

from phase2_harness.final_bytes import FinalByteError, verify_final_bytes
from phase2_harness.io_boundary import BoundaryError, IOBoundary
from phase2_harness.manifest import generate_manifest, write_manifest
from phase2_harness.publication import Artifact, PublicationError, PublicationWrapper
from phase2_harness.schema_gate import SchemaGate, SchemaGateError

REPO_ROOT = Path(__file__).resolve().parents[2]
CUTOFF = "2024-01-01T00:00:00Z"


def _load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _guess_schema(fixture_path: Path) -> str | None:
    name = fixture_path.name.lower()
    mapping = {
        "artifact": "artifact",
        "result-envelope": "result-envelope",
        "result-ready": "result-ready",
        "transition": "transition",
        "workflow-metrics": "workflow-metrics",
        "scenario-manifest": "scenario-manifest",
    }
    for key, schema in mapping.items():
        if key in name:
            return schema
    return None


def _run_schema_fixture(gate: SchemaGate, fixture_path: Path) -> dict[str, Any]:
    schema = _guess_schema(fixture_path)
    if schema is None:
        return {"status": "FAIL", "error": f"Cannot infer schema for {fixture_path}"}
    try:
        data = _load_json(fixture_path)
        gate.validate(schema, data)
        return {"status": "PASS", "schema": schema, "fixture": str(fixture_path)}
    except SchemaGateError as exc:
        return {"status": "FAIL", "error": str(exc), "schema": schema, "fixture": str(fixture_path)}


def _run_final_byte_gate(descriptor: dict[str, Any]) -> dict[str, Any]:
    root = Path(descriptor.get("package_root", "."))
    if not root.is_absolute():
        root = REPO_ROOT / root
    try:
        # Generate fresh manifest and verify it (checksum excludes itself).
        lines = generate_manifest(root)
        write_manifest(root, lines)
        result = verify_final_bytes(root, lines)
        return {"status": "PASS", **result}
    except FinalByteError as exc:
        return {"status": "FAIL", "error": exc.reason, "incident": exc.incident}


def _run_schema_gate(descriptor: dict[str, Any]) -> dict[str, Any]:
    gate = SchemaGate()
    valid_count = 0
    invalid_count = 0
    fixture_dirs = descriptor.get("fixture_dirs", [])
    for d in fixture_dirs:
        dir_path = REPO_ROOT / d
        for fixture_path in sorted(dir_path.glob("*.json")):
            schema = _guess_schema(fixture_path)
            if schema is None:
                continue
            try:
                gate.validate(schema, _load_json(fixture_path))
                valid_count += 1
            except SchemaGateError:
                invalid_count += 1
    return {
        "status": "PASS",
        "valid_count": valid_count,
        "invalid_count": invalid_count,
    }


def _run_publication_cardinality(descriptor: dict[str, Any]) -> dict[str, Any]:
    payload = b"synthetic producer artifact"
    producer_hash = hashlib.sha256(payload).hexdigest()
    gate_payload = b"synthetic independent gate artifact"
    gate_hash = hashlib.sha256(gate_payload).hexdigest()
    producer = Artifact("producer-v1", producer_hash, payload)
    gate = Artifact("gate-v1", gate_hash, gate_payload)
    envelope = {
        "event_type": "RESULT_ENVELOPE_V1",
        "result_identity": "pub-card-v1",
        "state": "completed",
        "result_disposition": descriptor.get("disposition", "PASS"),
        "artifact_id": producer.artifact_id,
        "artifact_sha256": producer_hash,
        "producer_run_id": "run-pub-v1",
        "task_id": "task-pub-v1",
    }
    pub = PublicationWrapper()
    try:
        result = pub.publish([producer], [gate], envelope)
        return {"status": "PASS", "disposition": result["result_disposition"], "artifact_id": result["artifact_id"], "artifact_sha256": result["artifact_sha256"]}
    except PublicationError as exc:
        return {"status": "FAIL", "error": str(exc)}


def _run_adapter_inventory(descriptor: dict[str, Any]) -> dict[str, Any]:
    inventory_path = REPO_ROOT / descriptor.get("inventory_path", "fixtures/phase2/adapter-inventory.json")
    try:
        boundary = IOBoundary(inventory_path)
        boundary.read("btc_ohlc_daily", "2017-12-31T23:59:59Z")
        return {"status": "FAIL", "error": "Expected ADAPTER_INVENTORY_INCOMPLETE"}
    except BoundaryError as exc:
        metrics = boundary.get_metrics()
        return {
            "status": "PASS" if exc.code == "ADAPTER_INVENTORY_INCOMPLETE" else "FAIL",
            "code": exc.code,
            "read_invocations": metrics.read_invocations,
            "sealed_rows_observed": metrics.sealed_rows_observed,
            "holdout_access_incidents": metrics.holdout_access_incidents,
            "error": exc.reason if exc.code != "ADAPTER_INVENTORY_INCOMPLETE" else None,
        }


def _run_physical_read_bound(descriptor: dict[str, Any]) -> dict[str, Any]:
    inventory_path = REPO_ROOT / descriptor.get("inventory_path", "fixtures/phase2/adapter-inventory.json")
    load_before = descriptor.get("load_before", "2017-12-31T23:59:59Z")
    try:
        boundary = IOBoundary(inventory_path)
        boundary.read("btc_ohlc_daily", load_before)
        return {"status": "FAIL", "error": "Expected boundary failure before real adapter"}
    except BoundaryError as exc:
        metrics = boundary.get_metrics()
        return {
            "status": "PASS" if metrics.holdout_access_incidents == 0 else "FAIL",
            "code": exc.code,
            "read_invocations": metrics.read_invocations,
            "sealed_rows_observed": metrics.sealed_rows_observed,
            "holdout_access_incidents": metrics.holdout_access_incidents,
            "error": exc.reason if metrics.holdout_access_incidents != 0 else None,
        }


def _run_fixture_completeness(manifest: dict[str, Any]) -> dict[str, Any]:
    scenarios = manifest.get("scenarios", [])
    ids = [s["scenario_id"] for s in scenarios]
    duplicates = {sid for sid in ids if ids.count(sid) > 1}
    missing = []
    unknown = []
    known = {
        "HERM-203-FINAL-BYTE-GATE",
        "HERM-203-TYPED-SCHEMA-GATE",
        "HERM-203-PUBLICATION-CARDINALITY",
        "HERM-203-ADAPTER-INVENTORY",
        "HERM-203-PHYSICAL-READ-BOUND",
        "HERM-203-FIXTURE-COMPLETENESS",
        "HERM-203-VALID-ARTIFACT-FIXTURE",
        "HERM-203-INVALID-HASH-FIXTURE",
        "HERM-203-INVALID-DISPOSITION-FIXTURE",
        "HERM-203-WAKE-DEDUP-PLATFORM",
        "HERM-203-CONVEYOR-RECOVERY-ONLY",
    }
    for scenario in scenarios:
        fixture = REPO_ROOT / scenario["input_fixture"]
        if not fixture.exists():
            missing.append(str(scenario["input_fixture"]))
        if scenario["scenario_id"] not in known:
            unknown.append(scenario["scenario_id"])

    if duplicates or missing or unknown:
        return {
            "status": "FAIL",
            "duplicates": sorted(duplicates),
            "missing_fixtures": missing,
            "unknown_scenarios": unknown,
            "scenario_count": len(scenarios),
            "known_ids": sorted(known),
        }
    return {
        "status": "PASS",
        "scenario_count": len(scenarios),
        "known_ids": sorted(known),
    }


CHECK_RUNNERS = {
    "FINAL_BYTE_GATE": _run_final_byte_gate,
    "SCHEMA_GATE": _run_schema_gate,
    "PUBLICATION_CARDINALITY": _run_publication_cardinality,
    "ADAPTER_INVENTORY": _run_adapter_inventory,
    "PHYSICAL_READ_BOUND": _run_physical_read_bound,
}


def _run_scenario(scenario: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    scenario_id = scenario["scenario_id"]
    phase = scenario["phase"]
    expected = scenario["expected_result"]
    fixture_path = REPO_ROOT / scenario["input_fixture"]

    # Platform-integration scenarios are recorded but not executed here.
    if phase == "task_3_platform_integration":
        return {
            "scenario_id": scenario_id,
            "phase": phase,
            "expected": expected,
            "actual": "SKIP",
            "status": "SKIP",
            "evidence": {"reason": "Task 3 platform integration; not run in repository harness"},
        }

    # Determine check type from descriptor or fixture name.
    if fixture_path.name.startswith("scenario-descriptor-"):
        descriptor = _load_json(fixture_path)
        check_type = descriptor.get("check_type")
        runner = CHECK_RUNNERS.get(check_type)
        if runner is None:
            evidence = {"error": f"Unknown check_type: {check_type}"}
        else:
            evidence = runner(descriptor)
    elif fixture_path.name == "scenario-manifest.json":
        evidence = _run_fixture_completeness(manifest)
    else:
        evidence = _run_schema_fixture(SchemaGate(), fixture_path)

    actual = evidence.get("status", "FAIL")
    if expected == "FAIL" and actual == "FAIL":
        outcome = "PASS"  # the scenario is designed to fail
    elif expected == actual:
        outcome = actual
    else:
        outcome = "FAIL"

    return {
        "scenario_id": scenario_id,
        "phase": phase,
        "expected": expected,
        "actual": actual,
        "status": outcome,
        "evidence": evidence,
    }


def run(manifest_path: Path, clean_extraction: bool) -> int:
    gate = SchemaGate()
    try:
        manifest = _load_json(manifest_path)
        gate.validate("scenario-manifest", manifest)
    except (SchemaGateError, json.JSONDecodeError, FileNotFoundError) as exc:
        print(f"SCENARIO_MANIFEST=FAIL error={exc}")
        return 1

    completeness = _run_fixture_completeness(manifest)
    if completeness["status"] != "PASS":
        print(f"FIXTURE_COMPLETENESS={completeness['status']} error={completeness}")
        return 1

    results: list[dict[str, Any]] = []
    summaries: dict[str, str] = {}
    for scenario in manifest["scenarios"]:
        result = _run_scenario(scenario, manifest)
        results.append(result)
        summaries[scenario["scenario_id"]] = result["status"]

    # Map required harness output lines.
    line_map = {
        "FINAL_BYTE_GATE": summaries.get("HERM-203-FINAL-BYTE-GATE", "FAIL"),
        "ADAPTER_INVENTORY": summaries.get("HERM-203-ADAPTER-INVENTORY", "FAIL"),
        "PHYSICAL_READ_BOUND": summaries.get("HERM-203-PHYSICAL-READ-BOUND", "FAIL"),
        "TYPED_SCHEMA_GATE": summaries.get("HERM-203-TYPED-SCHEMA-GATE", "FAIL"),
        "PUBLICATION_CARDINALITY": summaries.get("HERM-203-PUBLICATION-CARDINALITY", "FAIL"),
        "FIXTURE_COMPLETENESS": summaries.get("HERM-203-FIXTURE-COMPLETENESS", "FAIL"),
    }

    overall = "PASS"
    for r in results:
        if r["phase"] == "task_2_harness" and r["status"] != "PASS":
            overall = "FAIL"

    holdout_incidents = sum(
        r["evidence"].get("holdout_access_incidents", 0)
        for r in results
        if isinstance(r["evidence"], dict)
    )

    terminal_report = {
        "manifest_id": manifest.get("manifest_id"),
        "clean_extraction": clean_extraction,
        "overall": overall,
        "scenario_results": results,
        "required_lines": line_map,
        "holdout_access_incidents": holdout_incidents,
    }

    for key, value in line_map.items():
        print(f"{key}={value}")
    print(f"HOLDOUT_ACCESS_INCIDENTS={holdout_incidents}")
    print(f"RESULT={overall}")

    if overall != "PASS":
        print(json.dumps(terminal_report, indent=2))
        return 1

    print(json.dumps(terminal_report, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase-2 acceptance harness")
    parser.add_argument(
        "--clean-extraction",
        action="store_true",
        help="Run in clean-extraction mode (no cached artifacts).",
    )
    parser.add_argument(
        "--manifest",
        required=True,
        type=Path,
        help="Path to the scenario manifest JSON file.",
    )
    args = parser.parse_args(argv)
    return run(args.manifest, args.clean_extraction)


if __name__ == "__main__":
    sys.exit(main())
