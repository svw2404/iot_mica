"""Simple event bus implementation."""

from typing import Callable, Dict, List


class EventBus:
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event: str, callback: Callable) -> None:
        self._subscribers.setdefault(event, []).append(callback)

    def publish(self, event: str, data):
        for callback in self._subscribers.get(event, []):
            callback(data)
