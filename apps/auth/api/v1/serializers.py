from rest_framework import serializers

from apps.user.models import User, UserVerification


class UserSignUpSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict):
        phone_number = validated_data.pop("phone_number")
        password = validated_data.pop("password")
        user: User = User.objects.create_user(
            phone_number=phone_number, password=password, **validated_data
        )
        return user

    class Meta:
        model = User
        fields = ["id", "phone_number", "type", "name", "password"]
        extra_kwargs = {"password": {"write_only": True, "required": True}}


class SendVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerification
        fields = ["phone_number"]
