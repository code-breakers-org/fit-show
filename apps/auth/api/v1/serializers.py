import django.contrib.auth.password_validation as validators
from django.utils import timezone
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.core.enums import UserVerificationStatus
from apps.core.exceptions import DataInvalidException
from apps.core.utils import generate_random_string
from apps.notifications.strategies.strategies import SmsPasswordStrategy
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


class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(max_length=13)

    def validate(self, attrs: dict):
        phone_number = attrs.get("phone_number")
        user_qs = User.objects.filter(phone_number=phone_number)
        if not user_qs.exists():
            raise DataInvalidException("User does not exist")
        return attrs

    def save(self, **kwargs):
        phone_number = self.validated_data.get("phone_number")
        user_qs = User.objects.filter(phone_number=phone_number)
        user: User = user_qs.first()
        new_password: str = generate_random_string(8)
        user.set_password(new_password)
        user.save(update_fields=["password"], force_update=True)
        user.notification_context.strategy = SmsPasswordStrategy()
        user.notify_by_phone_number(message=new_password)
