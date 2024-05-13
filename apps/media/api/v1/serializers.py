from rest_framework import serializers

from apps.media.models import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ("id", "file", "alt", "mime_type")
        extra_kwargs = {
            "file": {
                "required": True,
            },
            "id": {"read_only": True},
            "mime_type": {"read_only": True},
        }
