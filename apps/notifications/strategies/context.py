from .strategy_abstract import NotificationStrategy


class NotificationContext:
    def __init__(self, strategy: NotificationStrategy = None) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> NotificationStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: NotificationStrategy) -> None:
        self._strategy = strategy

    def send(self, receiver: str, message: str) -> None:
        return self._strategy.execute(receiver=receiver, message=message)
