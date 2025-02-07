import uuid

from django.db import models

from .user import User


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    capacity = models.IntegerField(default=20)
    members = models.ManyToManyField(User, blank=True)
