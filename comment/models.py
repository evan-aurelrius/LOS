from django.db import models
from account.models import User
from application.models import Application
import os


def generate_path(self, filename):
    url = f"comment_attachments/{self.application.id}/{filename}"
    return url


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    message = models.TextField()
    attachment = models.FileField(
        upload_to=generate_path, blank=True, null=True)

    @property
    def filename(self):
        return os.path.basename(self.attachment.name)

    def __str__(self):
        return self.title
