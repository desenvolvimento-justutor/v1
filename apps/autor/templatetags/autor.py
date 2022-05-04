# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.utils.html import mark_safe
from ..models import (
    QuestionarioAluno,
    RespostaQuestionarioAluno,
    PREVISTO, ANDAMENTO, ENCERRADO, INDEFINIDO
)


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_resposta_aluno(context, questionario_aluno, questao):
    try:
        ret = RespostaQuestionarioAluno.objects.get(
            questionario_aluno=questionario_aluno,
            questao=questao.questao,
            questao_grupo=questao
        )
    except RespostaQuestionarioAluno.DoesNotExist:
        ret = RespostaQuestionarioAluno.objects.none()
    return ret


@register.assignment_tag(takes_context=True)
def get_questionario_aluno(context, simulado):
    aluno = context['request'].user.aluno
    try:
        ret = QuestionarioAluno.objects.get(
            aluno=aluno,
            simulado=simulado
        )
    except QuestionarioAluno.DoesNotExist:
        ret = QuestionarioAluno.objects.none()
    return ret


@register.filter(is_safe=False)
def list_alpha(value):
    print('...', value)
    l = 'ABCDEFGHIJKLMNOPKRSTUVXZ'
    return l[value]


@register.assignment_tag(takes_context=True)
def simulado_aluno_status(context, simulado):
    questionario_aluno = get_questionario_aluno(context, simulado)
    status_simulado = simulado.status
    flags_simulado = simulado.status_flags
    alow_edit = False
    create = False
    block = True
    btn_title = 'Iniciar resolução do simulado'
    if questionario_aluno:
        status_questionario = questionario_aluno.status_flags
    else:
        status_questionario = {
            'title': 'Resolução não iniciada',
            'tag': 'danger',
            'bg': 'red-bg'
        }

    label = '<span class="label label-{}">{}</label>'.format(
        status_questionario['tag'], status_questionario['title']
    )

    if status_simulado == PREVISTO:
        msg = 'Aguarde até {1} do dia {0}'.format(
            simulado.data_inicio.strftime('%d/%m/%Y'),
            simulado.data_inicio.strftime('%H:%M')
        )
    else:
        if status_simulado == ANDAMENTO:
            alow_edit = True
            if questionario_aluno:
                if questionario_aluno.data_conclusao:
                    msg = 'Você finalizou seu simulado às {1} do dia {0}'.format(
                        questionario_aluno.data_conclusao.strftime('%d/%m/%Y'),
                        questionario_aluno.data_conclusao.strftime('%H:%M')
                    )
                    btn_title = 'Ver gabarito e comentários do simulado'
                else:
                    msg = 'Você ainda não finalizou seu simulado!'
                    btn_title = 'Continuar resolução do simulado'
                    flags_simulado['tag'] = 'warning'
            else:
                create = True
                msg = 'Você ainda não iniciou seu simulado!'
        elif status_simulado == ENCERRADO:
            btn_title = 'Ver gabarito e comentários do simulado'
            alow_edit = False
            if questionario_aluno:
                if questionario_aluno.data_conclusao:
                    msg = 'Você finalizou seu simulado às {1} do dia {0}.'.format(
                        questionario_aluno.data_conclusao.strftime('%d/%m/%Y'),
                        questionario_aluno.data_conclusao.strftime('%H:%M')
                    )
                else:
                    msg = 'Você não finalizou o simulado no prazo. Por isso, sua nota não constará no ranking.'
            else:
                msg = 'Você não iniciou o simulado no prazo. Por isso, sua nota não constará no ranking.'

    return {
        'message': msg,
        'status_questionario': status_questionario,
        'status_simulado': status_simulado,
        'flags_simulado': flags_simulado,
        'allow_edit': alow_edit,
        'label': mark_safe(label),
        'btn_title': btn_title,
        'create': create
    }


