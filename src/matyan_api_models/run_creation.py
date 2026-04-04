"""Request and response models for creating a run via the backend REST API.

Used when the client or UI creates a run record before connecting to the frontier
for ingestion.  Run identifiers must satisfy :class:`matyan_api_models.typing.RunId`
(ULID) validation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from matyan_api_models.typing import RunId


class RunCreateRequest(BaseModel):
    """Payload for ``POST`` (or equivalent) run creation on the backend.

    :param id: New run identifier as canonical ULID text
    :param project: Project name (non-empty)
    :param experiment: Experiment name to associate with the run (non-empty)
    :param name: Human-readable run name (non-empty)
    :param description: Free-text run description
    """

    id: RunId
    project: str = Field(min_length=1)
    experiment: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str


class RunCreateResponse(BaseModel):
    """Successful run creation acknowledgement from the backend.

    :param creation_timestamp: Server-assigned creation time as an integer timestamp
        (epoch; unit matches the backend API contract)
    """

    creation_timestamp: int
