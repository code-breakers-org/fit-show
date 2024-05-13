from django.urls import path

from apps.user.api.v1 import views

urlpatterns = [
    path("avatar/", views.AvatarView.as_view(), name="upload-avatar"),
    path("me/", views.CurrentUserView.as_view(), name="current-user"),
    path("profile/", views.ProfileCreateView.as_view(), name="profile-create"),
    path(
        "profile/<user_id>/",
        views.ProfileDetailView.as_view(),
        name="profile-detail",
    ),
]
