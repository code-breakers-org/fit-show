from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.auth.api.v1.views import (
    SignupView,
    SendVerificationCodeView,
    VerifyVerificationCodeView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/", TokenObtainPairView.as_view(), name="signin"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "otp/send",
        SendVerificationCodeView.as_view(),
        name="send_otp",
    ),
    path(
        "otp/verify",
        VerifyVerificationCodeView.as_view(),
        name="verify_otp",
    ),
]
