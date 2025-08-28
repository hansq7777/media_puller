"""Utilities for removing duplicate files."""
from __future__ import annotations

import hashlib
import logging
import os
from typing import Dict, List

logger = logging.getLogger(__name__)

_HASH_CHUNK_SIZE = 1024 * 1024  # 1MB


def _hash_file(path: str, chunk_size: int = _HASH_CHUNK_SIZE) -> str:
    """Compute the SHA256 hash for a file.

    Parameters
    ----------
    path: str
        File path to hash.
    chunk_size: int, optional
        Number of bytes to read per iteration. Defaults to ``_HASH_CHUNK_SIZE``.

    Returns
    -------
    str
        Hexadecimal SHA256 digest of the file.

    Raises
    ------
    OSError
        If the file cannot be read.
    """
    sha256 = hashlib.sha256()
    with open(path, "rb") as file:
        while chunk := file.read(chunk_size):
            sha256.update(chunk)
    return sha256.hexdigest()


def remove_duplicates(directory: str) -> List[str]:
    """Remove duplicate files within a directory based on content hash.

    Parameters
    ----------
    directory: str
        Root directory to scan recursively for duplicate files.

    Returns
    -------
    List[str]
        List of file paths that were removed due to duplication.

    Raises
    ------
    ValueError
        If ``directory`` is not a valid directory.
    OSError
        Propagated if deletion of a duplicate file fails.

    Side Effects
    ------------
    Files may be deleted from the filesystem. Log entries are emitted for
    duplicate detections and removals.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"{directory!r} is not a valid directory")

    seen_hashes: Dict[str, str] = {}
    removed: List[str] = []

    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            try:
                file_hash = _hash_file(path)
            except OSError as exc:
                logger.warning("Skipping unreadable file %s: %s", path, exc)
                continue

            if file_hash in seen_hashes:
                try:
                    os.remove(path)
                    removed.append(path)
                    logger.info(
                        "Removed duplicate file %s (matches %s)",
                        path,
                        seen_hashes[file_hash],
                    )
                except OSError as exc:
                    logger.error("Failed to remove duplicate %s: %s", path, exc)
                    raise
            else:
                seen_hashes[file_hash] = path

    return removed
