from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.core.exceptions import NotFoundException
from apps.core.mixins.views import UpsertAndRetrieveViewSet
from apps.core.responses import RetrieveResponse
from apps.user.api.v1.serializers import (
    ProfileSerializer,
    UserSerializer,
    AvatarSerializer,
)
from apps.user.models import Profile


class ProfileViewSet(UpsertAndRetrieveViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            user = self.request.user
            qs_object = self.queryset.get(user_id=user.id)
            return qs_object
        except:
            raise NotFoundException()


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return RetrieveResponse(data=serializer.data)


class UserMediaUploadView(generics.CreateAPIView):
    serializer_class = AvatarSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]


class AvatarView(UserMediaUploadView):
    pass
