import uuid
from datetime import timedelta

from core.settings import OTP_RETENTION_DAYS
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
from django.utils import timezone


class AccountManager(BaseUserManager):
    def get_user_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404("User not found")

    def create_user(
        self, email, username, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(
            email=email, username=username, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class Account(AbstractUser):
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        auto_created=True,
        default=uuid.uuid4,
    )
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = AccountManager()

    _last_otp_clean = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

    @property
    def is_time_to_clean_otp(self):
        return self._last_otp_clean < timezone.now + timedelta(
            days=OTP_RETENTION_DAYS
        )

    class Meta:
        db_table = "accounts"
