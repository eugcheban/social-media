import logging

from django.contrib.auth import get_user_model
from django.db import DatabaseError, IntegrityError
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from otp.models import OTP, PasswordResetSession
from otp.services import OTPService

logger = logging.getLogger(__name__)

from ..serializers.password_serializers import (
    PasswordChangeSerizliser,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    PaswordResetVerifySerializer,
)


class PasswordViewSet(viewsets.GenericViewSet):
    serializer_class = PasswordChangeSerizliser
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="change")
    def change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated successfully"})


class PasswordResetViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "reset":
            return PasswordResetRequestSerializer
        if self.action == "verify":
            return PaswordResetVerifySerializer
        if self.action == "confirm":
            return PasswordResetConfirmSerializer
        return super().get_serializer_class()

    @action(
        detail=False,
        methods=["post"],
        url_path="reset",
    )
    def reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        send_email_response, otp_pair = OTPService.send_email_otp(
            user=user,
            email=serializer.validated_data["email"],
        )

        if not send_email_response:
            return Response(
                {
                    "error": "Internal server error while reseting password!",
                    "email_response": send_email_response,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        otp_instance, _code = otp_pair
        try:
            PasswordResetSession.objects.create(
                email=user.email, otp_hash=otp_instance.hash_otp
            )
        except (DatabaseError, IntegrityError) as e:
            logger.error(f"Failed to create password reset session for {user.email}: {e}")
            return Response(
                {"error": "Failed to create reset session"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"code_uuid": otp_instance.code_uuid}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"], url_path="verify")
    def verify(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code_uuid = serializer.validated_data["code_uuid"]
        otp_value = serializer.validated_data["otp"]

        otp_instance = OTP.objects.filter(code_uuid=code_uuid).first()
        if not otp_instance or not otp_instance.is_valid:
            return Response(
                {"error": "OTP is invalid or expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = PasswordResetSession.objects.filter(
            otp_hash=otp_instance.hash_otp, is_verified=False
        ).order_by("-created_at").first()

        if not session or session.expires_at < timezone.now():
            return Response(
                {"error": "Password reset session expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_valid = OTPService.verify_otp(otp_instance, otp_value)
        if not is_valid:
            return Response(
                {"error": "OTP is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            otp_instance.used_at = timezone.now()
            otp_instance.save(update_fields=["used_at"])
            session.is_verified = True
            session.save(update_fields=["is_verified"])
        except DatabaseError as e:
            logger.error(f"Failed to update OTP/session verification: {e}")
            return Response(
                {"error": "Failed to verify OTP"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"detail": "OTP verified"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="confirm")
    def confirm(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code_uuid = serializer.validated_data["code_uuid"]
        otp_value = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]

        otp_instance = OTP.objects.filter(code_uuid=code_uuid).first()
        if not otp_instance or not otp_instance.is_valid:
            return Response(
                {"error": "OTP is invalid or expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = PasswordResetSession.objects.filter(
            otp_hash=otp_instance.hash_otp
        ).order_by("-created_at").first()

        if not session or session.expires_at < timezone.now():
            return Response(
                {"error": "Password reset session expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not session.is_verified:
            validated = OTPService.verify_otp(otp_instance, otp_value)
            if not validated:
                return Response(
                    {"error": "OTP is incorrect"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            session.is_verified = True
            session.save(update_fields=["is_verified"])

        user_model = get_user_model()
        user = user_model.objects.filter(email=session.email).first()
        if not user:
            return Response(
                {"error": "User not found for this reset request"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            user.set_password(new_password)
            user.save(update_fields=["password"])

            otp_instance.used_at = timezone.now()
            otp_instance.save(update_fields=["used_at"])

            # Blacklist outstanding tokens to force re-authentication
            tokens = OutstandingToken.objects.filter(user=user)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)
        except DatabaseError as e:
            logger.error(f"Failed to reset password for {user.email}: {e}")
            return Response(
                {"error": "Failed to reset password"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Failed to blacklist tokens for {user.email}: {e}")

        return Response(
            {"detail": "Password has been reset"},
            status=status.HTTP_200_OK,
        )
