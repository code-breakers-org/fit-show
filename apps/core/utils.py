import random
from datetime import timedelta

from django.utils import timezone


def generate_verification_code():
    return random.randrange(100_000, 999_999)


def add_date_time_to_now(
    days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0
):
    return timezone.now() + timedelta(
        minutes=minutes,
        seconds=seconds,
        milliseconds=milliseconds,
        weeks=weeks,
        days=days,
        hours=hours,
        microseconds=microseconds,
    )
