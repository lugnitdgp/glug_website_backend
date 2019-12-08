from django import forms
from mailer.models import MailConfig

class MailComposeForm(forms.Form):
    subject = forms.CharField(label="Subject", max_length=1024)
    to = forms.CharField(label="To", max_length=1024)
    body = forms.Textarea()
    attachment = forms.FileField(required=False)
