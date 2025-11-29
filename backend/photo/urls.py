from django.urls import include, path

from .routers import router
from .views import UserPhotoViewSet

app_name = "photo"

urlpatterns = [path("", include(router.urls))]
