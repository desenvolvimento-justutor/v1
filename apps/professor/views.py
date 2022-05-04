# -*- coding: utf-8 -*-
# Autor: christian
import operator
from decimal import Decimal
from operator import itemgetter

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Count, Sum, Avg
from django.http import HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader, Context
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from apps.aluno.models import Aluno
from apps.curso.models import (
    Curso,
    SentencaAvulsaAluno,
    SentencaAvulsa,
    SentencaOABAvulsaAluno,
    SentencaOAB,
    TarefaAtividade,
    Atividade,
)
from apps.formulario_correcao.models import (
    Formulario,
    TabelaCorrecaoAluno,
    TabelaAluno,
    Nota
)
from apps.professor.models import Professor
from apps.website.utils import enviar_email
from .models import Mensagem


def professor_required(f):
    def wrap(request, *args, **kwargs):
        # this check the session if userid key exist, if not it will redirect to login page
        if 'userid' not in request.session.keys():
            return HttpResponseRedirect(reverse('login'))
        else:
            pass
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def test_login(user):
    try:
        user.professor
    except:
        print(user)
        raise PermissionDenied('Área restrita a professores')
    return user


@login_required
@user_passes_test(test_login)
def painel(request):
    professor = request.user.professor
    order_by = 'atividade'
    fprofessor = None
    categoria_tipo = 'C'
    context = {
        'menu': 'painel',
        'professor': professor,
        'professores': Professor.objects.all(),
        'filtro': {
            'disponivel': 'on'
        }
    }
    if request.method == 'POST':

        kwargs = {}
        disponivel = request.POST.get('disponivel')
        tipo = request.POST.get('tipo')
        professor_id = request.POST.get('professor')
        if professor_id:
            fprofessor = professor = Professor.objects.get(id=professor_id)
            kwargs['atividade__professores'] = fprofessor
        order_by = request.POST.get('order_by')
        if tipo:
            kwargs['categoria__tipo'] = tipo
            categoria_tipo = tipo
        kwargs['disponivel'] = True if disponivel else False
        cursors = Curso.objects.filter(**kwargs).distinct()
        filtro = {
            'disponivel': disponivel,
            'tipo': tipo,
            'order_by': order_by,
            'professor': fprofessor,
        }
    else:
        cursors = Curso.objects.filter(
            disponivel=True,
            categoria__tipo=categoria_tipo,
            atividade__professores=professor
        ).distinct()
        filtro = {
            'disponivel': 'on',
            'tipo': 'C',
            'order_by': 'atividade'
        }
    context.update(dict(filtro=filtro))
    atividades = Atividade.objects.filter(
        curso__categoria__tipo=categoria_tipo,
        professores=professor
    )
    tarefas = TarefaAtividade.objects.filter(
        corrigido=False,
        atividade__curso__categoria__tipo=categoria_tipo,
        atividade__professores=professor,
        concluido=True,
        atividade__tipo_retorno='C',
        limitada=False,
    ).order_by(order_by)
    context.update({
        'atividades': atividades,
        'tarefas': tarefas,
        'cursos': cursors
    })
    return render(request, 'professor/painel.html', context)


@login_required
@user_passes_test(test_login)
def cursos(request):
    professor = request.user.professor
    query = professor.curso_set.all()
    get_curso = request.GET.get('curso')
    if get_curso:
        curso = Curso.objects.get(pk=get_curso)
    else:
        curso = query.first()
    context = {
        'menu': 'cursos',
        'cursos': query,
        'curso': curso
    }
    return render(request, 'professor/cursos.html', context)


@login_required
@user_passes_test(test_login)
def sentenca_view(request, pk):
    sentenca_avulsa = SentencaAvulsa.objects.get(pk=pk)
    return HttpResponse(sentenca_avulsa.conteudo)


@login_required
@user_passes_test(test_login)
def sentencas(request):
    prof = request.user.professor
    filtro = {}
    if request.method == 'GET':
        data = request.GET
        f_sentenca_avulsa = data.get('sentenca_avulsa')
        if f_sentenca_avulsa:
            filtro['sentenca_avulsa_id'] = f_sentenca_avulsa
        f_status = data.get('status', 'A')
        if f_status:
            filtro['status'] = f_status
        f_corrigido = data.get('corrigido')
        if f_corrigido == 'S':
            filtro['correcao__isnull'] = False
        elif f_corrigido == 'N':
            filtro['correcao__isnull'] = True
        f_tipo = data.get('tipo')
        if f_tipo:
            filtro['sentenca_avulsa__curso__categoria__nome'] = f_tipo
        print('dddd', data)
    osentencas = SentencaAvulsaAluno.objects.filter(**filtro)

    context = {
        'menu': 'Sentenças para Correção',
        'sentencas': osentencas,
        'sentencas_avulsas': SentencaAvulsa.objects.filter(professor=prof),
        'filtro': filtro
    }
    return render(request, 'professor/sentencas.html', context)


@login_required
@user_passes_test(test_login)
def recursos(request):
    professor_id = request.user.professor.pk
    status_in = ['solicitado', 'analise']
    data = request.GET
    f = {
        'status__in': status_in
    }
    f_profressor_id = data.get('professor_id')
    if f_profressor_id:
        professor_id = f_profressor_id
        if f_profressor_id != 'T':
            f.update({'professor_id': f_profressor_id})
    if data:
        status_in = [x.split('_')[-1] for x, y in data.iteritems() if y == 'on']
        f.update({'status__in': status_in})
    context = {
        'menu': 'Recursos',
    }
    tabelas = TabelaCorrecaoAluno.objects.filter(
        corrigido=True, **f
    )

    context.update({
        'professor_id': professor_id,
        'tabelas': tabelas,
        'status': status_in,
        'professores': Professor.objects.all()
    })
    return render(request, 'professor/recursos.html', context)


@login_required
@user_passes_test(test_login)
def sentencas_oab(request):
    prof = request.user.professor
    filtro = {
        'sentenca_oab__professor': prof
    }
    if request.method == 'POST':
        data = request.POST
        f_sentenca_avulsa = data.get('sentenca_avulsa')
        if f_sentenca_avulsa:
            filtro['sentenca_avulsa_id'] = f_sentenca_avulsa
        f_status = data.get('status')
        if f_status:
            filtro['status'] = f_status
        f_corrigido = data.get('corrigido')
        if f_corrigido == 'S':
            filtro['correcao__isnull'] = False
        elif f_corrigido == 'N':
            filtro['correcao__isnull'] = True

    osentencas = SentencaOABAvulsaAluno.objects.filter(**filtro)

    context = {
        'menu': 'OAB 2ª Fase',
        'sentencas': osentencas,
        'sentencas_avulsas': SentencaOAB.objects.filter(professor=prof),
        'filtro': filtro
    }
    return render(request, 'professor/sentencas-oab.html', context)


@login_required
@user_passes_test(test_login)
def mensagens(request, pk=None):
    professor = request.user.professor
    tipo = request.GET.get('tipo', 'cr')
    context = {
        'menu': 'mensagens',
        'tipo': tipo,
        'todas_msg_st': Mensagem.objects.filter(professor=professor, sentenca=True, resposta=False, lido=False).count(),
        'todas_msg_oab': Mensagem.objects.filter(professor=professor, oab=True, resposta=False, lido=False).count()
    }
    if pk and tipo == 'cr':
        context['pagina'] = 'mensagens'
        curso = get_object_or_404(Curso, id=pk)
        context['pagina'] = 'mensagens'
        context['submenu'] = curso
        todas_msg = Mensagem.objects.filter(professor=professor, curso=curso).order_by('-data')
        context['todas_msg'] = todas_msg
        msgs = todas_msg.values('aluno').annotate(Count('aluno'))
        alunos = Aluno.objects.filter(id__in=map(lambda x: x['aluno'], msgs))
        alunos_msg = []
        for aluno in curso.get_alunos:
            alunos_msg.append({
                'aluno': aluno,
                'msg_count': Mensagem.objects.filter(
                    aluno=aluno, professor=professor, curso=curso, resposta=False, lido=False
                ).count()
            })
        context['alunos_msg'] = alunos_msg
    elif tipo == 'st':
        context['pagina'] = 'mensagens'
        todas_msg = Mensagem.objects.filter(professor=professor, sentenca=True).order_by('-data')
        context['todas_msg'] = todas_msg
        msgs = todas_msg.values('aluno').annotate(Count('aluno'))
        alunos = Aluno.objects.filter(id__in=map(lambda x: x['aluno'], msgs))
        alunos_msg = []
        for aluno in alunos:
            alunos_msg.append({
                'aluno': aluno,
                'msg_count': Mensagem.objects.filter(
                    aluno=aluno, professor=professor, sentenca=True, resposta=False, lido=False
                ).count()
            })
        context['alunos_msg'] = alunos_msg
    elif tipo == 'oab':
        context['pagina'] = 'mensagens'
        todas_msg = Mensagem.objects.filter(professor=professor, oab=True).order_by('-data')
        context['todas_msg'] = todas_msg
        msgs = todas_msg.values('aluno').annotate(Count('aluno'))
        alunos = Aluno.objects.filter(id__in=map(lambda x: x['aluno'], msgs))
        alunos_msg = []
        for aluno in alunos:
            alunos_msg.append({
                'aluno': aluno,
                'msg_count': Mensagem.objects.filter(
                    aluno=aluno, professor=professor, oab=True, resposta=False, lido=False
                ).count()
            })
        context['alunos_msg'] = alunos_msg

    cursors = professor.curso_set.filter(sentenca_oab__isnull=True, sentenca_avulsa__isnull=True)
    msg_cursos = []
    filtro = 'N'
    if request.method == 'POST':
        filtro = request.POST.get('filtro')
    context['filtro'] = filtro
    for curso in cursors:
        n = curso.mensagem_set.filter(professor=professor, resposta=False, lido=False).count()
        if filtro == 'N':
            if n:
                msg_cursos.append({
                    'curso': curso,
                    'msg_naolidas': n
                })
        else:
            msg_cursos.append({
                'curso': curso,
                'msg_naolidas': n
            })
    context['msg_cursos'] = msg_cursos
    return render(request, 'professor/mensagens.html', context)


@login_required
def get_message(request):

    tipo = request.GET.get('tipo')
    aid = request.GET.get('aid')
    pid = request.GET.get('pid')
    cid = request.GET.get('cid')
    msg = []
    if tipo == 'prof':
        aluno = Aluno.objects.get(id=aid)
        if not aid or aid == 'false':
            if cid == 'st':
                todas_msg = Mensagem.objects.filter(sentenca=True, professor=request.user.professor).order_by('-data')
            else:
                todas_msg = Mensagem.objects.filter(curso_id=cid, professor=request.user.professor).order_by('-data')

        else:
            if cid == 'st':
                todas_msg = Mensagem.objects.filter(aluno=aluno, professor_id=request.user.professor).order_by('-data')
            else:
                todas_msg = Mensagem.objects.filter(
                    aluno=aluno, curso_id=cid, professor_id=request.user.professor
                ).order_by('-data')
    else:
        aluno = request.user.aluno
        if not pid or pid == 'false':
            ocursos = Curso.objects.get(id=cid)
            todas_msg = Mensagem.objects.filter(
                aluno=aluno, curso_id=cid, professor__in=ocursos.professores.all()
            ).order_by('-data')
        else:
            if cid == 'st':
                todas_msg = Mensagem.objects.filter(aluno=aluno, professor_id=pid, sentenca=True).order_by('-data')
            elif cid == 'oab':
                todas_msg = Mensagem.objects.filter(aluno=aluno, professor_id=pid, oab=True).order_by('-data')
            else:
                todas_msg = Mensagem.objects.filter(aluno=aluno, curso_id=cid, professor_id=pid).order_by('-data')

    for mensagem in todas_msg:
        msg.append(dict(
            aluno_id=mensagem.aluno.id,
            aluno=mensagem.aluno.nome,
            professor=mensagem.professor.nome,
            texto=mensagem.html,
            aluno_url=mensagem.aluno.get_absolute_url(),
            img_url=mensagem.aluno.foto_url,
            img_prof_url=mensagem.professor.foto_url,
            data=mensagem.str_data,
            lido=mensagem.lido,
            mensagem_id=mensagem.id,
            resposta=mensagem.resposta,
            is_professor=mensagem.resposta

        ))
    return JsonResponse(msg, safe=False)


@login_required
@user_passes_test(test_login)
def redigir_correcao(request, pk):
    tarefa_atividade = get_object_or_404(TarefaAtividade, pk=pk)
    context = {
        'menu': 'Correção',
        'tarefa': tarefa_atividade,
        'video_url': request.session.get('videos')
    }
    return render(request, 'professor/redigir-correcao.html', context)


def render_tabela(tabela_correcao, tarefa_atividade):
    br = u'<br/>'
    hr = u'<hr/>'
    texto = u'<h3><center>CORREÇÃO INDIVIDUALIZADA</center></h3>'
    texto += hr
    texto += tarefa_atividade.atividade.formulario.texto
    texto += br
    texto += u'<table style="border: 1px solid black;">'
    texto += u'    <tr style="border: 1px solid black;">'
    texto += u'        <th style="border: 1px solid black;" colspan="3">Correção individualizada</th>'
    texto += u'    </tr>'
    for tabela in tabela_correcao.tabelas.all():
        texto += u'    <tr style="border: 1px solid black;">'
        texto += u'        <td style="border: 1px solid black;"><center>Item</center></td>'
        texto += u'        <td style="border: 1px solid black;"><center>Valor</center></td>'
        texto += u'        <td style="border: 1px solid black;"><center>Nota</center></td>'
        texto += u'    </tr>'

        txt = u'<h4><strong>%s</strong></h4>' % tabela.tabela.item
        txt += tabela.tabela.comentarios
        for nota in tabela.notas.all().order_by('-id'):
            txt += nota.texto

        if tabela.texto:
            txt += tabela.texto
        texto += u'    <tr style="border: 1px solid black;">'
        texto += u'        <td style="border: 1px solid black; padding: 0px 15px 15px 15px;">%s</td>' % txt
        texto += u'        <td style="padding-top: 20px; border: 1px solid black; font-size: 1em" valign="top"><center><strong>%.02f</strong></center></td>' % tabela.tabela.valor
        texto += u'        <td style="padding-top: 20px; border: 1px solid black; font-size: 1em" valign="top"><center><strong>%.02f</strong></center></td>' % tabela.nota
        texto += u'    </tr>'
    texto += u'</table>'

    if tabela_correcao.texto:
        texto += br
        texto += u'<h4><strong>Comentário final do professor:</strong></h4>'
        texto += tabela_correcao.texto
    texto += br
    texto += u'<h4>Nota obtida: <strong>%.02f</strong></h4>' % tabela_correcao.total().get('nota')
    return texto


@login_required
@user_passes_test(test_login)
def formulario_correcao(request, pk):
    tarefa_atividade = get_object_or_404(TarefaAtividade, pk=pk)
    context = {
        'menu': 'Correção',
        'tarefa': tarefa_atividade
    }
    if request.method == 'POST':
        action = request.POST.get('action')
        tabela_correcao = TabelaCorrecaoAluno.objects.get(pk=request.POST.get('tabela-pk'))
        if action == 'finalizar_recurso':
            tabela_correcao.status = 'analisado'
            tabela_correcao.save()
            texto = render_tabela(tabela_correcao, tarefa_atividade)
            tarefa_atividade.gabarito = texto
            tarefa_atividade.save()
            enviar_email(
                'curso/email/sentenca-analisado.html', 'Seu recurso foi julgado!',
                [tarefa_atividade.aluno.email],
                context={'tarefa': tarefa_atividade},
                ead=True
            )
        if action == 'comentar':
            tabela_correcao.texto = request.POST.get('comentario-professor')
            tabela_correcao.save()

            if request.POST.get('finalizar') == 'on':
                # tabela_correcao = TabelaCorrecaoAluno.objects.filter(
                #     aluno=tarefa_atividade.aluno, formulario=tarefa_atividade.atividade.formulario
                # ).first()
                tabela_correcao.corrigido = True
                tabela_correcao.data_correcao = timezone.now()
                tabela_correcao.save()
                texto = render_tabela(tabela_correcao, tarefa_atividade)
                tarefa_atividade.corrigido = True
                tarefa_atividade.gabarito = texto
                tarefa_atividade.save()

                messages.success(request, 'Correção finalizada.')
                # ENVIAR EMAIL
                tarefa = tarefa_atividade
                enviar_email('curso/email/correcao-enviada.html', 'Sua atividade foi corrigida!',
                             [tarefa.aluno.email], context={'tarefa': tarefa}, ead=True)
                o_curso = tarefa.atividade.curso
                limitar_correcao = o_curso.limitar_correcao
                aluno = tarefa.aluno
                tarefas_concluidas = TarefaAtividade.objects.filter(
                    atividade__tipo_retorno='C',
                    atividade__curso=o_curso,
                    aluno_id=aluno,
                    corrigido=True,
                )
                if limitar_correcao and tarefas_concluidas.count() >= limitar_correcao:
                    tarefas_pendentes = TarefaAtividade.objects.filter(
                        atividade__tipo_retorno='C',
                        atividade__curso=o_curso,
                        aluno_id=aluno,
                        corrigido=False,
                        limitada=False
                    ).exclude(id=tarefa.pk)
                    tarefas_pendentes.update(limitada=True)

            else:
                messages.success(request, 'Comentário final atualizado.')
            tabela_correcao.save()

        elif action == 'texto-tabela':
            tabela_aluno = TabelaAluno.objects.get(pk=request.POST.get('tabela-correcao-pk'))
            tabela_aluno.texto = request.POST.get('texto-corecao')
            tabela_aluno.save()
            messages.success(request, 'Texto atualizado.')
        elif action == 'nota':
            data = request.POST

            for k in data.keys():
                if not k.startswith('tabela'):
                    continue
                key, value = k.split('-')
                if key == 'tabela':
                    tabela_aluno = TabelaAluno.objects.get(pk=value)

                    tabela_aluno.notas.clear()
                    for nota in request.POST.getlist('notas-%s' % value):
                        onota = Nota.objects.get(pk=nota)
                        tabela_aluno.notas.add(onota.pk)

                    cnota = request.POST.get('nota-%s' % value)
                    if request.POST.get('renderizar-%s' % value) == 'on':
                        tabela_aluno.nota = cnota
                        tabela_aluno.nota_calc = True
                    else:
                        tabela_aluno.nota = Decimal(tabela_aluno.tabela.valor) - Decimal(tabela_aluno.total_notas())
                        tabela_aluno.nota_calc = False
                    tabela_aluno.save()
            messages.success(request, 'Correção atualizada.')
        return HttpResponseRedirect(reverse('professor:formulario-correcao', kwargs={'pk': pk}))
    else:
        try:
            formulario = Formulario.objects.get(atividade=tarefa_atividade.atividade)
            tabela_correcao = TabelaCorrecaoAluno.objects.filter(
                aluno=tarefa_atividade.aluno, formulario=formulario
            ).first()
            if not tabela_correcao:
                tabela_correcao = TabelaCorrecaoAluno(
                    aluno=tarefa_atividade.aluno,
                    formulario=formulario,
                    professor=request.user.professor
                )
                tabela_correcao.save()

            for tabela in tabela_correcao.formulario.tabelas.all():
                try:
                    TabelaAluno.objects.get(tabela_correcao=tabela_correcao, tabela=tabela)
                except TabelaAluno.DoesNotExist:
                    tabela_aluno = TabelaAluno(
                        tabela_correcao=tabela_correcao,
                        tabela=tabela
                    )
                    tabela_aluno.save()
            tabelas_aluno = tabela_correcao.tabelas.all()
        except Formulario.DoesNotExist:
            tabela_correcao = tabelas_aluno = formulario = False
        context.update({
            'formulario': formulario,
            'tabelas': tabelas_aluno,
            'tabela_correcao': tabela_correcao
        })

    return render(request, 'professor/formulario-correcao.html', context)


def render_tabela_sentenca(request, tabela_correcao, sentenca_avulsa_aluno):
    tabela_correcao.corrigido = True
    tabela_correcao.data_correcao = timezone.now()
    tabela_correcao.professor = request.user.professor
    tabela_correcao.save()
    br = u'<br/>'
    hr = u'<hr/>'
    texto = u'<h3><center>CORREÇÃO INDIVIDUALIZADA</center></h3>'
    texto += hr
    texto += sentenca_avulsa_aluno.sentenca_avulsa.formulario.texto
    texto += br
    texto += u'<table style="border: 1px solid black; width: 100%;">'
    texto += u'    <tr style="border: 1px solid black;">'
    texto += u'        <th style="padding-top: 4px; border: 1px solid black;" ' \
             u'colspan="3">Correção individualizada</th>'
    texto += u'    </tr>'
    for tabela in tabela_correcao.tabelas.all():
        texto += u'    <tr style="border: 1px solid black;">'
        texto += u'        <td style="padding-top: 4px; border: 1px solid black;">' \
                 u'<center>Item</center></td>'
        texto += u'        <td style="padding-top: 4px; border: 1px solid black;">' \
                 u'<center>Valor</center></td>'
        texto += u'        <td style="padding-top: 4px; border: 1px solid black;">' \
                 u'<center>Nota</center></td>'
        texto += u'    </tr>'

        txt = u'<h4><strong>%s</strong></h4>' % tabela.tabela.item
        txt += tabela.tabela.comentarios
        for nota in tabela.notas.all():
            txt += nota.texto

        if tabela.texto:
            txt += tabela.texto
        texto += u'    <tr style="border: 1px solid black;">'
        texto += u'        <td style="width: 90%; border: 1px solid black; padding: 4px 15px 15px 15px;">{}</td>'.\
            format(txt)
        texto += u'        <td style="width: 5%%; padding-top: 20px; border: 1px solid black; font-size: 1em"' \
                 u' valign="top"><center><strong>%.02f</strong></center></td>' % tabela.tabela.valor
        texto += u'        <td style="width: 5%%; padding-top: 20px; border: 1px solid black; font-size: 1em"' \
                 u' valign="top"><center><strong>%.02f</strong></center></td>' % tabela.nota
        texto += u'    </tr>'
    texto += u'</table>'

    if tabela_correcao.texto:
        texto += br
        texto += u'<h4><strong>Comentário final do professor:</strong></h4>'
        texto += tabela_correcao.texto
    texto += br
    texto += u'<h4>Nota obtida: <strong>%.02f</strong></h4>' % tabela_correcao.total().get('nota')

    sentenca_avulsa_aluno.status = 'C'
    sentenca_avulsa_aluno.correcao_individual = texto

    sentenca_avulsa_aluno.save()
    messages.success(request, 'Correção finalizada.')

    # ENVIAR EMAIL
    enviar_email('curso/email/sentenca-corrigida.html', 'Sua sentença já foi corrigida!',
                 [sentenca_avulsa_aluno.aluno.email], context={'sentenca': sentenca_avulsa_aluno}, ead=True)
    return texto


@login_required
@user_passes_test(test_login)
def formulario_correcao_sentenca(request, pk):
    sentenca_avulsa_aluno = get_object_or_404(SentencaAvulsaAluno, pk=pk)
    context = {
        'menu': 'Correção',
        'sentenca': sentenca_avulsa_aluno
    }
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'finalizar_recurso':
            tabela_correcao = TabelaCorrecaoAluno.objects.get(pk=request.POST.get('tabela-pk'))
            tabela_correcao.status = 'analisado'
            tabela_correcao.save()
            render_tabela_sentenca(request, tabela_correcao, sentenca_avulsa_aluno)
            enviar_email(
                'curso/email/sentenca-analisado.html', 'Seu recurso foi julgado!',
                [sentenca_avulsa_aluno.aluno.email],
                context={'sentenca': sentenca_avulsa_aluno},
                ead=True
            )
        if action == 'comentar':
            tabela_correcao = TabelaCorrecaoAluno.objects.get(pk=request.POST.get('tabela-pk'))
            tabela_correcao.texto = request.POST.get('comentario-professor')
            tabela_correcao.save()

            if request.POST.get('finalizar') == 'on':
                render_tabela_sentenca(request, tabela_correcao, sentenca_avulsa_aluno)

            else:
                messages.success(request, 'Comentário final atualizado.')
            tabela_correcao.save()

        elif action == 'texto-tabela':
            tabela_aluno = TabelaAluno.objects.get(pk=request.POST.get('tabela-correcao-pk'))
            tabela_aluno.texto = request.POST.get('texto-corecao')
            tabela_aluno.save()
            messages.success(request, 'Texto atualizado.')
        elif action == 'nota':
            data = request.POST

            for k in data.keys():
                if not k.startswith('tabela'):
                    continue
                key, value = k.split('-')
                if key == 'tabela':
                    tabela_aluno = TabelaAluno.objects.get(pk=value)

                    tabela_aluno.notas.clear()
                    for nota in request.POST.getlist('notas-%s' % value):
                        onota = Nota.objects.get(pk=nota)
                        tabela_aluno.notas.add(onota.pk)

                    cnota = request.POST.get('nota-%s' % value)
                    if request.POST.get('renderizar-%s' % value) == 'on':
                        tabela_aluno.nota = cnota
                        tabela_aluno.nota_calc = True
                    else:
                        tabela_aluno.nota = Decimal(tabela_aluno.tabela.valor) - Decimal(tabela_aluno.total_notas())
                        tabela_aluno.nota_calc = False
                    tabela_aluno.save()
            messages.success(request, 'Correção atualizada.')
        return HttpResponseRedirect(reverse('professor:formulario-correcao-sentenca', kwargs={'pk': pk}))
    else:
        try:
            formulario = Formulario.objects.get(sentenca_avulca=sentenca_avulsa_aluno.sentenca_avulsa)
            tabela_correcao = TabelaCorrecaoAluno.objects.filter(
                aluno=sentenca_avulsa_aluno.aluno, formulario=formulario
            ).first()
            if not tabela_correcao:
                tabela_correcao = TabelaCorrecaoAluno(
                    aluno=sentenca_avulsa_aluno.aluno, formulario=formulario
                )
                tabela_correcao.save()

            for tabela in tabela_correcao.formulario.tabelas.all():
                try:
                    TabelaAluno.objects.get(tabela_correcao=tabela_correcao, tabela=tabela)
                except TabelaAluno.DoesNotExist:
                    tabela_aluno = TabelaAluno(
                        tabela_correcao=tabela_correcao,
                        tabela=tabela
                    )
                    tabela_aluno.save()
            tabelas_aluno = tabela_correcao.tabelas.all()
        except Formulario.DoesNotExist:
            tabela_correcao = tabelas_aluno = formulario = False
        context.update({
            'formulario': formulario,
            'tabelas': tabelas_aluno,
            'tabela_correcao': tabela_correcao
        })

    return render(request, 'professor/formulario-sentenca.html', context)


def correcao_get_data(request):
    values = tabela_correcao = TabelaAluno.objects.values().get(pk=request.GET.get('pk'))
    # values = tabela_correcao.values()
    if not values.get('texto'):
        values['texto'] = ''
    return JsonResponse(values)


@csrf_exempt
def post_salvar_tabela(request):
    data = {
        'erro': False,
        'message': 'Nota atualizada.'
    }
    try:
        vals = request.POST
        pk = vals.getlist('pk')
        notas = vals.getlist('notas[]')
        nota = vals.get('nota')
        renderizar = vals.get('renderizar')

        tabela_aluno = TabelaAluno.objects.get(pk=pk[0])
        tabela_aluno.notas.clear()
        for cnota in notas:
            onota = Nota.objects.get(pk=cnota)
            tabela_aluno.notas.add(onota.pk)

        if renderizar == 'on':
            tabela_aluno.nota = nota
            tabela_aluno.nota_calc = True
        else:
            tabela_aluno.nota = Decimal(tabela_aluno.tabela.valor) - Decimal(tabela_aluno.total_notas())
            tabela_aluno.nota_calc = False
        tabela_aluno.save()
        total = TabelaAluno.objects.filter(
            tabela_correcao=tabela_aluno.tabela_correcao
        ).values('nota').aggregate(total=Sum('nota'))
        data['nota'] = '%.02f' % float(tabela_aluno.nota)
        data['total'] = '%.02f' % total.get('total')
        data['message'] = u'Correção: %03d - Atualizada' % tabela_aluno.pk
    except Exception as e:
        data['erro'] = True
        data['message'] = str(e)
    return JsonResponse(data)


@csrf_exempt
def formulario_recorrer(request):
    tabela_correcao_aluno = TabelaCorrecaoAluno.objects.get(pk=request.POST.get('pk'))
    if request.POST.get('tipo') == 'st':
        nome = tabela_correcao_aluno.formulario.sentenca_avulca.titulo
    else:
        nome = tabela_correcao_aluno.formulario.atividade.nome
    context = {
        'tabela_correcao': tabela_correcao_aluno
    }
    t = loader.get_template('professor/formulario-recorrer.html')
    c = Context(context)
    html = t.render(c)
    data = {
        'html': html,
        'atividade_nome': nome
    }
    return JsonResponse(data)


@csrf_exempt
def formulario_estatistica(request):
    atividade = Atividade.objects.get(pk=request.POST.get('pk'))
    context = {
        'atividade': atividade
    }
    average = []
    notas = []
    total = 0
    media_total = 0
    msg = False
    tabelas = TabelaCorrecaoAluno.objects.filter(corrigido=True, formulario__atividade=atividade)
    rendered = False
    try:
        formulario = atividade.formulario
    except Formulario.DoesNotExist:
        formulario = False
    if formulario:
        try:
            for tabela in tabelas:
                url = None
                try:
                    atividade = tabela.formulario.atividade
                    tarefa = TarefaAtividade.objects.get(atividade=atividade, aluno=tabela.aluno)
                    if tarefa.atividade.get_status().get('status') == 'Encerrado':
                        if tarefa.resposta:
                            url = '/curso/atividade/imprimir/%d/?action=resposta&notprint=sim' % tarefa.pk
                        elif tarefa.arquivo:
                            url = tarefa.arquivo.url
                except Exception as e:
                    print '>>>>', e
                notas.append({
                    'aluno': tabela.aluno,
                    'nota': tabela.total_aluno,
                    'url': url,
                    'tabela_pk': tabela.pk
                })

            for tbl in atividade.formulario.tabelas.all():
                media = TabelaAluno.objects.filter(
                    tabela__formulario__atividade=atividade, tabela_correcao__corrigido=True, tabela=tbl
                ).aggregate(total=Avg('nota')).get('total')
                media = media if media else 0
                average.append({
                    'tabela': tbl,
                    'avg': '%.02f' % media
                })
                total += tbl.valor
                media_total += media

            context.update({
                'notas': sorted(notas, key=itemgetter('nota'), reverse=True),
                'medias': average,
                'total': '%.02f' % total,
                'media_total': '%.02f' % media_total
            })
            t = loader.get_template('professor/formulario-estatistica.html')
            c = Context(context)
            rendered = t.render(c)
        except Exception as e:
            msg = str(e)
            raise e
    return JsonResponse({'html': rendered, 'message': msg})


@csrf_exempt
def formulario_estatistica_geral(request):
    curso = Curso.objects.get(pk=request.POST.get('pk'))
    atividades = curso.atividade_set.all()
    context = {
        'curso': curso,
        'atividades': atividades
    }
    notas_geral = {}
    media_geral = []
    total_geral = 0
    media_geral_total = 0
    for atividade in atividades:
        average = []
        notas = []
        total = 0
        media_total = 0
        msg = False
        tabelas = TabelaCorrecaoAluno.objects.filter(
            corrigido=True,
            formulario__atividade=atividade,
            formulario__atividade__resolucao_obrigatorio=True
        )
        rendered = False
        try:
            formulario = atividade.formulario
        except Formulario.DoesNotExist:
            formulario = False
        if formulario:
            try:
                for tabela in tabelas:
                    url = None
                    try:
                        atividade = tabela.formulario.atividade
                        tarefa = TarefaAtividade.objects.get(atividade=atividade, aluno=tabela.aluno)
                        if tarefa.atividade.get_status().get('status') == 'Encerrado':
                            if tarefa.resposta:
                                url = '/curso/atividade/imprimir/%d/?action=resposta&notprint=sim' % tarefa.pk
                            elif tarefa.arquivo:
                                url = tarefa.arquivo.url
                    except Exception as e:
                        print '>>>>', e
                    nota = float(tabela.total_aluno)
                    aluno = tabela.aluno
                    ngeral = notas_geral.get(aluno)
                    if ngeral:
                        notas_geral[aluno] = ngeral + nota
                    else:
                        notas_geral[aluno] = nota
                    notas.append({
                        'aluno': tabela.aluno,
                        'nota': tabela.total_aluno,
                        'url': url,
                        'tabela_pk': tabela.pk
                    })

                for tbl in atividade.formulario.tabelas.all():
                    media = TabelaAluno.objects.filter(
                        tabela__formulario__atividade=atividade, tabela_correcao__corrigido=True, tabela=tbl
                    ).aggregate(total=Avg('nota')).get('total')
                    media = media if media else 0
                    # average.append({
                    #     'tabela': tbl,
                    #     'avg': '%.02f' % media
                    # })
                    total += tbl.valor
                    media_total += media
                ctxm = {
                    # 'notas': sorted(notas, key=itemgetter('nota'), reverse=True),
                    'atividade': atividade,
                    # 'medias': average,
                    'total': total,
                    'media_total': media_total
                }
                media_geral_total += media_total
                total_geral += total
                media_geral.append(ctxm)
            except Exception as e:
                msg = str(e)
                raise e

    context['notas'] = sorted(notas_geral.items(), key=operator.itemgetter(1), reverse=True)
    context['medias_geral'] = sorted(media_geral, key=itemgetter('media_total'), reverse=True),
    context['media_geral_total'] = media_geral_total / len(media_geral)
    context['total_geral'] = total_geral / len(media_geral)
    t = loader.get_template('professor/formulario-estatistica-geral.html')
    c = Context(context)
    rendered = t.render(c)
    return JsonResponse({'html': rendered, 'message': msg})


@csrf_exempt
def formulario_estatistica_sentenca(request):
    sentenca = SentencaAvulsa.objects.get(pk=request.POST.get('pk'))
    context = {
        'sentenca': sentenca
    }
    average = []
    notas = []
    total = 0
    media_total = 0
    msg = False
    tabelas = TabelaCorrecaoAluno.objects.filter(corrigido=True, formulario__sentenca_avulca=sentenca)
    rendered = False
    try:
        formulario = sentenca.formulario
    except Formulario.DoesNotExist:
        formulario = False
    if formulario:
        # try:
            for tabela in tabelas:
                url = None
                try:
                    sentenca_avulca = tabela.formulario.sentenca_avulca
                    sentenca_aluno = SentencaAvulsaAluno.objects.get(aluno=tabela.aluno, sentenca_avulsa=sentenca_avulca)
                except Exception as e:
                    sentenca_aluno = None
                notas.append({
                    'aluno': tabela.aluno,
                    'nota': tabela.total_aluno,
                    'sentenca': sentenca_aluno,
                    'tabela_pk': tabela.pk
                })

            for tbl in sentenca.formulario.tabelas.all():
                media = TabelaAluno.objects.filter(
                    tabela__formulario__sentenca_avulca=sentenca, tabela_correcao__corrigido=True,
                    tabela=tbl
                ).aggregate(total=Avg('nota')).get('total')
                media = media if media else 0
                average.append({
                    'tabela': tbl,
                    'avg': '%.02f' % media
                })
                total += tbl.valor
                media_total += media

            context.update({
                'notas': sorted(notas, key=itemgetter('nota'), reverse=True),
                'medias': average,
                'total': '%.02f' % total,
                'media_total': '%.02f' % media_total
            })
            t = loader.get_template('professor/formulario-estatistica-sentenca.html')
            c = Context(context)
            rendered = t.render(c)
        # except Exception as e:
        #     msg = str(e)
        #     raise e
    return JsonResponse({'html': rendered, 'message': msg})


@csrf_exempt
def formulario_estatistica_correcao(request):
    correcao = TabelaCorrecaoAluno.objects.get(pk=request.POST.get('pk'))
    context = {
        'tabelas': correcao.tabelas.all(),
        'tabela_correcao': correcao
    }
    msg = False
    try:
        t = loader.get_template('professor/formulario-estatistica-correcao.html')
        c = Context(context)
        rendered = t.render(c)
    except Exception as e:
        msg = str(e)
        raise e
    return JsonResponse({'html': rendered, 'message': msg})


@csrf_exempt
def salvar_comentario_professor(request):
    erro = False
    msg = 'Comentário atualizado!'
    try:
        data = request.POST
        action = data.get('action')
        texto = data.get('texto')
        if not texto:
            texto = None
        tabela = TabelaAluno.objects.get(pk=data.get('pk'))
        tabela_correcao = tabela.tabela_correcao
        if action == 'salvar_comentario':
            tabela.texto = texto
            tabela.save()
        elif action == 'salvar_justificativa':
            tabela.texto_justificativa = texto
            tabela.save()

            if tabela_correcao.status in ['solicitado', 'analise']:
                tabelas_count = tabela_correcao.tabelas.filter(texto_justificativa__isnull=False).count()
                st = 'analise' if tabelas_count else 'solicitado'
                tabela_correcao.status = st
                tabela_correcao.save()

            msg = 'Justificativa atualizada!'
    except Exception as e:
        msg = str(e)
        erro = True
    return JsonResponse({
        'message': msg,
        'erro': erro,
        'texto': texto,
        'status': tabela_correcao.get_status_display(),
        'color': tabela_correcao.status_color,
    })


@csrf_exempt
def salvar_item_recorrer(request):
    erro = False
    msg = 'Item atualizado!'
    try:
        data = request.POST
        txt = data.get('texto')
        tabela = TabelaAluno.objects.get(pk=data.get('pk'))
        if not txt:
            txt = None
        tabela.texto_recurso = txt
        tabela.save()
    except Exception as e:
        msg = str(e)
        erro = True
    return JsonResponse({
        'message': msg,
        'erro': erro,
        'recorrido': tabela.recorrido
    })


@csrf_exempt
def post_confirmar_recorrer(request):
    erro = False
    msg = 'Envado para o professor!'
    try:
        data = request.POST
        tabela_c = TabelaCorrecaoAluno.objects.get(pk=data.get('pk'))
        if tabela_c.status == 'corrigido':
            tabelas_count = tabela_c.tabelas.filter(texto_recurso__isnull=False).count()
            if not tabelas_count:
                msg = u'Nenhum dos itens da sentença foi marcado como recorrido. Escreva os fundamentos de seu ' \
                      u'recurso em cada item em relação ao qual deseje recorrer e, depois, clique no respectivo ' \
                      u'símbolo de salvar à direita. Só então finalize seu recurso.'
                erro = True
            else:
                tabela_c.status = 'solicitado'
                tabela_c.data_solicitacao = timezone.now()
                tabela_c.save()
                msg = u'Seu recurso foi salvo corretamente no sistema e enviado para análise do professor. Quando a ' \
                      u'análise do recurso for finalizada, você receberá um aviso por e-mail.'
        else:
            erro = True
            msg = u'Ação não disponível'
    except Exception as e:
        msg = str(e)
        erro = True
    return JsonResponse({
        'message': msg,
        'erro': erro
    })


def get_sentenca_aluno(request, pk):
    tabela_aluno = get_object_or_404(TabelaAluno, pk=pk)
    return JsonResponse({})
