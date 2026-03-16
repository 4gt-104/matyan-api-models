from __future__ import annotations

import re
import uuid

from pydantic import BaseModel, Field, field_validator


class RunCreateRequest(BaseModel):
    id: str
    project: str = Field(min_length=1)
    experiment: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
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


class RunCreateResponse(BaseModel):
    creation_timestamp: int
