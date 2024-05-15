from django.core.files import File
from rest_framework import serializers

from apps.core.enums import UserMediaType
from apps.core.validators import FileValidator
from apps.media.api.v1.serializers import MediaSerializer
from apps.media.models import Media
from apps.user.models import Profile, User, UserMedia
from config import settings


class ProfileSerializer(serializers.ModelSerializer):
    def validate(self, attrs: dict):
        user = self.context.get("request").user
        attrs["user"] = user
        return attrs

    class Meta:
        model = Profile
        fields = [
            "gender",
            "bank_account_number",
            "iban",
            "email",
            "address",
            "user_id",
        ]
        extra_kwargs = {
            "gender": {"required": True},
            "bank_account_number": {"required": True},
            "iban": {"required": True},
            "user_id": {"read_only": True},
        }


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    media = MediaSerializer(source="usermedia_set", many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "type",
            "name",
            "profile",
            "media",
        )


class UserMediaSerializer(serializers.ModelSerializer):

    file = serializers.FileField(
        write_only=True,
    )
    media = MediaSerializer(
        read_only=True,
    )

    alt = serializers.CharField(
        write_only=True,
        required=False,
    )

    def max_file_size(self):
        return settings.MAX_FILE_SIZE_MB

    def allowed_extensions(self):
        return settings.ACCEPTABLE_MEDIA_TYPE

    def validate_file(self, value: File):
        FileValidator(
            allowed_extensions=self.allowed_extensions(),
            max_file_size_mega_bit=self.max_file_size(),
        )(value),
        return value

    class Meta:
        model = UserMedia
        fields = ("id", "type", "body_side", "file", "user_id", "media", "alt")
        extra_kwargs = {
            "body_side": {
                "required": False,
            },
            "type": {"read_only": True},
            "user_id": {"read_only": True},
        }

    def create(self, validated_data: dict):
        user = self.context["request"].user
        media_data: File = validated_data.get("file")
        alt = validated_data.get("alt")
        media = Media.objects.create(file=media_data, alt=alt)
        validated_data.pop("file")
        if validated_data.get("alt"):
            validated_data.pop("alt")

        return UserMedia.objects.create(user=user, media=media, **validated_data)


class AvatarSerializer(UserMediaSerializer):
    def create(self, validated_data: dict):
        validated_data["type"] = UserMediaType.AVATAR
        return super().create(validated_data)

    class Meta(UserMediaSerializer.Meta):
        fields = ("id", "type", "file", "user_id", "media", "alt")
        extra_kwargs = {
            "type": {
                "read_only": True,
            },
            "user_id": {"read_only": True},
        }
