# -*- coding: utf-8 -*-
from apps.enunciado.models import NotificacoesAluno


def proc_aluno(request):
    try:
        aluno = request.user.aluno
        ret_dict = {
            "notificacoes": NotificacoesAluno.objects.filter(para=aluno, lido=False).order_by('-data'),
            "mensagens": NotificacoesAluno.objects.filter(para=aluno, lido=False, tipo="G").order_by('-data')
        }
    except:
        ret_dict = {
            "notificacoes": 0
        }
    return {'proc_aluno': ret_dict}
