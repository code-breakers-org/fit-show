import logging
import uuid
from http import HTTPStatus

from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from apps.core.responses import ErrorResponse, Response

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
    if isinstance(exc,ValidationError):
        return Response(data=exc.message_dict,status=HTTPStatus.BAD_REQUEST)

    exc_id: str = str(uuid.uuid4())
    response = exception_handler(exc, context)
    if response is None:
        logger.exception(
            f"ID: {exc_id} | message -> Unexpected Exception | class Name -> {exc.__class__.__name__}",
            exc_info=exc,
        )
        error_message = "Something went wrong, Please try again."
        if settings.DEBUG:
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
    """
    This exception is raised when the maximum number of attempts is exceeded. This can occur in situations like:
        Requesting a password change with a date and time restriction. For example, if you are only allowed to request a
         password change once per day.
        Sending a verification code when the expiration date hasn't passed. This means you've already requested a code
        within the valid timeframe and need to wait before trying again.
    DON'T USE THIS EXCEPTION FOR RATE LIMITS EXCEPTIONS
    """
    def __init__(
            self,
            error_message="You have been exceeded the maximum limitation",
            error_data=None,
            **kwargs,
    ):
        super().__init__(
            error_message=error_message,
            error_data=error_data,
            **kwargs
        )


class ErrorException(CustomAPIException):
    ...


class NotFoundException(CustomAPIException):
    def __init__(
            self,
            error_message="Not Found",
            error_data=None,
            **kwargs,
    ):
        super().__init__(
            error_message=error_message,
            error_data=error_data,
            status_code=HTTPStatus.NOT_FOUND,
            **kwargs
        )
