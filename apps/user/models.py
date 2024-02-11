import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.enums import UserType, UserVerificationStatus
from apps.core.mixins.models import CustomBaseModel
from apps.core.utils import add_date_time_to_now, generate_verification_code
from apps.notifications import (
    NotificationContext,
    SmsStrategy,
    SmsOtpStrategy,
)
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
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    USERNAME_FIELD = "phone_number"
    objects = UserManager()

    # FIXME: dependency injection to prevent coupling and consider defining it in a common base class or mixin to
    #  avoid duplication.
    notification_context = NotificationContext(SmsStrategy())

    def __str__(self):
        return f"{self.phone_number}"

    def notify_by_phone_number(self, message: str):
        self.notification_context.send(receiver=self.phone_number, message=message)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        get_latest_by = "created_at"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["phone_number"], name="user_phone_number_idx"),
        ]

        db_table = "user"
        app_label = "user"


class UserVerification(CustomBaseModel):
    phone_number = PhoneNumberField(max_length=13)
    expire_on = models.DateTimeField()
    code = models.IntegerField()
    notification_context = NotificationContext(SmsOtpStrategy())
    status = models.CharField(
        max_length=10,
        choices=UserVerificationStatus.choices,
        default=UserVerificationStatus.PENDING,
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.expire_on = add_date_time_to_now(minutes=5)
        self.code = generate_verification_code()
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def notify_by_phone_number(self, message: str):
        self.notification_context.send(to=self.phone_number, message=message)

    def send_verification_code(self):
        self.notify_by_phone_number(str(self.code))

    # FIXME Explore using a more descriptive string, potentially including other relevant fields.
    def __str__(self):
        return f"{self.phone_number}"

    class Meta:
        verbose_name = _("user_verification")
        verbose_name_plural = _("users_verification")
        get_latest_by = "created_at"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["phone_number"], name="phone_number_verification_idx"),
        ]

        db_table = "user_verification"
        app_label = "user"
