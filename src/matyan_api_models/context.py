"""Deterministic mapping from context dicts to integer IDs.

Used by both the backend storage layer and the client backup module
to produce stable, reproducible context identifiers.
"""

from __future__ import annotations

import hashlib
import json


def context_to_id(context: dict | None) -> int:
    """Hash a context dict into a stable 32-bit integer ID.

    An empty or ``None`` context always maps to ``0``.

    :param context: Context dictionary (e.g. ``{"subset": "train"}``).
    :returns: Deterministic integer derived from the canonical JSON representation.
    """
    if not context:
        return 0
    canonical = json.dumps(context, sort_keys=True, separators=(",", ":"))
    return int(hashlib.sha256(canonical.encode()).hexdigest()[:8], 16)
