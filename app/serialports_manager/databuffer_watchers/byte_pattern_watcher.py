from . import GenericWatcher
from .. import DataBuffer
from ...utils import KMP
from enum import Enum


class BytePatternWatcher(GenericWatcher):
    class SearchIn(Enum):
        # Will search only in added values, and ignore what's in the buffer
        NEW_VALUES = 1
        # Will search in whole buffer, after new values has been added
        WHOLE_BUFFER = 2
        # Will search in new values, and if not found it'll look in the buffer
        # This is default.
        NEW_VALUES_AND_BUFFER = 3

    def __init__(self) -> None:
        super().__init__()
        self._pattern: bytearray = bytearray()
        self._behaviour: BytePatternWatcher.SearchIn = (
            BytePatternWatcher.SearchIn.NEW_VALUES_AND_BUFFER
        )
        self._kmp = KMP()

    @property
    def pattern(self) -> bytearray:
        return self._pattern

    @pattern.setter
    def pattern(self, new_pattern: bytearray) -> None:
        if len(new_pattern) > 0:
            self._pattern = new_pattern

    @property
    def behaviour(self) -> SearchIn:
        return self._behaviour

    @behaviour.setter
    def behaviour(self, new_behaviour: SearchIn) -> None:
        self._behaviour = new_behaviour

    def _check_new_data(self, buffer: DataBuffer, new_values: list) -> dict | None:
        pass

    def _check_if_pattern_exists(self, data_array: list) -> list[int] | None:
        """Checks if pattern exist in passed array.
        Returns a list with found pattern indexes, or None if no pattern has been found"""
        if len(data_array) < len(self.pattern):
            return None
        
        found_indexes = self._kmp.search(data_array, self.pattern)
        if len(found_indexes) == 0:
            return None

        return found_indexes

