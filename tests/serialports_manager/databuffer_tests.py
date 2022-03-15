import unittest

from app.serialports_manager import DataBuffer
from app.utils import Observer
from parameterized import parameterized


class DataBufferWatcher(Observer):
    def __init__(self) -> None:
        super().__init__()
        self.data: list = []
        self.data_from_last_notification: list = []
        self.amount_of_values_last_notified: int | None = None

    def update(self, subject, event_data: dict) -> None:
        if event_data["event_name"] == "newdata":
            # Save all the data related to notification
            self.data_from_last_notification = event_data["new_values"]
            self.amount_of_values_last_notified = len(event_data["new_values"])
            self.data += self.data_from_last_notification
        elif event_data["event_name"] == "clear":
            self.data.clear()


class DataBufferTests(unittest.TestCase):
    def test_buffer_creating(self):
        buffer = DataBuffer()

        # The list should be empty, and notifications should be performed instantly, every added value
        self.assertEqual(buffer.length, 0)
        self.assertListEqual(buffer.data, [])
        self.assertTrue(buffer.notifications_enabled)

    @parameterized.expand(
        [
            ("str", "abc", "def", ["a", "b", "c", "d", "e", "f"]),
            ("bytes", b"\x00\x01\x02", b"\x03\x04\x05", [0, 1, 2, 3, 4, 5]),
            ("ints", [2, 3, 4], [1, 2, 3], [2, 3, 4, 1, 2, 3]),
        ]
    )
    def test_adding_new_value_lists_to_buffer(
        self, _, values_first, values_second, expected_result
    ):
        buffer = DataBuffer()

        # Test both methods of adding collection of values to the buffer
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
        self, _, value_first, value_second, value_third, expected_result
    ):
        buffer = DataBuffer()

        # Check method of adding single value to the buffer
        buffer.add_value(value_first)
        buffer.add_value(value_second)
        buffer.add_value(value_third)

        self.assertEqual(buffer.data, expected_result)

    @parameterized.expand(
        [
            ("0", ""),
            ("1", "a"),
            ("2", "abc"),
            ("3", "123123qweqewasdasdzccz"),
        ]
    )
    def test_clearing_buffered_data(self, _, test_data):
        buffer = DataBuffer()
        buffer += test_data

        buffer.clear()

        # Check if the data has been cleared
        self.assertEqual(buffer.length, 0)

    @parameterized.expand(
        [
            ("0", ""),
            ("1", "a"),
            ("2", "abc"),
            ("3", "123123qweqewasdasdzccz"),
        ]
    )
    def test_getting_amount_of_currently_buffered_data(self, _, test_data):
        buffer = DataBuffer()
        buffer += test_data

        # Check if the amount of added data is correct
        self.assertEqual(buffer.length, len(test_data))

    def test_newdata_notification_event_new_value(self):
        test_data_a = "test string"
        test_data_b = "another test string"
        test_data = [test_data_a, test_data_b]

        buffer = DataBuffer()
        buffer_watcher = DataBufferWatcher()
        buffer.attach(buffer_watcher)

        # Add first value and check if it's been correctly notified about
        buffer.add_value(test_data_a)
        self.assertListEqual(buffer_watcher.data_from_last_notification, [test_data_a])
        self.assertEqual(buffer_watcher.amount_of_values_last_notified, 1)

        # Add second value and check if it's been correctly notified about
        buffer.add_value(test_data_b)
        self.assertListEqual(buffer_watcher.data_from_last_notification, [test_data_b])
        self.assertEqual(buffer_watcher.amount_of_values_last_notified, 1)

        # Verify data integrity
        self.assertListEqual(buffer.data, buffer_watcher.data)
        self.assertListEqual(buffer_watcher.data, test_data)

    def test_newdata_notification_event_new_values(self):
        test_data_a = [1, 2, 3]
        test_data_b = [4, 5]
        test_data = test_data_a + test_data_b

        buffer = DataBuffer()
        buffer_watcher = DataBufferWatcher()
        buffer.attach(buffer_watcher)

        # Add first collection of values and check if it's been correctly notified about
        buffer.add_values(test_data_a)
        self.assertListEqual(buffer_watcher.data_from_last_notification, test_data_a)
        self.assertEqual(
            buffer_watcher.amount_of_values_last_notified, len(test_data_a)
        )

        # Add second collection of values and check if it's been correctly notified about
        buffer.add_values(test_data_b)
        self.assertListEqual(buffer_watcher.data_from_last_notification, test_data_b)
        self.assertEqual(
            buffer_watcher.amount_of_values_last_notified, len(test_data_b)
        )

        # Verify data integrity
        self.assertListEqual(buffer.data, buffer_watcher.data)
        self.assertListEqual(buffer_watcher.data, test_data)

    def test_buffer_cleared_event_notification(self):
        test_data = [1, 2, 3, 4, 5]

        buffer = DataBuffer()
        buffer_watcher = DataBufferWatcher()
        buffer.attach(buffer_watcher)

        buffer.add_values(test_data)
        buffer.clear()

        # Check if the watching buffer has been notified to clear the data
        self.assertEqual(buffer.length, 0)
        self.assertEqual(len(buffer_watcher.data), 0)

    def test_buffer_cleared_event_notification_disabling(self):
        test_data = [1, 2, 3, 4, 5]

        buffer = DataBuffer()
        buffer_watcher = DataBufferWatcher()
        buffer.attach(buffer_watcher)

        buffer.add_values(test_data)
        buffer.notifications_enabled = False
        buffer.clear()

        # Check if the watching buffer has NOT been notified to clear the data
        self.assertEqual(buffer.length, 0)
        self.assertListEqual(buffer_watcher.data, test_data)

    def test_newdata_notification_disabling(self):
        test_data = [1, 2, 3, 4, 5]

        buffer = DataBuffer()
        buffer.notifications_enabled = False
        buffer_watcher = DataBufferWatcher()
        buffer.attach(buffer_watcher)

        buffer.add_values(test_data)

        # Verify that no notification has been sent to watching buffer, hence it should be empty
        self.assertIsNone(buffer_watcher.amount_of_values_last_notified)
        self.assertListEqual(buffer_watcher.data_from_last_notification, [])
        self.assertListEqual(buffer_watcher.data, [])

    def test_newdata_notification_reenabling(self):
        test_data_a = [1, 2, 3]
        test_data_b = [4, 5]

        buffer = DataBuffer()
        buffer.notifications_enabled = False
        buffer_watcher = DataBufferWatcher()
        buffer.attach(buffer_watcher)

        buffer.add_values(test_data_a)

        # Data added, but notifications were disabled so the watching buffer should be empty
        self.assertIsNone(buffer_watcher.amount_of_values_last_notified)
        self.assertListEqual(buffer_watcher.data_from_last_notification, [])
        self.assertListEqual(buffer_watcher.data, [])

        buffer.notifications_enabled = True
        buffer.add_values(test_data_b)

        # Data added after notifications has been enabled, verify if the notification was correct
        self.assertEqual(
            buffer_watcher.amount_of_values_last_notified, len(test_data_b)
        )
        self.assertListEqual(buffer_watcher.data_from_last_notification, test_data_b)
        self.assertListEqual(buffer_watcher.data, test_data_b)

    def test_container_like_access(self):
        test_data = [1, 2, 3, 4, 5, 6]

        buffer = DataBuffer()
        buffer += test_data

        self.assertEqual(len(buffer), len(test_data))
        for i in range(0, len(test_data)):
            self.assertEqual(buffer[i], test_data[i])

