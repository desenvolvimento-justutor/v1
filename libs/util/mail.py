# -*- coding: utf-8 -*-
# Autor: christian
from django.core.mail import EmailMultiAlternatives
import threading
from django.conf import settings
from django.core import mail


class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run(self):
        connection = mail.get_connection()
        connection.open()
        # print(connection.__dict__)
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list,
                                     connection=connection)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)
        connection.close()


def send_mail(subject, body, from_email, recipient_list, fail_silently=False, html=None, *args, **kwargs):
    settings.DEFAULT_FROM_EMAIL = 'Justutor <contato@justutor.com.br>'
    # settings.EMAIL_HOST_USER = 'naoresponder@justutor.com.br'
    from_email = 'Justutor <contato@justutor.com.br>'
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()


def send_mail_ead(subject, body, from_email, recipient_list, fail_silently=False, html=None, *args, **kwargs):
    settings.DEFAULT_FROM_EMAIL = 'Justutor <naoresponder@justutor.com.br>'
    # settings.EMAIL_HOST_USER = 'naoresponder@justutor.com.br'
    # settings.EMAIL_HOST_USER = 'ead@justutor.com.br'
    # settings.EMAIL_HOST_PASSWORD = 'TZ#@M?d2656r!C3'
    # settings.EMAIL_HOST_USER = 'ead@justutor.com.br'
    from_email = 'Justutor <contato@justutor.com.br>'
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()
