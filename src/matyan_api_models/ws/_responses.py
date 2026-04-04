"""WebSocket acknowledgement payloads returned by the frontier after each request.

The frontier validates the inbound message, publishes to Kafka, and replies with
:class:`WsResponse` so the client can detect failures without waiting for the worker.
"""

from __future__ import annotations

from pydantic import BaseModel


class WsResponse(BaseModel):
    """Frontier JSON response for a processed WebSocket message (or batch item).

    On success ``status`` is typically ``"ok"`` and ``error`` is ``None``.
    On validation or publish failure ``status`` indicates failure and ``error``
    carries a short diagnostic string.

    :param status: Outcome label (e.g. ``"ok"`` or ``"error"`` — exact values
        match frontier implementation)
    :param error: Human-readable error message when ``status`` is not success;
        ``None`` when the operation succeeded
    """

    status: str
    error: str | None = None
