import phonenumbers
from django.conf import settings

from .strategy_abstract import NotificationStrategy
from ..decorators import log_sms_info
from ..tasks import send_otp_sms_notification, send_sms_notification


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


class PhoneNumberVerificationStrategy(SmsStrategy):
    def send(self, receiver: str, message: str):
        send_otp_sms_notification.delay(receiver=receiver, code=message)
