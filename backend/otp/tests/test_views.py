import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestOTPViews:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        
    def test_create(self, Account_fixture):
        url = reverse('otp:main-otp')
        data = {
            'email': 'test_mail_1@mail.com'
        }
        
        response = self.client.post(url, data)
        
        assert response.status_code == 200
        
        # self.client.force_authenticate(user=Account_fixture)