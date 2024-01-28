import uuid

from django.db import models
from django.utils import timezone


class CustomBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     try:
    #         self.full_clean()
    #         super().save(*args, **kwargs)
    #     except ValidationError as e:
    #         raise ValidationError(", ".join(e.message_dict[NON_FIELD_ERRORS]))

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
