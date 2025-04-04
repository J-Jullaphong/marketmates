import uuid

from django.db import models
from django.urls import reverse

from .user import User


class ChatRoom(models.Model):
    """Represents a chat room where users can communicate."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    capacity = models.IntegerField(default=20)
    members = models.ManyToManyField(User, blank=True)

    def get_absolute_url(self):
        """Returns the absolute URL for the chat room page."""
        return reverse('marketmates:chat_room_page', kwargs={'room_id': self.pk})
