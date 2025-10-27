from django.urls import path, include
from .views import UserPhotoViewSet
from .routers import router

app_name = 'photo'

urlpatterns = [
    path('', include(router.urls))
]