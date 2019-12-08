from django.shortcuts import render
from mailer.forms import MailComposeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMultiAlternatives

from html2text import html2text

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
        msg.send()

        return HttpResponse("Email sent succesfully.")

    else:
        form = MailComposeForm()
        return HttpResponseRedirect('/mail/compose/',{'form':form})

def check_mail_config():
    pass
