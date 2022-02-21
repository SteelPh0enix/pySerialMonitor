from hashlib import new
from databuffer import DataBuffer
from app.utils.observer import Observer, Subject


class GenericDataBufferWatcher(Observer, Subject):
    """This is base class for all the DataBuffer watchers.
    Use `attach` method to add new Observer and receive notifications.
    Use `detach` to remove an Observer and stop receiving notifications"""

    def __init__(self) -> None:
        super().__init__()
        self._last_notified_value: int = 0

    @property
    def last_notified_value(self) -> int:
        return self._last_notified_value

    def _check_new_data(self, buffer: DataBuffer, new_values: list) -> dict | None:
        """Override this function and perform data validation.
        Return a `dict` with data that should be passed to observers, if the conditions for notification are fulfilled.
        Return `None` if observers should not be notified about new data."""
        raise NotImplementedError

    def update(self, subject: DataBuffer, event_data: dict) -> None:
        data_check_result = self._check_new_data(subject, event_data["new_data"])
        if data_check_result is not None:
            self.notify(data_check_result)
            self._last_notified_value = subject.length


class ValueAmountDataBufferWatcher(GenericDataBufferWatcher):
    def __init__(self) -> None:
        super().__init__()
