import pytest
from ..services import OTPService

class TestOTPServices:
    def test_check_otp(self, OTP_fixture, otp, hash_otp):
        assert True == OTPService.check_otp(OTP_fixture, otp, hash_otp)