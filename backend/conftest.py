from __future__ import annotations

import os
import sys
import django

import pytest
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile
from typing import Literal

# Get the absolute path to the backend directory
BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))

# Add parent directory so 'backend' package is importable
PARENT_DIR = os.path.dirname(BACKEND_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

# Setup Django before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# pylint: disable=import-outside-toplevel
# pylint: disable=redefined-outer-name


@pytest.fixture
def account_fixture(db):
    from account.models import Account

    return Account.objects.create_superuser(
        username="admin_user",
        email="test_mail_1@mail.com",
        bio="fixture bio.",
        password="admin_user",
    )


@pytest.fixture
def account_fixture_2(db):
    from account.models import Account

    return Account.objects.create_user(
        username="general_user",
        email="test_mail_2@mail.com",
        bio="fixture bio.",
        password="general_user",
    )


@pytest.fixture
def otp_fixture(db, account_fixture):
    from otp.models import OTP
    from otp.services import OTPService

    return OTP.objects.create(
        user=account_fixture, hash_otp=OTPService.hash_otp("789000")
    )


@pytest.fixture
def otp():
    return "123456"


@pytest.fixture
def hash_otp(otp: Literal["123456"]):
    return make_password(otp)


@pytest.fixture
def user_photo(account_fixture):
    from photo.models import UserPhoto

    image = SimpleUploadedFile(
        name="test_image.jpg",
        content=b"fake image content",
        content_type="image/jpeg",
    )

    return UserPhoto.objects.create(
        user=account_fixture, image=image, photo_type="avatar"
    )
