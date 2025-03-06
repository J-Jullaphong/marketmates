import uuid

from django.db import models

from .chat_room import ChatRoom
from .user import User


def message_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'message_images/chat_{instance.chat_room.id}/user_{instance.sender.id}/message_{instance.id}.{ext}'


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_messages')
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=message_image_upload_path, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    was_read = models.BooleanField(default=False)
