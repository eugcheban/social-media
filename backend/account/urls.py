from django.urls import include, path

from .routers import router

app_name = "account"

urlpatterns = [
    path("", include(router.urls)),
]
