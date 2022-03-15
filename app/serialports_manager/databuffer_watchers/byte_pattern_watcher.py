from . import GenericWatcher
from .. import DataBuffer
from ...utils import KMP


class BytePatternWatcher(GenericWatcher):
    def __init__(self) -> None:
        super().__init__()
        self._pattern: bytearray = bytearray()
        self._kmp = KMP()
        self._new_data_buffer = DataBuffer()
        self._return_with_pattern: bool = True

    @property
    def pattern(self) -> bytearray:
        return self._pattern

    @pattern.setter
    def pattern(self, new_pattern: bytearray) -> None:
        if len(new_pattern) > 0:
            self._pattern = new_pattern

    @property
    def return_data_with_pattern(self) -> bool:
        return self._return_with_pattern

    @return_data_with_pattern.setter
    def return_data_with_pattern(self, return_with_pattern: bool) -> None:
        self._return_with_pattern = bool(return_with_pattern)

    def _check_new_data(self, buffer: DataBuffer, new_values: list) -> dict | None:
        self._new_data_buffer += new_values
        found_indexes = self._check_if_pattern_exists(self._new_data_buffer.data)

        if found_indexes is None:
            return None

        # _check_if_pattern_exists returns a list of indexes where the pattern has been found
        # therefore, "new_values" will also be a list, in case more than one pattern has been found
        new_data_list: list[bytearray] = []
        last_index: int = 0
        for index in found_indexes:
            new_data_list.append(self._get_data_from_internal_buffer(last_index, index))
            last_index = index + len(self.pattern)

        # remove the fetched values from internal buffer (we got copies via _get_data_from_internal_buffer)
        del self._new_data_buffer.data[0:last_index]

        # return the dictionary with results
        return dict({"new_values": new_data_list})

    def _check_if_pattern_exists(self, data_array: list) -> list[int] | None:
        """Checks if pattern exist in passed array.
        Returns a list with found pattern indexes, or None if no pattern has been found"""
        if len(data_array) < len(self.pattern):
            return None

        found_indexes = self._kmp.search(data_array, self.pattern)
        if len(found_indexes) == 0:
            return None

        return found_indexes

    def _get_data_from_internal_buffer(
        self, start_index: int, end_index: int
    ) -> bytearray:
        real_end_index = end_index + (
            len(self.pattern) if self.return_data_with_pattern else 0
        )
        data = self._new_data_buffer.data[start_index:real_end_index].copy()
        return bytearray(data)
