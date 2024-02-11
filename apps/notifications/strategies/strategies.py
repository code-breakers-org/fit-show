from typing import List

import phonenumbers
from django.conf import settings

from .strategy_abstract import NotificationStrategy
from ..decorators import log_sms_info
from ..tasks import (
    send_sms_notification,
    send_template_sms_notification,
)


class SmsStrategy(NotificationStrategy):
    def send(self, receiver: str, message: str):
        return send_sms_notification.delay(receiver, message)

    @log_sms_info
    def execute(self, receiver: str, message: str):
        if not self.validate_phone_number(number=receiver):
            return False
        if not settings.DEBUG:
            self.send(receiver=str(receiver), message=message)

    def validate_phone_number(self, number: str):
        try:
            if isinstance(number, str):
                number = phonenumbers.parse(number, None)
            return phonenumbers.is_valid_number(number)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False


class SmsOtpStrategy(SmsStrategy):
    def send(self, receiver: str, message: str):
        template_id = self.get_template_id()
        template_body = self.get_template_body(value=message)
        send_template_sms_notification.delay(
            receiver=receiver, body=template_body, template_id=template_id
        )

    def get_template_id(self) -> int:
        return settings.SMS_OTP_TEMPLATE

    def get_template_body(self, value: str) -> List[dict]:
        return [{"name": "Code", "value": value}]


class SmsPasswordStrategy(SmsOtpStrategy):
    def get_template_id(self) -> int:
        return settings.SMS_PASSWORD_TEMPLATE

    def get_template_body(self, value: str) -> List[dict]:
        return [{"name": "PASSWORD", "value": value}]
