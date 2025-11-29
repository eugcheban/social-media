import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from account.models import Account


@pytest.mark.django_db
class TestAccountViews:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    def test_list_accounts(self, account_fixture, account_fixture_2):
        self.client.force_authenticate(user=account_fixture)
        keys_to_check = [
            "id",
            "username",
            "email",
            "date_joined",
            "is_active",
            "photos",
        ]

        response = self.client.get("/api/users/")

        assert response.status_code == 200
        assert len(response.json()) == 2
        assert account_fixture.check_password("admin_user")
        assert account_fixture_2.check_password("general_user")
        assert all(key in response.json()[0] for key in keys_to_check)

    def test_create_account(self):
        url = reverse("account:useraccount-list")

        data = {
            "username": "test_user",
            "email": "test_user@mail.com",
            "password": "secure_password",
            # 'first_name': 'Test',
            # 'last_name': 'User',
            "is_active": True,
        }
        response = self.client.post(url, data)

        assert response.status_code == 201
        assert response.json().get("username") == "test_user"
        assert response.json().get("email") == "test_user@mail.com"
        assert response.json().get("is_active") == True
        assert Account.objects.filter(username="test_user").exists()
        assert (
            Account.objects.filter(username="test_user")
            .first()
            .check_password("secure_password")
        )

    # def test_forgot_password(self, Account_fixture):
