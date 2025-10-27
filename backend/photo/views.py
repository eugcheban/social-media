from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import UserPhoto
from .serializers import UserPhotoSerializer

class UserPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = UserPhotoSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        photo_id = self.request.query_params.get('pk')
        
        if self.action in ['get', 'delete', 'update', 'partial_update'] and photo_id is not None:
            return UserPhoto.objects.filter(id=user_id)
        
        if self.request.user.is_superuser:
            return UserPhoto.objects.all()
        else:
            return UserPhoto.objects.filter(id=user_id)
        
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]