from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import BaseModel


class IngestionMessage(BaseModel):
    """Envelope for all messages on the ``data-ingestion`` Kafka topic.

    Both frontier (producer) and ingestion workers (consumer) depend on this
    schema.  The ``type`` field discriminates the payload shape.
    """

    type: str
    run_id: str
    timestamp: datetime
    payload: dict


class ControlEvent(BaseModel):
    """Envelope for all messages on the ``control-events`` Kafka topic.

    Published by the backend API after synchronous FDB writes.
    Consumed by control workers for async side effects (S3 cleanup, etc.).
    """

    type: str
    timestamp: datetime
    payload: dict
