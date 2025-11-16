import pytest
from ..services import OTPService

class TestOTPServices:
    def test_check_otp(self, otp, hash_otp):
        assert True == OTPService.check_otp(otp, hash_otp)