from django.shortcuts import render
from mailer.forms import MailComposeForm
from django.contrib.auth.decorators import login_required


@login_required
def compose_mail(req):
    form = MailComposeForm()
    return render(req, 'mailer/compose.html', {'form': form})

def check_mail_config():
    pass