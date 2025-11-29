import pytest

from ..services import OTPService
from rest_framework.test import APIClient


class TestOTPServices:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    def test_check_otp(self, otp_fixture, otp, hash_otp):
        assert True == OTPService.check_otp(
            otp_fixture, otp, hash_otp
        )

    def test_verify_otp(self, otp_fixture):
        assert OTPService.verify_otp(otp_fixture, "789000") == True
