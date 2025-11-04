from rest_framework import serializers
from .models import OTP

class OTPSerializer(serializers.ModelSerializer):
    hash_otp = serializers.CharField(read_only=True)
    is_valid = serializers.Boolean(read_only=True)
    
    class Meta:
        model = OTP
        fields = ['hash_otp', 'is_valid']