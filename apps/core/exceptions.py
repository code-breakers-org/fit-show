import logging
import uuid

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from apps.core.responses import ErrorResponse

logger = logging.getLogger(settings.LOGGER_NAME)


def custom_exception_handler(exc: Exception, context: dict):
    """Custom API exception handler"""

    if isinstance(exc, CustomAPIException):
        return ErrorResponse(
            message=exc.error_message, data=exc.error_data, status_code=exc.status_code
        )

    exc_id: str = str(uuid.uuid4())
    response = exception_handler(exc, context)

    if response is None:
        logger.exception(
            f"ID: {exc_id} | message -> Unexpected Exception | class Name -> {exc.__class__.__name__}",
            exc_info=exc,
        )
        return ErrorResponse(
            message=f"Unexpected Error with error id of {exc_id}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return response


class CustomAPIException(APIException):
    def __init__(
        self,
        error_message="Error",
        error_data=None,
        status_code=status.HTTP_400_BAD_REQUEST,
        **kwargs,
    ):
        self.error_message = error_message
        self.error_data = error_data
        self.status_code = status_code
        super().__init__(**kwargs)


class DataInvalidException(CustomAPIException): ...


class MaximumLimitException(CustomAPIException): ...


class ErrorException(CustomAPIException): ...
