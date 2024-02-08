import logging
from typing import Mapping

import phonenumbers
from django.conf import settings

from apps.notifications.providers import SmsIrProvider
from apps.notifications.strategies.strategy_abstract import NotificationStrategy
from config.envs import DEBUG

logger = logging.getLogger(settings.LOGGER_NAME)


class SmsStrategy(NotificationStrategy):
    provider = SmsIrProvider()

    def send(self, to: str, message: str):
        return self.provider.send(to, message)

    def execute(self, to: str, message: str):
        if not self.validate_phone_number(number=to):
            return False
        response = None
        if not DEBUG:
            response = self.send(to=str(to), message=message)
        self.log(to=to, message=message, extra=response)

    def log(self, to: str, message: str, extra: Mapping[str, object] | None = None):
        logger.info(
            msg=f"Sms has been sent to {to} with this message: {message} ", extra=extra
        )

    def validate_phone_number(self, number: str):
        try:
            if type(number) is str:
                number = phonenumbers.parse(number, None)
            return phonenumbers.is_valid_number(number)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False


class PhoneNumberVerificationStrategy(SmsStrategy):
    def send(self, to: str, message: str):
        self.provider.send_verify_code(to=to, code=message)
