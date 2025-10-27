from django.urls import path, include
from .views import AccountViewSet
from .routers import router

app_name = 'account'

urlpatterns = [
    path('', include(router.urls)),
]