"""Backup manifest: metadata about a backup archive."""

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
        """Return a list of validation errors (empty if valid)."""
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
