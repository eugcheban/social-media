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


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

class Account:
    def __init__(
        self,
        public_id,
        email,
        bio
    ):
        self.public_id = public_id
        self,email = email
        self.bio = bio

    
@pytest.fixture
def otp():
    return "123456"

@pytest.fixture
def hash_otp(otp):
    return make_password(otp)

