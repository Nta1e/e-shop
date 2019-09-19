from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from turing_backend import settings

class SendMail:
    from_email = settings.EMAIL_HOST_USER

    def __init__(self, template, context, subject, to_email):
        self.template = template
        self.to_email = to_email
        self.context = context
        self.subject = subject

    def _compose_mail(self):
        html_body = render_to_string(
            self.template,
            self.context
        )
        subject = self.subject
        to_email = self.to_email
        message = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=SendMail.from_email,
            to=to_email
        )
        message.content_subtype = 'html'
        return message

    def send(self):
        mail = self._compose_mail()
        mail.send(fail_silently=False)
        return
