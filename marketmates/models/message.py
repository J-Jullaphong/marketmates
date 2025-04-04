import uuid

from django.db import models

from .chat_room import ChatRoom
from .user import User


def message_image_upload_path(instance, filename):
    """Returns the upload path for message images."""
    ext = filename.split('.')[-1]
    return f'message_images/chat_{instance.chat_room.id}/message_{instance.id}.{ext}'


class Message(models.Model):
    """Represents a message in a chat room."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=message_image_upload_path, max_length=1024, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns a string representation of the message."""
        return f"{self.sender.username} sent a message"
