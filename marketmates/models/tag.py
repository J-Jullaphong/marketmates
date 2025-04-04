import uuid

from django.db import models


class Tag(models.Model):
    """Represents a tag that can be associated with forums."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag_name = models.CharField(max_length=50, unique=True)
