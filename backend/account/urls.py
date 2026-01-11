from django.urls import include, path

from .routers import router
from .views.password_views import PasswordViewSet, PasswordResetViewSet

app_name = "account"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "account/password/",
        PasswordViewSet.as_view({"post": "change"}),
        name="change-password",
    ),
    path(
        "account/password-reset/request", 
        PasswordResetViewSet.as_view({"post": "reset"}),
        name="password-reset-request",
    ),
    path(
        "account/password-reset/verify",
        PasswordResetViewSet.as_view({"post": "verify"}),
        name="password-reset-verify",
    ),
    path(
        "account/password-reset/confirm",
        PasswordResetViewSet.as_view({"post": "confirm"}),
        name="password-reset-confirm",
    )
]
