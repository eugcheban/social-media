from rest_framework import serializers

from .models import UserPhoto


class UserPhotoSerializer(serializers.ModelSerializer):
    uploaded_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )

    class Meta:
        model = UserPhoto
        fields = ["id", "image", "uploaded_at", "photo_type"]
