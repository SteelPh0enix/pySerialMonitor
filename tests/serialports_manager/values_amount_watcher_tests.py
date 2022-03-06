import unittest

from app.serialports_manager import DataBuffer
from app.serialports_manager.databuffer_watchers import ValuesAmountDataBufferWatcher
from .test_observer import TestObserver


class ValuesAmountDataBufferWatcherTests(unittest.TestCase):
    def test_basic_notifications_single_values(self):
        buffer = DataBuffer()
        watcher = ValuesAmountDataBufferWatcher()
        observer = TestObserver()

        # Attach the watcher to the buffer
        buffer.attach(watcher)

        # Attach our test observer to the watcher
        watcher.attach(observer)

        # Set watcher threshold
        watcher.notification_threshold = 3

        # Start adding data and watch for notifications
        buffer.add_value(1)
        # No notification should happen yet
        self.assertIsNone(observer.last_updated_data)

        buffer.add_value(2)
        # No notification should happen yet
        self.assertIsNone(observer.last_updated_data)

        buffer.add_value(3)
        # Now notification should be triggered
        self.assertIsNotNone(observer.last_updated_data)
        self.assertDictContainsSubset(
            {"databuffer": buffer, "new_data": [1, 2, 3]}, observer.last_updated_data
        )

        buffer.add_value(4)
        # No new notification should be fired, so the previous asserts should still be true
        self.assertIsNotNone(observer.last_updated_data)
        self.assertDictContainsSubset(
            {"databuffer": buffer, "new_data": [1, 2, 3]}, observer.last_updated_data
        )
