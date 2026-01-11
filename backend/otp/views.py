import logging

from account.models import Account
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, IntegrityError, transaction
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from smtp_client import send_email

from .models import OTP
from .serializers import OTPSerializer
from .services import OTPService

logger = logging.getLogger(__name__)


class OTPViewsSet(APIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer

    def post(self, request):
        user = request.user
        account_user = Account.objects.filter(id=user.id).first()
        from_addr = request.data.get("from_addr")
        to_addr = request.data.get("to_addr")
        otp = OTPService.generate_code(user=account_user)

        if send_email(
            from_addr=from_addr,
            to_addr=to_addr,
            msg=f"Your OTP code for authentication is {otp[1]}",
        ):
            return Response(
                data={
                    "uuid": otp[0].code_uuid,
                }
            )
        else:
            return Response(
                data={"msg": "Error while sending email!"}, status=500
            )

    def get(self, request):
        user = request.user
        code_uuid = request.query_params.get("pk")
        otp = request.query_params.get("otp")

        # clear old codes
        if user.is_time_to_clean_otp:
            try:
                otps = OTP.objects.filter(user=request.user).all()

                for otp_item in otps:
                    if not otp_item.is_valid:
                        otp_item.delete()
            except DatabaseError as e:
                logger.warning(f"Failed to clean old OTPs for user {user.id}: {e}")

        try:
            otp_instance = OTP.objects.get(code_uuid=code_uuid)
            hash_otp = otp_instance.hash_otp

            return Response(
                data={
                    "validation": OTPService.check_otp(
                        otp_instance, otp, hash_otp
                    )
                },
                status=200,
            )
        except ObjectDoesNotExist:
            logger.error(f"OTP with code_uuid {code_uuid} not found")
            return Response(
                data={"error": "OTP not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except DatabaseError as e:
            logger.error(f"Database error validating OTP: {e}")
            return Response(
                data={"error": "Failed to validate OTP"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
