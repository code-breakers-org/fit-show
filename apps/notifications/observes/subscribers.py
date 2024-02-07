import logging
from typing import Mapping

import phonenumbers
from django.conf import settings

from apps.notifications.observes.notification_abstracts import (
    NotificationSubscriberAbstract,
)
from apps.notifications.providers import SmsIrProvider
from config.envs import DEBUG

logger = logging.getLogger(settings.LOGGER_NAME)


class SmsSubscriber(NotificationSubscriberAbstract):
    provider = SmsIrProvider()

    def send(self, to: str, message: str):
        return self.provider.send(to, message)

    def update(self, who: str, message: str):
        if not self.validate_phone_number(number=who):
            return False
        response = None
        if not DEBUG:
            response = self.send(to=str(who), message=message)
        self.log(to=who, message=message, extra=response)

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


class PhoneNumberVerificationSubscriber(SmsSubscriber):
    def send(self, to: str, message: str):
        self.provider.send_verify_code(to=to, code=message)
