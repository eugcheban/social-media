from rest_framework import routers

from .views.account_views import AccountViewSet


app_name = "account"

router = routers.DefaultRouter()
router.register(r"users", AccountViewSet, basename="user-account")
