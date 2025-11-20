from __future__ import annotations
import sys
import os
import django


from django.contrib.auth.hashers import make_password, check_password
import pytest

# Get the absolute path to the backend directory
BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))

# Add backend directory to PYTHONPATH (if not already there)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

@pytest.fixture
def Account_fixture(db):
    from account.models import Account
    return Account.objects.create(
        email='test_fixture@mail.com',
        bio="fixture bio."
    )

@pytest.fixture
def OTP_fixture(db, Account_fixture):
    from otp.models import OTP
    from otp.services import OTPService
    
    return OTP.objects.create(
        user=Account_fixture,
        hash_otp=OTPService.hash_otp('789000')
    )
    
@pytest.fixture
def otp():
    return "123456"

@pytest.fixture
def hash_otp(otp):
    return make_password(otp)

