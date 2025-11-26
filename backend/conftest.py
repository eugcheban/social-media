from __future__ import annotations
import sys
import os
import django
from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib.auth.hashers import make_password, check_password
import pytest


# Get the absolute path to the backend directory
BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))

# Add backend directory to PYTHONPATH (if not already there)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

@pytest.fixture
def Account_fixture(db):
    from account.models import Account, AccountManager
    return Account.objects.create_user(
        username='admin_user',
        email='test_mail_1@mail.com',
        bio="fixture bio.",
        password='admin_user'
    )
    
    
@pytest.fixture
def Account_fixture_2(db):
    from account.models import Account, AccountManager
    return Account.objects.create_user(
        username='general_user',
        email='test_mail_2@mail.com',
        bio="fixture bio.",
        password='general_user',
        
    )
    
    # return Account.objects.create(
    #     usernmae='genral_user',
    #     email='test_fixture@mail.com',
    #     bio="fixture bio."
    # )

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

@pytest.fixture
def User_photo(Account_fixture):
    from photo.models import UserPhoto
    
    image = SimpleUploadedFile(
        name="test_image.jpg",
        content=b"fake image content",
        content_type="image/jpeg"
    )
    
    return UserPhoto.objects.create(
        user=Account_fixture,
        image=image,
        photo_type='avatar'
    )