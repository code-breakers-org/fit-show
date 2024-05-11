from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.user.api.v1.serializers import ProfileCreateSerializer
from apps.user.models import Profile


class ProfileCreate(generics.CreateAPIView):
    serializer_class = ProfileCreateSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    lookup_field = "user_id"
    serializer_class = ProfileCreateSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
