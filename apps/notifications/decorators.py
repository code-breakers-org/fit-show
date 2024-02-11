import logging
from functools import wraps
from typing import List

from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)


def log_info(message: str, sensitive_keys: List[str] = None):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            sanitized_dict = {}
            for key, value in kwargs.items():
                if sensitive_keys is not None and key not in sensitive_keys:
                    sanitized_dict[key] = value

            if "message" in sanitized_dict:
                val = sanitized_dict.pop("message")
                sanitized_dict["_message"] = val

            logger.info(
                msg=f"{message}",
                extra=sanitized_dict,
            )
            return function(*args, **kwargs)

        return wrapper

    return decorator
