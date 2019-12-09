from django.shortcuts import render
from mailer.forms import MailComposeForm
from mailer.models import MailSent
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

from html2text import html2text

def check_mail_config():
    if hasattr(settings, 'EMAIL_HOST_USER') and hasattr(settings, 'EMAIL_HOST_PASSWORD'):
        if settings.EMAIL_HOST_USER != 'None' and settings.EMAIL_HOST_PASSWORD != 'None':
            return True
    return False

@login_required
def index(req):
    conf_check = check_mail_config()
    history = MailSent.objects.all()
    return render(req, 'mailer/index.html',{'history':history, 'check':conf_check})

@login_required
def compose_mail(req):
    form = MailComposeForm()
    return render(req, 'mailer/compose.html', {'form': form})

@login_required
def send_mail(req):
    if req.method == "POST":
        subject = req.POST['subject']
        body = req.POST['body']
        to = req.POST['to']
        # attachment = req.POST['attachment']

        # Use multipart for low bounce rates
        html_msg = body
        text_msg = html2text(body)
        from_email = 'no-reply@nitdgplug.org'

        msg = EmailMultiAlternatives(subject, text_msg, from_email, [to])
        msg.attach_alternative(html_msg, "text/html")

        try:
            msg.send()

            # log the sent email
            m = MailSent(subject= subject, body=text_msg, from_email=from_email, to=to, sent_by=req.user, time=timezone.now())
            m.save()

            messages.add_message(
                req, messages.SUCCESS, 'Email successfully sent')
        except Exception as e:
            print("ERROR in SMTP :: ", e)
            messages.add_message(
                req, messages.ERROR, 'An error occured. Check configuration again.')
        
        return HttpResponseRedirect('/mail/compose/')

    else:
        form = MailComposeForm()
        return HttpResponseRedirect('/mail/compose/',{'form':form})
