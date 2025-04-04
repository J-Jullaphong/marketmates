import uuid

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from bs4 import BeautifulSoup

from .forum import Forum
from .user import User


class Comment(models.Model):
    """Represents a comment in a forum."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = CKEditor5Field('Comment Content', config_name='default')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_images(self):
        """Extracts all image URLs from the comment content."""
        soup = BeautifulSoup(self.comment_content, "html.parser")
        img_tags = soup.find_all("img")
        return [img["src"] for img in img_tags if "src" in img.attrs]

    def get_formatted_content(self):
        """Returns the comment content without images."""
        soup = BeautifulSoup(self.comment_content, "html.parser")
        for img in soup.find_all("img"):
            img.decompose()
        return str(soup)

    def __str__(self):
        """Returns a string representation of the comment."""
        return f"{self.user.username}: {self.get_formatted_content()[:30]}"

