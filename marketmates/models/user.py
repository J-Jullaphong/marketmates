import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


def user_profile_picture_upload_path(instance, filename):
    """Returns the upload path for user profile pictures."""
    ext = filename.split('.')[-1]
    return f'user_profile_pictures/{instance.id}/{instance.username}_profile_picture.{ext}'


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_description = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_upload_path, blank=True, null=True)

    def __str__(self):
        """Returns a string representation of the user."""
        return self.username
