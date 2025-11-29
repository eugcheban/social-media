from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response

from ..models import Account
from ..serializers.account_serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer

    def get_queryset(self):
        user = self.request.user

        if self.action == "list":
            return Account.objects.all()

        return Account.objects.filter(id=user.id)

    def create(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        elif self.action == "list":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
