from django.shortcuts import render
from rest_framework.permissions import isAdminUser

from .models import Account
from .serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('pk')
        
        if self.action in ['get', 'delete', 'update', 'partial_update']:
            return Account.objects.filter(id=user_id)
        
        if self.request.user.is_staff:
            return Account.objects.all()
        else:    
            return Account.objects.none()