from django.urls import include, path

from .routers import router
from .views.password_views import PasswordViewSet

app_name = "account"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "account/password/",
        PasswordViewSet.as_view({"post": "change"}),
        name="change-password",
    ),
    path(
        "account/password/reset", 
        PasswordViewSet.as_view({"post": "reset"}),
        name="reset-password"
    )
]
