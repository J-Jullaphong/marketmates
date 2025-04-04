import uuid

from django.db import models

from .forum import Forum
from .user import User


class FavoriteForum(models.Model):
    """Represents a user's favorite forum."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
