from account.models import Account
from django.db import IntegrityError, transaction
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from smtp_client import send_email

from .models import OTP
from .serializers import OTPSerializer
from .services import OTPService


class OTPViewsSet(APIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer

    def post(self, request):
        user = request.user
        account_user = Account.objects.filter(id=user.id).first()
        from_addr = request.data.get("from_addr")
        to_addr = request.data.get("to_addr")
        code_otp = OTPService.generate_code()
        try:
            with transaction.atomic():
                otp_code = OTP(
                    user=account_user or None,
                    hash_otp=OTPService.hash_otp(code_otp),
                )
                otp_code.save()

        except IntegrityError:
            return Response(
                {"error": "Database integrity error"}, status=500
            )

        except Exception:
            return Response(
                {"error": "Unexpected server error"}, status=500
            )

        if send_email(
            from_addr=from_addr,
            to_addr=to_addr,
            msg=f"Your OTP code for authentication is {code_otp}",
        ):
            return Response(
                data={
                    "uuid": otp_code.code_uuid,
                }
            )
        else:
            return Response(
                data={"msg": "Error while sending email!"}, status=500
            )

    def get(self, request):
        user = request.user
        code_uuid = request.query_params.get("pk")
        otp = requests.query_params.get("otp")

        # clear old codes
        if user.is_time_to_clean_otp:
            otps = OTP.object.filter(user=request.user).all()

            for otp in otps:
                if not otp.is_valid:
                    otp.delete()

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
