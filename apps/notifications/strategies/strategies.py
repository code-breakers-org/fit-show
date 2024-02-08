import phonenumbers
from django.conf import settings

from .strategy_abstract import NotificationStrategy
from ..decorators import log_sms_info
from ..tasks import send_otp_sms_notification, send_sms_notification


class SmsStrategy(NotificationStrategy):
    def send(self, to: str, message: str):
        return send_sms_notification.delay(to, message)

    @log_sms_info
    def execute(self, to: str, message: str):
        if not self.validate_phone_number(number=to):
            return False
        if not settings.DEBUG:
            self.send(to=str(to), message=message)

    def validate_phone_number(self, number: str):
        try:
            if type(number) is str:
                number = phonenumbers.parse(number, None)
            return phonenumbers.is_valid_number(number)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False


class PhoneNumberVerificationStrategy(SmsStrategy):
    def send(self, to: str, message: str):
        print("PhoneNumberVerificationStrategy")
        send_otp_sms_notification.delay(to=to, code=message)
