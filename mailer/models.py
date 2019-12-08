from django.db import models
from django.core.mail.message import EmailMessage


class MailSent(models.Model):
    subject = models.CharField(max_length=1024)
    body = models.TextField(blank=True, null=True)
    from_email = models.CharField(max_length=512)
    to = models.CharField(max_length=1024)
    headers = models.TextField(blank=True, null=True)
    attachment = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
