"""On-disk backup manifest and layout contract for client or tooling exports.

A backup directory contains a JSON sidecar named ``MANIFEST_FILE`` plus a ``runs/``
tree.  :class:`BackupManifest` records what was exported and supports round-trip
read/write and filesystem validation.

**Constants**

- ``FORMAT_VERSION`` — integer schema version for the manifest JSON; readers must
  reject unknown versions
- ``MANIFEST_FILE`` — filename of the manifest inside the backup root (``manifest.json``)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

FORMAT_VERSION = 1
MANIFEST_FILE = "manifest.json"


@dataclass
class BackupManifest:
    """Summary metadata for a Matyan run backup archive on local disk.

    :param format_version: Manifest schema version (must match ``FORMAT_VERSION`` for writes)
    :param created_at: ISO 8601 timestamp string; empty string means ``write`` will fill UTC ``now``
    :param run_count: Number of runs represented (informational; should match ``run_hashes`` length)
    :param run_hashes: Run directory names under ``runs/``, each expected to hold JSON snapshots
    :param entity_counts: Optional counts of related entities (experiments, tags, etc.) for UI or audits
    :param blob_count: Number of large blobs referenced or included (informational)
    :param blob_bytes: Total byte size of blobs (informational)
    :param filters: Arbitrary JSON-serializable export filters (experiment name, date range, etc.)
    :param include_blobs: Whether blob payloads were included or only references
    """

    format_version: int = FORMAT_VERSION
    created_at: str = ""
    run_count: int = 0
    run_hashes: list[str] = field(default_factory=list)
    entity_counts: dict[str, int] = field(default_factory=dict)
    blob_count: int = 0
    blob_bytes: int = 0
    filters: dict[str, Any] = field(default_factory=dict)
    include_blobs: bool = True

    def write(self, backup_dir: Path) -> None:
        """Serialize this manifest to ``backup_dir / MANIFEST_FILE``.

        Fills ``created_at`` with the current UTC ISO timestamp when it is empty.

        :param backup_dir: Root directory of the backup (must exist; is not created here)
        """
        data = {
            "format_version": self.format_version,
            "created_at": self.created_at or datetime.now(tz=timezone.utc).isoformat(),
            "run_count": self.run_count,
            "run_hashes": self.run_hashes,
            "entity_counts": self.entity_counts,
            "blob_count": self.blob_count,
            "blob_bytes": self.blob_bytes,
            "filters": self.filters,
            "include_blobs": self.include_blobs,
        }
        (backup_dir / MANIFEST_FILE).write_text(json.dumps(data, indent=2) + "\n")

    @classmethod
    def read(cls, backup_dir: Path) -> BackupManifest:
        """Load a manifest from ``backup_dir / MANIFEST_FILE``.

        :param backup_dir: Root directory of the backup
        :returns: Parsed manifest instance
        :raises FileNotFoundError: If the manifest file is missing
        :raises ValueError: If ``format_version`` does not match ``FORMAT_VERSION``
        """
        path = backup_dir / MANIFEST_FILE
        if not path.exists():
            msg = f"No {MANIFEST_FILE} found in {backup_dir}"
            raise FileNotFoundError(msg)

        data = json.loads(path.read_text())
        version = data.get("format_version", 0)
        if version != FORMAT_VERSION:
            msg = f"Unsupported backup format version {version} (expected {FORMAT_VERSION})"
            raise ValueError(msg)

        return cls(
            format_version=version,
            created_at=data.get("created_at", ""),
            run_count=data.get("run_count", 0),
            run_hashes=data.get("run_hashes", []),
            entity_counts=data.get("entity_counts", {}),
            blob_count=data.get("blob_count", 0),
            blob_bytes=data.get("blob_bytes", 0),
            filters=data.get("filters", {}),
            include_blobs=data.get("include_blobs", True),
        )

    def validate(self, backup_dir: Path) -> list[str]:
        """Check that on-disk layout matches this manifest.

        Verifies ``runs/`` exists, run subdirectory names match ``run_hashes``, and each
        run folder contains ``run.json``, ``attrs.json``, ``traces.json``, and ``contexts.json``.

        :param backup_dir: Root directory of the backup to inspect
        :returns: Human-readable error strings; empty list means the tree matches the manifest
        """
        errors: list[str] = []
        runs_dir = backup_dir / "runs"
        if not runs_dir.is_dir():
            errors.append("Missing 'runs/' directory")
            return errors

        found_hashes = sorted(d.name for d in runs_dir.iterdir() if d.is_dir())
        expected = sorted(self.run_hashes)
        if found_hashes != expected:
            missing = set(expected) - set(found_hashes)
            extra = set(found_hashes) - set(expected)
            if missing:
                errors.append(f"Missing run directories: {missing}")
            if extra:
                errors.append(f"Unexpected run directories: {extra}")

        for rh in found_hashes:
            run_dir = runs_dir / rh
            errors.extend(
                f"Run {rh}: missing {required}"
                for required in ("run.json", "attrs.json", "traces.json", "contexts.json")
                if not (run_dir / required).exists()
            )

        return errors
