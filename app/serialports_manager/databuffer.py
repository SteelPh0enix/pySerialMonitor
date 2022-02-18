from app.utils.observer import Subject




class DataBuffer(Subject):
    """DataBuffer - simple data buffer class with configurable notifications.

    Available notifications:
    * "clear" - buffer has been cleared
    * "newdata" - new data has been added to the buffer
    """
    def __init__(self) -> None:
        super().__init__()
        self._buffer: list = []

    @property
    def data(self) -> list:
        return self._buffer

    @property
    def length(self) -> int:
        return len(self._buffer)

    def clear(self) -> None:
        self._buffer.clear()
        self.notify("clear")

    def add_value(self, value) -> None:
        self._buffer.append(value)
        self.notify("newdata")

    def add_values(self, values) -> None:
        self._buffer += values
        self.notify("newdata")

    def __iadd__(self, new_data):
        self.add_values(new_data)
        return self
