import uuid
from datetime import timedelta

import pytest
from django.http import Http404
from django.utils import timezone

from account.models import Account
from core.settings import OTP_RETENTION_DAYS


@pytest.mark.django_db
class TestAccountManager:
    def test_create_user_requires_email(self):
        with pytest.raises(ValueError):
            Account.objects.create_user(
                username="no_email", email=None, password="pwd"
            )

    def test_create_superuser_sets_flags_and_password(self):
        user = Account.objects.create_superuser(
            username="admin", email="admin@example.com", password="secret"
        )

        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.email == "admin@example.com"
        assert user.username == "admin"
        assert user.check_password("secret") is True

    def test_get_user_by_public_id(self, account_fixture):
        found = Account.objects.get_user_by_public_id(account_fixture.public_id)

        assert found == account_fixture

    def test_get_user_by_public_id_missing_raises(self):
        with pytest.raises(Http404):
            Account.objects.get_user_by_public_id(uuid.uuid4())


@pytest.mark.django_db
class TestAccountModel:
    def test_str_returns_username(self, account_fixture):
        assert str(account_fixture) == account_fixture.username

    def test_is_time_to_clean_otp_true_when_older_than_retention(self, account_fixture):
        account_fixture._last_otp_clean = timezone.now() - timedelta(
            days=OTP_RETENTION_DAYS + 1
        )

        assert account_fixture.is_time_to_clean_otp is True

    def test_is_time_to_clean_otp_false_when_within_retention(self, account_fixture):
        account_fixture._last_otp_clean = timezone.now() - timedelta(hours=1)

        assert account_fixture.is_time_to_clean_otp is False
