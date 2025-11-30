from django.urls import include, path

from .routers import router


app_name = "photo"

urlpatterns = [path("", include(router.urls))]
