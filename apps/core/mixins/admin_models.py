from django.contrib import admin


class CustomAdminModelMixin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
