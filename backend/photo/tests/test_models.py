import pytest


@pytest.mark.django_db
def test_user_photo_str_returns_expected(user_photo):
    assert str(user_photo) == f"Photo {user_photo.id} uploaded by User {user_photo.user_id}"


@pytest.mark.django_db
def test_user_photo_fields_persist(account_fixture, user_photo):
    assert user_photo.user == account_fixture
    assert user_photo.photo_type == "avatar"
    assert user_photo.uploaded_at is not None
    assert account_fixture.photos.count() == 1
