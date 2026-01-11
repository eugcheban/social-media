import logging
import random
import string
from typing import Optional

from core.settings import (
    COMPANY_CONTACT_INFORMATION,
    COMPANY_EMAIL,
    COMPANY_NAME,
    OTP_LENGTH,
)
from django.contrib.auth.hashers import check_password, make_password
from django.db import DatabaseError, IntegrityError, transaction
from django.utils import timezone
from smtp_client import send_email

from .models import OTP

logger = logging.getLogger(__name__)

class OTPService:
    @staticmethod
    def hash_otp(otp):
        return make_password(otp)

    @staticmethod
    def check_otp(otp_instance, otp, hash_otp):
        checked = check_password(otp, hash_otp)

        if checked and otp_instance.used_at is None:
            try:
                otp_instance.used_at = timezone.now()
                otp_instance.save(update_fields=["used_at"])
                return True
            except DatabaseError as e:
                logger.error(f"Failed to mark OTP as used: {e}")
                return False

        return False

    @staticmethod
    def verify_otp(otp_instance, otp):
        return check_password(otp, otp_instance.hash_otp)

    @staticmethod
    def generate_code(user: Optional[object] = None):
        code = "".join(random.choices(string.digits, k=OTP_LENGTH))
        
        try:
            with transaction.atomic():
                otp = OTP(
                    user=user or None,
                    hash_otp=OTPService.hash_otp(code),
                )
                otp.save()
            return otp, code

        except IntegrityError as e:
            logger.error(f"Database integrity error generating OTP: {e}")
            return False, {"error": f"Database integrity error:: {e}"}

        except DatabaseError as e:
            logger.error(f"Database error generating OTP: {e}")
            return False, {"error": f"Database error:: {e}"}

        except Exception as e:
            logger.error(f"Unexpected error generating OTP: {e}")
            return False, {"error": f"Unexpected server error:: {e}"}
        

    @staticmethod
    def send_email_otp(user, email):
        otp = OTPService.generate_code(user=user)
        
        response = send_email(
            from_addr=COMPANY_EMAIL,
            to_addr=email,
            msg=f"""Dear {user.username},

            We received a request to reset your email for your account. Please use the one-time password (OTP) below to verify your identity:

            Your OTP: {otp[1]}

            This OTP will expire in 10 minutes. Please do not share this code with anyone.

            If you did not request an email reset, please ignore this message.

            Thank you!

            Best regards,
            {COMPANY_NAME}
            {COMPANY_CONTACT_INFORMATION}
            """
        )
        
        return response, otp
    