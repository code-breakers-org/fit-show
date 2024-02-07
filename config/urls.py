from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

admin_urlpatterns = [
    path("admin/", admin.site.urls),
]

api_docs_urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="docs",
    ),
    path(
        "api/docs/detail",
        SpectacularRedocView.as_view(url_name="schema"),
        name="docs-detail",
    ),
]

v1_urlpatterns = [
    path("api/v1/auth/", include("apps.auth.api.v1.urls")),
]

urlpatterns = [] + api_docs_urlpatterns + v1_urlpatterns + admin_urlpatterns


handler500 = "apps.core.exceptions.server_error"
