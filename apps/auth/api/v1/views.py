from rest_framework.views import APIView

from apps.core.responses import CreateResponse
from apps.user.api.v1.serializers import UserSerializer


class SignupView(APIView):
    serializer_class = UserSerializer
    authentication_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CreateResponse(message="User created", data=serializer.data)
