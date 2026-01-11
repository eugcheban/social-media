from datetime import timedelta

import pytest
from django.utils import timezone

from core.settings import OTP_DELTA
from otp.models import OTP


@pytest.mark.django_db
def test_is_valid_true_for_unused_and_unexpired(account_fixture):
    otp = OTP.objects.create(
        user=account_fixture,
        hash_otp="hashed",
        expires_at=timezone.now() + timedelta(minutes=5),
    )

    assert otp.is_valid is True


@pytest.mark.django_db
def test_is_valid_false_when_expired(account_fixture):
    otp = OTP.objects.create(
        user=account_fixture,
        hash_otp="hashed",
        expires_at=timezone.now() - timedelta(minutes=1),
    )

    assert otp.is_valid is False


@pytest.mark.django_db
def test_is_valid_false_when_used(account_fixture):
    otp = OTP.objects.create(
        user=account_fixture,
        hash_otp="hashed",
        expires_at=timezone.now() + timedelta(minutes=5),
        used_at=timezone.now(),
    )

    assert otp.is_valid is False


@pytest.mark.django_db
def test_default_expires_at_uses_delta(account_fixture):
    before = timezone.now()
    otp = OTP.objects.create(user=account_fixture, hash_otp="hashed")
    after = timezone.now()

    expected = before + OTP_DELTA
    assert abs((otp.expires_at - expected).total_seconds()) < 5
    assert otp.expires_at > before
    assert otp.expires_at < after + OTP_DELTA
