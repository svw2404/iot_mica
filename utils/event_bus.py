"""A super-lightweight in-process pub-sub event bus."""
from __future__ import annotations
from collections import defaultdict
from threading import Lock
from typing import Callable, Dict, List, Any

class EventBus:
    def __init__(self) -> None:
        self._subs: Dict[str, List[Callable[[str, Any], None]]] = defaultdict(list)
        self._lock = Lock()

    def subscribe(self, topic: str, handler: Callable[[str, Any], None]) -> None:
        with self._lock:
            self._subs[topic].append(handler)

    def publish(self, topic: str, payload: Any) -> None:
        with self._lock:
            handlers = list(self._subs.get(topic, []))
        for h in handlers:
            h(topic, payload)
