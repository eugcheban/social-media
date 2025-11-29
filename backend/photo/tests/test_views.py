from io import BytesIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from rest_framework.test import APIClient


class TestPhotoViews:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    @staticmethod
    def generate_test_image(
        name="test.jpg", size=(100, 100), color="white"
    ):
        file = BytesIO()
        image = Image.new("RGB", size, color)
        image.save(file, "JPEG")
        file.seek(0)
        return SimpleUploadedFile(
            name=name, content=file.read(), content_type="image/jpeg"
        )

    def test_photo_get(self, user_photo, account_fixture):
        self.client.force_authenticate(user=account_fixture)
        url = reverse("photo:userphoto-list") + "?photo_type=avatar"

        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_photo_delete(self, account_fixture, user_photo):
        from photo.models import UserPhoto

        url = reverse(
            "photo:userphoto-detail",
            kwargs={
                "pk": UserPhoto.objects.filter(
                    user=account_fixture, photo_type="avatar"
                )
                .first()
                .pk
            },
        )

        response = self.client.delete(url)
        assert response.status_code == 401

        self.client.force_authenticate(user=account_fixture)
        response = self.client.delete(url)
        assert response.status_code == 204

    def test_photo_create(self, account_fixture):
        from photo.models import UserPhoto

        self.client.force_authenticate(account_fixture)
        url = reverse("photo:userphoto-list")
        data = {
            "image": self.generate_test_image(),
            "photo_type": "personal_galery",
        }

        response = self.client.post(path=url, data=data)

        assert response.status_code == 201
        assert response.json().get("photo_type") == "personal_galery"
        print(
            f"=============== {UserPhoto.objects.get(id=response.json().get('id'))}"
        )
        assert (
            UserPhoto.objects.get(id=response.json().get("id")).user
            == account_fixture
        )

    def test_photo_update(self, account_fixture, user_photo):
        from photo.models import UserPhoto

        url = reverse(
            "photo:userphoto-detail",
            kwargs={
                "pk": UserPhoto.objects.filter(
                    user=account_fixture, photo_type="avatar"
                )
                .first()
                .pk
            },
        )

        data = {
            "image": self.generate_test_image(),
            "photo_type": "other",
        }

        response = self.client.patch(
            path=url, data=data, format="multipart"
        )
        assert response.status_code == 401

        data = {
            "image": self.generate_test_image(),
            "photo_type": "other",
        }

        self.client.force_authenticate(user=account_fixture)
        response = self.client.patch(
            path=url, data=data, format="multipart"
        )
        assert response.status_code == 200
        assert response.json().get("photo_type") == "other"
