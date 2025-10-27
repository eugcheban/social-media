from django.db import models

from account.models import Account

class BasePhoto(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/')

    class Meta:
        abstract = True
        
class UserPhoto(BasePhoto):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)

    def __str__(self):
        return f"Photo {self.id} uploaded by User {self.user_id}"
    
    class Meta:
        db_table = 'user_photos'