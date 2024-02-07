from abc import abstractmethod, ABC


class SMSProviderAbstract(ABC):
    @abstractmethod
    def send(self, to: str, message: str):
        pass

    @abstractmethod
    def send_verify_code(self, to: str, code: str):
        pass
