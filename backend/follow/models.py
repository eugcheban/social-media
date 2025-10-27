from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core import settings
from django.db import models

class Follow(models.Model):
    # ForeignKey linking to the user who is following
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Uses the custom user model defined in settings
        on_delete=models.CASCADE    # Deletes the Follow instance if the user is deleted
    )
    
    # ForeignKey to identify the type of content being followed (User, Post, Tag, etc.)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE    # Deletes Follow instance if the content type is deleted
    )
    
    # The primary key ID of the object being followed (e.g., a specific User or Post ID)
    object_id = models.PositiveIntegerField()
    
    # A generic foreign key that allows for a dynamic link to any model instance
    target = GenericForeignKey('content_type', 'object_id')
    
    # Timestamp indicating when the follow action was created
    created_at = models.DateTimeField(auto_now_add=True)