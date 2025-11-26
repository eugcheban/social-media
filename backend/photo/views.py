from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import UserPhoto
from account.models import Account
from .serializers import UserPhotoSerializer

class UserPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = UserPhotoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        user_id = self.request.user.id
        user = Account.objects.get(id=user_id)
        photo_type = self.kwargs.get('photo_type')
        
        if photo_type:
            return UserPhoto.objects.filter(photo_type=photo_type)
        
        return UserPhoto.objects.filter(user=user)
        

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