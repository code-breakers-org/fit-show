from rest_framework import serializers

from apps.user.models import User, UserVerification


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone_number", "type", "name", "password"]
        extra_kwargs = {"password": {"write_only": True, "required": True}}


class SendVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerification
        fields = ["phone_number"]
