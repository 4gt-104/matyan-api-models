"""Concrete Pydantic envelopes for Matyan Kafka topics.

Defines :class:`IngestionMessage` and :class:`ControlEvent` with shared header fields
and a JSON-serializable ``payload`` dict per message kind.
"""

from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import BaseModel

from matyan_api_models.typing import ProjectId, RunId  # noqa: TC001


class IngestionMessage(BaseModel):
    """Envelope for all messages on the ``data-ingestion`` Kafka topic.

    Both frontier (producer) and ingestion workers (consumer) depend on this
    schema.  The ``type`` field discriminates the payload shape.

    :param type: Message type (e.g. ``"create_run"``, ``"log_metric"``).
    :param run_id: The run this message belongs to.
    :param project_id: The project this message belongs to; scopes all FDB
        writes to the correct project key space.
    :param timestamp: When the message was created.
    :param payload: Type-specific data dict.
    """

    type: str
    run_id: RunId
    project_id: ProjectId
    timestamp: datetime
    payload: dict


class ControlEvent(BaseModel):
    """Envelope for all messages on the ``control-events`` Kafka topic.

    Published by the backend API after synchronous FDB writes.
    Consumed by control workers for async side effects (S3 cleanup, etc.).

    Valid ``type`` values: ``"run_deleted"``, ``"run_archived"``,
    ``"run_unarchived"``, ``"experiment_deleted"``, ``"tag_deleted"``,
    ``"project_deleted"``.
    """

    type: str
    timestamp: datetime
    payload: dict
