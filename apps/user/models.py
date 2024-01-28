import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.enums import UserType
from apps.core.mixins.models import CustomBaseModel, SoftDeleteMixin


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):

        if not phone_number:
            raise ValueError(_("The phone number must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        # TODO set referral percent based on admin setting
        if not user.is_superuser:
            user.referral_percent = 10

        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("name", "Superuser")
        extra_fields.setdefault("type", UserType.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, CustomBaseModel, SoftDeleteMixin, PermissionsMixin):
    phone_number = PhoneNumberField(max_length=13)
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
        constraints = [
            models.UniqueConstraint(
                fields=["phone_number"],
                condition=Q(deleted_at=None),
                name="phone_number_if_not_deleted_uniqueness",
                violation_error_message="Given phone number already exist",
            ),
        ]
        db_table = "user"
        app_label = "user"
