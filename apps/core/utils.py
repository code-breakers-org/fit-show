import random
import string
from datetime import timedelta

from django.utils import timezone


def generate_verification_code():
    return random.randrange(10_000, 99_999)


def generate_random_string(length: int) -> str:
    """Generates a random string of the specified length.

    Args:
        length: The desired length of the random string.

    Returns:
        A randomly generated string of the specified length.
    """

    # Define the character set to use for generating the random string.
    characters = (
        string.ascii_letters + string.digits + string.punctuation
    )  # Includes letters, digits, and punctuation

    # Use random.choices to generate a random sequence of characters from the character set.
    random_string = "".join(random.choices(characters, k=length))

    return random_string


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
