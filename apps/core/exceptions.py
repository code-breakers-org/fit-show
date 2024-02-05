import logging
import uuid

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from apps.core.responses import ErrorResponse
from config.envs import DEBUG

logger = logging.getLogger(settings.LOGGER_NAME)


def server_error(request, *args, **kwargs):
    return ErrorResponse(
        message="Something went wrong, Please try again.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


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
        error_message = "Something went wrong, Please try again."
        if DEBUG:
            error_message = f"Error ID :{exc_id} | {exc}"
        return ErrorResponse(
            message=error_message,
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


class DataInvalidException(CustomAPIException):
    ...


class MaximumLimitException(CustomAPIException):
    ...


class ErrorException(CustomAPIException):
    ...
