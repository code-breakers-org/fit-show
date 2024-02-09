import logging
from functools import wraps

from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)


def log_sms_info(function):
    @wraps(function)
    def wrap(self, *args, **kwargs):
        to = str(kwargs.get("to"))
        message = kwargs.get("message")
        logger.info(msg=f"Sms has been sent to {to} with this message: {message} ")
        return function(self, *args, **kwargs)

    return wrap
