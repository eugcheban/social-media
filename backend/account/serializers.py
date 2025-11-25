from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    photos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'date_joined', 'is_active', 'photos', 'password']
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = Account(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance