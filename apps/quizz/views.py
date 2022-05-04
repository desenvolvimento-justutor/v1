# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Bloco, Questao, Pergunta, RespostaAluno, Comentario
from django.core.exceptions import PermissionDenied
from apps.curso.models import Curso


def check_access(request, quizz):
    curso_id = request.session.get('curso_id')

    if not curso_id:
        raise PermissionDenied

    curso = get_object_or_404(Curso, pk=curso_id)

    if not quizz.curso_set.filter(pk=curso.pk).count() or not curso.disponivel:
        raise PermissionDenied


def quizz(request, pk):
    obj_bloco = get_object_or_404(Bloco, pk=pk)
    check_access(request, obj_bloco)
    ctx = {
        'menu': 'Quizz / %s' % obj_bloco,
        'bloco': obj_bloco,
        'aluno': request.user.aluno,
        'curso_id': request.session.get('videos')
    }
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'reiniciar':
            RespostaAluno.objects.filter(questao__bloco=obj_bloco, aluno=request.user.aluno).delete()
            messages.success(request, u'Todas as suas respostas foram excluídas.')
    return render(request, 'quizz/painel-quizz-quizz.html', ctx)


def questao(request, qpk, pk):
    obj_bloco = get_object_or_404(Bloco, pk=qpk)
    check_access(request, obj_bloco)
    obj_questao = get_object_or_404(Questao, pk=pk)
    aluno = request.user.aluno
    total_respostas = RespostaAluno.objects.filter(questao=obj_questao).count()
    total_erradas = tota_corretas = 0
    if total_respostas:
        tota_corretas = RespostaAluno.objects.filter(
            questao=obj_questao, resposta__correta=True).count() * 100 / total_respostas
        total_erradas = RespostaAluno.objects.filter(
            questao=obj_questao, resposta__correta=False).count() * 100 / total_respostas
    ctx = {
        'menu': 'Quizz / %s / %s' % (obj_bloco, obj_questao.pk),
        'bloco': obj_bloco,
        'questao': obj_questao,
        'aluno': request.user.aluno,
        'curso_id': request.session.get('videos'),
        'total_corretas': tota_corretas,
        'total_erradas': total_erradas,
        'total_geral': total_respostas

    }
    resposta_aluno = False
    if request.method == 'POST':
        resposta = request.POST.get('resposta')
        comentario = request.POST.get('comentario')
        if comentario:
            o_comentario = Comentario(
                aluno=aluno,
                questao=obj_questao,
                comentario=comentario
            )
            o_comentario.save()
            messages.success(request, u'Comentário enviado com sucesso.')
            return HttpResponseRedirect(
                    reverse('quizz:questao', kwargs={'qpk': obj_bloco.pk, 'pk': obj_questao.pk})
                )
        else:
            if not resposta:
                messages.error(request, u'Selecione uma opção')
            else:
                pergunta_obj = Pergunta.objects.get(pk=resposta)
                resposta_aluno = RespostaAluno(aluno=aluno, resposta=pergunta_obj, questao=obj_questao)
                resposta_aluno.save()
                if pergunta_obj.correta:
                    messages.success(request, u'Resposta Correta')
                else:
                    messages.error(request, u'Resposta Errada')
                return HttpResponseRedirect(
                    reverse('quizz:questao', kwargs={'qpk': obj_bloco.pk, 'pk': obj_questao.pk})
                )
            # else:
            #     return HttpResponseRedirect(
            #         reverse('quizz:quizz', kwargs={'pk': obj_bloco.pk})
            #     )
    else:
        try:
            resposta_aluno = RespostaAluno.objects.get(aluno=aluno, questao=obj_questao)
        except RespostaAluno.DoesNotExist:
            resposta_aluno = False
    ctx['resposta_aluno'] = resposta_aluno
    print ctx
    return render(request, 'quizz/painel-quizz-questao.html', ctx)