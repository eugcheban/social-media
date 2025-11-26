import string, random
from django.contrib.auth.hashers import make_password, check_password
from core.settings import OTP_LENGTH
from django.utils import timezone

class OTPService:
    @staticmethod
    def hash_otp(otp):
        return make_password(otp)
    
    @staticmethod
    def check_otp(otp_instance, otp, hash_otp):
        checked = check_password(otp, hash_otp)
        
        if checked and otp_instance.used_at == None:
            otp_instance.used_at = timezone.now()
            return True
        
        return False
    
    @staticmethod
    def verify_otp(otp_instance, otp):
        return check_password(otp, otp_instance.hash_otp)
    
    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.digits, k=OTP_LENGTH))
