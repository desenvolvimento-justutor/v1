# -*- coding: utf-8 -*-
# Autor: christian
import os
import random
import re

from boto.ses import connect_to_region
from django.template import loader, Context

from justutorial.settings import SITEADD, EMAIL_HOST_USER
from libs.util.mail import send_mail, send_mail_ead
from django.core import mail

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
SES_REGION_NAME = 'us-west-2'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG_EMAIL = False  # os.path.exists(os.path.join(BASE_DIR, 'website', 'debug'))


def sess_connect():
    conn = connect_to_region(
        region_name=SES_REGION_NAME,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    return conn


def render_email_template(template, context=None):
    ctx = {
        'dominio': SITEADD,
        'absolute_static_url': '{0}/static/'.format(SITEADD)
    }
    if context:
        ctx.update(context)
    t = loader.get_template(template)
    c = Context(ctx)
    return t.render(c)


def enviar_email_old(template, titulo, email, context=None, ead=None):
    ctx = {
        'dominio': SITEADD,
        'absolute_static_url': '{0}/static/'.format(SITEADD)
    }
    if context:
        ctx.update(context)
    t = loader.get_template(template)
    c = Context(ctx)
    rendered = t.render(c)
    if DEBUG_EMAIL:
        print("DEBUG E-MAIL")
        email = ['leticia@smartweb.com.br', 'max@smartweb.com.br']
    if ead:
        send_mail_ead(titulo, '', EMAIL_HOST_USER, email, html=rendered)
    else:
        send_mail(titulo, '', EMAIL_HOST_USER, email, html=rendered)
    return True


def enviar_email_ses(connect, template, titulo, emails, context=None, ead=False):
    connection = mail.get_connection()
    connection.open()
    enviar_email_old(template, titulo, emails, context, ead)
    return connection.close()


def enviar_email_ses_(connect, template, titulo, emails, context=None, ead=False):
    ctx = {
        'dominio': SITEADD,
        'absolute_static_url': '{0}/static/'.format(SITEADD)
    }
    if context:
        ctx.update(context)
    email_sender = 'JusTutor - Ensino <ead@justutor.com.br>' if ead else 'naoresponder@justutor.com.br'
    t = loader.get_template(template)
    c = Context(ctx)
    rendered = t.render(c)
    if DEBUG_EMAIL:
        emails = ['christian.douglas.alcantara@gmail.com', 'alexandre.henry.alves@gmail.com	']
    conn = connect
    send = conn.send_email(email_sender, titulo, rendered, emails, format='html')
    return send


def enviar_email(template, titulo, email, context=None, ead=False):
    # return enviar_email_ses(sess_connect(), template, titulo, email, context, ead)
    return enviar_email_old(template, titulo, email, context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CPF(object):
    def __init__(self, cpf=None):
        """Create a CPF instance.

        If a string is provided as argument, use it as the CPF number; otherwise, generate a new one.

        If the string provided doesn't contain 11 digits, exactly, raise ValueError.
        """
        if cpf is None:
            cpf = self.gen()
        else:
            cpf = str(cpf)
            cpf = re.sub(r'[^\d]+', '', cpf)

            if len(cpf) is not 11:
                raise ValueError("CPF should contain 11 digits")

            self.cpf = [int(token) for token in cpf]
        return None

    def __eq__(self, other):
        if not isinstance(other, CPF):
            other = CPF(other)
        return self.cpf == other.cpf

    def __genNumber__(self):
        trial_digits = [random.randint(0, 9) for i in range(0, 11)]
        return trial_digits

    def __getitem__(self, index):
        return str(self.cpf[index])

    def __int__(self):
        return int(''.join([str(x) for x in self.cpf]))

    def __repr__(self):
        return "CPF('%s')" % ''.join([str(x) for x in self.cpf])

    def __str__(self):
        d = ((3, "."), (7, "."), (11, "-"))
        s = [str(token) for token in self.cpf]

        for i, v in d:
            s.insert(i, v)

        return ''.join(s)

    def gen(self, __return__=False):
        self.cpf = self.__genNumber__()

        while self.valid() == False:
            self.cpf = self.__genNumber__()
        return (True, self.cpf)[__return__]

    def valid(self):
        c = self.cpf[:9]
        p = [10, 9, 8, 7, 6, 5, 4, 3, 2]

        while len(c) < 11:
            t = sum([x * y for (x, y) in zip(c, p)]) % 11
            c.append((0, 11 - t)[t >= 2])
            p.insert(0, 11)
        return bool(c == self.cpf)
