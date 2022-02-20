from typing import Collection
from app.utils.observer import Subject
import schedule


class DataBuffer(Subject):
    """Simple data buffer class with configurable notifications.

    Provided notification events:
    * `{event_name: clear}` - buffer has been cleared
    * `{event_name: newdata, new_values: (list)}` - new data has been added to the buffer

    By default `newdata` notification is triggered instantly, every added value.
    This behaviour can be changed using two methods:
    * `set_notification_threshold` - specifies amount of new values required to trigger notification
    * `set_notification_timeout` - specifies the interval of notifications, `None` or `0` means no interval

    If interval is set, the notification threshold will be checked periodically, instead
    of checking it every time new value is added. That way, you'll avoid notification storm
    when frequently buffering small amounts of data.
    """

    def __init__(self) -> None:
        super().__init__()
        self._buffer: list = []
        self._last_notified_index: int = 0
        self.set_data_notification_threshold(1)
        self.set_data_notification_timeout(None)

    @property
    def data(self) -> list:
        """Access the buffered data"""
        return self._buffer

    @property
    def length(self) -> int:
        """Return the amount of items in buffer"""
        return len(self._buffer)

    @property
    def are_notifications_instant(self) -> bool:
        """Returns `True` if the notifications are instant, `False` if they are scheduled"""
        return self._notification_ms_delay is None or self._notification_ms_delay == 0

    @property
    def unnotified_values_amount(self) -> int:
        """Returns the amount of values added since last notification. Will be >0 only when notifications are scheduled."""
        return self.length - self._last_notified_index

    @property
    def should_notify(self) -> bool:
        """Returns `True` if the notification threshold is exceeded, `False` otherwise.

        Use only if notifications are scheduled, otherwise it'll never be `True` (because of instant notifications)"""
        return self.unnotified_values_amount >= self._notification_values_threshold

    def set_data_notification_threshold(self, values: int) -> bool:
        """Set the amount of new buffered values required to trigger `newdata` notification

        Returns `True` on success, `False` on invalid argument value (must be >= 1)"""
        values = int(values)
        if values >= 1:
            self._notification_values_threshold = values
            return True
        return False

    def set_data_notification_timeout(self, milliseconds: int | None) -> bool:
        """Set the amount of time between notification threshold checks, read the class description for more info

        Returns `True` on success, `False` on invalid argument value (must be >= 0 or None)"""
        if milliseconds is None:
            self._notification_ms_delay = None
            return True

        milliseconds = int(milliseconds)
        if milliseconds >= 0:
            self._notification_ms_delay = milliseconds
            return True

        return False

    def clear(self) -> None:
        """Clear the content of the buffer"""
        self._buffer.clear()
        self.notify({"event_name": "clear"})

    def add_value(self, value: object) -> None:
        """Add value to the buffer"""
        self._buffer.append(value)
        self._notify_newdata_instant_if_needed()

    def add_values(self, values: Collection) -> None:
        """Add multiple values (collection) to the buffer"""
        self._buffer += values
        self._notify_newdata_instant_if_needed()

    def __iadd__(self, new_data: Collection):
        """+= operator overload"""
        self.add_values(new_data)
        return self

    def _notify_newdata(self):
        """Perform `newdata` notification and update object's internal state"""
        new_values_amount = self.unnotified_values_amount
        self._last_notified_index = self.length
        self.notify(
            {"event_name": "newdata", "new_values": self.data[-new_values_amount:]}
        )

    def _notify_newdata_instant_if_needed(self):
        """Perform instant `newdata` notification if the conditions are fulfilled"""
        if self.are_notifications_instant and self.should_notify:
            self._notify_newdata()
