from django.urls import path

from apps.user.api.v1 import views

urlpatterns = [
    path("profile/", views.ProfileCreate.as_view(), name="profile-create"),
    path(
        "profile/<user_id>/",
        views.ProfileDetail.as_view(),
        name="profile-detail",
    ),
]
