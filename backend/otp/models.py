import uuid
from datetime import datetime, timedelta

from account.models import Account
from core.settings import OTP_DELTA
from django.db import models
from django.utils import timezone


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

    @property
    def expired_by(self):
        return self.issued_by + OTP_DELTA

    @property
    def is_valid(self):
        return datetime.now() < self.expired_by
