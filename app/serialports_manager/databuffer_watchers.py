from databuffer import DataBuffer
from app.utils.observer import Observer, Subject


class GenericDataBufferWatcher(Observer, Subject):
    """This is base class for all the DataBuffer watchers.

    Use `attach` method to add new Observer and receive notifications.

    Use `detach` to remove an Observer and stop receiving notifications

    You can also enable or disable notifications by setting `notifications_enabled` property value to `True` and `False` accordingly"""

    def __init__(self) -> None:
        super().__init__()
        self._last_notified_value: int = 0
        self._buffer_length: int = 0
        self._notifications_enabled: bool = True

    @property
    def last_notified_value(self) -> int:
        return self._last_notified_value

    @property
    def notifications_enabled(self) -> bool:
        return self._notifications_enabled

    @notifications_enabled.setter
    def notifications_enabled(self, enabled: bool) -> None:
        enabled = bool(enabled)
        self._notifications_enabled = enabled

    def _check_new_data(self, buffer: DataBuffer, new_values: list) -> dict | None:
        """Override this function and perform data validation.
        Return a `dict` with data that should be passed to observers, if the conditions for notification are fulfilled.
        Return `None` if observers should not be notified about new data."""
        raise NotImplementedError

    def update(self, subject: DataBuffer, event_data: dict) -> None:
        self._buffer_length += len(event_data["new_data"])
        if self.notifications_enabled:
            data_check_result = self._check_new_data(subject, event_data["new_data"])
            if data_check_result is not None:
                self.notify(data_check_result)
                self._last_notified_value = subject.length


class ValuesAmountDataBufferWatcher(GenericDataBufferWatcher):
    """This watcher looks for specified amount of values added to the buffer.
    
    Notifies with `{"event_name": "newdata", "new_values": [list of new values]}`"""
    def __init__(self) -> None:
        super().__init__()
        self._notification_threshold: int = 1

    @property
    def notification_threshold(self) -> int:
        return self._notification_threshold

    @notification_threshold.setter
    def notification_threshold(self, new_threshold: int) -> None:
        new_threshold = int(new_threshold)
        if new_threshold > 0:
            self._notification_threshold = new_threshold

    def _check_new_data(self, buffer: DataBuffer, new_values: list) -> dict | None:
        pass
