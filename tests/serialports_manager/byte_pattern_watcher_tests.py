import unittest

from app.serialports_manager import DataBuffer
from app.serialports_manager.databuffer_watchers import BytePatternWatcher
from app.utils import observer
from .test_observer import TestObserver


class BytePatternWatcherTest(unittest.TestCase):
    def test_notifications_single_byte_pattern(self):
        buffer = DataBuffer()
        watcher = BytePatternWatcher()
        observer = TestObserver()

        # Attach the watcher to the buffer
        buffer.attach(watcher)

        # Attach our test observer to the watcher
        watcher.attach(observer)

        # Set watcher pattern
        watcher.pattern = b"\n"

        # Start adding values - first, without pattern
        buffer.add_value(b"a")
        buffer.add_value(b"b")
        buffer.add_values([b"c", b"d", b"e", b"f"])

        self.assertIsNone(observer.last_updated_data)

        # Now let's add the pattern
        buffer.add_value(b"\n")

        self.assertIsNotNone(observer.last_updated_data)