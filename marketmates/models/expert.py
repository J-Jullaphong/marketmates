import uuid

from django.db import models
from django.utils import timezone

from .user import User


def expert_document_upload_path(instance, filename):
    """Returns the upload path for expert verification documents."""
    ext = filename.split('.')[-1]
    return f'expert_documents/user_{instance.user.id}/document.{ext}'


class Expert(models.Model):
    """Represents an expert user who has been verified."""
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

    def __str__(self):
        """Returns the expert's full name and status."""
        return f"{self.user.first_name} {self.user.last_name} ({self.status})"

    def save(self, *args, **kwargs):
        """Updates the verified_at field and user status when approved."""
        if self.status == 'Approved':
            if not self.verified_at:
                self.verified_at = timezone.now()
            if not self.user.is_active:
                self.user.is_active = True
                self.user.save()
        super().save(*args, **kwargs)
