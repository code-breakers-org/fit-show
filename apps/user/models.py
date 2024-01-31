import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.enums import UserType
from apps.core.mixins.models import CustomBaseModel
from apps.user.manager import UserManager


class User(AbstractBaseUser, CustomBaseModel, PermissionsMixin):
    phone_number = PhoneNumberField(max_length=13, unique=True)
    type = models.CharField(max_length=16, choices=UserType.choices)
    device_token = models.UUIDField(default=uuid.uuid4)
    referral_code = models.UUIDField(
        default=uuid.uuid4,
    )
    referral_percent = models.FloatField(default=0)
    name = models.CharField(_("first name"), max_length=250)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "phone_number"
    objects = UserManager()

    def __str__(self):
        return f"{self.phone_number}"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        get_latest_by = "created_at"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["phone_number"], name="phone_number_idx"),
        ]

        db_table = "user"
        app_label = "user"
