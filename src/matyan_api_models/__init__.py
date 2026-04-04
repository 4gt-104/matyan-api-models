"""Shared Pydantic models and helpers for Matyan HTTP, WebSocket, and Kafka APIs.

This package is consumed by ``matyan-backend``, ``matyan-frontier``, ``matyan-client``,
and workers.  The root namespace re-exports a small convenience surface; subpackages
``kafka``, ``ws``, ``typing``, and ``backup`` hold additional schemas.

Exports:

- ``DEFAULT_PROJECT_ID`` — default 8-hex project scope
- ``RunCreateRequest`` / ``RunCreateResponse`` — run creation over REST
- ``ReadMetricResponse``, ``LogHParamsResponse``, ``LogMetricResponse`` — common response bodies
- ``context_to_id`` — deterministic hash of a metric context dict
"""

from .context import context_to_id
from .responses import LogHParamsResponse, LogMetricResponse, ReadMetricResponse
from .run_creation import RunCreateRequest, RunCreateResponse
from .typing import DEFAULT_PROJECT_ID

__all__ = [
    "DEFAULT_PROJECT_ID",
    "LogHParamsResponse",
    "LogMetricResponse",
    "ReadMetricResponse",
    "RunCreateRequest",
    "RunCreateResponse",
    "context_to_id",
]
