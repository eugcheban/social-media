from rest_framework import viewsets
from .models import UserPhoto
from .serializers import UserPhotoSerializer


class UserPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = UserPhotoSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        photo_id = self.request.query_params.get('pk')
        if photo_id is None and user_id is None:
            return UserPhoto.objects.none()
        
        if self.action in ['get', 'delete', 'update', 'partial_update'] and photo_id is not None:
            return UserPhoto.objects.filter(id=user_id)
        
        return UserPhoto.objects.all()