from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    @abstractmethod
    def execute(self, to: str, message: str):
        pass
