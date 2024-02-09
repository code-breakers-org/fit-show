from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    @abstractmethod
    def execute(self, receiver: str, message: str):
        pass
