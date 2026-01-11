import logging

from account.models import Account
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response

from .models import UserPhoto
from .serializers import UserPhotoSerializer

logger = logging.getLogger(__name__)


class UserPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = UserPhotoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user_id = self.request.user.id
        try:
            user = Account.objects.get(id=user_id)
        except ObjectDoesNotExist:
            logger.error(f"User with id {user_id} not found")
            return UserPhoto.objects.none()
        
        photo_type = self.kwargs.get("photo_type")

        if photo_type:
            return UserPhoto.objects.filter(photo_type=photo_type)

        return UserPhoto.objects.filter(user=user)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated]
        elif self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
