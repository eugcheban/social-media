import logging

from account.models import Account
from django.contrib.auth.password_validation import validate_password
from django.db import DatabaseError
from rest_framework import serializers

logger = logging.getLogger(__name__)

class PasswordChangeSerizliser(serializers.Serializer):
    old_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)

    def validate(self, attrs):
        user = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError(
                {"old_password": "old_password is incorrect!"}
            )

        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError(
                {
                    "new_password": "New password cannot be the same as the old one"
                }
            )

        validate_password(attrs["new_password"], user)

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        try:
            user.save()
        except DatabaseError as e:
            logger.error(f"Failed to save password change for user {user.id}: {e}")
            raise serializers.ValidationError(
                {"error": "Failed to change password"}
            )
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, attrs):
        try:
            user = Account.objects.get(email=attrs["email"])
        except Account.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "email": f"User with email {attrs['email']} not found!"
                }
            )
        
        attrs['user'] = user
        return attrs


class PaswordResetVerifySerializer(serializers.Serializer):
    code_uuid = serializers.UUIDField()
    otp = serializers.CharField(max_length=6)
    
    def validate(self, attrs):
        return attrs
    

class PasswordResetConfirmSerializer(serializers.Serializer):
    code_uuid = serializers.UUIDField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(max_length=100)
    
    def validate(self, attrs):
        validate_password(attrs["new_password"])
        return attrs