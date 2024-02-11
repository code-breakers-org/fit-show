from typing import List

from celery import shared_task

from apps.core.types import NameValueDict
from apps.notifications.providers import SmsProvider


@shared_task()
def send_template_sms_notification(
    receiver: str, template_id: int, body: List[NameValueDict]
):
    provider = SmsProvider()
    provider.send_verify_code(receiver=receiver, body=body, template_id=template_id)


@shared_task()
def send_sms_notification(receiver: str, message: str):
    provider = SmsProvider()
    provider.send(receiver=receiver, message=message)
