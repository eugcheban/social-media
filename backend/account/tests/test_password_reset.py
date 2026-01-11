from datetime import timedelta

import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from otp.models import OTP, PasswordResetSession
from otp.services import OTPService


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_reset_creates_session_and_returns_code_uuid(api_client, account_fixture, monkeypatch):
    otp = OTP.objects.create(
        user=account_fixture,
        hash_otp=make_password("123456"),
        expires_at=timezone.now() + timedelta(minutes=10),
    )

    def fake_send_email_otp(user, email):
        return True, (otp, "123456")

    monkeypatch.setattr(OTPService, "send_email_otp", fake_send_email_otp)

    url = reverse("account:password-reset-request")
    response = api_client.post(url, {"email": account_fixture.email})

    assert response.status_code == 200
    assert str(response.data["code_uuid"]) == str(otp.code_uuid)
    assert PasswordResetSession.objects.filter(otp_hash=otp.hash_otp).exists()


@pytest.mark.django_db
def test_verify_marks_session_verified(api_client, account_fixture, monkeypatch):
    code = "654321"
    otp = OTP.objects.create(
        user=account_fixture,
        hash_otp=make_password(code),
        expires_at=timezone.now() + timedelta(minutes=10),
    )
    PasswordResetSession.objects.create(
        email=account_fixture.email,
        otp_hash=otp.hash_otp,
        expires_at=timezone.now() + timedelta(minutes=10),
    )

    url = reverse("account:password-reset-verify")
    response = api_client.post(url, {"code_uuid": otp.code_uuid, "otp": code})

    session = PasswordResetSession.objects.get(otp_hash=otp.hash_otp)
    otp.refresh_from_db()

    assert response.status_code == 200
    assert session.is_verified is True
    assert otp.used_at is not None


@pytest.mark.django_db
def test_confirm_resets_password(api_client, account_fixture, monkeypatch):
    code = "112233"
    otp = OTP.objects.create(
        user=account_fixture,
        hash_otp=make_password(code),
        expires_at=timezone.now() + timedelta(minutes=10),
    )
    PasswordResetSession.objects.create(
        email=account_fixture.email,
        otp_hash=otp.hash_otp,
        expires_at=timezone.now() + timedelta(minutes=10),
        is_verified=True,
    )

    url = reverse("account:password-reset-confirm")
    new_password = "new-secret-pass!42"
    response = api_client.post(
        url,
        {
            "code_uuid": otp.code_uuid,
            "otp": code,
            "new_password": new_password,
        },
    )

    account_fixture.refresh_from_db()
    otp.refresh_from_db()

    assert response.status_code == 200
    assert account_fixture.check_password(new_password) is True
    assert otp.used_at is not None
