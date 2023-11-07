# -*- coding: utf-8 -*-
# Autor: christian
from __future__ import unicode_literals

import datetime
import json
import uuid
from collections import OrderedDict
from decimal import Decimal

import xmltodict
from dateutil import parser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.validators import ValidationError, validate_email
from django.db.models import Count, Q
from django.db.transaction import atomic
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from apps.aluno.models import Aluno
from apps.curso.templatetags.curso import moeda_nosymbol
from apps.enunciado.models import (Cargo, Concurso, Disciplina, EsferaEspecifica, Localidade, TipoPecaPratica,
                                   TipoProcedimento)
from apps.pagseguro.api import PagSeguroApiTransparent, PagSeguroItem
from apps.pagseguro.models import Checkout, Transaction
from apps.pagseguro.settings import TRANSACTION_STATUS
from apps.professor.models import Professor
from apps.website.models import Anuncio, WhatsAppGroup
from apps.website.utils import enviar_email, enviar_email_old
from carton.cart import Cart
from libs.util.tipos import ESTADOS_BRASILEIROS_NOMES
from .models import (Atividade, Categoria, CheckoutItens, ComboAluno, Cortesia, Curso, CursoAvaliacao, CursoGratis,
                     LiberarCompraCurso, SentencaAvulsaAluno, SentencaOABAvulsaAluno, Serie, Simulado, TarefaAtividade)
import logging

logger = logging.getLogger("django")

def get_curso_url(curso):
    categoria_obj = curso.categoria
    if categoria_obj.tipo == 'S':
        url = reverse("aluno:sentencas-avulsas")
    elif categoria_obj.tipo == 'D':
        url = reverse("aluno:simuladoinfo", args=[curso.simulado_id])
    else:
        url = reverse("aluno:sentencas-oab")
    return url


def create_checkout(curso, aluno, request=None):
    now = timezone.now()
    checkout_obj = Checkout.objects.create(
        code=uuid.uuid4().hex,
        aluno=aluno,
        date=now,
        success=True,
        transaction_type=1,
        transaction_status=3
    )
    Transaction.objects.create(
        code=checkout_obj.code,
        checkout=checkout_obj,
        status='pago'

    )
    CheckoutItens.objects.create(
        checkout=checkout_obj,
        curso=curso,
        qtda=1,
        valor=0
    )
    if request:
        msg = "Voce adquiriu gratuitamente o(a)</br></br> {}: {}.</br></br>" \
              " <a href='{}'>Clique aqui</a> para acessar".format(
            curso.categoria.nome, curso, get_curso_url(curso)
        )
        messages.success(request, msg)
    return checkout_obj


@require_POST
@login_required
def relatorio(request):
    filename = 'relatorio'
    filtro = [Q(success=True)]
    count = total = desc = 0
    txt = 'Nome                                                                             C.P.F           Data        Vl Tot Status\n'
    txt += 'Produto                                                                          QTDA.                Valor   Total           \n'
    txt += '================================================================================ =============== ========== ======= ==========\n'
    mes = request.POST.get('mes')
    ano = request.POST.get('ano')
    curso = request.POST.get('curso')
    if mes:
        filename += '-' + mes
        filtro.append(Q(date__month=mes))
    if ano:
        filename += '-' + ano
        filtro.append(Q(date__year=ano))
    if curso:
        filename += '-' + curso
        filtro.append(Q(checkoutitens__curso_id=curso))
    chks = Checkout.objects.filter(*filtro).order_by('-date')
    for chk in chks:
        try:
            transc = chk.transaction
            if transc.status not in ['pago', 'disponivel']:
                continue
        except:
            continue
        count += 1
        try:
            aluno_nome = chk.aluno.nome
            aluno_email = chk.aluno.email
        except:
            aluno_nome = 'N/A'
            aluno_email = 'N/A'

        txt += u'{0:80s} {1:15s} {2} {3:7f} {4:10s}\n'.format(
            u'{0} ({1})'.format(aluno_nome, aluno_email), chk.cpf or '', chk.date.strftime('%d/%m/%Y'),
            chk.total, transc.get_status_display()
        )
        txt += u'{0:107s} {1:7.2f} {2:10.2f}\n'.format(
            '', Decimal(chk.get_desconto), chk.total + Decimal(chk.get_desconto)
        )
        total += chk.total
        desc += Decimal(chk.get_desconto)
        endereco = chk.get_endereco_ps
        if endereco['logradouro']:
            txt += u'{0}, {1} - {2}\n'.format(endereco['logradouro'], endereco['numero'], endereco['bairro'])
            txt += u'{0} - {1}/{2}\n'.format(endereco['cep'], endereco['cidade'], endereco['uf'])
        else:
            txt += u'*** Sem endereço ***\n'
        # txt += '-' * 50 + '\n'
        items = chk.checkoutitens_set.all()
        inc = 0
        if items.count():
            txt += '-------------------------------------------------------------------------------- --------------- ---------- ------- ----------\n'
        for item in items:
            txt += u'{1:80s}             {0:03d} {2:10f} {3:7f}\n'.format(
                item.qtda, item, item.valor, item.total
            )
            inc += 1
            ic = items.count()
            if ic > 1 and ic != inc:
                txt += '------------------------------------------------------------------------------- --------------- ---------- ------- ----------\n'
        txt += '================================================================================ =============== ========== ==================\n'
    txt += 'Qtda de Registros: {0:03d} de {0:03d}\n'.format(count, chks.count())
    txt += 'Total............:          {0:9.2f}\n'.format(total)
    txt += 'Desconto.........:          {0:9.2f}\n'.format(desc)
    txt += 'Subtotal.........:          {0:9.2f}'.format(total + desc)
    response = HttpResponse(txt, content_type='text/plain; charset=utf8')
    response['Content-Disposition'] = 'attachment; filename="{}.txt"'.format(filename)
    return response


def categoria(request, slug):
    obj_categoria = get_object_or_404(Categoria, slug=slug)
    user = request.user

    if request.method == "POST":
        curso = Curso.objects.get(id=request.POST.get("curso_id"))
        create_checkout(curso, user.aluno, request)
        return HttpResponseRedirect(reverse("curso:categoria", args=[obj_categoria.slug]))

    now = timezone.now()
    ocursos = Curso.objects.filter(
        categoria=obj_categoria, aluno__isnull=True
    )
    context = {
        'categoria': obj_categoria,
        'cursos': ocursos,
        'cursos_inativos': True
    }
    if request.method == 'GET':
        inativos = request.GET.get('inativos', 'nao')
        if inativos == 'nao':
            args = [Q(data_fim__gte=now) | Q(data_fim__isnull=True)]
            ocursos = ocursos.filter(*args)
            if user.is_authenticated():
                try:
                    l_cursos = LiberarCompraCurso.objects.filter(
                        curso__categoria=obj_categoria,
                        aluno=user.aluno,
                        data__gte=now,
                        ativo=True
                    )
                    lcursos = map(lambda x: x, ocursos)
                    for l in l_cursos:
                        c = l.curso
                        if c not in lcursos:
                            lcursos.append(c)
                    ocursos = lcursos
                except Aluno.DoesNotExist:
                    print('not aluno')

        context['cursos'] = ocursos
        context['inativos'] = inativos
    if obj_categoria.tipo in ['S', 'O', 'D']:
        kwargs = {
            'sentencaavulsa__isnull': False
        }

        if obj_categoria.tipo == 'O':
            kwargs = {'sentencaoab__isnull': False}
            # TIPOS PECA
            tipos_peca = TipoPecaPratica.objects.filter(**kwargs).values(
                'id', 'nome').annotate(t=Count('id'))
            context['tipos_peca'] = tipos_peca
            professores = Professor.objects.filter(**kwargs).values(
                'id', 'nome').annotate(t=Count('id'))
            context['professores'] = professores
        elif obj_categoria.tipo == 'D':
            kwargs = {
                'simulado__isnull': False
            }
            context.update(
                esferas_especificas=EsferaEspecifica.objects.filter(
                    simulado__curso__categoria__tipo='D'
                ).values('id', 'nome').annotate(t=Count('id')),
                cargos=Cargo.objects.filter(
                    simulado__curso__categoria__tipo='D'
                ).values('id', 'nome').annotate(t=Count('id')),
                concursos=Concurso.objects.filter(
                    simulado__curso__categoria__tipo='D'
                ).values('id', 'nome').annotate(t=Count('id')),
                localidades=Localidade.objects.filter(
                    simulado__curso__categoria__tipo='D'
                ).values('id', 'nome').annotate(t=Count('id'))
            )
        else:
            # ESFERAS_ESPECIFICAS
            esferas_especificas = EsferaEspecifica.objects.filter(**kwargs).values(
                'id', 'nome').annotate(t=Count('id'))
            context['esferas_especificas'] = esferas_especificas
            # TIPOS PROCEDIMENTO
            tipos_procedimento = TipoProcedimento.objects.filter(**kwargs).values(
                'id', 'nome').annotate(t=Count('id'))
            context['tipos_procedimento'] = tipos_procedimento
        if obj_categoria.tipo != "D":
            # DISCIPLINAS
            disciplinas = Disciplina.objects.filter(**kwargs).values(
                'id', 'nome').annotate(t=Count('id'))
            context['disciplinas'] = disciplinas
        if request.method == 'POST':
            data = dict(request.POST)
            data.pop('csrfmiddlewaretoken')
            kwargs = {'categoria': obj_categoria}
            for k, v in data.iteritems():
                v = v[0]
                if v:
                    kwargs[k] = v
            ocursos = Curso.objects.filter(**kwargs)
            context['cursos'] = ocursos
            context['filtro'] = kwargs

    return render(request, 'listagem-cursos.html', context)


def serie(request, slug):
    obj_serie = get_object_or_404(Serie, slug=slug)
    series = obj_serie.cursogratis_set.all()
    context = {
        'serie': obj_serie,
        'series': series,
    }
    return render(request, 'listagem-serie.html', context)


def curso_gratis(request, slug):
    obj_curso = get_object_or_404(CursoGratis, slug=slug)
    videos = obj_curso.videogratis_set.filter(Q(data_ini__lte=timezone.now()) | Q(data_ini=None))
    context = {
        'curso': obj_curso,
        'videos': videos,
        'anuncios': Anuncio.objects.filter(pag_curso_gratis=True, ativo=True)
    }

    return render(request, 'detalhe-curso-gratis.html', context)


def curso(request, slug):
    obj_curso = get_object_or_404(Curso, slug=slug)
    cursos = Curso.objects.filter(categoria=obj_curso.categoria).exclude(id=obj_curso.id)

    aval_otimo = CursoAvaliacao.objects.filter(curso_id=obj_curso.id, avaliacao='O').count()
    aval_bom = CursoAvaliacao.objects.filter(curso_id=obj_curso.id, avaliacao='B').count()
    aval_ruim = CursoAvaliacao.objects.filter(curso_id=obj_curso.id, avaliacao='R').count()
    try:
        objcheckout = CheckoutItens.objects.filter(curso=obj_curso, checkout__aluno=request.user.aluno).first()
    except:
        objcheckout = None
    context = {
        'curso': obj_curso,
        'cursos': cursos,
        'checkout': objcheckout,
        'anuncios': Anuncio.objects.filter(pag_cursos=True, ativo=True),
        'avaliacao': {
            'otimo': aval_otimo,
            'bom': aval_bom,
            'ruim': aval_ruim,
            'total': (aval_otimo + aval_bom + aval_ruim)
        }
    }
    return render(request, 'detalhe-curso.html', context)


def pre_inscricao(request):
    now = timezone.now()
    grupos = WhatsAppGroup.objects.filter(ativo=True)
    cursos = [x.curso for x in grupos]
    context = {
        "cursos": cursos
    }
    return render(request, 'pre_inscricao.html', context=context)


def livro(request, slug):
    obj_livro = get_object_or_404(Curso, slug=slug)

    aval_otimo = CursoAvaliacao.objects.filter(curso_id=obj_livro.id, avaliacao='O').count()
    aval_bom = CursoAvaliacao.objects.filter(curso_id=obj_livro.id, avaliacao='B').count()
    aval_ruim = CursoAvaliacao.objects.filter(curso_id=obj_livro.id, avaliacao='R').count()
    try:
        objcheckout = CheckoutItens.objects.filter(curso=obj_livro, checkout__aluno=request.user.aluno).first()
    except:
        objcheckout = None

    ctx = {
        'checkout': objcheckout,
        'titulo': obj_livro.nome,
        'livro': obj_livro,
        'avaliacao': {
            'otimo': aval_otimo,
            'bom': aval_bom,
            'ruim': aval_ruim,
            'total': (aval_otimo + aval_bom + aval_ruim)
        }
    }
    return render(request, 'detalhe-livro.html', ctx)


def curso_sentenca(request, slug):
    obj_curso = get_object_or_404(Curso, slug=slug)
    if request.method == "POST":
        create_checkout(obj_curso, request.user.aluno, request)
        return HttpResponseRedirect(reverse("curso:curso-sentenca", args=[obj_curso.slug]))

    cursos = Curso.objects.filter(categoria=obj_curso.categoria).exclude(id=obj_curso.id)
    try:
        objcheckout = CheckoutItens.objects.filter(curso=obj_curso, checkout__aluno=request.user.aluno).last()
        checkout = objcheckout.checkout
        if checkout.transaction_status in [6, 7]:
            checkout.delete()
            objcheckout = None
    except:
        objcheckout = checkout = None
    obj_categoria = obj_curso.categoria
    context = {
        'curso': obj_curso,
        'categoria': obj_categoria,
        'cursos': cursos,
        'checkout': checkout,
        'anuncios': Anuncio.objects.filter(pag_cursos=True, ativo=True),
        'action': request.GET.get('action')
    }
    if obj_categoria.tipo in ['S', 'O']:
        kwargs = {'sentencaavulsa__isnull': False}
        if obj_categoria.tipo == 'O':
            kwargs = {'sentencaoab__isnull': False}
            # TIPOS PECA
            tipos_peca = TipoPecaPratica.objects.filter(**kwargs).values(
                'id', 'nome').annotate(t=Count('id'))
            context['tipos_peca'] = tipos_peca
            professores = Professor.objects.filter(**kwargs).values(
                'id', 'nome').annotate(t=Count('id'))
            context['professores'] = professores
        else:
            # ESFERAS_ESPECIFICAS
            esferas_especificas = EsferaEspecifica.objects.filter(**kwargs).values(
                'id', 'nome').annotate(t=Count('id'))
            context['esferas_especificas'] = esferas_especificas
            # TIPOS PROCEDIMENTO
            tipos_procedimento = TipoProcedimento.objects.filter(**kwargs).values(
                'id', 'nome').annotate(t=Count('id'))
            context['tipos_procedimento'] = tipos_procedimento
        # DISCIPLINAS
        disciplinas = Disciplina.objects.filter(**kwargs).values(
            'id', 'nome').annotate(t=Count('id'))
        context['disciplinas'] = disciplinas
    return render(request, 'detalhe-curso-sentenca.html', context)


class CursoSimuladoListView(ListView):
    model = Simulado


def cursos(request):
    now = timezone.now()
    cursos = Curso.objects.filter(data_ini__gt=now).exclude(categoria__tipo="B")
    context = {
        "cursos": cursos
    }
    return render(request, 'listagem-cursos.html', context=context)


def carrinho(request):
    return HttpResponseRedirect(reverse_lazy('checkout:cart'))


@login_required
@csrf_exempt
def get_payment_methods(request):
    ctx = {}
    if request.method == 'POST':
        ctx = {
            'pgtos': request.POST.get('payments')
        }
    return render(request, 'get-payment-methods.html', ctx)


@login_required
@csrf_exempt
def carrinho_pagamento(request):
    ctx = {
        'aluno': request.user.aluno,
        'estados': ESTADOS_BRASILEIROS_NOMES
    }
    cart = Cart(request.session)
    if not cart.count:
        messages.error(request, 'Não há itens no carrinho.')
        return HttpResponseRedirect(reverse('website:index'))

    api_pagseguro = PagSeguroApiTransparent()
    data = api_pagseguro.get_session_id()
    if data.get('status_code') == 200:
        ctx.update({
            'session_id': data.get('session_id')
        })
    else:
        messages.error(request, data.get('response_text'))
    if request.method == 'POST':
        payment_methods = json.loads(request.POST.get('payment_methods'))
        ctx.update({
            'payment_methods': payment_methods
        })
    return render(request, 'carrinho-pagamento.html', ctx)


@login_required
@csrf_exempt
def checkout(request):
    ret = {}
    cart = Cart(request.session)
    data = request.POST
    # DADOS PAGSEGURO
    pm_name = data.get('pm_name')
    pm_type = data.get('pm_type')
    pm_hash = data.get('has')
    cc_token = data.get('cc_token')
    # DADOS COMPRADOR
    ps_email = data.get('ps_email')
    ps_nome = data.get('ps_nome')
    ps_cpf = data.get('ps_cpf')
    ps_ddd = data.get('ps_ddd')
    ps_telefone = data.get('ps_telefone')
    # DADOS CARTAO
    cc_parcelas = data.get('cc_parcelas')
    cc_valor = data.get('cc_valor')
    # DADOS ENDERECO
    end_logradouro = data.get('end_logradouro')
    end_numero = data.get('end_numero')
    end_bairro = data.get('end_bairro')
    end_cep = data.get('end_cep')
    end_cidade = data.get('end_cidade')
    end_uf = data.get('end_uf')
    api = PagSeguroApiTransparent()
    for i in cart.items:
        item = PagSeguroItem(
            id='{0:06d}'.format(i.product.pk),
            description=u'{0}'.format(i.product.nome),
            amount='{0:.2f}'.format(i.price),
            quantity=i.quantity
        )
        api.add_item(item)

    sender = {
        'name': ps_nome,
        'area_code': ps_ddd,
        'phone': ps_telefone,
        'email': ps_email or request.user.email,
        'cpf': ps_cpf
    }
    api.set_sender(**sender)

    shipping = {
        'street': end_logradouro,
        'number': end_numero,
        'complement': '',
        'district': end_bairro,
        'postal_code': end_cep,
        'city': end_cidade,
        'state': end_uf,
        'country': 'BRA'
    }

    if cart.discount > 0:
        api.set_extra_amount(cart.discount * -1)

    api.set_shipping(**shipping)

    api.set_payment_method(pm_type)
    if pm_type == 'eft':
        api.set_bank_name(pm_name)
    elif pm_type == 'creditcard':
        sender.pop('email')
        sender.update({
            'quantity': cc_parcelas,
            'value': cc_valor,
            'birth_date': '27/10/1987',
        })
        api.set_creditcard_data(**sender)
        api.set_creditcard_billing_address(**shipping)
        api.set_creditcard_token(cc_token)
    api.set_sender_hash(pm_hash)
    data_api = api.checkout()
    success = data_api.get('success')
    ret.update({
        'success': success,
    })
    message = data_api.get('message')
    if not success:
        message = xmltodict.parse(message)

        errors = message.get('errors').get('error')
        if isinstance(errors, OrderedDict):
            errors = [errors]
        ret.update({
            'errors': errors
        })
    else:
        trans = message.get('transaction')
        ret.update({
            'link': trans.get('paymentLink', ''),
            'code': data_api.get('code')
        })
        chk = Checkout(
            code=data_api.get('code'),
            aluno=request.user.aluno,
            date=data_api.get('date'),
            success=data_api.get('success'),
            message=data_api.get('response'),
            cpf=ps_cpf
        )
        chk.save()
        for i in cart.items:
            item = CheckoutItens(
                checkout=chk,
                curso=i.product,
                valor=i.price,
                qtda=i.quantity
            )
            item.save()
            p = item.product
            if p.aluno:
                p.state = 'F'
                p.save()
        cart.clear()
    return JsonResponse(ret)


@login_required
def trans(request):
    code = request.GET.get('code')
    check_out = get_object_or_404(Checkout, code=code)
    data = xmltodict.parse(check_out.message)
    ctx = {
        'code': code,
        'data': data,
        'status': TRANSACTION_STATUS.get(data.get('transaction').get('status'))
    }
    return render(request, 'trans.html', ctx)


def get_tarefa_json(request):
    try:
        atividade = Atividade.objects.get(id=request.GET.get('pk'))
        tarefa = atividade.tarefa
    except Exception as e:
        tarefa = 'Erro: {0}'.format(e)
    return JsonResponse({'tarefa': tarefa})


@csrf_exempt
def get_alunos_curso_json(request):
    curso_id = request.POST.getlist('curso_id[]')
    cursos = Curso.objects.filter(id__in=curso_id)
    data = []
    count = 1
    for ocurso in cursos:
        for aluno in ocurso.get_alunos:
            d = dict(value=aluno.id, name=aluno.nome)
            if d not in data:
                data.append(d)
                count += 1
    return JsonResponse(data, safe=False)


def get_amostra_json(request):
    vals = {}

    if request.GET.get('tipo') == 'resposta':
        st = SentencaAvulsaAluno.objects.get(pk=request.GET.get('pk'))
        vals['conteudo'] = u"{0}".format(st.resposta)
    else:
        try:
            ocurso = Curso.objects.get(id=request.GET.get('pk'))
            if ocurso.categoria.tipo == 'S':
                st = ocurso.sentenca_avulsa
            elif ocurso.categoria.tipo == 'O':
                st = ocurso.sentenca_oab

            amostra = st.amostra
            vals['conteudo'] = u"{0}".format(st.conteudo)
        except Exception as e:
            amostra = 'Erro: {0}'.format(e)
        vals['amostra'] = amostra
    return JsonResponse(vals)


@csrf_exempt
@login_required
def post_resposta(request, pk):
    flag = 'success'
    msg = 'Resposta salva com sucesso!!!'
    data = request.POST
    finalizar = True if data.get('concluido') == 'true' else False
    try:
        tarefa = TarefaAtividade.objects.get(id=pk)
        tarefa.resposta = data.get('content')
        if data.get('tempo'):
            try:
                tarefa.tempo = data.get('tempo')
                tarefa.save()
            except:
                pass
        if not any([tarefa.arquivo, len(tarefa.resposta)]):
            msg = "Atividade em branco! Você não escreveu nada no editor de textos e nem anexou arquivo com sua" \
                  " resposta. Sem uma dessas duas opções, não é possível finalizar a atividade."
            flag = 'error'
            finalizar = False
        else:
            if data.get('concluido') == 'true':
                tarefa.concluido = True
                tarefa.data_conclusao = timezone.now()
                tarefa.save()
                o_curso = tarefa.atividade.curso
                limitar_correcao = o_curso.limitar_correcao
                aluno = tarefa.aluno
                tarefas_concluidas = TarefaAtividade.objects.filter(
                    atividade__tipo_retorno='C',
                    atividade__curso=o_curso,
                    aluno_id=aluno,
                    corrigido=True,
                    # limitada=False
                )
                if limitar_correcao and tarefas_concluidas.count() == limitar_correcao:
                    tarefa.limitada = True
                    tarefa.save()
                    # tarefas_pendentes = TarefaAtividade.objects.filter(
                    #     atividade__tipo_retorno='C',
                    #     atividade__curso=o_curso,
                    #     aluno_id=aluno,
                    #     concluido=False,
                    #     limitada=False
                    # )
                    # tarefas_pendentes.update(limitada=True)
                    msg = 'Você já respondeu ao número máximo de atividades com direito à correção individual, sendo ' \
                          'disponibilizado, para esta atividade, apenas o gabarito criado pelo professor.'
                    flag = 'error'
    except Exception as e:
        msg = str(e)
        flag = 'error'

    return JsonResponse({
        'msg': msg,
        'flag': flag,
        'finalizar': finalizar
    })


@csrf_exempt
@login_required
def post_correcao(request, pk):
    flag = 'success'
    msg = 'Correção salva com sucesso!!!'
    data = request.POST
    try:
        tarefa = TarefaAtividade.objects.get(id=pk)
        if not tarefa.professor:
            tarefa.professor = request.user.professor
        tarefa.gabarito = data.get('content')
        tarefa.save()
        if data.get('concluido') == 'true':
            tarefa.corrigido = True
            tarefa.save()
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

    except Exception as e:
        msg = str(e)
        flag = 'error'

    return JsonResponse({
        'msg': msg,
        'flag': flag
    })


@csrf_exempt
@login_required
def post_sentenca(request, pk):
    flag = 'success'
    msg = 'Resposta salva com sucesso!!!'
    data = request.POST
    try:
        sentenca = SentencaAvulsaAluno.objects.get(id=pk)
        sentenca.resposta = data.get('content')
        if data.get('tempo'):
            sentenca.tempo = data.get('tempo')
        if data.get('concluido') == 'true':
            sentenca.status = 'A'
            sentenca.data_conclusao = timezone.now()
            enviar_email('curso/email/sentenca-finalizada.html', 'Nova sentença disponível para correção',
                         [sentenca.sentenca_avulsa.professor.user.email], ead=True)
        sentenca.save()
    except Exception as e:
        msg = str(e)
        flag = 'error'

    return JsonResponse({
        'msg': msg,
        'flag': flag
    })


@csrf_exempt
@login_required
def post_sentenca_oab(request, pk):
    flag = 'success'
    msg = 'Resposta salva com sucesso!!!'
    data = request.POST
    try:
        sentenca = SentencaOABAvulsaAluno.objects.get(id=pk)
        sentenca.resposta = data.get('content')
        if data.get('tempo'):
            sentenca.tempo = data.get('tempo')
        if data.get('concluido') == 'true':
            sentenca.status = 'A'
            enviar_email('curso/email/sentenca-oab-finalizada.html',
                         'Nova peça disponível para correção',
                         ['christian.douglas.alcantara@gmail.com',
                          sentenca.sentenca_oab.professor.user.email],
                         ead=True)
        sentenca.save()
    except Exception as e:
        msg = str(e)
        flag = 'error'

    return JsonResponse({
        'msg': msg,
        'flag': flag
    })


@login_required
def atividade_responder(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)
    aluno = request.user.aluno
    try:
        tarefa = TarefaAtividade.objects.get(
            atividade=atividade,
            aluno=aluno
        )
    except Exception as e:
        messages.info(request, str(e))
        tarefa = TarefaAtividade(
            atividade=atividade,
            aluno=aluno
        )
        tarefa.save()
    if request.method == 'POST':
        ofile = request.FILES.get('inputUpload')
        tarefa.arquivo = ofile
        tarefa.data_upload = timezone.now()
        tarefa.save()
        if ofile:
            # tarefa.concluido = True
            # tarefa.save()
            messages.info(request, 'Arquivo enviado com sucesso!')
    ctx = {
        'titulo': 'Responder atividade',
        'menu': 'Responder atividade',
        'submenu': atividade,
        'tarefa': tarefa,
        'aluno': aluno,
        'video_url': request.session.get('videos')
    }
    return render(request, 'atividade-responder.html', ctx)


@login_required
def sentenca_responder(request, pk):
    sentenca = get_object_or_404(SentencaAvulsaAluno, pk=pk)
    if request.method == 'POST':
        ofile = request.FILES.get('inputUpload')
        sentenca.arquivo = ofile
        sentenca.data_upload = timezone.now()
        if ofile:
            sentenca.save()
            messages.info(request, 'Arquivo enviado com sucesso!')
    if sentenca.expirado:
        messages.error(
            request,
            'O prazo de 01 (um) ano para resolver esta Atividade Avulsa já expirou.'
            ' Você ainda pode acessar o gabarito da atividade'
        )
    ctx = {
        'titulo': sentenca,
        'menu': 'Atividade Avulsa',
        'sentenca': sentenca
    }
    return render(request, 'sentenca-responder.html', ctx)


@login_required
def sentenca_oab_responder(request, pk):
    sentenca = get_object_or_404(SentencaOABAvulsaAluno, pk=pk)
    ctx = {
        'titulo': sentenca,
        'menu': 'OAB 2ª Fase',
        'sentenca': sentenca
    }
    return render(request, 'sentenca-oab-responder.html', ctx)


def imprimir(request, pk):
    if request.GET.get('action') == 'resposta':
        tarefa = get_object_or_404(TarefaAtividade, id=pk)
        ctx = {
            'conteudo': tarefa.resposta,
            'titulo': tarefa.atividade
        }
    elif request.GET.get('action') == 'resposta_sentenca':
        sentenca_aluno = SentencaAvulsaAluno.objects.get(pk=pk)
        ctx = {
            'conteudo': sentenca_aluno.correcao_individual,
            'titulo': sentenca_aluno.sentenca_avulsa
        }
    else:
        atividade = get_object_or_404(Atividade, id=pk)
        ctx = {
            'conteudo': atividade.tarefa,
            'titulo': atividade
        }
    if request.GET.get('notprint') == 'sim':
        ctx['print'] = False
    else:
        ctx['print'] = True

    # template = get_template('imprimir-atividade.html')
    # context = Context(ctx)
    # html = template.render(context)
    # result = StringIO.StringIO()
    #
    # pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    return render(request, 'imprimir-atividade.html', ctx)


def baixar_correcao(request, pk):
    ctx = {}
    action = request.GET.get('action')
    tarefa = None
    if action == 'gabarito_atv':
        ctx['gabarito'] = True
        atividade = get_object_or_404(Atividade, id=pk)
    else:
        if action == 'gabarito':
            ctx['gabarito'] = True
        tarefa = get_object_or_404(TarefaAtividade, id=pk)
        atividade = tarefa.atividade
    ctx.update({
        'tarefa': tarefa,
        'atividade': atividade,
        'titulo': atividade
    })
    return render(request, 'baixar-correcao.html', ctx)


def sentenca_imprimir(request, pk):
    if request.GET.get('tipo') == 'st':
        sa = SentencaAvulsaAluno.objects.get(id=pk)
        conteudo = sa.resposta
        titulo = sa
    elif request.GET.get('tipo') == 'oab':
        ocurso = get_object_or_404(Curso, id=pk)
        conteudo = ocurso.sentenca_oab.conteudo
        titulo = ocurso.sentenca_oab
    else:
        ocurso = get_object_or_404(Curso, id=pk)
        conteudo = ocurso.sentenca_avulsa.conteudo
        titulo = ocurso.sentenca_avulsa
    ctx = {
        'conteudo': conteudo,
        'titulo': titulo
    }
    # template = get_template('imprimir-atividade.html')
    # context = Context(ctx)
    # html = template.render(context)
    # result = StringIO.StringIO()
    #
    # pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    return render(request, 'imprimir-atividade.html', ctx)


def download_tarefa(request, pk):
    pk = int(pk)
    if request.GET.get('tipo') == 'st':
        sentenca = get_object_or_404(SentencaAvulsaAluno, id=pk)
        conteudo = sentenca.resposta
        aluno = sentenca.aluno
    elif request.GET.get('tipo') == 'oab':
        sentenca = get_object_or_404(SentencaOABAvulsaAluno, id=pk)
        conteudo = sentenca.resposta
        aluno = sentenca.aluno
    else:
        tarefa = get_object_or_404(TarefaAtividade, id=pk)
        conteudo = tarefa.resposta
        aluno = tarefa.aluno

    response = HttpResponse(content_type='text/html; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="T{0:03d}-{1}.html"'.format(pk, slugify(aluno))
    html = u"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>T{0:03d}-{1}</title>
    </head>
    <body>
        {2}
    </body>
    </html>
    """.format(pk, slugify(aluno), conteudo)
    response.write(html)
    return response


@csrf_exempt
def enviar_correcao(request):
    data = request.POST
    ofile = request.FILES.get('inputUpload')
    pk = data.get('id_tarefa')
    try:
        if data.get('action') == 'sentenca':
            sentenca = SentencaAvulsaAluno.objects.get(id=pk)
            sentenca.correcao = ofile
            sentenca.status = 'C'
            sentenca.save()
            messages.success(request, u'Sentença enviada com sucesso')
            enviar_email('curso/email/sentenca-corrigida.html', 'Sua sentença já foi corrigida!',
                         [sentenca.aluno.email], context={'sentenca': sentenca}, ead=True)
        elif data.get('action') == 'oab':
            sentenca = SentencaOABAvulsaAluno.objects.get(id=pk)
            sentenca.correcao = ofile
            sentenca.status = 'C'
            sentenca.save()
            messages.success(request, u'Peça enviada com sucesso')
            enviar_email('curso/email/sentenca-corrigida-oab.html', 'Sua peça já foi corrigida!',
                         ['christian.douglas.alcantara@gmail.com', sentenca.aluno.email],
                         context={'sentenca': sentenca}, ead=True)
        else:
            tarefa = TarefaAtividade.objects.get(id=pk)
            tarefa.correcao = ofile
            tarefa.corrigido = True
            tarefa.save()
            enviar_email('curso/email/correcao-enviada.html', 'Sua atividade foi corrigida!',
                         [tarefa.aluno.email], context={'tarefa': tarefa}, ead=True)

            messages.info(request, 'Arquivo enviado com sucesso!!!')
    except Exception as e:
        messages.error(request, str(e))
    return HttpResponseRedirect(data.get('redirect', '/'))


# @csrf_exempt
def enviar_resposta_padrao(request):
    data = request.POST
    file = request.FILES.get('file')
    try:
        atividade = Atividade.objects.get(id=data.get('atividade_id'))
        atividade.resposta_padra = file
        atividade.resposta_padrao_data = parser.parse(data.get('data'))
        atividade.save()
        messages.info(request, 'Arquivo enviado com sucesso!!!')
    except Exception as e:
        messages.error(request, str(e))
    return HttpResponseRedirect(data.get('redirect', '/'))


def montar_pacote(request):
    context = {
        'titulo': 'Pacote personalizado'
    }
    template_name = 'curso/montar_pacote_list.html'
    filtro = dict(categoria__tipo='S')
    # ESFERAS_ESPECIFICAS
    esferas_especificas = EsferaEspecifica.objects.filter(sentencaavulsa__isnull=False).values('id', 'nome'). \
        annotate(t=Count('id'))
    context['esferas_especificas'] = esferas_especificas
    # TIPOS PROCEDIMENTO
    tipos_procedimento = TipoProcedimento.objects.filter(sentencaavulsa__isnull=False).values('id', 'nome'). \
        annotate(t=Count('id'))
    context['tipos_procedimento'] = tipos_procedimento
    # DISCIPLINAS
    disciplinas = Disciplina.objects.filter(sentencaavulsa__isnull=False).values('id', 'nome').annotate(t=Count('id'))
    context['disciplinas'] = disciplinas
    # DISCIPLINAS
    disciplinas = Categoria.objects.filter(tipo='S').values('id', 'nome').annotate(t=Count('id'))
    context['categorias'] = disciplinas

    if request.method == 'GET':
        data = request.GET
        for key, value in data.iteritems():
            if value:
                filtro[key] = value
        context['filtro'] = filtro

    args = [Q(data_fim__gte=timezone.now()) | Q(data_fim__isnull=True)]
    qs = Curso.objects.filter(*args, **filtro)
    context.update(dict(cursos=qs))
    user = request.user
    if user.is_authenticated:
        try:
            aluno = user.aluno
            combo_aluno = ComboAluno.objects.filter(status='A', aluno=aluno).first()
            context.update(dict(combo_aluno=combo_aluno))
        except:
            combo_aluno = None
        if request.method == 'POST':
            action = request.POST.get('action')
            curso_pk = request.POST.get('curso_pk')
            qs_curso = Curso.objects.get(pk=curso_pk)
            if action == 'add' and curso_pk:
                if not combo_aluno:
                    qs_categoria = Categoria.objects.filter(tipo='B').first()
                    desc = """Você está adquirindo um pacote personalizado de Atividades Avulsas que inclui as propostas
                     discriminadas nesta página. Você poderá fazer as atividades de acordo com a sua 
                     disponibilidade, no prazo de até 01 (um) ano da data da compra. As atividades poderão ser entregues 
                     de forma digitada ou manuscrita, por meio das ferramentas disponíveis em nossa área de ensino. As 
                     correções individualizadas serão feitas pelos nossos professores no prazo previsto em nossa 
                     "Política de uso". Você ainda poderá recorrer da nota e trocar mensagens com os professores.
                     Caso queira fazer alguma alteração neste pacote personalizado, retorne à página respectiva para 
                     adicionar ou excluir atividades. Após clicar em "Comprar este pacote", não será mais possível 
                     fazer alterações, embora você ainda possa desistir da compra. Após a confirmação do pagamento, 
                     acesse a "Área do aluno", opção "Atividades Avulsas", para ter acesso às propostas. 
                     Desejamos um bom estudo para você!"""
                    combo_aluno = ComboAluno(
                        categoria=qs_categoria,
                        aluno=aluno,
                        descricao=desc,
                        valor=0,
                        economia=0,
                        order=0
                    )
                    combo_aluno.save()
                    title = u'Pacote personalizado #{:04d}'.format(combo_aluno.pk)
                    combo_aluno.nome = title
                    combo_aluno.slug = slugify(title)
                    combo_aluno.save()
                combo_aluno.cursos.add(qs_curso)
                calc = combo_aluno.calc(True)
                desconto_valor = calc.get('desconto_valor')
                desconto_porcento = calc.get('desconto_porcento')
                msg = u'{} adicionado ao pacote'.format(qs_curso.nome)
                if desconto_porcento:
                    msg += u'<div class="alert alert-success" role="alert" style="margin-top: 10px;">' \
                           u'<small style="text-align: justify">Você já conseguiu {}% de desconto, economizando R$ {}.' \
                           u' Quanto mais atividades você escolher, maior será o seu desconto.</small></div>'.format(
                        moeda_nosymbol(desconto_porcento), moeda_nosymbol(desconto_valor)
                    )
                messages.success(request, msg)
            elif action == 'remove':
                combo_aluno.cursos.remove(qs_curso)
                if not combo_aluno.cursos.count():
                    combo_aluno.delete()
                else:
                    combo_aluno.calc(True)
                messages.error(request, u'{} removido do pacote'.format(qs_curso.nome))

            return HttpResponseRedirect(reverse('curso:montar-pacote'))
    return render(request, template_name, context)


def ajax_search_simulado(request):
    cursos = Curso.objects.filter(
        nome__icontains=request.GET['q'],
        simulado__isnull=False
    ).values('nome')
    values = [curso['nome'] for curso in cursos]
    return JsonResponse(
        values, safe=False
    )


def ajax_gerar_cortesia(request):
    data = request.GET
    try:
        status = 200
        pk = data.get('pk')
        emails = data.get('emails')
        c = Curso.objects.get(pk=pk)

        if emails:
            message = 'Cortesia gerada'
            cadastrados = []
            for email in emails.split(','):
                try:
                    validate_email(email)
                    try:
                        aluno = Aluno.objects.get(email=email)
                        cortesia = Cortesia(curso=c)
                        cortesia.aluno = aluno
                        cortesia.email = email
                        cortesia.utilizado = True
                        cortesia.save()
                        cadastrados.append(email)
                        checkout = Checkout.objects.create(
                            code=cortesia.codigo,
                            aluno=aluno,
                            date=datetime.datetime.now(),
                            transaction_status=3
                        )
                        checkout.save()
                        transaction = Transaction.objects.create(
                            code=cortesia.codigo,
                            checkout=checkout,
                            status="pago",
                        )
                        transaction.save()
                        items = CheckoutItens.objects.create(
                            checkout=checkout,
                            curso=cortesia.curso,
                            qtda=1,
                            valor=Decimal(0)
                        )
                        items.save()
                    except Aluno.DoesNotExist:
                        cortesia = Cortesia(curso=c)
                        cortesia.email = email
                        cortesia.save()
                        ctx = {'curso': c, 'codigo': cortesia.codigo}
                        enviar_email_old(
                            'curso/email/cortesia.html', u'Seu código de cortesia já está disponível!',
                            [email], ctx
                        )
                except ValidationError:
                    status = 500
                    message = u'Email "%s" invalido' % email
            response = JsonResponse(data={'message': message}, status=status)
            response.reason_phrase = message
            ctx = {
                'curso': c
            }
            if cadastrados:
                enviar_email(
                    'curso/email/cortesia-cadastrado.html', u'Seu acesso de cortesia já está liberado!',
                    cadastrados, ctx
                )
            return response
        else:
            @atomic
            def create():
                for x in range(int(data['q'])):
                    Cortesia.objects.create(curso=c)

            create()
            return JsonResponse(
                {'message': '%s cortesia(s) gerada(s)!' % data['q']}
            )
    except Exception as e:
        response = JsonResponse(data={'status': 'false', 'message': 'message'}, status=500)
        response.reason_phrase = '%s' % e
        return response


def ajax_validar_cortesia(request):
    data = request.GET
    status = 200
    error = False
    message = 'Código aplicado'
    simulado = None
    try:
        aluno = request.user.aluno

        def aplicar(c):
            c.aluno = aluno
            c.utilizado = True
            c.save()

        try:
            c = Cortesia.objects.get(curso_id=data['pk'], codigo=data['code'])
            simulado = c.curso.simulado.pk
            status = 500
            if c.utilizado:
                message = 'Cortesia nao disponivel'
            elif c.aluno:
                if c.aluno == aluno:
                    message = 'Cortesia aplicada'
                    status = 200
                    aplicar(c)
                else:
                    message = 'Nao pertence a voce'
            else:
                message = 'Cortesia aplicada'
                status = 200
                aplicar(c)



        except Cortesia.DoesNotExist:
            message = 'Codigo invalido'
            status = 500
    except Exception as e:
        status = 500
        message = 'Nao foi possivel aplicar a cortesia'

    response = JsonResponse(
        data={
            'message': message,
            'statusText': message,
            'error': error,
            'simulado': simulado
        }, status=status
    )
    if status == 500:
        response.reason_phrase = message
    return response
