import logging
from typing import List

from django.conf import settings
from sms_ir.services import SmsIr

from apps.core.types import NameValueDict
from .sms_provider_abstract import SMSProviderAbstract


class CustomSmsIr(SmsIr):
    def config_logger(self):
        self.log_level = logging.INFO
        self.logger = logging.getLogger(settings.LOGGER_NAME)
        self.logger.setLevel(self.log_level)


class SmsProvider(SMSProviderAbstract):
    def __init__(self):
        self.instance = CustomSmsIr(
            settings.SMS_API_KEY,
            settings.SMS_LINE_NUMBER,
        )

    def send(self, receiver: str, message: str):
        return self.instance.send_sms(number=receiver, message=message)

    def send_bulk(self, receiver: list[str], message: str):
        return self.instance.send_bulk_sms(receiver, message)

    def send_verify_code(
        self, receiver: str, body: List[NameValueDict], template_id: int
    ):
        return self.instance.send_verify_code(
            number=receiver,
            template_id=template_id,
            parameters=body,
        )
