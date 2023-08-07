# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import Simulado, QuestionarioAluno, RespostaQuestionarioAluno, QuestaoEscolha
from apps.curso.models import Cortesia
from django.http import JsonResponse
from django.template.loader import render_to_string
from libs.util.format import timedelta_str, convert_timedelta
from django.utils import timezone
from django.utils.html import mark_safe
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
import sys
import traceback
from django.core.exceptions import PermissionDenied


def questionario(request, pk):
    simulado = get_object_or_404(Simulado, pk=pk)
    aluno = request.user.aluno
    cc = simulado.curso.checkoutitens_set.filter(
        curso=simulado.curso,
        checkout__aluno=aluno,
        checkout__transaction__status__in=['pago', 'disponivel']
    ).exists()
    cort = Cortesia.objects.filter(aluno=aluno, utilizado=True, curso__simulado=simulado).exists()

    if not cc | cort and not request.user.is_superuser:
        raise PermissionDenied('Área restrita a professores')
    try:
        questionario_aluno = QuestionarioAluno.objects.get(
            aluno=aluno,
            simulado=simulado
        )
    except QuestionarioAluno.DoesNotExist:
        questionario_aluno = QuestionarioAluno.objects.create(
            aluno=aluno,
            simulado=simulado
        )
        questionario_aluno.create_resposta()
    questionario_estatisticas = None
    if questionario_aluno.data_conclusao:
        questionario_estatisticas = questionario_aluno.estatisticas()
        resposta_questionario_aluno = questionario_aluno.respostas_aluno.first()
    else:
        resposta_questionario_aluno = questionario_aluno.respostas_aluno.filter(
            questao_escolha__isnull=True, viu_comentario=False
        ).first() or questionario_aluno.respostas_aluno.first()

    context = {
        'menu': 'Simulados',
        'submenu': simulado,
        'simulado': simulado,
        'questionario_aluno': questionario_aluno,
        'resposta_questionario_aluno': resposta_questionario_aluno,
        'questionario_estatisticas': questionario_estatisticas
    }
    questoes = []
    for grupo in simulado.grupos.all():
        for disciplina in grupo.grupo.disciplinas.all():
            for questao in disciplina.questoes.all():
                questoes.append(questao)
    context['questoes'] = questoes
    # context['questao'] = questoes[0]
    return render(request, 'autor/responder.html', context)


def ajax_responder(request):
    try:
        data = request.GET
        message = False
        tag = 'success'
        resposta_questionario_aluno = RespostaQuestionarioAluno.objects.get(
            pk=data['resposta_questionario_aluno_id']
        )
        questionario_aluno = resposta_questionario_aluno.questionario_aluno
        questao_escolha = data['questao_escolha_id']
        simulado_obj = questionario_aluno.simulado
        rest_later = 0
        if simulado_obj.encerrado:
            tag = 'error'
            message = 'Simulado encerrado'
        else:
            if not questionario_aluno.data_conclusao:
                if questao_escolha in ['false', 'true']:
                    if not resposta_questionario_aluno.viu_comentario:
                        tag = 'error'
                        message = mark_safe(
                            'Questão [{}] bloqueada!'.format(resposta_questionario_aluno.questao_grupo.questao)
                        )
                    if questao_escolha == 'true' and questionario_aluno.confirmar_visualizar_comentario:
                        questionario_aluno.confirmar_visualizar_comentario = False
                        questionario_aluno.save()
                    resposta_questionario_aluno.viu_comentario = True
                    resposta_questionario_aluno.save()

                else:
                    escolha = QuestaoEscolha.objects.get(pk=questao_escolha)
                    resposta_questionario_aluno.questao_escolha = escolha
                    if resposta_questionario_aluno.questao_grupo.questao.situacao == "N":
                        correta = True
                    else:
                        correta = escolha.correta
                    resposta_questionario_aluno.respondida = True
                    resposta_questionario_aluno.correta = correta
                    resposta_questionario_aluno.save()
                    rest_later = questionario_aluno.get_respostas_restantes().count()
                    message = mark_safe('{}. - Faltam {}'.format(escolha.numeracao, rest_later))
            else:
                message = 'Você não pode mais alterar o simulado depois de finalizado!'
                tag = 'danger'
            if not rest_later:
                rest_later = questionario_aluno.get_respostas_restantes().count()
        data = {
            'message': message,
            'tag': tag,
            'concluidas': questionario_aluno.get_respostas_concluidas().count(),
            'restantes': rest_later,
            'html': get_html_resposta_form(request, resposta_questionario_aluno),
            'html_chart': get_html_chart(request, questionario_aluno),
            'html_resultado': get_html_resultado(request, questionario_aluno),
            'show_end': rest_later == 0,
            'next': resposta_questionario_aluno.next().pk if resposta_questionario_aluno.next() else 0,
        }
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        trace = traceback.format_tb(exc_traceback)
        return JsonResponse(
            data={
                'err': mark_safe('<br/>'.join(trace))
            },
            status=500
        )
    return JsonResponse(data)


def get_html_chart(request, questionario_aluno):
    context = {
        'questionario_aluno': questionario_aluno
    }
    html = render_to_string('autor/chart.html', context=context)
    return html


def get_html_resposta_form(request, resposta_questionario_aluno):
    questionario_aluno = resposta_questionario_aluno.questionario_aluno
    context = {
        'simulado': questionario_aluno.simulado,
        'questionario_aluno': questionario_aluno,
        'resposta_questionario_aluno': resposta_questionario_aluno
    }
    html = render_to_string('autor/lista-de-questoes.html', context=context)
    return html


def get_html_resultado(request, questionario_aluno):
    questionario_aluno = questionario_aluno
    context = {
        'simulado': questionario_aluno.simulado,
        'questionario_aluno': questionario_aluno,
    }
    html = render_to_string('autor/resultado.html', context=context)
    return html


def get_html(request, questionario_aluno, resposta_questionario_aluno=False):
    if not resposta_questionario_aluno:
        resposta_questionario_aluno = questionario_aluno.respostas_aluno.first()

    html_resposta_form = get_html_resposta_form(request, resposta_questionario_aluno)
    html_chart = get_html_chart(request, questionario_aluno)
    html_resultado = get_html_resultado(request, questionario_aluno)
    return {
        'html_resposta_form': html_resposta_form,
        'html_chart': html_chart,
        'html_resultado': html_resultado
    }


def ajax_render_html(request):
    questionario_aluno_id = request.GET['questionario_aluno_id']
    resposta_questionario_aluno_id = request.GET['resposta_questionario_aluno_id']

    questionario_aluno = QuestionarioAluno.objects.get(id=questionario_aluno_id)

    if resposta_questionario_aluno_id:
        resposta_questionario_aluno = RespostaQuestionarioAluno.objects.get(id=resposta_questionario_aluno_id)
    else:
        resposta_questionario_aluno = questionario_aluno.respostas_aluno.first()

    html = get_html(request, questionario_aluno, resposta_questionario_aluno)
    return JsonResponse({
        'html': html
    })


def ajax_questao_render(request):
    resposta_questionario_aluno = RespostaQuestionarioAluno.objects.get(
        pk=request.GET.get('pk')
    )
    context = {
        'resposta_questionario_aluno': resposta_questionario_aluno,
        'simulado': resposta_questionario_aluno.questionario_aluno.simulado,
        'context': {
            'request': request
        }
    }
    html = render_to_string('autor/box_questao.html', context=context, request=request)
    data = {
        'html': html,

    }
    return JsonResponse(data, safe=False)


def ajax_update_timer(request):
    questionario_obj = QuestionarioAluno.objects.get(
        pk=request.GET.get('pk')
    )
    t1 = questionario_obj.tempo_de_prova
    t2 = questionario_obj.tempo_restante
    tsplit = convert_timedelta(t1)
    finalizado = True if questionario_obj.data_conclusao else False
    minutos_restantes = int(t2.total_seconds() / 60)
    tempo_esgotado = t2.total_seconds() < 0
    time_left = questionario_obj.simulado.get_time_left
    time_left.pop('left')
    block = False
    if time_left['end']:
        questionario_obj.status_simulado = 'finalizado'
        questionario_obj.tempo_esgotado = True
        questionario_obj.save()
        block = True
    if tempo_esgotado:
        questionario_obj.status_simulado = 'Iniciado'
        questionario_obj.tempo_esgotado = True
        questionario_obj.save()
        block = True
    data = {
        'now': timezone.now().strftime('%d/%d/%Y %H:%M:%S'),
        'time_hours': '%02d' % tsplit.get('hours', 0),
        'time_minutes': '%02d' % tsplit.get('minutes', 0),
        'time_seconds': '%02d' % tsplit.get('seconds', 0),
        'timer': timedelta_str(t1, False),
        'tempo_restante': str(t2),
        'timer_out': '00:00:00' if tempo_esgotado else timedelta_str(t2),
        'timer_repr': convert_timedelta(t2),
        'tempo_esgotado': tempo_esgotado,
        'finalizado': finalizado,
        'minutos_restantes': minutos_restantes,
        'msg_voltar': True if finalizado or tempo_esgotado else False,
        'time_left': time_left,
        'block': block
    }
    return JsonResponse(data, safe=False)


def ajax_check_time(request):
    questionario_obj = QuestionarioAluno.objects.get(
        pk=request.GET.get('pk')
    )
    t2 = questionario_obj.tempo_restante
    show = t2.total_seconds() / 60 < 30 and not questionario_obj.data_conclusao
    data = {
        'minutos_restantes': int(t2.total_seconds() / 60),
        'show': show
    }
    return JsonResponse(data, safe=False)


def ajax_encerrar_simulado(request):
    questionario_obj = QuestionarioAluno.objects.get(
        pk=request.GET.get('pk')
    )
    questionario_obj.data_conclusao = timezone.now()
    questionario_obj.save()

    data = {}
    return JsonResponse(data, safe=False)


def ajax_render_comentario(request):
    try:
        resposta_questionario_aluno = RespostaQuestionarioAluno.objects.get(
            pk=request.GET.get('resposta_questionario_aluno_id')
        )
        context = {
            'resposta_questionario_aluno': resposta_questionario_aluno,
            'simulado': resposta_questionario_aluno.questionario_aluno.simulado,
        }
        html = render_to_string('autor/modal_comentarios.html', context=context)
        data = {
            'html': html,
            'title': '%s' % resposta_questionario_aluno.questao_grupo

        }
    except Exception as e:
        data = {
            'html': '%s' % e
        }
        return JsonResponse(data, status=500)
    return JsonResponse(data, safe=False)


def ajax_modal_estatisticas(request):
    try:
        questionario_aluno = QuestionarioAluno.objects.get(
            pk=request.GET.get('questionario_aluno_id')
        )
        context = {
            'questionario_estatisticas': questionario_aluno.estatisticas(),
            'accordion_id': questionario_aluno.pk
        }
        html = render_to_string('autor/tabs/estatistica.html', context=context, request=request)
    except Exception as e:
        html = str(e)

    data = {
        'html': html,

    }
    return JsonResponse(data, safe=False)
