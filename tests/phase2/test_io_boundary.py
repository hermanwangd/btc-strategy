"""Tests for phase2_harness.io_boundary."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

from phase2_harness.io_boundary import BoundaryError, IOBoundary, IOMetrics


class TestIOBoundary(unittest.TestCase):
    def _inventory(self, adapter_id: str, available: bool):
        return {
            "inventory_id": "test-inventory",
            "cutoff": "2024-01-01T00:00:00Z",
            "adapters": [
                {
                    "adapter_id": adapter_id,
                    "repo_commit": "deadbeef" * 5,
                    "module": "test.module",
                    "entrypoint": "load",
                    "physical_predicate": {
                        "field": "load_before",
                        "operator": "<",
                        "cutoff": "2024-01-01T00:00:00Z",
                    },
                    "available": available,
                    "incomplete_reason": "Unavailable for testing." if not available else "",
                }
            ],
        }

    def _write_inventory(self, data):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return path

    def test_missing_inventory(self):
        with self.assertRaises(BoundaryError) as ctx:
            IOBoundary("/does/not/exist.json")
        self.assertEqual(ctx.exception.code, "ADAPTER_INVENTORY_MISSING")

    def test_malformed_inventory(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write("not json")
        try:
            with self.assertRaises(BoundaryError) as ctx:
                IOBoundary(path)
            self.assertEqual(ctx.exception.code, "ADAPTER_INVENTORY_MALFORMED")
        finally:
            os.unlink(path)

    def test_unavailable_adapter_reports_incomplete(self):
        path = self._write_inventory(self._inventory("btc_ohlc_daily", False))
        try:
            boundary = IOBoundary(path)
            with self.assertRaises(BoundaryError) as ctx:
                boundary.read("btc_ohlc_daily", "2017-12-31T23:59:59Z")
            self.assertEqual(ctx.exception.code, "ADAPTER_INVENTORY_INCOMPLETE")
            self.assertEqual(boundary.get_metrics().read_invocations, 0)
            self.assertEqual(boundary.get_metrics().sealed_rows_observed, 0)
            self.assertEqual(boundary.get_metrics().holdout_access_incidents, 0)
        finally:
            os.unlink(path)

    def test_uninstrumented_adapter(self):
        path = self._write_inventory(self._inventory("btc_ohlc_daily", False))
        try:
            boundary = IOBoundary(path)
            with self.assertRaises(BoundaryError) as ctx:
                boundary.read("unknown_adapter", "2017-12-31T23:59:59Z")
            self.assertEqual(ctx.exception.code, "UNINSTRUMENTED_ADAPTER")
            self.assertEqual(boundary.get_metrics().read_invocations, 0)
            self.assertEqual(boundary.get_metrics().sealed_rows_observed, 0)
            self.assertEqual(boundary.get_metrics().holdout_access_incidents, 1)
        finally:
            os.unlink(path)

    def test_omitted_load_before(self):
        path = self._write_inventory(self._inventory("btc_ohlc_daily", True))
        try:
            boundary = IOBoundary(path)
            with self.assertRaises(BoundaryError) as ctx:
                boundary.read("btc_ohlc_daily", None)
            self.assertEqual(ctx.exception.code, "OMITTED_LOAD_BEFORE")
            self.assertEqual(boundary.get_metrics().read_invocations, 0)
            self.assertEqual(boundary.get_metrics().sealed_rows_observed, 0)
            self.assertEqual(boundary.get_metrics().holdout_access_incidents, 1)
        finally:
            os.unlink(path)

    def test_malformed_load_before(self):
        path = self._write_inventory(self._inventory("btc_ohlc_daily", True))
        try:
            boundary = IOBoundary(path)
            with self.assertRaises(BoundaryError) as ctx:
                boundary.read("btc_ohlc_daily", "not-a-date")
            self.assertEqual(ctx.exception.code, "MALFORMED_LOAD_BEFORE")
            self.assertEqual(boundary.get_metrics().read_invocations, 0)
            self.assertEqual(boundary.get_metrics().sealed_rows_observed, 0)
            self.assertEqual(boundary.get_metrics().holdout_access_incidents, 1)
        finally:
            os.unlink(path)

    def test_naive_datetime_rejected(self):
        path = self._write_inventory(self._inventory("btc_ohlc_daily", True))
        try:
            boundary = IOBoundary(path)
            with self.assertRaises(BoundaryError) as ctx:
                boundary.read("btc_ohlc_daily", "2017-12-31T23:59:59")
            self.assertEqual(ctx.exception.code, "MALFORMED_LOAD_BEFORE")
            self.assertEqual(boundary.get_metrics().holdout_access_incidents, 1)
        finally:
            os.unlink(path)

    def test_at_cutoff_fails(self):
        path = self._write_inventory(self._inventory("btc_ohlc_daily", True))
        try:
            boundary = IOBoundary(path)
            with self.assertRaises(BoundaryError) as ctx:
                boundary.read("btc_ohlc_daily", "2024-01-01T00:00:00Z")
            self.assertEqual(ctx.exception.code, "AT_OR_AFTER_CUTOFF")
            self.assertEqual(boundary.get_metrics().read_invocations, 0)
            self.assertEqual(boundary.get_metrics().sealed_rows_observed, 0)
            self.assertEqual(boundary.get_metrics().holdout_access_incidents, 1)
        finally:
            os.unlink(path)

    def test_after_cutoff_fails(self):
        path = self._write_inventory(self._inventory("btc_ohlc_daily", True))
        try:
            boundary = IOBoundary(path)
            with self.assertRaises(BoundaryError) as ctx:
                boundary.read("btc_ohlc_daily", "2025-01-01T00:00:00Z")
            self.assertEqual(ctx.exception.code, "AT_OR_AFTER_CUTOFF")
            self.assertEqual(boundary.get_metrics().read_invocations, 0)
            self.assertEqual(boundary.get_metrics().sealed_rows_observed, 0)
            self.assertEqual(boundary.get_metrics().holdout_access_incidents, 1)
        finally:
            os.unlink(path)

    def test_load_before_filter_not_boundary(self):
        path = self._write_inventory(self._inventory("btc_ohlc_daily", True))
        try:
            boundary = IOBoundary(path)
            with self.assertRaises(BoundaryError) as ctx:
                boundary.read(
                    "btc_ohlc_daily",
                    "2017-12-31T23:59:59Z",
                    load_before_filter=True,
                )
            self.assertEqual(ctx.exception.code, "LOAD_BEFORE_FILTER_NOT_BOUNDARY")
            self.assertEqual(boundary.get_metrics().read_invocations, 0)
            self.assertEqual(boundary.get_metrics().sealed_rows_observed, 0)
            self.assertEqual(boundary.get_metrics().holdout_access_incidents, 1)
        finally:
            os.unlink(path)

    def test_safe_read_before_cutoff_invocation_blocked(self):
        # Even with a valid predicate, real adapter invocation is blocked in harness.
        path = self._write_inventory(self._inventory("btc_ohlc_daily", True))
        try:
            boundary = IOBoundary(path)
            with self.assertRaises(BoundaryError) as ctx:
                boundary.read("btc_ohlc_daily", "2017-12-31T23:59:59Z")
            self.assertEqual(ctx.exception.code, "REAL_ADAPTER_INVOCATION")
            self.assertEqual(boundary.get_metrics().read_invocations, 1)
            self.assertEqual(boundary.get_metrics().sealed_rows_observed, 0)
            self.assertEqual(boundary.get_metrics().holdout_access_incidents, 0)
        finally:
            os.unlink(path)

    def test_fixture_inventory_reports_incomplete(self):
        inventory_path = Path(__file__).resolve().parents[2] / "fixtures" / "phase2" / "adapter-inventory.json"
        boundary = IOBoundary(inventory_path)
        with self.assertRaises(BoundaryError) as ctx:
            boundary.read("btc_ohlc_daily", "2017-12-31T23:59:59Z")
        self.assertEqual(ctx.exception.code, "ADAPTER_INVENTORY_INCOMPLETE")
        metrics = boundary.get_metrics()
        self.assertEqual(metrics.read_invocations, 0)
        self.assertEqual(metrics.sealed_rows_observed, 0)
        self.assertEqual(metrics.holdout_access_incidents, 0)


if __name__ == "__main__":
    unittest.main()
