from rest_framework import routers

from .views import UserPhotoViewSet

router = routers.DefaultRouter()
router.register(r"userphotos", UserPhotoViewSet, basename="userphoto")
