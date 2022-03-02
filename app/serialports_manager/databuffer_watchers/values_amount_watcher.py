from . import GenericDataBufferWatcher
from .. import DataBuffer


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
