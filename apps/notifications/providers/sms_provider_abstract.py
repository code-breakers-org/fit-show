from abc import abstractmethod, ABC


class SMSProviderAbstract(ABC):
    @abstractmethod
    def send(self, receiver: str, message: str):
        pass

    @abstractmethod
    def send_verify_code(self, receiver: str, code: str):
        pass
