# coding=utf-8
from __future__ import unicode_literals
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from .views import send_email_contato


@dajaxice_register(method='GET')
def enviar_email(request, nome, email, mensagem):
    x = Dajax()
    send_email_contato(nome, email, mensagem)
    x.script("Swal.fire('Sua mensagem foi enviada, agradecemos o seu contato!',"
             " 'A resposta à sua mensagem será enviada no e-mail <b>%s</b>.', 'success');" % email)
    x.script("$('#id-contato-mensagem').val('')")
    x.script("$('#btn-enviar-contato').button('reset');")
    return x.json()
