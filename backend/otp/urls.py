from django.urls import path, include
from .views import OTPViewsSet

app_name = 'otp'

urlpatterns = [
    path('otp/', OTPViewsSet.as_view(), name='main-otp')
]