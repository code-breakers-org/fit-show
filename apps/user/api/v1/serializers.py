from rest_framework import serializers

from apps.user.models import Profile


class ProfileCreateSerializer(serializers.ModelSerializer):
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
