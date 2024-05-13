import magic
from django.core.files import File
from django.db import models


class MediaManager(models.Manager):
    def create(self, **extra_fields):
        file: File = extra_fields.get("file")
        extra_fields["mime_type"] = magic.from_buffer(file.read(1024), mime=True)
        media = self.model(**extra_fields)
        media.save()
        return media
