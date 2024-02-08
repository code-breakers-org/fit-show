import logging

from django.conf import settings
from sms_ir.services import SmsIr

from config.envs import SMS_API_KEY, SMS_LINE_NUMBER, SMS_TEMPLATE
from .sms_provider_abstract import SMSProviderAbstract


class CustomSmsIr(SmsIr):
    def config_logger(self):
        self.log_level = logging.INFO
        self.logger = logger = logging.getLogger(settings.LOGGER_NAME)
        self.logger.setLevel(self.log_level)


class SmsProvider(SMSProviderAbstract):

    instance = CustomSmsIr(
        SMS_API_KEY,
        SMS_LINE_NUMBER,
    )

    def send(self, to: str, message: str):
        return self.instance.send_sms(
            number=to,
            message=message,
            linenumber=SMS_LINE_NUMBER,
        )

    def send_bulk(self, to: list[str], message: str):
        return self.instance.send_bulk_sms(
            to,
            message,
            SMS_LINE_NUMBER,
        )

    def send_verify_code(self, to: str, code: str):
        body = [{"name": "Code", "value": code}]

        return self.instance.send_verify_code(
            number=to,
            template_id=SMS_TEMPLATE,
            parameters=body,
        )
