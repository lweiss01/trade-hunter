from __future__ import annotations

from collections.abc import Callable

from ..models import MarketEvent


EventSink = Callable[[MarketEvent], object]
StatusSink = Callable[[str, dict], None]


class FeedAdapter:
    name = "feed"

    def __init__(self, emit: EventSink, publish_status: StatusSink) -> None:
        self.emit = emit
        self.publish_status = publish_status

    def start(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError
