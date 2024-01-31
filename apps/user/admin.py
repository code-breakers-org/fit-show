from django.contrib import admin
from django.contrib.auth.admin import (
    UserAdmin,
)
from django.utils.translation import gettext_lazy as _

from apps.core.mixins.admin_models import CustomAdminModelMixin
from apps.user.models import User


@admin.register(User)
class UserAdminConfigMixin(UserAdmin, CustomAdminModelMixin):
    ordering = ["-created_at"]
    list_display = [
        "id",
        "phone_number",
        "name",
        "type",
        "is_staff",
        "is_active",
        "created_at",
    ]
    search_fields = (
        "phone_number",
        "name",
    )
    search_help_text = "Search by phone number or name"

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("General info"), {"fields": ("name", "type", "last_login")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
