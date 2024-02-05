from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.auth.api.v1.views import SignupView, SendVerificationCodeView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/", TokenObtainPairView.as_view(), name="signin"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "verificatation/send",
        SendVerificationCodeView.as_view(),
        name="send_verification_code",
    ),
]
