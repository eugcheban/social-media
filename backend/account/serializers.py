from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'date_joined', 'is_active']