import uuid
from datetime import timedelta

from account.models import Account
from core.settings import OTP_DELTA
from django.db import models
from django.utils import timezone


def default_expires_at():
    return timezone.now() + OTP_DELTA


class OTP(models.Model):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="otps",
    )
    hash_otp = models.CharField(max_length=120)
    issued_by = models.DateTimeField(default=timezone.now)
    used_at = models.DateTimeField(null=True, blank=True)
    code_uuid = models.UUIDField(
        max_length=36, default=uuid.uuid4, editable=False
    )
    expires_at = models.DateTimeField(default=default_expires_at)

    @property
    def is_valid(self):
        now = timezone.now()
        return self.used_at is None and now < self.expires_at
    

class PasswordResetSession(models.Model):
    email = models.EmailField()
    otp_hash = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expires_at)
