from celery import shared_task

from apps.notifications.providers import SmsProvider


@shared_task()
def send_otp_sms_notification(to: str, code: str):
    provider = SmsProvider()
    provider.send_verify_code(to=to, code=code)


@shared_task()
def send_sms_notification(to: str, message: str):
    provider = SmsProvider()
    provider.send(to=to, message=message)
