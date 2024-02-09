from celery import shared_task

from apps.notifications.providers import SmsProvider


@shared_task()
def send_otp_sms_notification(receiver: str, code: str):
    provider = SmsProvider()
    provider.send_verify_code(receiver=receiver, code=code)


@shared_task()
def send_sms_notification(receiver: str, message: str):
    provider = SmsProvider()
    provider.send(receiver=receiver, message=message)
