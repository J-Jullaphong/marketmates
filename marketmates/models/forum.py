import uuid

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from bs4 import BeautifulSoup

from .tag import Tag
from .user import User


class Forum(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = CKEditor5Field('Description', config_name='default')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def get_first_image(self):
        soup = BeautifulSoup(self.description, "html.parser")
        img_tag = soup.find("img")
        return img_tag["src"] if img_tag else None

    def get_images(self):
        soup = BeautifulSoup(self.description, "html.parser")
        img_tags = soup.find_all("img")
        return [img["src"] for img in img_tags if "src" in img.attrs]

    def get_formatted_content(self):
        soup = BeautifulSoup(self.description, "html.parser")
        for img in soup.find_all("img"):
            img.decompose()
        return str(soup)
