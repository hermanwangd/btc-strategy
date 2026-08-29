"""Tests for phase2_harness.final_bytes and phase2_harness.manifest."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

from phase2_harness.final_bytes import FinalByteError, verify_final_bytes
from phase2_harness.manifest import generate_manifest, package_hash, write_manifest


class TestFinalBytes(unittest.TestCase):
    def test_valid_package_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a.txt").write_text("alpha")
            (Path(tmp) / "b.txt").write_text("beta")
            checksum_path = write_manifest(tmp)
            self.assertEqual(checksum_path.name, "SHA256SUMS.txt")
            result = verify_final_bytes(Path(tmp))
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["file_count"], 2)
            expected_hash = package_hash(generate_manifest(tmp))
            self.assertEqual(result["outer_package_hash"], expected_hash)

    def test_checksum_excludes_itself(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a.txt").write_text("alpha")
            write_manifest(tmp)
            manifest_text = (Path(tmp) / "SHA256SUMS.txt").read_text()
            self.assertNotIn("SHA256SUMS.txt", manifest_text)

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            a_path = Path(tmp) / "a.txt"
            a_path.write_text("alpha")
            write_manifest(tmp)
            a_path.unlink()
            with self.assertRaises(FinalByteError) as ctx:
                verify_final_bytes(Path(tmp))
            self.assertIn("Missing files", str(ctx.exception))
            self.assertTrue(ctx.exception.incident)

    def test_unlisted_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a.txt").write_text("alpha")
            write_manifest(tmp)
            (Path(tmp) / "b.txt").write_text("beta")
            with self.assertRaises(FinalByteError) as ctx:
                verify_final_bytes(Path(tmp))
            self.assertIn("Unlisted files", str(ctx.exception))
            self.assertTrue(ctx.exception.incident)

    def test_mutated_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a.txt").write_text("alpha")
            write_manifest(tmp)
            (Path(tmp) / "a.txt").write_text("ALPHA")
            with self.assertRaises(FinalByteError) as ctx:
                verify_final_bytes(Path(tmp))
            self.assertIn("Hash mismatch", str(ctx.exception))
            self.assertTrue(ctx.exception.incident)

    def test_missing_checksum_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a.txt").write_text("alpha")
            with self.assertRaises(FinalByteError) as ctx:
                verify_final_bytes(Path(tmp))
            self.assertIn("Checksum file missing", str(ctx.exception))
            self.assertTrue(ctx.exception.incident)

    def test_malformed_manifest_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "SHA256SUMS.txt").write_text("not-a-valid-line")
            with self.assertRaises(FinalByteError) as ctx:
                verify_final_bytes(Path(tmp))
            self.assertIn("Malformed manifest line", str(ctx.exception))

    def test_duplicate_manifest_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            lines = ["a" * 64 + "  a.txt", "b" * 64 + "  a.txt"]
            (Path(tmp) / "SHA256SUMS.txt").write_text("\n".join(lines))
            with self.assertRaises(FinalByteError) as ctx:
                verify_final_bytes(Path(tmp))
            self.assertIn("Duplicate manifest entry", str(ctx.exception))


class TestManifest(unittest.TestCase):
    def test_generate_manifest_sorted(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "z.txt").write_text("z")
            (Path(tmp) / "a.txt").write_text("a")
            lines = generate_manifest(tmp)
            self.assertEqual(len(lines), 2)
            self.assertEqual(lines, sorted(lines))

    def test_package_hash_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a.txt").write_text("a")
            (Path(tmp) / "b.txt").write_text("b")
            lines = generate_manifest(tmp)
            self.assertEqual(package_hash(lines), package_hash(lines))
            reversed_lines = list(reversed(lines))
            self.assertEqual(package_hash(lines), package_hash(reversed_lines))


if __name__ == "__main__":
    unittest.main()
