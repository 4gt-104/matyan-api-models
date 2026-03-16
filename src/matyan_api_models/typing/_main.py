from __future__ import annotations

import re
import uuid
from typing import Annotated, Any

from pydantic import BeforeValidator


def _validate_run_id(value: str | None) -> str:
    if value is None:
        return uuid.uuid4().hex

    # Ensure it contains only valid hexadecimal characters
    if not re.fullmatch(r"[0-9a-f]{32}", value):
        msg = "UUID must be a 32-character hexadecimal lowercase string"
        raise ValueError(msg)

    try:
        _ = uuid.UUID(hex=value)
    except ValueError as e:
        msg = "Not a valid UUID hex format"
        raise ValueError(msg) from e

    return value


RunId = Annotated[str, BeforeValidator(_validate_run_id)]
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
