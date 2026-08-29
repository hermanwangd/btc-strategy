"""Final-byte gate: verify every shipped final byte against a manifest.

The gate rejects:
  - missing listed files;
  - unlisted files on disk;
  - cached/stale declared hashes;
  - mutated files whose current bytes do not match the manifest hash.

The outer package hash is computed from the manifest lines but is recorded
only inside a terminal result envelope, never persisted as a side file.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from phase2_harness.manifest import CHECKSUM_FILENAME, package_hash, sha256_file


class FinalByteError(Exception):
    """Raised when the package fails the final-byte gate."""

    def __init__(self, reason: str, incident: bool = False) -> None:
        super().__init__(reason)
        self.reason = reason
        self.incident = incident


def parse_manifest(text: str) -> dict[str, str]:
    """Parse standard `sha256sum` manifest text into {relative_path: sha256}."""
    entries: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        # Standard sha256sum format: "<hash>  <path>" (two spaces)
        parts = line.split("  ", 1)
        if len(parts) != 2:
            raise FinalByteError(f"Malformed manifest line: {raw_line!r}")
        digest, rel_path = parts
        if len(digest) != 64:
            raise FinalByteError(f"Invalid digest length on line: {raw_line!r}")
        if rel_path in entries:
            raise FinalByteError(f"Duplicate manifest entry: {rel_path}")
        entries[rel_path] = digest
    return entries


def verify_final_bytes(
    package_root: Path,
    manifest_lines: Iterable[str] | None = None,
    checksum_filename: str = CHECKSUM_FILENAME,
) -> dict[str, str | int]:
    """Verify every shipped final byte and return an evidence record.

    Args:
        package_root: Directory to inspect.
        manifest_lines: Expected manifest lines. If None, read the checksum file.
        checksum_filename: Name of the checksum file.

    Returns:
        Evidence dict with outer_package_hash, file_count, and status.

    Raises:
        FinalByteError: on any integrity violation.
    """
    root = Path(package_root).resolve()
    if manifest_lines is None:
        checksum_path = root / checksum_filename
        if not checksum_path.exists():
            raise FinalByteError(f"Checksum file missing: {checksum_path}", incident=True)
        with open(checksum_path, "r", encoding="utf-8") as f:
            manifest_lines = f.read().splitlines()

    expected = parse_manifest("\n".join(manifest_lines))

    # Discover every non-excluded file on disk under the root.
    excluded = {checksum_filename}
    observed_files = set()
    for path in root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            if rel in excluded or rel.startswith(".git/"):
                continue
            observed_files.add(rel)

    # Check for missing files
    missing = set(expected.keys()) - observed_files
    if missing:
        raise FinalByteError(
            f"Missing files listed in manifest: {sorted(missing)}", incident=True
        )

    # Check for unlisted files
    unlisted = observed_files - set(expected.keys())
    if unlisted:
        raise FinalByteError(
            f"Unlisted files present: {sorted(unlisted)}", incident=True
        )

    # Verify each listed file's hash
    for rel_path, expected_hash in expected.items():
        current = sha256_file(root / rel_path)
        if current != expected_hash:
            raise FinalByteError(
                f"Hash mismatch for {rel_path}: expected={expected_hash} current={current}",
                incident=True,
            )

    outer = package_hash(manifest_lines)
    return {
        "status": "PASS",
        "outer_package_hash": outer,
        "file_count": len(expected),
    }
