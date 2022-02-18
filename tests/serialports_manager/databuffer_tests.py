import unittest

from app.serialports_manager.databuffer import DataBuffer
from app.utils.observer import Observer
from parameterized import parameterized


class DataBufferWatcher(Observer):
    def __init__(self) -> None:
        super().__init__()
        self.data: list = []

    def update(self, subject, event_name: str) -> None:
        if event_name == "newdata":
            self.data = subject.data
        elif event_name == "clear":
            self.data.clear()


class DataBufferTests(unittest.TestCase):
    def test_buffer_creating(self):
        buffer = DataBuffer()

        self.assertEqual(buffer.length, 0)
        self.assertListEqual(buffer.data, [])

    @parameterized.expand(
        [
            ("str", "abc", "def", ["a", "b", "c", "d", "e", "f"]),
            ("bytes", b"\x00\x01\x02", b"\x03\x04\x05", [0, 1, 2, 3, 4, 5]),
            ("ints", [2, 3, 4], [1, 2, 3], [2, 3, 4, 1, 2, 3]),
        ]
    )
    def test_adding_new_value_lists_to_buffer(
        self, type_name, values_first, values_second, expected_result
    ):
        buffer = DataBuffer()

        buffer.add_values(values_first)
        buffer += values_second

        self.assertEqual(buffer.data, expected_result)

    @parameterized.expand(
        [
            ("str", "a", "b", "c", ["a", "b", "c"]),
            ("bytes", b"\x00", b"\x03", b"\x06", [b"\x00", b"\x03", b"\x06"]),
            ("ints", 100, 1000, 10000, [100, 1000, 10000]),
        ]
    )
    def test_adding_new_values_to_buffer(
        self, type_name, value_first, value_second, value_third, expected_result
    ):
        buffer = DataBuffer()

        buffer.add_value(value_first)
        buffer.add_value(value_second)
        buffer.add_value(value_third)

        self.assertEqual(buffer.data, expected_result)

    def test_clearing_buffered_data(self):
        buffer = DataBuffer()
        buffer += "abcdef"

        self.assertEqual(buffer.length, 6)

        buffer.clear()

        self.assertEqual(buffer.length, 0)

    def test_getting_amount_of_currently_buffered_data(self):
        buffer = DataBuffer()
        buffer += "abcdef"

        self.assertEqual(buffer.length, 6)

    def test_data_notification_event_new_value(self):
        test_data = "test string"

        buffer = DataBuffer()
        buffer_watcher = DataBufferWatcher()
        buffer.attach(buffer_watcher)

        buffer.add_value(test_data)

        self.assertListEqual(buffer.data, buffer_watcher.data)
        self.assertListEqual(buffer_watcher.data, [test_data])

    def test_data_notification_event_new_values(self):
        test_data = [1, 2, 3, 4, 5]

        buffer = DataBuffer()
        buffer_watcher = DataBufferWatcher()
        buffer.attach(buffer_watcher)

        buffer.add_values(test_data)

        self.assertListEqual(buffer.data, buffer_watcher.data)
        self.assertListEqual(buffer_watcher.data, test_data)

    def test_data_notification_event_buffer_cleared(self):
        test_data = [1, 2, 3, 4, 5]

        buffer = DataBuffer()
        buffer_watcher = DataBufferWatcher()
        buffer.attach(buffer_watcher)

        buffer.add_values(test_data)

        self.assertListEqual(buffer.data, buffer_watcher.data)
        self.assertListEqual(buffer_watcher.data, test_data)

        buffer.clear()

        self.assertEqual(buffer.length, 0)
        self.assertEqual(len(buffer_watcher.data), 0)

    def test_data_notification_event_timeout(self):
        self.fail("Not implemented yet!")

    def test_data_notification_event_character_detected(self):
        self.fail("Not implemented yet!")

    def test_data_notification_event_character_sequence_detected(self):
        self.fail("Not implemented yet!")
