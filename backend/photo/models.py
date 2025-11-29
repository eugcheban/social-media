from account.models import Account
from django.db import models


class BasePhoto(models.Model):
    photo_choices = {
        "avatar": "Avatar Photo",
        "personal_galery": "Personal Galery",
        "other": "Other",
    }
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="photos/")
    photo_type = models.CharField(choices=photo_choices, default="OT")

    class Meta:
        abstract = True


class UserPhoto(BasePhoto):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="photos",
    )

    def __str__(self):
        return f"Photo {self.id} uploaded by User {self.user_id}"

    class Meta:
        db_table = "user_photos"
