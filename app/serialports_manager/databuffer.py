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
        self._notification_timeout_ms: int | None = None
        self._notification_values_threshold: int | None = None

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
    def notification_values_threshold(self) -> int | None:
        """Returns the amount of new values needed to trigger `newdata` notification"""
        return self._notification_values_threshold

    @property
    def notification_timeout_ms(self) -> int | None:
        """Returns the notification timeout in milliseconds, or None if scheduling is disabled"""
        return self._notification_timeout_ms

    @property
    def are_notifications_instant(self) -> bool:
        """Returns `True` if the notifications are instant, `False` if they are scheduled"""
        return self.notification_timeout_ms is None

    @property
    def unnotified_values_amount(self) -> int:
        """Returns the amount of values added since last notification. Will be >0 only when notifications are scheduled."""
        return self.length - self._last_notified_index

    @property
    def should_notify(self) -> bool:
        """Returns `True` if the notification threshold is exceeded, `False` otherwise.

        Use only if notifications are scheduled, otherwise it'll never be `True` (because of instant notifications)"""
        if self.notification_values_threshold is None:
            return False

        return self.unnotified_values_amount >= self.notification_values_threshold

    def set_data_notification_threshold(
        self,
        values: int | None,
        reset_notifications: bool = False,
        instant_notification: bool = False,
    ) -> bool:
        """Set the amount of freshly buffered values required to trigger `newdata` notification

        If `values` is set to `0` or `None`, notifications will be disabled

        By default, when notifications are enabled after being disabled, DataBuffer will notify about all the data that's been added since last notification.
        If `reset_notifications` is `True`, DataBuffer will not notify about already stored data.
        It will notify only about data that will be added after the notifications were re-enabled.

        If `instant_notification` is `True`, this function will perform `newdata` notification if value threshold will been exceeded.

        Returns `True` on success, `False` on invalid `values` argument value (must be >=0 or None)"""
        if values is None:
            self._notification_values_threshold = None
            return True

        values = int(values)
        if values > 0:
            self._notification_values_threshold = values
            if instant_notification:
                self._notify_newdata()
            if reset_notifications:
                self._last_notified_index = self.length
            return True
        elif values == 0:
            self._notification_values_threshold = None
            return True

        return False

    def set_data_notification_timeout(self, milliseconds: int | None) -> bool:
        """Set the amount of time between notification threshold checks, read the class description for more info

        Returns `True` on success, `False` on invalid argument value (must be >=0 or None)"""
        if milliseconds is None:
            self._notification_timeout_ms = None
            return True

        milliseconds = int(milliseconds)
        if milliseconds > 0:
            self._notification_timeout_ms = milliseconds
            return True
        elif milliseconds == 0:
            self._notification_timeout_ms = None

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
