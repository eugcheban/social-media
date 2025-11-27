import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


class TestPhotoViews:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client=APIClient()
    
    @staticmethod
    def generate_test_image(name="test.jpg", size=(100, 100), color="white"):
        file = BytesIO()
        image = Image.new("RGB", size, color)
        image.save(file, "JPEG")
        file.seek(0)
        return SimpleUploadedFile(
                name=name,
                content=file.read(),
                content_type="image/jpeg",
            )
        
    def test_photo_get(self, User_photo, Account_fixture):
        self.client.force_authenticate(user=Account_fixture)
        url = reverse('photo:userphoto-list') + '?photo_type=avatar'
        
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()) > 0
        
    def test_photo_delete(self, Account_fixture, User_photo):
        from photo.models import UserPhoto
        
        url = reverse('photo:userphoto-detail', kwargs={
            'pk': UserPhoto.objects.filter(
                user=Account_fixture,
                photo_type='avatar'
            ).first().pk
        })
        
        response = self.client.delete(url)
        assert response.status_code == 401
        
        self.client.force_authenticate(user=Account_fixture)
        response = self.client.delete(url)
        assert response.status_code == 204
        
    def test_photo_create(self, Account_fixture):
        from photo.models import UserPhoto
        self.client.force_authenticate(Account_fixture)
        url = reverse('photo:userphoto-list')
        data = {
            'image': self.generate_test_image(),
            'photo_type': 'personal_galery'
        }
        
        response = self.client.post(path=url, data=data)
        
        assert response.status_code == 201
        assert response.json().get('photo_type') == 'personal_galery'
        print(f"=============== {UserPhoto.objects.get(id=response.json().get('id'))}")
        assert UserPhoto.objects.get(id=response.json().get('id')).user == Account_fixture
    
    def test_photo_update(self, Account_fixture, User_photo):
        from photo.models import UserPhoto
        
        url = reverse('photo:userphoto-detail', kwargs={
            'pk': UserPhoto.objects.filter(
                user=Account_fixture,
                photo_type='avatar'
            ).first().pk
        })
        
        data = {
            'image': self.generate_test_image(),
            'photo_type': 'other'
        }
        
        response = self.client.patch(path=url, data=data, format='multipart')
        assert response.status_code == 401
        
        data = {
            'image': self.generate_test_image(),
            'photo_type': 'other'
        }
        
        self.client.force_authenticate(user=Account_fixture)
        response = self.client.patch(path=url, data=data, format='multipart')
        assert response.status_code == 200
        assert response.json().get('photo_type') == 'other'