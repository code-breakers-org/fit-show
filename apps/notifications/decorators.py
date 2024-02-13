import logging
from functools import wraps

from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)


def log_debug(message: str):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            copied_kwargs = kwargs.copy()
            if "message" in copied_kwargs:
                val = copied_kwargs.pop("message")
                copied_kwargs["_message"] = val
            formatted_message = message.format(**kwargs)
            logger.debug(
                msg=formatted_message,
                extra=copied_kwargs,
            )
            return function(*args, **kwargs)

        return wrapper

    return decorator
