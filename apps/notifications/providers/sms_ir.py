from sms_ir.services import SmsIr

from apps.notifications.providers.sms_provider_abstract import SMSProviderAbstract
from config.environment_variables import SMS_API_KEY, SMS_LINE_NUMBER, SMS_TEMPLATE


class SmsIrProvider(SMSProviderAbstract):

    instance = SmsIr(
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
