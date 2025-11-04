from django.db import models
from account.models import Account
from core.settings import OTP_DELTA

import uuid
from datetime import timedelta, datetime
from django.utils import timezone

class OTP(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, related_name='otp')
    hash_otp = models.CharField(max_length=64)
    issued_by = models.DateTimeField(default=timezone.now)
    used_at = models.DateTimeField(default=None)
    code_uuid = models.UUIDField(max_length=36, default=uuid.uuid4, editable=False)
    used_at = models.DateTimeField(default=None)
    
    @property
    def expired_by(self):
        return self.issued_by + OTP_DELTA
            
    @property
    def is_valid(self):
        return datetime.now() < self.expired_by
    