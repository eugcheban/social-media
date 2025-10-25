from django.urls import path
from .views import UserPhotoViewSet

app_name = 'photo'

urlpatterns = [
    path('', UserPhotoViewSet.as_view({'list'}), name='userphoto-list'),
    path('create/', UserPhotoViewSet.as_view({'post': 'create'}), name='userphoto-create'),
    path('<int:pk>/', UserPhotoViewSet.as_view({'get': 'retrieve'}), name='userphoto-detail'),
    path('<int:pk>/update/', UserPhotoViewSet.as_view({'put': 'update'}), name='userphoto-update'),
    path('<int:pk>/delete/', UserPhotoViewSet.as_view({'delete': 'destroy'}), name='userphoto-delete'),
]