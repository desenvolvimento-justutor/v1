# -*- coding: utf-8 -*-

import json
from logging import getLogger

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.nfse.models import NSFe
from apps.website.utils import enviar_email

_log = getLogger('apps')


@csrf_exempt
@require_http_methods(['POST'])
def receive_notification(request):
    _log.debug("NFSe Notification: %s" % str(request.body))
    data = json.loads(request.body)
    ref = data.get("ref")
    try:
        nfse = NSFe.objects.get(ref=ref)
        nfse.status = data.get('status')
        nfse.codigo_verificacao = data.get('codigo_verificacao')
        nfse.caminho_xml_nota_fiscal = data.get('caminho_xml_nota_fiscal')
        nfse.url = data.get('url')
        nfse.numero = data.get('numero')
        nfse.numero_rps = data.get('numero_rps')
        # nfse.status = data.get('data_emissao')
        nfse.serie_rps = data.get('serie_rps')
        nfse.save()
        message = "OK"
    except NSFe.DoesNotExist as e:
        _log.error("NFSe DoesNotExist: %s" % str(e))
        message = str(e)
    except Exception as e:
        _log.error("NFSe Exception: %s" % str(e))
        message = str(e)

    enviar_email(
        'nfse/nfs.html',
        'Nfs %s' % ref,
        ['christian.dev.py@gmail.com'],
        context={'ref': ref, "mensagem": message, "body": data},
        ead=False
    )
    return HttpResponse(b"OK", status=200)


