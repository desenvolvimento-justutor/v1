# -*- coding: utf-8 -*-
import logging

from .models import Configuracao
from justutorial.settings import SITEADD
from django.utils import timezone

logger = logging.getLogger(__name__)


def website(request):
    dominiows = request.build_absolute_uri()
    ret_dict = {
        'dominiows': dominiows,
        'dominio': dominiows.rstrip('/'),
        'absolute_static_url': '{0}/static/'.format(SITEADD),
        'aluno': False
    }
    try:
        ret_dict.update(dict(
            aluno=request.user.aluno
        ))
    except:
        pass
    # Configuração
    try:
        ret_dict.update({'config': Configuracao.objects.filter(ativo=True).first()})
    except Exception as e:
        logger.debug(str(e))
    return {'website': ret_dict}
