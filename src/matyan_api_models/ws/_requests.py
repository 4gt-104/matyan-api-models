from __future__ import annotations

from datetime import datetime  # noqa: TC003
from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter


class BaseWsRequest(BaseModel):
    type: str
    run_id: str


class CreateRunWsRequest(BaseWsRequest):
    type: Literal["create_run"] = "create_run"
    client_datetime: datetime
    force_resume: bool = False


class LogMetricWsRequest(BaseWsRequest):
    type: Literal["log_metric"] = "log_metric"
    name: str
    value: float
    step: int | None
    epoch: int | None
    context: dict | None
    dtype: str | None
    client_datetime: datetime


class LogHParamsWsRequest(BaseWsRequest):
    type: Literal["log_hparams"] = "log_hparams"
    value: dict


class FinishRunWsRequest(BaseWsRequest):
    type: Literal["finish_run"] = "finish_run"


class SetRunPropertyWsRequest(BaseWsRequest):
    """Set one or more run properties (name, description, archived, experiment)."""

    type: Literal["set_run_property"] = "set_run_property"
    name: str | None = None
    description: str | None = None
    archived: bool | None = None
    experiment: str | None = None


class AddTagWsRequest(BaseWsRequest):
    """Add a tag to a run (by tag name — will be created if it doesn't exist)."""

    type: Literal["add_tag"] = "add_tag"
    tag_name: str


class RemoveTagWsRequest(BaseWsRequest):
    """Remove a tag from a run (by tag name)."""

    type: Literal["remove_tag"] = "remove_tag"
    tag_name: str


class LogCustomObjectWsRequest(BaseWsRequest):
    """Track a custom object (Image, Audio, Text, Distribution, Figure).

    ``value`` carries the serialized metadata dict (and for blob types, the
    ``s3_key`` referencing the already-uploaded binary data).
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
    """A single captured terminal output line (stdout/stderr)."""

    type: Literal["log_terminal_line"] = "log_terminal_line"
    line: str
    step: int


class LogRecordWsRequest(BaseWsRequest):
    """A structured log record (log_info / log_warning / log_error / log_debug)."""

    type: Literal["log_record"] = "log_record"
    message: str
    level: int
    timestamp: float
    logger_info: list | None = None
    extra_args: dict | None = None


class BlobRefWsRequest(BaseWsRequest):
    """Notify that a blob has been uploaded to S3 (sent after successful PUT)."""

    type: Literal["blob_ref"] = "blob_ref"
    s3_key: str
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


WsRequestTAdapter: TypeAdapter[WsRequestT] = TypeAdapter(WsRequestT)  # ty:ignore[invalid-assignment]
