import uuid

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from .forum import Forum
from .user import User


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = CKEditor5Field('Comment Content', config_name='default')
    created_at = models.DateTimeField(auto_now_add=True)
