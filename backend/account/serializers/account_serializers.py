import logging

from account.models import Account
from django.db import DatabaseError, IntegrityError
from rest_framework import serializers

logger = logging.getLogger(__name__)


class AccountSerializer(serializers.ModelSerializer):
    """Account serializer"""

    id = serializers.UUIDField(
        source="public_id", read_only=True, format="hex"
    )
    date_joined = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    photos = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        """Meta"""

        model = Account
        fields = [
            "id",
            "username",
            "email",
            "date_joined",
            "is_active",
            "photos",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = Account(**validated_data)
        instance.set_password(password)
        try:
            instance.save()
        except IntegrityError as e:
            logger.error(f"Failed to create account {validated_data.get('email')}: {e}")
            raise serializers.ValidationError(
                {"error": "Account with this email already exists"}
            )
        except DatabaseError as e:
            logger.error(f"Database error creating account: {e}")
            raise serializers.ValidationError(
                {"error": "Failed to create account"}
            )
        return instance
