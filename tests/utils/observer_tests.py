import unittest
from app.utils.observer import Observer, Subject


class TestObserver(Observer):
    def __init__(self) -> None:
        self._value: int | None = None

    def update(self, subject: Subject) -> None:
        self.value = subject.value

    @property
    def value(self) -> int | None:
        return self._value

    @value.setter
    def value(self, new_value: int) -> None:
        self._value = new_value


class TestSubject(Subject):
    def __init__(self) -> None:
        super().__init__()
        self._value: int = 0

    def triggerEvent(self) -> None:
        self._value += 1
        self.notify()

    @property
    def value(self):
        return self._value


class ObserverTests(unittest.TestCase):
    def test_notifications(self):
        observer = TestObserver()
        subject = TestSubject()

        self.assertIsNone(observer.value)

        subject.attach(observer)
        subject.triggerEvent()

        self.assertEqual(observer.value, 1)


if __name__ == "__main__":
    unittest.main()
