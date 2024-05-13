from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.mixins.models import CustomBaseModel
from apps.core.utils import get_file_name
from apps.media.manager import MediaManager


class Media(CustomBaseModel):
    file = models.FileField(
        upload_to=get_file_name,
        null=False,
        blank=False,
    )
    alt = models.CharField(max_length=250, blank=True, null=True)
    mime_type = models.CharField(
        max_length=250,
        null=False,
        blank=False,
    )
    objects = MediaManager()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.id}-{self.mime_type}"

    class Meta:
        verbose_name = _("media")
        verbose_name_plural = _("medias")
        get_latest_by = "created_at"
        ordering = ["-created_at"]
        db_table = "media"
        app_label = "media"
