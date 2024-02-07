from abc import abstractmethod, ABC
from typing import Mapping


class NotificationSubscriberAbstract(ABC):
    @abstractmethod
    def update(self, to: str, message: str):
        pass

    @abstractmethod
    def log(self, to: str, message: str, extra: Mapping[str, object] | None = None):
        pass

    @abstractmethod
    def send(self, to: str, message: str):
        pass
