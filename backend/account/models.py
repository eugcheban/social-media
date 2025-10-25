from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'accounts'