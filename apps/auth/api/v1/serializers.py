from rest_framework import serializers

from apps.user.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone_number", "type", "name", "password"]
        extra_kwargs = {"password": {"write_only": True, "required": True}}
