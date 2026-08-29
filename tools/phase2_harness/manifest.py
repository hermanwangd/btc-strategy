"""Generate a package manifest with per-file SHA-256 and the self-omission rule."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Iterable

CHECKSUM_FILENAME = "SHA256SUMS.txt"


def sha256_file(path: os.PathLike) -> str:
    """Compute the SHA-256 hex digest of a file's bytes."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_path(path: Path, root: Path) -> str:
    """Return a POSIX-style relative path from root."""
    return path.relative_to(root).as_posix()


def is_excluded(rel_path: str, checksum_filename: str = CHECKSUM_FILENAME) -> bool:
    """Return True for paths that must never appear in a reproducible manifest."""
    if rel_path == checksum_filename or rel_path == ".git" or rel_path.startswith(".git/"):
        return True
    if "__pycache__/" in rel_path or rel_path.endswith(".pyc") or rel_path.endswith(".pyo"):
        return True
    if rel_path.startswith(".worktrees/"):
        return True
    return False


def generate_manifest(
    package_root: os.PathLike,
    extra_excludes: Iterable[str] | None = None,
) -> list[str]:
    """Generate sorted manifest lines in `sha256sum` format.

    The checksum file itself is always excluded from the manifest so that
    the manifest can be written to disk without changing its own hash.

    Args:
        package_root: Root directory to scan.
        extra_excludes: Additional path strings (relative POSIX) to skip.

    Returns:
        Sorted list of manifest lines `<sha256>  <relative/path>`.
    """
    root = Path(package_root).resolve()
    excludes = {CHECKSUM_FILENAME}
    if extra_excludes:
        excludes.update(extra_excludes)

    lines: list[str] = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            file_path = Path(dirpath) / filename
            rel = normalize_path(file_path, root)
            if rel in excludes or is_excluded(rel, CHECKSUM_FILENAME):
                continue
            digest = sha256_file(file_path)
            lines.append(f"{digest}  {rel}")

    lines.sort()
    return lines


def write_manifest(
    package_root: os.PathLike,
    lines: Iterable[str] | None = None,
    checksum_filename: str = CHECKSUM_FILENAME,
) -> Path:
    """Write the manifest to disk, excluding itself from its own content."""
    root = Path(package_root).resolve()
    if lines is None:
        lines = generate_manifest(root)
    checksum_path = root / checksum_filename
    with open(checksum_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
        if lines:
            f.write("\n")
    return checksum_path


def package_hash(manifest_lines: Iterable[str]) -> str:
    """Compute the canonical outer package hash from sorted manifest lines."""
    canonical = "\n".join(sorted(manifest_lines)).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()
