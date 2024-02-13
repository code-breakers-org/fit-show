from abc import abstractmethod, ABC
from typing import Any


class SMSProviderAbstract(ABC):
    @abstractmethod
    def send(self, receiver: str, message: str):
        pass

    @abstractmethod
    def send_verify_code(self, receiver: str, body: Any, template_id: str):
        pass
