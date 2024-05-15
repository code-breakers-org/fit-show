from django.urls import path

from apps.core.mixins.routers import SimpleRouterWithoutLookup
from apps.user.api.v1 import views

router = SimpleRouterWithoutLookup()
router.register(r"profile", views.ProfileViewSet)

urlpatterns = [
    path("avatar/", views.AvatarView.as_view(), name="upload-avatar"),
    path("me/", views.CurrentUserView.as_view(), name="current-user"),
]

urlpatterns = urlpatterns + router.urls
