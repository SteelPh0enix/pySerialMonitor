from typing import List


class DataBuffer:
    def __init__(self) -> None:
        self._buffer: List = []

    def data(self) -> List:
        return self._buffer
