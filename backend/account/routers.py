from rest_framework import routers

from .views.account_views import AccountViewSet

router = routers.DefaultRouter()
router.register(r"users", AccountViewSet, basename="useraccount")
