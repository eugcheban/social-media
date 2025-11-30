from django.urls import include, path

from .routers import router
from .views.password_views import PasswordViewSet

app_name = "account"

urlpatterns = [
    path("", include(router.urls, namespace='account')),
    path("account/password/", PasswordViewSet.as_view({'post': 'change'}), name='change-password')
]
