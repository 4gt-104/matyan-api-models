"""Kafka message envelopes shared by frontier producers and backend workers.

Exports ``IngestionMessage`` for the high-volume ``data-ingestion`` topic and
``ControlEvent`` for the ``control-events`` topic (deletes, archive toggles, and
related side effects).
"""

from ._messages import ControlEvent, IngestionMessage

__all__ = ["ControlEvent", "IngestionMessage"]
