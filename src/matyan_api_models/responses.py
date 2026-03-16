from pydantic import BaseModel


class ReadMetricResponse(BaseModel):
    value: float
    timestamp: int


class ReadHParamsResponse(BaseModel):
    value: dict


class LogHParamsResponse(BaseModel):
    status: int


class LogMetricResponse(BaseModel):
    status: int
