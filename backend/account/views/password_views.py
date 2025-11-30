from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from ..models import Account
from ..serializers.password_serializers import PasswordSerizliser

from rest_framework.decorators import action
from rest_framework.response import Response


class PasswordViewSet(viewsets.GenericViewSet):
    serializer_class = PasswordSerizliser
    permission_classes = [IsAuthenticated]
    
    @action(
        detail=False,
        methods=['post'],
        url_path='change'
    )
    def change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated successfully"})
