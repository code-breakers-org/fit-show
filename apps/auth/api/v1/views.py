from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.auth.api.v1.serializers import (
    UserSignUpSerializer,
    SendVerificationSerializer,
    VerifyVerificationSerializer,
    ForgotPasswordSerializer,
)
from apps.core.enums import UserVerificationStatus
from apps.core.responses import CreateResponse, UpdateResponse, SuccessResponse
from apps.user.models import UserVerification, User


class SignupView(APIView):
    serializer_class = UserSignUpSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        serializer: UserSignUpSerializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        phone_number = serializer.validated_data.get("phone_number")
        UserVerification.objects.filter(phone_number=phone_number).delete()
        return CreateResponse(message="User created", data=serializer.data)


class SendVerificationCodeView(CreateAPIView):
    serializer_class = SendVerificationSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    queryset = UserVerification.objects.all()

    def perform_create(self, serializer: SendVerificationSerializer):
        phone_number = serializer.validated_data.get("phone_number")
        user_verification_qs = self.queryset.filter(phone_number=phone_number)

        if user_verification_qs.exists():
            user_verification_qs.delete()

        user_verification: UserVerification = serializer.save()
        user_verification.send_verification_code()


class VerifyVerificationCodeView(APIView):
    serializer_class = VerifyVerificationSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def put(self, request: Request):
        serializer: VerifyVerificationSerializer = self.serializer_class(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get("phone_number")
        UserVerification.objects.filter(phone_number=phone_number).update(
            status=UserVerificationStatus.VERIFIED
        )
        return UpdateResponse(message="Verification code validated")


class ForgetPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def post(self, request: Request):
        serializer: ForgotPasswordSerializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(message="New password has been sent")
