from django.contrib import admin, messages
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS


class CustomAdminModelMixin(admin.ModelAdmin):
    save_on_top = True
    save_as = True

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
            super(self).save_model(request, obj, form, change)
        except ValidationError as e:
            raise ValidationError(", ".join(e.message_dict[NON_FIELD_ERRORS]))

    def add_view(self, request, form_url="", extra_context=None):
        try:
            return super(CustomAdminModelMixin, self).add_view(
                request, form_url, extra_context
            )
        except ValidationError as e:
            error_message = e.message if hasattr(e, "message") else str(e)
            request.method = "GET"
            messages.error(request, error_message)
            return super(CustomAdminModelMixin, self).add_view(
                request, form_url, extra_context
            )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        try:
            return super(CustomAdminModelMixin, self).change_view(
                request, object_id, form_url, extra_context
            )
        except ValidationError as e:
            error_message = e.message if hasattr(e, "message") else str(e)
            request.method = "GET"
            messages.error(request, error_message)
            return super(CustomAdminModelMixin, self).change_view(
                request, object_id, form_url, extra_context
            )
