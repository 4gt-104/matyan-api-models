"""Canonical run and project identifiers plus lightweight semantic type aliases.

**Constants**

- ``DEFAULT_PROJECT_ID`` — eight zero digits ``"00000000"``, the default multi-tenant
  scope when no explicit project ID is supplied

**Pydantic-integrated types**

- ``RunId`` — ``str`` validated as a 26-character Crockford Base32 ULID (uppercase
  after normalization).  Used in WebSocket requests, Kafka envelopes, and REST models.
  See :func:`normalize_run_id` for non-Pydantic call sites.

- ``ProjectId`` — ``str`` validated as exactly eight lowercase hexadecimal characters.
  The default project uses ``DEFAULT_PROJECT_ID``.  See :func:`normalize_project_id`.

**Plain aliases** (documentation-only hints for static typing and readers)

- ``RunIdT``, ``RunNameT``, ``ProjectNameT``, ``ExperimentNameT``, ``DescriptionT`` —
  string roles for run and experiment metadata
- ``MetricNameT`` — metric or sequence name string (not exported from the package
  ``__init__`` but available from this submodule if needed)
- ``StepT``, ``EpochT`` — integer step and epoch indices
- ``ContextT`` — context dict passed with metric and object logs
- ``DtypeT``, ``MetricT`` — dtype / metric name strings in traces
- ``HParams`` — mapping type for hyperparameter blobs (``dict[str, Any]``)

Use :func:`normalize_run_id` and :func:`normalize_project_id` when validating outside
Pydantic (CLI, storage layer, workers).
"""

from __future__ import annotations

import re
from typing import Annotated, Any

from pydantic import BeforeValidator

_ULID_RE = re.compile(r"^[0-9A-HJKMNP-TV-Z]{26}$")
_PROJECT_ID_RE = re.compile(r"^[0-9a-f]{8}$")
DEFAULT_PROJECT_ID = "00000000"


def normalize_run_id(value: str) -> str:
    """Normalize and validate a run ID as canonical ULID text.

    :param value: Candidate run identifier.
    :returns: Canonical uppercase ULID text.
    :raises ValueError: If value is not a valid ULID.
    """
    normalized = value.strip().upper()
    if not _ULID_RE.fullmatch(normalized):
        msg = "Run ID must be a valid ULID (26 chars Crockford Base32)"
        raise ValueError(msg)
    return normalized


def _validate_run_id(value: str | None) -> str:
    """Reject None and delegate to :func:`normalize_run_id` for Pydantic ``RunId``."""
    if value is None:
        msg = "Run ID is required"
        raise ValueError(msg)
    return normalize_run_id(value)


def normalize_project_id(value: str) -> str:
    """Normalize and validate a project ID.

    Accepted values are ``00000000`` and lowercase 8-char hex IDs.

    :param value: Candidate project identifier.
    :returns: Canonical project ID.
    :raises ValueError: If value does not match project ID format.
    """
    normalized = value.strip()
    if not _PROJECT_ID_RE.fullmatch(normalized):
        msg = "Project ID must be 8 lowercase hex characters"
        raise ValueError(msg)
    return normalized


def _validate_project_id(value: str | None) -> str:
    """Reject None and delegate to :func:`normalize_project_id` for Pydantic ``ProjectId``."""
    if value is None:
        msg = "Project ID is required"
        raise ValueError(msg)
    return normalize_project_id(value)


RunId = Annotated[str, BeforeValidator(_validate_run_id)]
ProjectId = Annotated[str, BeforeValidator(_validate_project_id)]
RunIdT = str
RunNameT = str
ProjectNameT = str
ExperimentNameT = str
DescriptionT = str

MetricNameT = str
StepT = int
EpochT = int
ContextT = dict
DtypeT = str
MetricT = str
HParams = dict[str, Any]
