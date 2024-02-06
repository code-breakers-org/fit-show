from django.db import models
from django.utils.translation import gettext_lazy as _


class UserType(models.TextChoices):
    COACH = "coach", _("Coach")
    ATHLETE = "athlete", _("Athlete")
    ADMIN = "admin", _("Admin")


class UserVerificationStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    VERIFIED = "verified", _("Verified")
