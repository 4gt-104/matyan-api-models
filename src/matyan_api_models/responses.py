"""Small Pydantic response bodies for metric and hyperparameter logging endpoints.

These shapes mirror Aim-compatible REST responses where the server returns either
a logged value (read-back) or a simple numeric status code for write operations.
"""

from pydantic import BaseModel


class ReadMetricResponse(BaseModel):
    """Single scalar metric point returned from a read-style metric endpoint.

    :param value: Metric value at the requested step or index
    :param timestamp: Associated wall-clock or event timestamp from storage
    """

    value: float
    timestamp: int


class ReadHParamsResponse(BaseModel):
    """Hyperparameters dict returned from a read-style hparams endpoint.

    :param value: Full hyperparameters mapping as stored for the run
    """

    value: dict


class LogHParamsResponse(BaseModel):
    """Acknowledgement after logging hyperparameters.

    :param status: HTTP-style or API-specific status code (0 or 200 typically means success)
    """

    status: int


class LogMetricResponse(BaseModel):
    """Acknowledgement after logging a metric point.

    :param status: HTTP-style or API-specific status code (0 or 200 typically means success)
    """

    status: int
