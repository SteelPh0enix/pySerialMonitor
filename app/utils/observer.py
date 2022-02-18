# courtesy of https://github.com/faif/python-patterns from where i took the implementation
from contextlib import suppress
from typing import Protocol


class Observer(Protocol):
    def update(self, subject, event_name: str) -> None:
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

    def notify(self, event_name: str = "", modifier: Observer | None = None) -> None:
        for observer in self._observers:
            if modifier != observer:
                observer.update(self, event_name)
