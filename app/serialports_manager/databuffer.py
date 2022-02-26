from typing import Collection
from app.utils.observer import Subject


class DataBuffer(Subject):
    """Simple data buffer class with configurable notifications.

    Provided notification events:
    * `{event_name: clear}` - buffer has been cleared
    * `{event_name: newdata, new_values: list}` - new data has been added to the buffer

    `newdata` notification will be emitted every time new value(s) are added to the buffer.
    If you need more specific notifications, see `databuffer_watchers` module.

    You can also control if notifications should be enabled or disabled, with `notifications_enabled` property
    """

    def __init__(self) -> None:
        super().__init__()
        self._buffer: list = []
        self._notifications_enabled: bool = True

    @property
    def data(self) -> list:
        """Access the buffered data"""
        return self._buffer

    @property
    def length(self) -> int:
        """Return the amount of items in buffer"""
        return len(self._buffer)

    @property
    def notifications_enabled(self) -> bool:
        return self._notifications_enabled

    @notifications_enabled.setter
    def notifications_enabled(self, enabled: bool) -> None:
        self._notifications_enabled = bool(enabled)

    def clear(self) -> None:
        """Clear the content of the buffer"""
        self._buffer.clear()
        self._notify_clear()

    def add_value(self, value: object) -> None:
        """Add value to the buffer"""
        self._buffer.append(value)
        self._notify_newdata([value])

    def add_values(self, values: Collection) -> None:
        """Add multiple values (collection) to the buffer"""
        self._buffer += values
        self._notify_newdata(values)

    def __iadd__(self, new_data: Collection):
        """+= operator overload"""
        self.add_values(new_data)
        return self

    def __getitem__(self, key: int | slice):
        return self.data[key]

    def __len__(self) -> int:
        return self.length

    def _notify_clear(self) -> None:
        if self._notifications_enabled:
            self.notify({"event_name": "clear"})

    def _notify_newdata(self, values: Collection) -> None:
        """Perform `newdata` notification and update object's internal state"""
        if self._notifications_enabled:
            self.notify({"event_name": "newdata", "new_values": values})
