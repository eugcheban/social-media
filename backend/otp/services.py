import random
import string

from core.settings import OTP_LENGTH, COMPANY_EMAIL, COMPANY_CONTACT_INFORMATION, COMPANY_NAME
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from smtp_client import send_email
from django.db import IntegrityError, transaction
from .models import OTP


class OTPService:
    @staticmethod
    def hash_otp(otp):
        return make_password(otp)

    @staticmethod
    def check_otp(otp_instance, otp, hash_otp):
        checked = check_password(otp, hash_otp)

        if checked and otp_instance.used_at is None:
            otp_instance.used_at = timezone.now()
            return True

        return False

    @staticmethod
    def verify_otp(otp_instance, otp):
        return check_password(otp, otp_instance.hash_otp)

    @staticmethod
    def generate_code(user):
        code = "".join(random.choices(string.digits, k=OTP_LENGTH))
        
        try:
            with transaction.atomic():
                otp = OTP(
                    user=user or None,
                    hash_otp=OTPService.hash_otp(code),
                )
                otp.save()

        except IntegrityError:
            return False, {"error": "Database integrity error"}

        except Exception:
            return False, {"error": "Unexpected server error"}
        
        return True, code

    @staticmethod
    def send_otp(user, email):
        
        response = send_email(
            COMPANY_EMAIL,
            email,
            f"""Dear {user.username},

            We received a request to reset your email for your account. Please use the one-time password (OTP) below to verify your identity:

            Your OTP: {}

            This OTP will expire in 10 minutes. Please do not share this code with anyone.

            If you did not request an email reset, please ignore this message.

            Thank you!

            Best regards,
            {COMPANY_NAME}
            {COMPANY_CONTACT_INFORMATION}
            """
        )