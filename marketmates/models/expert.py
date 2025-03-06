import uuid

from django.db import models

from .user import User


def expert_document_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'expert_documents/user_{instance.user.id}/document.{ext}'


class Expert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=50)
    document = models.FileField(upload_to=expert_document_upload_path, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10,
                              choices=[
                                  ('Pending', 'Pending'),
                                  ('Approved', 'Approved'),
                                  ('Rejected', 'Rejected')],
                              default='Pending')
    rank = models.PositiveIntegerField(default=0)
