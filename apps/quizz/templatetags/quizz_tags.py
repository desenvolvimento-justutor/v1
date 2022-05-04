# -*- coding: utf-8 -*-
# Autor: christian
from django import template
from apps.quizz.models import Questao, Pergunta, RespostaAluno

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_questao_status(context, questao):
    aluno = context['request'].user.aluno
    try:
        resposta_aluno = RespostaAluno.objects.get(aluno=aluno, questao=questao)
        opcao_aluno = resposta_aluno.resposta
        if Pergunta.objects.filter(questao=questao, correta=True).first() == opcao_aluno:
            status = '<i class="fa fa-check lg text-success"></i>'
        else:
            status = '<i class="fa fa-remove lg text-danger"></i>'
    except:
        status = '<i class="fa fa-hourglass-2 lg"></i>'
    return status


@register.assignment_tag(takes_context=True)
def get_total(context, bloco):
    aluno = context['request'].user.aluno
    total_questo = bloco.questoes.all()
    total_respostas = RespostaAluno.objects.filter(aluno=aluno, questao__in=total_questo).count()
    corretas = RespostaAluno.objects.filter(aluno=aluno, resposta__correta=True, questao__in=total_questo).count()
    erradas = RespostaAluno.objects.filter(aluno=aluno, resposta__correta=False, questao__in=total_questo).count()
    completo = err = corr = 0
    if total_respostas:
        corr = corretas * 100 / total_respostas
        err = erradas * 100 / total_respostas
        completo = total_respostas * 100 / total_questo.count()
    return {
        'corr': corr,
        'err': err,
        'corretas': corretas,
        'erradas': erradas,
        'total': total_questo.count(),
        'completo': completo
    }


@register.assignment_tag(takes_context=True)
def get_proxima(context, bloco, questao):
    return Questao.objects.filter(bloco=bloco, id__gt=questao.pk).first()


@register.assignment_tag(takes_context=True)
def get_resposta(context, questao):
    aluno = context['request'].user.aluno
    return RespostaAluno.objects.filter(questao=questao, aluno=aluno).first()

