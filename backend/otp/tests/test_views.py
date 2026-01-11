import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestOTPViews:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    def test_create_anonymous_code(self):
        url = reverse("otp:main-otp")
        data = {
            "from_addr": "test_mail_1@mail.com",
            "to_addr": "recepient@gmail.com",
        }

        response = self.client.post(url, data)
        print(f"=== Response Data: {response.json()} ===")
        assert response.status_code == 200

    def test_create_user_code(self, account_fixture):
        from otp.models import OTP

        self.client.force_authenticate(user=account_fixture)
        url = reverse("otp:main-otp")
        data = {
            "from_addr": "test_mail_1@mail.com",
            "to_addr": "recepient@gmail.com",
        }

        response = self.client.post(url, data)

        assert response.status_code == 200
        assert OTP.objects.get(user=account_fixture) is not None
