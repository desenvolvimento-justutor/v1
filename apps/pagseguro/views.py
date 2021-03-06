# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

import six

from .api import PagSeguroApi
from logging import getLogger
_log = getLogger('django')

@csrf_exempt
@require_http_methods(['POST'])
def receive_notification(request):
    _log.debug(str(request.POST))
    notification_code = request.POST.get('notificationCode', None)
    notification_type = request.POST.get('notificationType', None)
    if notification_code and notification_type == 'transaction':
        pagseguro_api = PagSeguroApi()
        response = pagseguro_api.get_notification(notification_code)
        if response.status_code == 200:
            if six.PY2:
                return HttpResponse(six.b('Notificação recebida com sucesso.'))
            return HttpResponse(six.u('Notificação recebida com sucesso.'))

    if six.PY2:
        return HttpResponse(six.b('Notificação inválida.'), status=400)
    return HttpResponse(six.u('Notificação inválida.'), status=400)
