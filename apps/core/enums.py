from django.db import models
from django.utils.translation import gettext_lazy as _


class UserType(models.TextChoices):
    COACH = "coach", _("Coach")
    ATHLETE = "athlete", _("Athlete")
    ADMIN = "admin", _("Admin")


class UserVerificationStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    VERIFIED = "verified", _("Verified")

class UserMediaType(models.TextChoices):
    AVATAR='avatar',_('avatar')
    USER_BODY='user_body',_('exercise')
    LICENCE='licence',_('licence')

class UserBodySide(models.TextChoices):
    FRONT='front',_('front')
    BACK='back',_('back')
    LEFT='left',_('left')
    RIGHT='right',_('right')