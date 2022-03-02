import unittest

from app.utils import Observer, Subject


class TestSubject(Subject):
    def __init__(self) -> None:
        super().__init__()
        self._value: int = 0

    def triggerAddEvent(self) -> None:
        self._value += 1
        self.notify({"event_name": "add"})

    def triggerSubEvent(self) -> None:
        self._value -= 1
        self.notify({"event_name": "sub"})

    @property
    def value(self):
        return self._value


class TestEventBlindObserver(Observer):
    def __init__(self) -> None:
        self._value: int = 0

    def update(self, subject: TestSubject, event_data: dict) -> None:
        self.value = subject.value

    @property
    def value(self) -> int | None:
        return self._value

    @value.setter
    def value(self, new_value: int) -> None:
        self._value = new_value


class TestEventWatchingObserver(TestEventBlindObserver):
    def update(self, subject: TestSubject, event_data: dict) -> None:
        if event_data["event_name"] == "add":
            self._value += 1
        elif event_data["event_name"] == "sub":
            self._value -= 1


class ObserverTests(unittest.TestCase):
    def test_blind_notifications(self):
        observer = TestEventBlindObserver()
        subject = TestSubject()
        subject.attach(observer)

        self.assertEqual(observer.value, 0)

        subject.triggerAddEvent()
        self.assertEqual(observer.value, 1)

        subject.triggerSubEvent()
        self.assertEqual(observer.value, 0)

    def test_notification_descriptions(self):
        observer = TestEventWatchingObserver()
        subject = TestSubject()
        subject.attach(observer)

        self.assertEqual(observer.value, 0)

        subject.triggerAddEvent()
        self.assertEqual(observer.value, 1)

        subject.triggerSubEvent()
        self.assertEqual(observer.value, 0)
