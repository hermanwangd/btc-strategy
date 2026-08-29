"""I/O boundary: enforce physical read predicate before invoking real adapters.

The boundary requires every read to carry a strictly-before-cutoff predicate
(`< 2024-01-01T00:00:00Z`). It fails before storage invocation for missing,
malformed, omitted-flag, load-before-filter, at-or-after-cutoff, or
uninstrumented-adapter cases. Real adapters are never substituted with an
in-memory row list; boundary proof comes from the predicate and inventory.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CUTOFF = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
CUTOFF_ISO = "2024-01-01T00:00:00Z"


class BoundaryError(Exception):
    """Raised when a read cannot satisfy the physical boundary."""

    def __init__(self, reason: str, code: str, metrics_impact: dict[str, int] | None = None):
        super().__init__(reason)
        self.reason = reason
        self.code = code
        self.metrics_impact = metrics_impact or {}


@dataclass
class IOMetrics:
    """Counters required by the Phase-2 workflow metrics schema."""

    read_invocations: int = 0
    sealed_rows_observed: int = 0
    holdout_access_incidents: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            "read_invocations": self.read_invocations,
            "sealed_rows_observed": self.sealed_rows_observed,
            "holdout_access_incidents": self.holdout_access_incidents,
        }


@dataclass
class AdapterSpec:
    """Description of a real storage adapter and its predicate contract."""

    adapter_id: str
    repo_commit: str
    module: str
    entrypoint: str
    physical_predicate: dict[str, Any]
    available: bool = False
    incomplete_reason: str = ""


class IOBoundary:
    """Wrap real storage adapters with a fail-closed pre-read predicate."""

    def __init__(self, inventory_path: str | Path, metrics: IOMetrics | None = None) -> None:
        self.inventory_path = Path(inventory_path)
        self.metrics = metrics if metrics is not None else IOMetrics()
        self.adapters: dict[str, AdapterSpec] = {}
        self._load_inventory()

    def _load_inventory(self) -> None:
        if not self.inventory_path.exists():
            raise BoundaryError(
                f"Adapter inventory missing: {self.inventory_path}",
                "ADAPTER_INVENTORY_MISSING",
            )
        try:
            with open(self.inventory_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as exc:
            raise BoundaryError(
                f"Malformed adapter inventory: {exc}",
                "ADAPTER_INVENTORY_MALFORMED",
            ) from exc

        for entry in data.get("adapters", []):
            spec = AdapterSpec(
                adapter_id=entry["adapter_id"],
                repo_commit=entry["repo_commit"],
                module=entry["module"],
                entrypoint=entry["entrypoint"],
                physical_predicate=entry["physical_predicate"],
                available=bool(entry.get("available", False)),
                incomplete_reason=entry.get("incomplete_reason", ""),
            )
            self.adapters[spec.adapter_id] = spec

    def _validate_predicate(self, load_before: Any) -> None:
        if load_before is None:
            self._raise(
                "load_before predicate is required",
                "OMITTED_LOAD_BEFORE",
                {"holdout_access_incidents": 1},
            )
        if not isinstance(load_before, str):
            self._raise(
                "load_before predicate must be an ISO-8601 string",
                "MALFORMED_LOAD_BEFORE",
                {"holdout_access_incidents": 1},
            )
        try:
            when = datetime.fromisoformat(load_before.replace("Z", "+00:00"))
        except ValueError:
            self._raise(
                f"load_before not a valid datetime: {load_before}",
                "MALFORMED_LOAD_BEFORE",
                {"holdout_access_incidents": 1},
            )
        if when.tzinfo is None:
            self._raise(
                "load_before must be timezone-aware (UTC)",
                "MALFORMED_LOAD_BEFORE",
                {"holdout_access_incidents": 1},
            )
        if when >= CUTOFF:
            self._raise(
                f"load_before {load_before} is at or after cutoff {CUTOFF_ISO}",
                "AT_OR_AFTER_CUTOFF",
                {"holdout_access_incidents": 1},
            )

    def _bump_metrics(self, impact: dict[str, int]) -> None:
        for key, delta in impact.items():
            current = getattr(self.metrics, key, 0)
            setattr(self.metrics, key, current + delta)

    def _raise(self, reason: str, code: str, impact: dict[str, int] | None = None):
        self._bump_metrics(impact or {})
        raise BoundaryError(reason, code, impact)

    def read(
        self,
        adapter_id: str,
        load_before: str | None,
        load_before_filter: bool = False,
    ) -> Any:
        """Request a read from a real storage adapter.

        Args:
            adapter_id: Identifier of the adapter.
            load_before: Exclusive UTC upper bound for the read.
            load_before_filter: Must be False; post-filtering is not boundary proof.

        Raises:
            BoundaryError: if any boundary check fails before adapter invocation.
        """
        # Require explicit boundary predicate, never a soft filter.
        if load_before_filter:
            self._raise(
                "load_before_filter is not a physical predicate",
                "LOAD_BEFORE_FILTER_NOT_BOUNDARY",
                {"holdout_access_incidents": 1},
            )

        spec = self.adapters.get(adapter_id)
        if spec is None:
            self._raise(
                f"Uninstrumented adapter: {adapter_id}",
                "UNINSTRUMENTED_ADAPTER",
                {"holdout_access_incidents": 1},
            )

        if not spec.available:
            self._raise(
                f"Adapter {adapter_id} unavailable: {spec.incomplete_reason}",
                "ADAPTER_INVENTORY_INCOMPLETE",
            )

        self._validate_predicate(load_before)

        # At this point the read would be delegated to the real adapter.
        # This harness has no real adapters, so reaching here is unexpected.
        self.metrics.read_invocations += 1
        raise BoundaryError(
            f"Real adapter {adapter_id} invoked unexpectedly in harness",
            "REAL_ADAPTER_INVOCATION",
            {"read_invocations": 1},
        )

    def get_metrics(self) -> IOMetrics:
        return self.metrics
