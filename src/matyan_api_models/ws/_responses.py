from __future__ import annotations

from pydantic import BaseModel


class WsResponse(BaseModel):
    status: str
    error: str | None = None
