from app.utils import Observer


class TestObserver(Observer):
    def __init__(self) -> None:
        super().__init__()
        self._last_updated_data: dict | None = None

    @property
    def last_updated_data(self) -> dict | None:
        return self._last_updated_data

    def update(self, subject, event_data: dict) -> None:
        self._last_updated_data = event_data