import pytest
from ..services import OTPService

class TestOTPServices:
    def test_check_otp(self, OTP_fixture, otp, hash_otp):
        assert True == OTPService.check_otp(OTP_fixture, otp, hash_otp)
        
    def test_verify_otp(self, OTP_fixture):
        assert OTPService.verify_otp(OTP_fixture, '789000') == True