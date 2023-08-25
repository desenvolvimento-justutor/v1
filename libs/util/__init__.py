# coding:utf-8
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core.mail.message import EmailMultiAlternatives
from django.template.defaultfilters import slugify
import urllib, urllib2, base64, threading
from urllib2 import HTTPError, URLError
from django.utils.encoding import force_unicode
from justutorial import settings
from datetime import datetime
from os.path import join
from libs.util.decorators import threaded
import re
from django.utils.html import strip_tags

BASE64_KEY = getattr(settings, 'BASE64_KEY', 'RlIuMzg3eWZh')
EMAIL_SENDER = getattr(settings, 'DEFAULT_FROM_EMAIL', 'EMAIL_HOST_USER')


class EmailThread(threading.Thread):
    def __init__(self, subject, html, body, from_email, recipient_list, headers, fail_silently, ):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        self.headers = headers
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list, self.headers)
        if self.html: msg.attach_alternative(self.html, "text/html")
        msg.extra_headers.update(self.headers)
        msg.send(self.fail_silently)


def send_mail(subject, recipient_list, html, body='', from_email=EMAIL_SENDER, headers=None, fail_silently=False,
              *args,
              **kwargs):
    if not headers: headers = {'Reply-To': ','.join(recipient_list)}
    EmailThread(subject, html, body, from_email, recipient_list, headers, fail_silently).start()


def titzr(txt): return slugify(txt).replace('-', ' ').title()


def codifica(txt):
    sc = (base64.b64encode(BASE64_KEY))[:-2]
    txt = base64.b64encode('%s%s' % (sc, base64.b64encode('%s' % txt)))
    return txt


def decodifica(code):
    txt = base64.b64decode(code)
    sc = (base64.b64encode(BASE64_KEY))[:-2]
    txt = txt.replace(sc, '')
    return base64.b64decode(txt)


class SMSThread(threading.Thread):
    def __init__(self, phone, text):
        self.phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        self.text = text
        self.username = getattr(settings, 'SMS_USER')
        self.password = getattr(settings, 'SMS_PASS')
        self.pais = getattr(settings, 'SMS_PAIS')
        self.url = getattr(settings, 'SMS_ADDR')
        self.url_envio = None
        threading.Thread.__init__(self)

    def run(self):
        if getattr(settings, 'SMS_ENAB'):
            try:
                data = urllib.urlencode({
                    "username": self.username,
                    "password": self.password,
                    "from": self.username,
                    "to": '%s%s' % (self.pais, self.phone),
                    "text": u'%s' % urllib2.quote(self.text.encode('utf8'))
                })
                self.url_envio = '%s?%s' % (self.url, data)
                f = urllib2.urlopen(self.url_envio)
                contents = f.read()
                send_mail('SMS enviado', ['julio.max@webtupi.com.br', ], '%s\r\n%s' % (contents, self.url_envio))
                f.close()

            except HTTPError, e:
                txt = '%s\r\n%s' % (e.code, self.url_envio)
                send_mail('Ocorreu um erro ao enviar o sms 1', ['julio.max@webtupi.com.br', ], txt)
            except URLError, e:
                send_mail('Ocorreu um erro ao enviar o sms 2', ['julio.max@webtupi.com.br', ], e.reason)


def send_sms(phone, text): SMSThread(phone, text).start()


def send_mail(subject, recipient_list, html, body='', from_email=EMAIL_SENDER, headers=None, fail_silently=False,
              *args,
              **kwargs):
    if not headers: headers = {'Reply-To': ','.join(recipient_list)}
    EmailThread(subject, html, body, from_email, recipient_list, headers, fail_silently).start()


class ZLogger(threading.Thread):
    texto, pasta, arquivo = None, None, None

    def __init__(self, texto, pasta=None, arquivo=None):
        self.arquivo = arquivo
        self.texto = texto
        self.pasta = getattr(settings, 'LOG_ROOT', join(getattr(settings, 'MEDIA_ROOT', 'logs'), 'logs'))
        if pasta: self.pasta = join(self.pasta, pasta)
        if not arquivo: self.arquivo = 'log-%s.log' % datetime.now().strftime('%Y-%m-%d-%H%M%S')
        threading.Thread.__init__(self)

    def run(self):
        narq = join(self.pasta, self.arquivo)
        arq = open(narq, 'a')
        arq.write(self.texto)
        arq.close()


def zlog(texto, pasta=None, arquivo=None):
    ZLogger(texto, pasta, arquivo).start()


@threaded
def zlogadm(request, obj, action, msg=''):
    try:
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            object_repr=force_unicode(obj),
            action_flag=action,
            change_message=msg
        )
    except:
        pass


class D2O(dict):
    """
    Classe para melhorar a forma de utilizar os dicionários...
    cansei de ter que colocar colchetes e aspas em cada chave do dicionário
    é muito mais prático acessar as chaves com . (ponto)
    ao invés de usar assim: dados['mensagem'], utilizo assim agora: dados.mensagem
    """

    def __init__(self, dados, **kwargs):
        super(D2O, self).__init__(**kwargs)
        self.__dict__ = self
        for k, v in dados.items():
            if not isinstance(v, dict):
                self.__setitem__(k, v)
            else:
                self.__setitem__(k, D2O(v))


def textify(html):
    # Remove html tags and continuous whitespaces
    text_only = re.sub('[ \t]+', ' ', strip_tags(html))
    # Strip single spaces in the beginning of each line
    return text_only.replace('\n ', '\n').strip().encode("utf-8")
