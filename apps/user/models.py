import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.db.models import UniqueConstraint, Q
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.enums import (
    UserType,
    UserVerificationStatus,
    UserMediaType,
    UserBodySide,
)
from apps.core.mixins.models import CustomBaseModel
from apps.core.utils import add_date_time_to_now, generate_verification_code
from apps.media.models import Media
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
    last_change_password = models.DateTimeField(editable=True, null=True, blank=True)

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
    status = models.CharField(
        max_length=10,
        choices=UserVerificationStatus.choices,
        default=UserVerificationStatus.PENDING,
    )
    notification_context = NotificationContext(SmsOtpStrategy())

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
        self.notification_context.send(receiver=self.phone_number, message=message)

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


class UserMedia(CustomBaseModel):
    type = models.CharField(max_length=16, choices=UserMediaType.choices)
    body_side = models.CharField(max_length=16, choices=UserBodySide.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type}-{self.user},{self.media}"

    class Meta:
        verbose_name = _("user_media")
        verbose_name_plural = _("user_medias")
        get_latest_by = "created_at"
        ordering = ["type"]
        indexes = [
            models.Index(fields=["user"], name="user_idx"),
        ]

        constraints = [
            UniqueConstraint(
                fields=["user", "body_side"],
                condition=Q(body_side__isnull=False),
                name="unique_user_body_side_when_body_side_not_null",
            ),
        ]

        db_table = "user_media"
        app_label = "user"
