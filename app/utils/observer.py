# courtesy of https://github.com/faif/python-patterns from where i took the implementation
from contextlib import suppress
from typing import Protocol


class Observer(Protocol):
    def update(self, subject, event_data: dict) -> None:
        """`event_data` is a dict of values passed from the subject.
        Read the subject's documentation to see what's inside."""
        pass


class Subject:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        with suppress(ValueError):
            self._observers.remove(observer)

    def notify(self, event_data: dict = {}, modifier: Observer | None = None) -> None:
        """event_data is a dict that will be passed to every observer."""
        for observer in self._observers:
            if modifier != observer:
                observer.update(self, event_data)
