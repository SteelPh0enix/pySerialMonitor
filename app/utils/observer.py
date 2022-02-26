# courtesy of https://github.com/faif/python-patterns from where i took the implementation
from contextlib import suppress
from typing import Protocol


class Observer(Protocol):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        pass

    def update(self, subject, event_data: dict) -> None:
        """This method is called when Observer receives notification from Subject.
        
        `event_data` is a dict of values passed from the subject.
        Read the subject's documentation to see what's inside."""
        raise NotImplementedError


class Subject:
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Add a new observer to the list of objects to notify"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Remove observer from the list of objects to notify"""
        with suppress(ValueError):
            self._observers.remove(observer)

    def notify(self, event_data: dict = {}, modifier: Observer | None = None) -> None:
        """Notify the observers on the list.
        
        event_data is a dict that will be passed to every observer."""
        for observer in self._observers:
            if modifier != observer:
                observer.update(self, event_data)
