# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

import six

from .api import PagSeguroApi
from logging import getLogger
_log = getLogger('pags')

@csrf_exempt
@require_http_methods(['POST'])
def receive_notification(request):
    _log.debug(str(request.POST))
    _log.debug("*" * 100)
    notification_code = request.POST.get('notificationCode', None)
    notification_type = request.POST.get('notificationType', None)

    if notification_code and notification_type == 'transaction':
        pagseguro_api = PagSeguroApi()
        response = pagseguro_api.get_notification(notification_code)
        if response.status_code == 200:
            if six.PY2:
                return HttpResponse(six.b('Notificação recebida com sucesso.'))
            return HttpResponse(six.u('Notificação recebida com sucesso.'))
        else:
            return HttpResponse(response.text, status=response.status_code)

    if six.PY2:
        return HttpResponse(six.b('Notificação inválida.'), status=400)
    return HttpResponse(six.u('Notificação inválida.'), status=400)


@csrf_exempt
def receive_notification_pix(request):
    _log.debug("--- PIX ---")
    _log.debug(str(request.POST))
    _log.debug("*" * 100)
    return HttpResponse('Notificação recebida com sucesso.')
