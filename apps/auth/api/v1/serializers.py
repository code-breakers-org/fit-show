import django.contrib.auth.password_validation as validators
from django.utils import timezone
from rest_framework import serializers

from apps.core.enums import UserVerificationStatus
from apps.core.exceptions import DataInvalidException
from apps.user.models import User, UserVerification


class UserSignUpSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        try:
            validators.validate_password(value)
        except serializers.ValidationError as e:
            raise DataInvalidException(str(e))
        return value

    def validate(self, attrs: dict):
        phone_number = attrs.get("phone_number")
        user_verification = UserVerification.objects.filter(
            phone_number=phone_number,
            status__exact=UserVerificationStatus.VERIFIED,
        )
        if not user_verification.exists():
            raise DataInvalidException("You should verify your phone number first.")
        attrs["is_active"] = True
        return attrs

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
    def validate(self, attrs: dict):
        phone_number = attrs.get("phone_number")
        user_verification = UserVerification.objects.filter(
            phone_number=phone_number,
            status__exact=UserVerificationStatus.PENDING,
            expire_on__gt=timezone.now(),
        )

        if user_verification.exists():
            expire_on = user_verification.first().expire_on
            remaining_time = expire_on - timezone.now()
            total_seconds = remaining_time.total_seconds()
            raise DataInvalidException(
                "You can't send verification",
                {
                    "remaining_total_seconds": total_seconds,
                },
            )
        return attrs

    class Meta:
        model = UserVerification
        fields = ["phone_number", "expire_on"]
        extra_kwargs = {"expire_on": {"read_only": True}}


class VerifyVerificationSerializer(serializers.ModelSerializer):
    def validate(self, attrs: dict):
        phone_number = attrs.get("phone_number")
        code = attrs.get("code")
        user_verification = UserVerification.objects.filter(
            phone_number=phone_number,
            code=code,
            status__exact=UserVerificationStatus.PENDING,
            expire_on__gt=timezone.now(),
        )
        if not user_verification.exists():
            raise DataInvalidException("Verification code is not valid")
        return attrs

    class Meta:
        model = UserVerification
        fields = ["phone_number", "code"]


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number"]
