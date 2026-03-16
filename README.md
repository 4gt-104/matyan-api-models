# Matyan API Models

Shared Pydantic models for the Matyan stack. Used by **matyan-frontier** (WebSocket + Kafka producer), **matyan-backend** (Kafka consumers, API), and **matyan-client** (WebSocket and REST client). Part of the Matyan experiment-tracking stack (fork of Aim).

## Layout

- **`src/matyan_api_models/`** — Python package. No CLI or server; import as a library.
- **`ws/`** — WebSocket request and response models: `CreateRunWsRequest`, `LogMetricWsRequest`, `LogHParamsWsRequest`, `FinishRunWsRequest`, `SetRunPropertyWsRequest`, `AddTagWsRequest`, `RemoveTagWsRequest`, `LogCustomObjectWsRequest`, `LogTerminalLineWsRequest`, `LogRecordWsRequest`, `BlobRefWsRequest`, `WsRequestTAdapter`, `WsResponse`.
- **`kafka/`** — Kafka message models: `IngestionMessage` (envelope for the data-ingestion topic), `ControlEvent` (for the control-events topic).
- **Root** — `RunCreateRequest`, `RunCreateResponse`; `LogHParamsResponse`, `LogMetricResponse`, `ReadMetricResponse`.

Source of truth for the wire format between frontier, backend, and client.

## Prerequisites

- Python 3.10+. Single dependency: `pydantic~=2.0`. The monorepo uses `uv`; from the package dir: `uv sync` then import `matyan_api_models`.

## Usage

Install as a dependency (editable in the monorepo):

```bash
# From repo root or extra/matyan-api-models
uv sync
```

Then in Python:

```python
from matyan_api_models.ws import CreateRunWsRequest, WsResponse
from matyan_api_models.kafka import IngestionMessage
from matyan_api_models import RunCreateRequest, RunCreateResponse
```

Frontier validates WebSocket payloads with `WsRequestTAdapter` and publishes `IngestionMessage` to Kafka; backend workers consume `IngestionMessage` and `ControlEvent`; the client builds WS requests from these models.

## Related

- **Frontier**: Accepts WebSocket messages and REST run-creation; produces `IngestionMessage` to Kafka.
- **Backend**: Consumes `IngestionMessage` and `ControlEvent`; uses run-creation and response models for REST.
- **Client**: Builds WebSocket requests and run-creation requests from these models.
- **Monorepo**: This package lives under `extra/matyan-api-models` in the matyan-core repo.
