from django import forms
from ckeditor.widgets import CKEditorWidget

class MailComposeForm(forms.Form):
    subject = forms.CharField(label="Subject", max_length=1024)
    to = forms.CharField(label="To", max_length=1024)
    body = forms.CharField(label="Message", max_length=4096,
        widget=forms.Textarea(attrs={'id':'editor'}),
        required=False)
    attachment = forms.FileField(required=False)
