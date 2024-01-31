from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.auth.api.v1.serializers import UserSignUpSerializer
from apps.core.responses import CreateResponse


class SignupView(APIView):
    serializer_class = UserSignUpSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        serializer: UserSignUpSerializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CreateResponse(message="User created", data=serializer.data)
