from app.serialports_manager.databuffer import DataBuffer
from app.utils.observer import Observer, Subject


class GenericDataBufferWatcher(Subject, Observer):
    """This is base class for all the DataBuffer watchers.

    Use `attach` method to add new Observer and receive notifications.
    Use `detach` to remove an Observer and stop receiving notifications

    Every notification will have `databuffer` field with reference to DataBuffer that triggered it

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
        self._buffer_length += len(event_data["new_values"])
        if self.notifications_enabled:
            data_check_result = self._check_new_data(subject, event_data["new_values"])
            if data_check_result is not None:
                data_check_result["databuffer"] = subject
                self.notify(data_check_result)
                self._last_notified_value = subject.length


class ValuesAmountDataBufferWatcher(GenericDataBufferWatcher):
    """This watcher looks for specified amount of values added to the buffer.

    Notifies with `{"event_name": "newdata", "new_values": [list of new values]}`"""

    def __init__(self) -> None:
        super().__init__()
        self._notification_threshold: int = 1
        self._values_added_since_last_notification: int = 0

    @property
    def notification_threshold(self) -> int:
        return self._notification_threshold

    @notification_threshold.setter
    def notification_threshold(self, new_threshold: int) -> None:
        new_threshold = int(new_threshold)
        if new_threshold > 0:
            self._notification_threshold = new_threshold

    @property
    def values_added_since_last_notification(self) -> int:
        return self._values_added_since_last_notification

    def _check_new_data(self, buffer: DataBuffer, new_values: list) -> dict | None:
        self._values_added_since_last_notification += len(new_values)
        if self._values_added_since_last_notification >= self.notification_threshold:
            event_data = dict(
                {"new_data": buffer[-self.values_added_since_last_notification :]}
            )
            self._values_added_since_last_notification = 0
            return event_data
        return None
