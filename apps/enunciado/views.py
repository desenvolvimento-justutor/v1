# -*- coding: utf-8 -*-
# Autor: christian
import cStringIO as StringIO
from cgi import escape
from datetime import datetime
from decimal import Decimal
from string import ascii_uppercase

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa

from apps.aluno.models import Filtro, ranking_top_pontos, Aluno, Seguir
from apps.aluno.models import aluno_from_user_request
from apps.corretor.models import Corretor
from apps.enunciado import FLAG_PONTOS_RESPONDER, FLAG_PONTOS_CORRIGIR, FLAG_PONTOS_CORRIGIREM, FLAG_TIPO_ENUNCIADO_P
from apps.financeiro.models import ConfiguracaoPacote, Credito, CreditoResgate
from apps.pregao.models import SolicitarCorrecao
from apps.website.models import Anuncio
from apps.website.utils import enviar_email
from carton.cart import Cart
from justutorial.settings import SITEADD
from libs.util.paginar import listing
from .models import (EnunciadoProposta, EsferaEspecifica, Cargo, Resposta, Correcao, NotaResposta, RankingPremiado,
                     AvaliacaoCorrecao, ComentarioCorrecao, Tag, Concurso, RoteiroEstudo, RoteiroEstudoItem,
                     RoteiroEstudoSubItem, RespostaComentario, Coletania, SeguirComentario, CurtirComentario)

MAP_TIPO = {
    'questao': 'QD',
    'peca': 'PP',
    'sentenca': 'ST'
}


def atividade(request):
    respostas = Resposta.objects.filter(concluido=True, ativo=True).order_by('-data_termino')[:100]
    avaliacoes = NotaResposta.objects.filter().order_by('-data')[:100]
    comentarios = RespostaComentario.objects.filter().order_by('-data')[:100]
    ctx = {
        'respostas': respostas,
        'avaliacoes': avaliacoes,
        'comentarios': comentarios,
        'anuncios': Anuncio.objects.filter(pag_atividades=True, ativo=True)
    }
    return render(request, 'atividade.html', ctx)


def temas_abordados(request):
    args = []
    if request.method == 'GET':
        filtro = request.GET.get('q')
        if filtro:
            args.append(Q(nome__icontains=filtro))
    tags = Tag.objects.filter(*args).annotate(total=Count('enunciadoproposta')).order_by('-total')
    ctx = {
        'tags': listing(request, tags, 50),
        'anuncios': Anuncio.objects.filter(pag_temas=True, ativo=True)
    }
    return render(request, 'temas-abordados.html', ctx)


def mais_populares(request):
    respostas = Resposta.objects.filter(concluido=True, ativo=True).values('enunciado').annotate(
        total=Count('enunciado')).order_by('-total')
    enunciado_ids = map(lambda x: x.get('enunciado'), respostas)
    enunciados = EnunciadoProposta.objects.filter(
        id__in=enunciado_ids, resposta__ativo=True, resposta__concluido=True
    ).annotate(total=Count('resposta')).order_by('-total')
    ctx = {
        'enunciados': listing(request, enunciados, 40),
        'anuncios': Anuncio.objects.filter(pag_populares=True, ativo=True)
    }
    return render(request, 'mais-populares.html', ctx)


def ranking_mais_responderam(data_ini=False, data_fim=False, tipo=False):
    n = datetime.now()
    mais_responderam = []
    args = [Q(ativo=True) | Q(concluido=True)]
    if data_ini and data_fim:
        args.append(Q(data_termino__range=[data_ini, data_fim]))
    if tipo:
        args.append(Q(enunciado__classificacao=tipo))

    respostas = Resposta.objects.filter(*args).values('aluno').annotate(total=Count('aluno')).order_by('-total')[:12]

    for resp in respostas:
        mais_responderam.append({
            'aluno': Aluno.objects.get(id=resp.get('aluno')),
            'total': resp.get('total')
        })
    return mais_responderam


def get_chart(request):
    aluno = Aluno.objects.get(id=request.GET.get('aluno_id'))
    ret = []
    total_pontos = 0

    for pt in aluno.get_total_respondidos():
        total = pt.get('total') * FLAG_PONTOS_RESPONDER.get(pt.get('classificacao'))
        total_pontos += total
        ret.append({
            'y': total,
            'name': u'{1} - Respostas elaboradas ({0})'.format(
                pt.get('total'), FLAG_TIPO_ENUNCIADO_P.get(pt.get('classificacao'))
            )
        })
    for pt in aluno.get_total_corrigir():
        total = pt.get('total') * FLAG_PONTOS_CORRIGIR.get(pt.get('classificacao'))
        total_pontos += total
        ret.append({
            'y': total,
            'name': u'{1} - Correções de respostas ({0})'.format(
                pt.get('total'), FLAG_TIPO_ENUNCIADO_P.get(pt.get('classificacao')))
        })

    for pt in aluno.get_total_corrigirem():
        total = pt.get('total') * FLAG_PONTOS_CORRIGIREM.get(pt.get('classificacao'))
        total_pontos += total
        ret.append({
            'y': total,
            'name': u'{1} - Correções recebidas ({0})'.format(
                pt.get('total'), FLAG_TIPO_ENUNCIADO_P.get(pt.get('classificacao'))
            )
        })

    pt = aluno.get_pontos_avaliacao()
    if pt:
        total = pt
        total_pontos += total
        ret.append({
            'y': total,
            'name': u'Avaliações úteis ({0})'.format(aluno.get_pontos_avaliacao())
        })

    return JsonResponse({'pieData': ret, 'aluno': aluno.nome, 'total': total_pontos})


def ranking(request):
    # GERAL
    ranking_geral = ranking_top_pontos()
    # MAIS RESPONDERAM
    mais_responderam = ranking_mais_responderam()
    # MAIS CORRIGIRAM
    mais_corrigiram = []
    corecoes = NotaResposta.objects.all().values('aluno').annotate(total=Count('aluno')).order_by('-total')
    for correc in corecoes:
        mais_corrigiram.append({
            'aluno': Aluno.objects.get(id=correc.get('aluno')),
            'total': correc.get('total')
        })
    # MAIS POPULARES
    mais_populares = []
    seguidores = Seguir.objects.all().values('para_aluno').annotate(total=Count('para_aluno')).order_by('-total')
    for seguidor in seguidores:
        mais_populares.append({
            'aluno': Aluno.objects.get(id=seguidor.get('para_aluno')),
            'total': seguidor.get('total')
        })
    ctx = {
        'ranking_geral': ranking_geral,
        'mais_responderam': mais_responderam,
        'mais_corrigiram': mais_corrigiram,
        'mais_populares': mais_populares
    }
    return render(request, 'ranking.html', ctx)


def ranking_premiado(request):
    q = []
    filtro = request.GET.get('q', 'I')
    if filtro == 'I':
        now = timezone.now()
        q.append(Q(data_ini__lte=now) & Q(data_fim__gte=now))
    elif filtro == 'F':
        q.append(Q(encerrado=True))
    else:
        q = []
    rankings = RankingPremiado.objects.filter(*q)
    ctx = {
        'rankings': rankings,
        'premiado': True,
        'filter': filtro
    }
    return render(request, 'ranking-premiado.html', ctx)


def tipo(request, ptipo, pid=False):
    ptipo = MAP_TIPO.get(ptipo)
    # ----------------------------------------------------------------------------------------
    if request.method == 'POST':
        aluno = request.user.aluno
        if not aluno:
            messages.error(request, 'Efetue login ou cadastre-se.')
        else:
            if request.POST.get('enunciado_id'):
                enunciado = get_object_or_404(EnunciadoProposta, classificacao=ptipo, id=pid)
                formulario = enunciado.formulario_autocorrecao
                totais = Credito.totais(aluno_id=aluno.pk)
                vlr_cr = formulario.creditos
                if totais.get('disponiveis') >= vlr_cr:
                    for cr in Credito.objects.filter(aluno=aluno):
                        if not vlr_cr:
                            break
                        cre = CreditoResgate(
                            credito=cr,
                            formulario=formulario
                        )
                        if cr.disponivel >= vlr_cr:
                            cre.quantidade = vlr_cr
                            vlr_cr = 0
                        else:
                            cre.quantidade = cr.disponivel
                            vlr_cr -= cr.disponivel
                        cre.save()
                else:
                    messages.error(request, 'Creditos insuficientes..')
            else:
                configuracao_pacote = ConfiguracaoPacote.objects.filter(ativo=True).first()
                cart = Cart(request.session)
                qtda = int(request.POST.get('qtda'))
                pacote_id = request.POST.get('pacote_id')
                valor = configuracao_pacote.valor_unitario * qtda
                if pacote_id and pacote_id != 'false':
                    pacote = configuracao_pacote.pacotes.get(id=pacote_id)
                    valor = pacote.valor
                else:
                    pacote_desconto = configuracao_pacote.descontos.filter(ate__gte=qtda, de__lte=qtda).first()
                    if pacote_desconto:
                        cart.discount = (valor * Decimal(pacote_desconto.desconto)) / 100

                cart.add(
                    configuracao_pacote.curso,
                    price=valor,
                    quantity=1,
                    configuracao_pacote=configuracao_pacote.pk,
                    quantidade=qtda,
                    pacote=pacote_id
                )
                return HttpResponseRedirect(reverse('curso:carrinho'))
    # ----------------------------------------------------------------------------------------
    ctx = {
        'anuncios': Anuncio.objects.filter(pag_enunciados=True, ativo=True),
        'resposta': False,
        'pagina': 'enunciados',
        'ranking_geral': ranking_top_pontos(),
        'mais_responderam': ranking_mais_responderam()
    }
    if pid:
        enunciado = get_object_or_404(EnunciadoProposta, classificacao=ptipo, id=pid)
        ctx.update({'enunciado': enunciado})
    else:
        enunciados = EnunciadoProposta.objects.filter(classificacao=ptipo)
        pages = listing(request, enunciados, 1)
        enunciado = pages.object_list[0]
        ctx.update({'enunciado': pages.object_list[0],
                    'paginar': True,
                    'enunciados': pages,
                    'pagina': 'enunciado'})

    try:
        resposta_aluno = enunciado.resposta_set.get(aluno_id=request.user.aluno.id, ativo=True)
        ctx.update({'resposta': resposta_aluno})
    except:
        pass

    return render(request, 'enunciados.html', ctx)


def correcao(request, cid):
    ctx = {
        'ranking_geral': ranking_top_pontos(),
        'mais_responderam': ranking_mais_responderam()
    }
    aluno = aluno_from_user_request(request)
    correc = get_object_or_404(Correcao, id=cid)  # Correção
    minha_correcao = Correcao.objects.filter(resposta=correc.resposta, aluno=aluno).first()
    minha_resposta = Resposta.objects.filter(
        enunciado=correc.resposta.enunciado, aluno=aluno, ativo=True,
    ).first()
    correcoes = Correcao.objects.filter(resposta=correc.resposta).exclude(id=correc.id)
    if request.method == 'POST':
        data = request.POST
        action = data.get('action')
        # ENVIAR CORRECAO
        if action == 'correcao':
            if not minha_correcao:
                content = request.POST.get('content')
                nota = request.POST.get('rating')
                ocorrecao = Correcao(
                    aluno=aluno,
                    resposta=correc.resposta,
                    texto=content
                )
                ocorrecao.save()
                minha_correcao = ocorrecao
                nota = NotaResposta(aluno=aluno, resposta=correc.resposta, nota=nota)
                nota.save()
                # messages.success(
                #     request, u'Você Corrigiu e acumulou <b class="text-primary">+{0}</b> pontos.'.format(
                #         ocorrecao.resposta.enunciado.get_pontos_corrigir)
                # )
                ctx.update({
                    'shared': True,
                    'shared_texto': 'Acabei de corrigir uma resposta no JusTutor. Confira e avalie a minha correção!',
                    'shared_url': '{0}{1}'.format(SITEADD, ocorrecao.get_absolute_url()),
                    'modal_text': 'A sua Correção foi Publicada.'
                })

            else:
                messages.error(request, u'Você já corrigiu essa resposta!')

        elif action == 'comentar':
            texto = data.get('texto-comentario')
            if texto:
                id_comentario = request.POST.get('id-comentario')
                del_comentario = request.POST.get('del_comentario')

                if id_comentario:
                    comentario = ComentarioCorrecao.objects.get(id=id_comentario)
                    if del_comentario:
                        comentario.delete()
                        messages.success(request, u'Comentário excluído com sucesso!')
                    else:
                        comentario.comentario = texto
                        comentario.data = timezone.now()
                        comentario.save()
                        messages.success(request, u'Comentário alterado com sucesso!')
                else:
                    ComentarioCorrecao.objects.create(
                        aluno=aluno,
                        correcao=correc,
                        comentario=texto
                    )
                    messages.success(request, u'Obrigado por Comentar!')
            else:
                messages.error(request, u'Digite algum texto.')

    nota = NotaResposta.objects.filter(aluno=aluno, resposta=correc.resposta).first()
    if nota:
        nota = nota.nota
    else:
        nota = 0
    ctx.update({
        'correcao': correc,
        'correcoes': correcoes,
        'resposta': correc.resposta,
        'enunciado': correc.resposta.enunciado,
        'minha_resposta': minha_resposta,
        'minha_correcao': minha_correcao,
        'nota': nota
    })
    return render(request, 'correcao.html', ctx)


def roteiros(request):
    data = request.GET
    ctx = {
        'anuncios': Anuncio.objects.filter(pag_roteiro=True, ativo=True),
        'ascii_uppercase': ascii_uppercase,
        'filtro': data
    }
    filtro = []
    filtro_iniciados = data.get('iniciados')
    if filtro_iniciados:
        filtro.append(Q(nome__startswith=filtro_iniciados))
    filtro_tipo = data.get('tipo')
    if filtro_tipo == "E":
        filtro.append(Q(edital=True))
    elif filtro_tipo == "D":
        filtro.append(Q(edital=False))

    rots = RoteiroEstudo.objects.filter(*filtro)
    ctx['roteiros'] = rots
    return render(request, 'enunciado/roteiros.html', ctx)


def roteiro(request, slug):
    ctx = {
        'anuncios': Anuncio.objects.filter(pag_roteiro=True, ativo=True)
    }
    rot = get_object_or_404(RoteiroEstudo, slug=slug)
    # paginator = listing(request, roteiros, 20)
    ctx['roteiro'] = rot
    return render(request, 'enunciado/roteiro-lista.html', ctx)


def roteiro_item(request, slug, item_slug):
    ctx = {
        'anuncios': Anuncio.objects.filter(pag_roteiro=True, ativo=True),
        'tipo': 'item'
    }
    rot_item = get_object_or_404(RoteiroEstudoItem, roteiro__slug=slug, slug=item_slug)
    ctx['roteiro'] = rot_item
    ctx['resultado'] = listing(request, rot_item.get_enunciados(), 10)
    return render(request, 'enunciado/enunciados.html', ctx)


def roteiro_subitem(request, slug, item_slug, sub_slug):
    ctx = {
        'anuncios': Anuncio.objects.filter(pag_roteiro=True, ativo=True),
        'tipo': 'subitem'
    }
    rot_subitem = get_object_or_404(RoteiroEstudoSubItem, item__roteiro__slug=slug, item__slug=item_slug, slug=sub_slug)

    ctx['roteiro'] = rot_subitem
    ctx['resultado'] = listing(request, rot_subitem.get_enunciados(), 10)
    return render(request, 'enunciado/enunciados.html', ctx)


def imprimir(request, eid):
    enunciado = get_object_or_404(EnunciadoProposta, id=eid)
    ctx = {
        'enunciado': enunciado
    }
    template = get_template('imprimir.html')
    context = Context(ctx)
    html = template.render(context)

    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def resposta(request, rid):
    resp = get_object_or_404(Resposta, id=rid)
    aluno = aluno_from_user_request(request)
    c = CurtirComentario.objects.filter(aluno=aluno, comentario__resposta=resp).values('comentario')
    ctx = {
        'anuncios': Anuncio.objects.filter(pag_enunciados=True, ativo=True),
        'ranking_geral': ranking_top_pontos(),
        'mais_responderam': ranking_mais_responderam(),
        'minha_coletanea': Coletania.objects.filter(aluno=aluno, resposta=resp).first(),
        'seguindo': False,
        'minhas_curtidas': map(lambda x: x.get('comentario'), c)
    }

    if not resp.ativo:
        return render(request, 'enunciado_error.html', ctx)

    if request.method == 'GET':
        if request.GET.get('shared'):
            ctx.update({
                'shared': True,
                'shared_texto': 'Acabei de responder um Enunciado JusTutor. Confira e avalie a minha Resposta!',
                'shared_url': '{0}{1}'.format(SITEADD, resp.get_absolute_url()),
                'modal_text': 'A sua Resolução foi Publicada.'
            })
    else:
        comentario = request.POST.get('comentario')
        com = RespostaComentario(
            aluno=aluno, comentario=comentario, resposta=resp
        )
        com.save()
        messages.success(request, 'Obrigado por comentar.')
        enviar_email(
            'email/email-comentario-resposta.html',
            u'Sua resposta recebeu um novo comentário',
            [resp.aluno.email], {'resposta': resp, 'comentario': comentario, 'aluno': aluno},
            ead=True
        )
        for seguindo in resp.seguircomentario_set.all():
            email = seguindo.aluno.email
            enviar_email(
                'email/email-comentario-resposta-seguir.html',
                'Resposta {} recebeu um novo comentário'.format(resp),
                [email], {'resposta': resp, 'comentario': comentario, 'aluno': aluno},
                ead=True
            )

    # Caso o aluno não respondeu, exibir link p responder
    minha_resposta = Resposta.objects.filter(aluno=aluno, enunciado=resp.enunciado, ativo=True).first()
    nota = NotaResposta.objects.filter(aluno=aluno, resposta=resp).first()
    if nota:
        ctx.update({'nota': nota})
    if not minha_resposta:
        seguindo = SeguirComentario.objects.filter(aluno=aluno, resposta=resp)
        ctx['seguindo'] = seguindo
    ctx.update({
        'resposta': resp,
        'enunciado': resp.enunciado,
        'minha_resposta': minha_resposta,
        # 'minha_correcao': minha_correcao
    })

    return render(request, 'resposta.html', ctx)


@login_required
def solicitar_correcao(request, rid):
    oresposta = get_object_or_404(Resposta, id=rid)
    try:
        solicitacao = oresposta.solicitarcorrecao
    except:
        solicitacao = False

    if request.method == 'POST' and not solicitacao:
        corretores_ids = request.POST.getlist('ckhprof')
        if len(corretores_ids) > 3:
            messages.error(request, u"Selecione no máximo 3 Corretores")
        else:
            messages.success(request, u"Solicitação enviada")
            solicitacao = SolicitarCorrecao(
                resposta=oresposta
            )
            solicitacao.save()
            if corretores_ids:
                solicitacao.corretores.add(*Corretor.objects.filter(id__in=corretores_ids))
                solicitacao.save()
    ctx = {
        'resposta': oresposta,
        'corretores': oresposta.enunciado.get_corretores(),
        'solicitacao': solicitacao
    }
    return render(request, 'solicitar-correcao.html', ctx)


@login_required
def _resposta(request, rid, cid=False):
    ctx = {
        'pagina': 'resposta',
        'show_editor': True,
        'show_correcao': False,
        'minha_correcao': False,
        'nota': 0
    }
    qry_resposta = get_object_or_404(Resposta, id=rid)
    aluno = aluno_from_user_request(request)
    if request.method == 'POST':
        data = request.POST
        if data.get('comentario'):
            correcao = get_object_or_404(qry_resposta.correcao_set, id=cid)
            ctx.update({'show_correcao': True})
            texto = data.get('texto-comentario')
            if texto:
                id_comentario = request.POST.get('id-comentario')
                del_comentario = request.POST.get('del_comentario')

                if id_comentario:
                    comentario = ComentarioCorrecao.objects.get(id=id_comentario)
                    if del_comentario:
                        comentario.delete()
                        messages.success(request, u'Comentário excluído com sucesso!')
                    else:
                        comentario.comentario = texto
                        comentario.data = timezone.now()
                        comentario.save()
                        messages.success(request, u'Comentário alterado com sucesso!')
                else:
                    ComentarioCorrecao.objects.create(
                        aluno=aluno,
                        correcao=correcao,
                        comentario=texto
                    )
                    messages.success(request, u'Obrigado por Comentar!')
            else:
                messages.error(request, u'Digite algum texto.')
        else:
            content = request.POST.get('content')
            nota = request.POST.get('rating')
            correcao = Correcao(
                aluno=aluno,
                resposta_id=rid,
                texto=content
            )
            if correcao.qtda_char < 150 or not nota:
                if not nota:
                    messages.error(request, u'Informe a nota')
                else:
                    messages.error(request, u'Digite no mínimo <b class="text-danger">150</b> caracteres')
                ctx.update({'content': content})
                ctx.update({'rating': nota})
                correcao = False
            else:
                correcao.save()
                nota = NotaResposta(aluno=aluno, resposta=qry_resposta, nota=nota)
                nota.save()
                messages.success(request, u'Você Corrigiu e acumulou <b class="text-primary">+145</b> pontos.')
                ctx.update({'show_correcao': True})
                ctx.update({'minha_correcao': correcao})
    else:
        if cid:
            correcao = get_object_or_404(qry_resposta.correcao_set, id=cid)
            ctx.update({'show_correcao': True})
            minha = qry_resposta.correcao_set.filter(aluno_id=aluno.id).first()
            ctx.update({'minha_correcao': minha})
            # caso aluno esteja avaliando a correção retorna json
            if request.GET.get('avaliar_correcao'):
                if correcao.aluno_id == aluno.id:
                    messages.error(request, u"Você não pode se auto-avaliar!")
                else:
                    try:
                        AvaliacaoCorrecao.objects.get(correcao_id=cid, aluno=aluno)
                        messages.error(request, u"Você já avaliou essa Correção")
                    except Exception as e:
                        avaliacao = AvaliacaoCorrecao(
                            aluno=aluno,
                            correcao_id=cid,
                            tipo=request.GET.get('tipo')
                        )
                        avaliacao.save()
                        messages.success(request, u"Obrigado por avaliar")
                return JsonResponse({})

        else:
            correcao = qry_resposta.correcao_set.filter(aluno_id=aluno.id).first()
            ctx.update({'minha_correcao': correcao})
        try:
            nota = NotaResposta.objects.get(aluno=aluno, resposta=qry_resposta)
            ctx.update({'nota': nota})
        except Exception as e:
            pass
        # Quando o usuario der a nota executa essa função via ajax
        if request.GET.get('avaliar'):
            nota = NotaResposta(aluno=aluno, resposta=qry_resposta, nota=request.GET.get('nota'))
            nota.save()
            return JsonResponse({})
    ctx.update({
        'resposta': qry_resposta,
        'enunciado': qry_resposta.enunciado,
        'correcao': correcao
    })
    return render(request, 'enunciado-resposta.html', ctx)


@login_required
def responder(request, ptipo, pid):
    resposta_aluno = False
    ptipo = MAP_TIPO.get(ptipo)
    enunciado = get_object_or_404(EnunciadoProposta, id=pid)
    ctx = {
        'flag_enunciado': True,
        'pagina_responder': True,
        'pagina': 'responder',
        'mais_responderam': ranking_mais_responderam(),
        'ranking_geral': ranking_top_pontos()
    }
    try:
        resposta_aluno = enunciado.resposta_set.get(aluno=request.user.aluno, ativo=True)
        if resposta_aluno.concluido:
            ctx.update({'flag_enunciado': False})
    except Exception as e:
        pass

    ctx.update({
        'enunciado': enunciado,
        'resposta': resposta_aluno,
    })
    return render(request, 'enunciado-responder.html', ctx)


def urlencode(data):
    url = []
    for k, v in data.iteritems():
        url.append(u'{}={}'.format(k, v))
    return '&'.join(url)


def busca(request):
    data = request.GET
    aluno = aluno_from_user_request(request)

    ctx = {
        'resultado': [],
        'anuncios': Anuncio.objects.filter(pag_resultado_busca=True, ativo=True)
    }
    kwargs = {}
    args = []
    fields_exclude = ['tags', 'texto', 'corrigidas', 'Respondidas', 'desatualizado', 'jarespondi', 'page']

    for key, value in data.iteritems():
        if value and value != '0' and key not in fields_exclude:
            kwargs[key] = value
    # PALAVRA CHAVE
    texto = data.get('texto')
    if texto:
        if texto.isdigit():
            args.append(Q(id=texto))
        elif texto:
            args.append(Q(texto__icontains=texto))
            ctx['hilitor'] = texto
    # FILTRAR POR CORRIGIDAS/RESPONDIDAS
    corrigidas = data.get('corrigidas')
    if corrigidas:
        args.append(Q(resposta__concluido=True))
        if corrigidas[0] == 'Respondidas':
            args.append(Q(resposta__isnull=False))
        else:
            args.append(Q(resposta__correcao__isnull=False))
    # EXCLUIR DESATUALIZADAS
    if data.get('desatualizado'):
        args.append(Q(desatualizado=False))
    # EXCLUIR JA RESPONDI
    if data.get('jarespondi'):
        if aluno:
            args.append(~Q(resposta__aluno=aluno))
    if kwargs.get('filtro'):
        del kwargs['filtro']
    resultado = EnunciadoProposta.objects.filter(*args, **kwargs)
    if corrigidas:
        resultado = resultado.distinct()

    ctx['resultado'] = listing(request, resultado, 10)
    ctx['data'] = data.copy()
    if ctx['data'].get('page'):
        ctx['data'].pop('page')
    ctx['ranking_geral'] = ranking_top_pontos()
    ctx.update(
        dict(urlextra='&' + urlencode(ctx['data']))
    )
    return render(request, 'busca-form.html', ctx)


def _busca(request):
    ctx = {
        'resultado': [],
        'anuncios': Anuncio.objects.filter(pag_resultado_busca=True, ativo=True)
    }
    aluno = aluno_from_user_request(request)
    if not request.method == 'POST':
        filtro = request.GET.get('filtro')
        if filtro in ['resposta', 'correcao']:
            if filtro == 'resposta':
                resultado = EnunciadoProposta.objects.filter(resposta__isnull=False)
            else:
                resultado = EnunciadoProposta.objects.filter(resposta__correcao__isnull=False)
            resultado = resultado.distinct()
            if resultado:
                ctx.update(dict(
                    resultado=listing(request, resultado, 10))
                )
            ctx.update(dict(ranking_geral=ranking_top_pontos()))
            return render(request, 'busca-form.html', ctx)

        if 'busca-enunciado-post' in request.session:
            request.POST = request.session['busca-enunciado-post']
            request.method = 'POST'
    if request.method == 'POST':
        request.session['busca-enunciado-post'] = request.POST
        data = dict(request.POST)
        data.pop('csrfmiddlewaretoken')
        if data.get('tags'):
            data.pop('tags')

        args = {}
        argsf = []
        # PALAVRA CHAVE
        texto = data.get('texto')
        if texto:
            texto = data.get('texto')[0]
            data.pop('texto')
            if texto.isdigit():
                args['id'] = texto
            else:
                args['texto__icontains'] = texto
                ctx.update({'hilitor': texto})

        # FILTRAR POR CORRIGIDAS/RESPONDIDAS
        corrigidas = data.get('corrigidas')
        if corrigidas:
            data.pop('corrigidas')
            args['resposta__concluido'] = True
            if corrigidas[0] == 'Respondidas':
                args['resposta__isnull'] = False
            else:
                args['resposta__correcao__isnull'] = False
        # EXCLUIR DESATUALIZADAS
        if data.get('desatualizado'):
            data.pop('desatualizado')
            args['desatualizado'] = False
        # EXCLUIR JA RESPONDI
        if data.get('jarespondi'):
            data.pop('jarespondi')
            if aluno:
                argsf.append(~Q(resposta__aluno=aluno))

        for field, value in data.iteritems():
            value = value[0]
            if value in ['0', '']:
                continue
            args[field] = value
        if data:
            resultado = EnunciadoProposta.objects.filter(*argsf, **args)
            if corrigidas:
                resultado = resultado.distinct()
            if resultado:
                ctx.update(dict(
                    resultado=listing(request, resultado, 10))
                )
        ctx.update(dict(fields=data, ranking_geral=ranking_top_pontos()))
    return render(request, 'busca-form.html', ctx)


@csrf_exempt
def avaliar_resposta(request, rid):
    ret = {'color': ''}
    try:
        error = False
        nota = request.GET.get('nota')
        if nota:
            oresposta = Resposta.objects.filter(pk=rid).first()
            aluno = request.user.aluno
            if not NotaResposta.objects.filter(aluno=aluno, resposta=oresposta):
                onota = NotaResposta(
                    aluno=aluno,
                    resposta=oresposta,
                    nota=nota
                )
                onota.save()
                mensagem = u"Agradecemos a sua avaliação."
                ret['color'] = onota.get_color()
                enviar_email(
                    'email/email-nota.html',
                    u'Sua resposta recebeu uma avaliação',
                    [oresposta.aluno.email], {'resposta': oresposta},
                    ead=True
                )
            else:
                error = True
                mensagem = u"Você já avaliou esta resposta."
        else:
            mensagem = u"É necessário informar uma nota."
            error = True
    except Exception as e:
        mensagem = str(e)
        error = True
    ret['mensagem'] = mensagem
    ret['error'] = error
    return JsonResponse(ret)


@csrf_exempt
def avaliar_correcao(request):
    cid = request.GET.get('cid')  # correcao id
    correcao = Correcao.objects.get(id=cid)
    erro = False

    if correcao.aluno_id == request.user.aluno.id:
        msg = u"Você não pode avaliar sua correção!"
        erro = True
    else:
        try:
            AvaliacaoCorrecao.objects.get(correcao_id=cid, aluno=request.user.aluno)
            msg = u"Você já avaliou essa Correção"
            erro = True
        except Exception as e:
            avaliacao = AvaliacaoCorrecao(
                aluno=request.user.aluno,
                correcao_id=cid
            )
            avaliacao.save()
            msg = u"Obrigado por avaliar"
    return JsonResponse({'mensagem': msg, 'erro': erro, 'pontos': correcao.get_avaliacao_positiva})


@csrf_exempt
def obter(request):
    aluno = aluno_from_user_request(request)
    res = []
    if request.method == 'GET':
        tipo = request.GET.get('tipo')
        parent_id = request.GET.get('parent_id')
        if tipo == 'E':
            queryset = EsferaEspecifica.objects.filter(esfera_geral_id=parent_id)
            res = map(lambda x: {'id': x.id, 'text': x.nome}, queryset)
        elif tipo == 'C':
            queryset = Cargo.objects.filter(esfera_especifica_id=parent_id)
            res = map(lambda x: {'id': x.id, 'text': x.nome}, queryset)
        elif tipo == 'concurso':
            queryset = Concurso.objects.filter(cargo_id=parent_id)
            res = map(lambda x: {'id': x.id, 'text': x.nome}, queryset)
        elif tipo == 'filtro' and aluno:
            queryset = aluno.filtro_set.all()
            res = map(lambda x: {'value': x.id, 'text': x.nome}, queryset)
        elif tipo == 'filtro' and not aluno:
            queryset = Filtro.objects.all()
            res = map(lambda x: {'value': x.id, 'text': x.nome}, queryset)
        elif tipo == 'aplicar_filtro':
            filtro_id = request.GET.get('filtro_id')
            filtro = Filtro.objects.get(id=filtro_id)
            res = []
            for key, value in model_to_dict(filtro).iteritems():
                checked = False
                if key in ['id', 'aluno', 'nome']:
                    continue
                elif key in ['corrigidas', 'desatualizado', 'respondidas']:
                    checked = True
                res.append(dict(
                    id_element='id_{0}'.format(key),
                    valor=value,
                    check=checked
                ))
    else:
        # SALVA O FILTRO DO FORMULÁRIO DE BUSCA
        data = dict(request.POST)
        if aluno:
            data.pop('tags')
            nome_filtro = data.pop('nome_filtro')
            nome_filtro = nome_filtro[0][:-1]  # remove a aspas que vem no final do input nome_filtro
            args = {}
            for field, value in data.iteritems():
                value = value[0]
                if value in ['0', ''] or field in ['csrfmiddlewaretoken', 'classificacao', '"csrfmiddlewaretoken']:
                    continue
                args[field] = value
            if len(args) >= 2:
                filtro_existe = Filtro.objects.filter(nome=nome_filtro, aluno_id=aluno.id)
                if filtro_existe:
                    res = {
                        'erro': True,
                        'mensagem': u'Filtro com o Nome: {0}. Já Existe!'.format(nome_filtro.upper())
                    }
                else:
                    f = Filtro(**args)
                    f.nome = nome_filtro
                    f.aluno_id = aluno.id
                    f.save()
                    res = {'erro': False}
            else:
                res = {
                    'erro': True,
                    'mensagem': u'Selecione ao menos uma Opção para poder Salvar um Filtro.'
                }

        else:
            res = {
                'erro': True,
                'mensagem': u'Efetue Login ou Cadastre-se para poder salvar um Filtro.'
            }

    return JsonResponse(res, safe=False)


@csrf_exempt
def salvar_resposta(request):
    ctx = {
        'status': 'success',
        'concluido': False,
    }
    data = request.POST
    resposta_id = data.get('resposta_id')
    enunciado_id = data.get('enunciado_id')
    texto_resposta = data.get('content')
    concluido = data.get('concluido')

    tempo = data.get('tempo')
    if resposta_id:
        resposta = Resposta.objects.get(id=resposta_id)
        resposta.data_termino = timezone.now()
        resposta.texto = texto_resposta
        resposta.tempo = tempo
        if concluido == '1':
            size = resposta.qtda_char
            min_size = resposta.enunciado.min_char
            ctx.update(dict(
                concluido=True,
                url='{0}{1}?shared=True'.format(SITEADD, resposta.get_absolute_url())
            ))
            resposta.concluido = concluido
            resposta.send_mail = True
        resposta.save()
    else:
        resposta = Resposta(
            texto=texto_resposta,
            enunciado_id=enunciado_id,
            aluno_id=request.user.aluno.id
        )
        resposta.save()
        ctx.update(dict(resposta_id=resposta.id))

    return JsonResponse(ctx)


@login_required
def resposta_desativar(request, rid):
    o_resposta = get_object_or_404(Resposta, id=rid)
    if o_resposta.aluno != request.user.aluno:
        raise PermissionDenied

    o_resposta.ativo = False
    o_resposta.save()
    enunciado = o_resposta.enunciado
    messages.success(request, u'Sua resposta foi desativada')
    return HttpResponseRedirect(reverse('enunciado:responder', args=(enunciado.get_tipo_url, enunciado.id)))


def recentes(request):
    ctx = {
        'resultado': listing(request, EnunciadoProposta.objects.all().order_by('-id')[:100]),
        'anuncios': Anuncio.objects.filter(pag_enunciados=True, ativo=True),
        'ranking_geral': ranking_top_pontos()
    }
    return render(request, 'enunciado/recentes.html', ctx)