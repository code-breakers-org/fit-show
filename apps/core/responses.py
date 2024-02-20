from collections import OrderedDict

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response


class ResponseSerializer(serializers.Serializer):
    """To be used on Swagger schema extending purposes"""

    status = serializers.IntegerField(min_value=100, max_value=599, read_only=True)
    message = serializers.CharField(read_only=True)
    result = serializers.SerializerMethodField(read_only=True, source="get_result")

    def get_result(self, obj) -> list | dict | None:
        return None


class CustomResponse(Response):
    default_status_code = status.HTTP_200_OK
    default_response_message = None

    def __init__(
        self,
        *,
        message=None,
        data=None,
        status_code=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None
    ):

        if message is None:
            self.message = self.default_response_message
        else:
            self.message = message

        if status_code is None:
            self.status_code = self.default_status_code
        else:
            self.status_code = status_code

        super().__init__(
            status=status_code,
            data=data,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )

        # JSON OUTPUT
        self.data = OrderedDict()
        self.data.update(
            {
                "status": self.status_code,
                "message": message,
                "result": data,
            }
        )

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.data


class CreateResponse(CustomResponse):
    default_status_code = status.HTTP_201_CREATED
    default_response_message = "Record created successfully"


class ListResponse(CustomResponse):
    default_status_code = status.HTTP_200_OK
    default_response_message = "Record listed"


class RetrieveResponse(CustomResponse):
    default_status_code = status.HTTP_200_OK
    default_response_message = "Record retrieved"


class UpdateResponse(CustomResponse):
    default_status_code = status.HTTP_200_OK
    default_response_message = "Record updated successfully"


class DeleteResponse(CustomResponse):
    default_status_code = status.HTTP_204_NO_CONTENT
    default_response_message = "Record deleted successfully"


class SuccessResponse(CustomResponse):
    default_status_code = status.HTTP_200_OK
    default_response_message = "Success response"


class ErrorResponse(CustomResponse):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_response_message = "Error response"
