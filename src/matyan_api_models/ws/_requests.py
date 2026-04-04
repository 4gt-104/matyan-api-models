"""JSON request bodies accepted by the frontier WebSocket run channel.

Training clients send these models to ``/api/v1/ws/runs/{run_id}`` (single object
or JSON array batch).  Each payload includes a string ``type`` literal; Pydantic
discriminates the concrete model from that field.

**Union and adapter**

- ``WsRequestT`` — annotated union of all request models with ``Field(discriminator="type")``
- ``WsRequestTAdapter`` — shared :class:`pydantic.TypeAdapter` for parsing and validating
  incoming JSON (dict or list of dicts) to ``WsRequestT``
"""

from __future__ import annotations

from datetime import datetime  # noqa: TC003
from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter

from matyan_api_models.typing import RunId  # noqa: TC001


class BaseWsRequest(BaseModel):
    """Common fields for every frontier WebSocket request.

    Concrete subclasses fix ``type`` to a literal and add payload fields.

    :param type: Discriminator string matching the message kind
    :param run_id: Run identifier (ULID) this message applies to
    """

    type: str
    run_id: RunId


class CreateRunWsRequest(BaseWsRequest):
    """Signal that a run session is starting on the frontier connection.

    :param type: Always ``"create_run"``
    :param run_id: Target run ULID
    :param client_datetime: Client wall time when the run was opened
    :param force_resume: If True, treat as resuming an existing run when supported
    """

    type: Literal["create_run"] = "create_run"
    client_datetime: datetime
    force_resume: bool = False


class LogMetricWsRequest(BaseWsRequest):
    """Log one scalar (or typed) metric step for a sequence.

    :param type: Always ``"log_metric"``
    :param run_id: Target run ULID
    :param name: Metric / sequence name
    :param value: Numeric value at this step
    :param step: Training step index, or None when using client-side auto-step
    :param epoch: Optional epoch index
    :param context: Optional context dict distinguishing traces (subset, etc.)
    :param dtype: Optional storage dtype hint (e.g. float tensor class name)
    :param client_datetime: Client time for this sample
    """

    type: Literal["log_metric"] = "log_metric"
    name: str
    value: float
    step: int | None
    epoch: int | None
    context: dict | None
    dtype: str | None
    client_datetime: datetime


class LogHParamsWsRequest(BaseWsRequest):
    """Replace or merge hyperparameters for the run (frontier → Kafka → worker).

    :param type: Always ``"log_hparams"``
    :param run_id: Target run ULID
    :param value: Hyperparameters mapping to persist
    """

    type: Literal["log_hparams"] = "log_hparams"
    value: dict


class FinishRunWsRequest(BaseWsRequest):
    """Mark the run as finished (inactive) after training completes.

    :param type: Always ``"finish_run"``
    :param run_id: Target run ULID
    """

    type: Literal["finish_run"] = "finish_run"


class SetRunPropertyWsRequest(BaseWsRequest):
    """Set one or more mutable run metadata fields (name, description, archived, experiment).

    Only fields that are not ``None`` are applied.

    :param type: Always ``"set_run_property"``
    :param run_id: Target run ULID
    :param name: New run display name, or None to leave unchanged
    :param description: New description, or None to leave unchanged
    :param archived: Archive flag, or None to leave unchanged
    :param experiment: Experiment name, or None to leave unchanged
    """

    type: Literal["set_run_property"] = "set_run_property"
    name: str | None = None
    description: str | None = None
    archived: bool | None = None
    experiment: str | None = None


class AddTagWsRequest(BaseWsRequest):
    """Attach a tag to the run by name (backend creates the tag if missing).

    :param type: Always ``"add_tag"``
    :param run_id: Target run ULID
    :param tag_name: Tag label to add
    """

    type: Literal["add_tag"] = "add_tag"
    tag_name: str


class RemoveTagWsRequest(BaseWsRequest):
    """Detach a tag from the run by name.

    :param type: Always ``"remove_tag"``
    :param run_id: Target run ULID
    :param tag_name: Tag label to remove
    """

    type: Literal["remove_tag"] = "remove_tag"
    tag_name: str


class LogCustomObjectWsRequest(BaseWsRequest):
    """Log a custom object (Image, Audio, Text, Distribution, Figure).

    ``value`` holds serialized object metadata; blob-backed types include a
    ``blob_key`` for data already uploaded via presigned URL.

    :param type: Always ``"log_custom_object"``
    :param run_id: Target run ULID
    :param name: Object / sequence name
    :param value: Serialized object dict (including ``blob_key`` when applicable)
    :param step: Optional step index
    :param epoch: Optional epoch index
    :param context: Optional context dict for the trace
    :param dtype: Object category discriminator (default ``"custom"``)
    :param client_datetime: Optional client timestamp for the sample
    """

    type: Literal["log_custom_object"] = "log_custom_object"
    name: str
    value: dict
    step: int | None = None
    epoch: int | None = None
    context: dict | None = None
    dtype: str = "custom"
    client_datetime: datetime | None = None


class LogTerminalLineWsRequest(BaseWsRequest):
    """Append one raw terminal line (stdout/stderr) to the run log stream.

    :param type: Always ``"log_terminal_line"``
    :param run_id: Target run ULID
    :param line: Single line of text (no trailing newline required)
    :param step: Step index associated with this line for ordering
    """

    type: Literal["log_terminal_line"] = "log_terminal_line"
    line: str
    step: int


class LogRecordWsRequest(BaseWsRequest):
    """Structured log record from the client logging API (info/warning/error/debug).

    :param type: Always ``"log_record"``
    :param run_id: Target run ULID
    :param message: Log message text
    :param level: Numeric level (mapping matches Python ``logging`` constants)
    :param timestamp: Event time as Unix timestamp (seconds, fractional allowed)
    :param logger_info: Optional logger name / path tuple as list
    :param extra_args: Optional structured extras dict
    """

    type: Literal["log_record"] = "log_record"
    message: str
    level: int
    timestamp: float
    logger_info: list | None = None
    extra_args: dict | None = None


class BlobRefWsRequest(BaseWsRequest):
    """Register an artifact blob after the client uploaded bytes to S3.

    Sent only after a successful PUT to the presigned URL.

    :param type: Always ``"blob_ref"``
    :param run_id: Target run ULID
    :param blob_key: Object key in the blob store
    :param artifact_path: Logical path / name inside the run (for UI and storage)
    :param content_type: MIME type of the uploaded object
    """

    type: Literal["blob_ref"] = "blob_ref"
    blob_key: str
    artifact_path: str
    content_type: str = "application/octet-stream"


WsRequestT = Annotated[
    CreateRunWsRequest
    | LogMetricWsRequest
    | LogHParamsWsRequest
    | FinishRunWsRequest
    | SetRunPropertyWsRequest
    | AddTagWsRequest
    | RemoveTagWsRequest
    | LogCustomObjectWsRequest
    | LogTerminalLineWsRequest
    | LogRecordWsRequest
    | BlobRefWsRequest,
    Field(discriminator="type"),
]


WsRequestTAdapter: TypeAdapter[WsRequestT] = TypeAdapter(WsRequestT)
