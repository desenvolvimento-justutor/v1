# -*- coding: utf-8 -*-
# Autor: christian
import logging

import requests
from allauth.account.signals import user_signed_up
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from pysendy import Sendy, AlreadySubscribedException
from xmltodict import parse

from apps.aluno.forms import CadastroAlunoForm
from apps.aluno.models import Aluno
from apps.aluno.views import split_name
from apps.curso.models import Categoria, Curso, CursoAvaliacao
from apps.curso.models import Certificado, CheckoutItens
from apps.enunciado.models import EnunciadoProposta, Resposta
from apps.pagseguro.models import Checkout, Transaction
from apps.professor.models import Professor
from apps.website.models import Anuncio, BannerFooter
from apps.website.utils import enviar_email
from carton.cart import Cart
from justutorial import settings
from justutorial.settings import SITEADD, SMARTWEB_MMKT_LIST_ID, SMARTWEB_MMKT_URL, SENDY_API_KEY
from libs.util.paginar import listing
from models import Institucional, Noticia, VideoJusTutor, NoticiaLida, ArtigoIndice, Artigo, _get_config_ativa
from .utils import get_client_ip

logger = logging.getLogger('django')


def handler500(request):
    data = {
        'request': request
    }

    for k, v in request.environ.iteritems():
        print k, v

    return render(request, '500.html', data, status=500)


@receiver(user_signed_up)
def populate_profile(sender, **kwargs):
    social_login = kwargs.get('sociallogin')
    user = social_login.user

    try:
        Aluno.objects.get(usuario=user)
    except Aluno.DoesNotExist:
        try:
            user.save()
            aluno = Aluno(
                nome=user.get_full_name(),
                email=user.email,
                usuario=user
            )
            aluno.save()
        except:
            pass


# @minified_response
def index(request):
    sleep_cookie = True if request.COOKIES.get('ssp_sleep') else False
    d = timezone.now()
    # rnk = ranking_top_pontos()
    context = {
        'video': VideoJusTutor.objects.filter(Q(data_ini__lte=timezone.now()) | Q(data_ini=None)).first(),
        'home': True,
        'titulo': u'Página inicial',
        'ranking_geral': [],
        'sleep_cookie': sleep_cookie,
        'ultimas_respostas': Resposta.objects.filter(concluido=True, ativo=True).order_by('-data_termino')[:9],
        'slide': request.GET.get('slide'),
        'bannerfooter': BannerFooter.objects.all()
    }
    config = _get_config_ativa()
    if config:
        context.update(dict(noticias=config.get_noticias[:5]))
    return render(request, 'index.html', context)


def email(request):
    import requests
    import json

    url = "https://dev.vdocipher.com/api/videos/33f6be48ad4263da35734b1050f3095a/otp"

    payloadStr = json.dumps({'ttl': 300})
    headers = {
        'Authorization': "Apisecret QPu1yL7eJ4A6JRzJV3KQbmDo6g5sviTdkzFRlRrhffoN3VbxC94tPYl7qYh7Kzxm",
        'Content-Type': "application/json",
        'Accept': "application/json"
    }

    response = requests.post(url, data=payloadStr, headers=headers)
    data = response.json()
    context = data
    return render(request, 'website/face.html', context)


def check_login(request):
    aluno = False
    try:
        aluno = request.user.aluno
        aluno = True
    except:
        pass
    return JsonResponse({'aluno': aluno})


@csrf_exempt
def ajax_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    ret = {
        'redirect': False
    }
    try:
        if user is not None:
            if user.is_active:
                login(request, user)
                ret.update({
                    'success': True,
                    'user': user.aluno.nome,
                    'msg': 'Login efetuado com sucesso!!!'
                })
            else:
                ret.update({
                    'success': True,
                    'user': user.aluno.nome,
                    'msg': 'Usuário desativado!!!'
                })
        else:
            ret.update({
                'success': False,
                'user': False,
                'msg': 'Email ou Senha Incorretos!!!'
            })
    except Exception as e:
        ret.update({
            'success': False,
            'user': False,
            'msg': '%s' % e
        })
    return JsonResponse(ret)


def ajax_cadastro(request):
    ret = {
        'redirect': False
    }

    form = CadastroAlunoForm()
    if request.method == 'POST':
        form = CadastroAlunoForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            # remover chaves da var 'data' que não pertencem ao model 'Aluno'
            password = data.pop('password')
            data.pop('password2')
            # Criar Usuário
            email = data.get('email')
            first_name = split_name(data.get('nome'))
            last_name = split_name(data.get('nome'), True)
            user = User.objects.create_user(
                email, email, password, first_name=first_name, last_name=last_name
            )
            data.update({'usuario_id': user.id})
            # CRIAR ALUNO
            aluno = Aluno(**data)
            aluno.save()
            user = authenticate(username=user.username, password=password)
            login(request, user)
            ret.update({
                'success': True,
                'user': aluno.nome,
                'msg': 'Login efetuado com sucesso!!!'
            })

        else:
            ret.update({
                'success': False,
                'user': False,
                'msg': "%s" % form.errors
            })
    return JsonResponse(ret)


def institucional(request, slug):
    obj_institucional = get_object_or_404(Institucional, slug=slug)
    context = {
        'titulo': obj_institucional,
        'conteudo': obj_institucional,
        'anuncios': Anuncio.objects.filter(pag_conteudo=True, ativo=True)
    }
    return render(request, 'conteudo.html', context)


def livraria(request, slug):
    obj_categoria = get_object_or_404(Categoria, slug=slug)
    context = {
        'titulo': obj_categoria,
        'categoria': obj_categoria,
        'livros': obj_categoria.curso_set.all(),
        'anuncios': Anuncio.objects.filter(pag_conteudo=True, ativo=True)
    }
    return render(request, 'livraria.html', context)


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


def noticia(request, slug):
    obj_noticia = get_object_or_404(Noticia, slug=slug)
    ip = get_client_ip(request)
    lida = NoticiaLida.objects.filter(noticia=obj_noticia, ip=ip).first()
    if not lida:
        lida = NoticiaLida(noticia=obj_noticia, ip=ip)
        lida.save()
    mais_lidas = []
    lidas = NoticiaLida.objects.all().values('noticia').annotate(total=Count('noticia')).order_by('-total')[:10]
    for lida in lidas:
        mais_lidas.append(Noticia.objects.get(id=lida.get('noticia')))
    context = {
        'titulo': obj_noticia.nome,
        'conteudo': obj_noticia,
        'is_noticia': True,
        'anuncios': Anuncio.objects.filter(pag_noticias=True, ativo=True),
        'mais_lidas': mais_lidas
    }
    return render(request, 'conteudo.html', context)


def consulta_certificado(request, chave):
    try:
        certificado = Certificado.objects.get(chave=chave)
    except Certificado.DoesNotExist:
        certificado = None
    context = {
        'certificado': certificado,
        'chave': chave
    }
    return render(request, 'consulta-certificado.html', context)


@csrf_exempt
def subscrible(request):
    res = True
    try:
        nome = request.POST.get('FNAME')
        email = request.POST.get('email')
        s = Sendy(base_url=SMARTWEB_MMKT_URL, api_key=SENDY_API_KEY)
        s.subscribe(
            NomeCompleto=nome,
            name=nome.split()[0],
            email=email,
            list_id=SMARTWEB_MMKT_LIST_ID,
            api_key=SENDY_API_KEY
        )
    except AlreadySubscribedException:
        res = True
    except:
        res = False
    result = {
        'result': res,
    }
    return JsonResponse(result)


def imagens(request):
    context = {}
    return render(request, 'imagens.html', context)


# TODO - Remover
def videos_justutor(request):
    videos = VideoJusTutor.objects.filter(Q(data_ini__lte=timezone.now()) | Q(data_ini=None))
    paginator = listing(request, videos, 10)
    context = {
        'videos': paginator,
        'video': paginator[0],
        'anuncios': Anuncio.objects.filter(pag_videos=True, ativo=True)
    }
    return render(request, 'videos.html', context)


def noticias_justutor(request):
    now = timezone.now
    noticias = Noticia.objects.filter(
        Q(ativo_inicio__lte=now), Q(ativo_fim__gte=now) | Q(ativo_fim=None)
    ).order_by('-ativo_inicio')

    paginator = listing(request, noticias, 20)

    mais_lidas = []
    lidas = NoticiaLida.objects.all().values('noticia').annotate(total=Count('noticia')).order_by('-total')[:10]
    for lida in lidas:
        mais_lidas.append(Noticia.objects.get(id=lida.get('noticia')))
    context = {
        'noticias': paginator,
        'anuncios': Anuncio.objects.filter(pag_conteudo=True, ativo=True),
        'mais_lidas': mais_lidas
    }
    return render(request, 'noticias.html', context)


def artigo_imprimir(request, aid):
    artigo = get_object_or_404(Artigo, id=aid)
    context = {'artigo': artigo}
    return render(request, 'artigo-imprimir.html', context)


def artigo_indice(request):
    context = {}
    if request.method == 'POST':
        q = request.POST.get('q')
        artigos = []
        if q:
            artigos = Artigo.objects.filter(Q(nome__icontains=q) | Q(conteudo__icontains=q) | Q(autor__icontains=q))
    else:
        indice = request.GET.get('indice')
        artigo = request.GET.get('artigo')
        if indice:
            context.update({
                'indice': ArtigoIndice.objects.get(id=indice)
            })
            artigos = Artigo.objects.filter(indice=indice)
        elif artigo:
            a = get_object_or_404(Artigo, id=artigo)
            context.update({
                'artigo': a
            })
            artigos = False
        else:
            artigos = Artigo.objects.all()
    context.update({
        'indices': ArtigoIndice.objects.all(),
        'artigos': artigos
    })
    return render(request, 'artigo-indice.html', context)


@require_GET
def busca_tag(request):
    ctx = {
        'busca_home': True,
    }
    q = request.GET.get('tag')

    if not q:
        if 'busca-tag' in request.session:
            q = request.session['busca-tag']['tag']
    else:
        request.session['busca-tag'] = request.GET

    res = EnunciadoProposta.objects.filter(
        Q(tags__nome__icontains=q)
    )
    ctx.update(dict(
        resultado=listing(request, res, 10),
        btag=q))
    return render(request, 'busca-form.html', ctx)


@require_GET
def busca(request):
    ctx = {'busca_home': True}
    q = request.GET.get('q')

    if not q:
        if 'busca-home' in request.session:
            q = request.session['busca-home']['q']
    else:
        request.session['busca-home'] = request.GET

    res = EnunciadoProposta.objects.filter(
        Q(texto__icontains=q) | Q(esfera_geral__nome__icontains=q) | Q(esfera_especifica__nome__icontains=q) |
        Q(cargo__nome__icontains=q) | Q(area_profissional__nome__icontains=q) | Q(orgao_entidade__nome__icontains=q) |
        Q(concurso__nome__icontains=q) | Q(disciplina__nome__icontains=q) | Q(tipo_procedimento__nome__icontains=q) |
        Q(tipo_sentenca__nome__icontains=q) | Q(tipo_peca_pratica__nome__icontains=q) |
        Q(num_questao_caderno__icontains=q) | Q(organizador__nome__icontains=q) | Q(localidade__nome__icontains=q) |
        Q(tags__nome__icontains=q)
    )
    ctx.update(dict(
        resultado=listing(request, res, 10),
        hilitor=q))
    #
    # else:
    #     messages.error(request, 'Informe algum texto para poder efetuar a busca.')
    #     return index(request)
    return render(request, 'busca-form.html', ctx)


def busca_aluno(request):
    q = request.POST.get('q')
    ctx = {'alunos': False}
    if q:
        alunos = Aluno.objects.filter(nome__icontains=q, usuario__is_active=True)
        ctx.update({'alunos': alunos})
    return render(request, 'busca-aluno.html', ctx)


def send_email_contato(nome, email, mensagem):
    logger.info("enviar email contato")

    ctx_email = {
        'dominio': SITEADD,
        'nome': nome,
        'email': email,
        'mensagem': mensagem
    }

    enviar_email(
        'email/email_contato.html',
        u'Contato feito pelo site',
        ["desenvolvimento@justutor.com.br"],
        ctx_email,
        ead=True
    )
    return True


def create_or_update_checkout(request, code, clear_cart=False):
    cart = Cart(request.session)
    try:
        chk = Checkout.objects.get(transaction_code=code)
    except Checkout.DoesNotExist:
        chk = Checkout(
            cpf=cart.cpf,
            code=code,
            transaction_code=code,
            aluno=request.user.aluno,
            date=timezone.now(),
            success=clear_cart,
        )
        chk.save()

    try:
        tr = Transaction.objects.get(code=code)
        if not tr.checkout:
            tr.checkout = chk
            tr.save()
    except Transaction.DoesNotExist:
        tr = Transaction(
            code=code,
            checkout=chk
        )
        tr.save()
    # Check itens
    itens = CheckoutItens.objects.filter(checkout=chk)
    if itens:
        itens.delete()
    else:
        for i in cart.items:
            item = CheckoutItens(
                checkout=chk,
                curso=i.product,
                valor=i.price,
                qtda=i.quantity
            )
            item.save()
    if clear_cart:
        cart.clear()
    return chk


@login_required
def pagseguro_checkout(request):
    cart = Cart(request.session)
    aluno = request.user.aluno
    ret = {
        'erro': False,
    }
    try:
        if settings.PAGSEGURO_SANDBOX:
            url = 'https://ws.sandbox.pagseguro.uol.com.br/v2/checkout'
        else:
            url = 'https://ws.pagseguro.uol.com.br/v2/checkout'
        data = {
            'email': settings.PAGSEGURO_EMAIL,
            'token': settings.PAGSEGURO_TOKEN,
            'currency': 'BRL',
            'reference': '{}:{}'.format(aluno.pk, cart.cpf),
            'shippingType': '3'
        }
        if cart.discount and cart.discount != '0':
            data['extraAmount'] = '-{}'.format(cart.discount)
            data['discountAmount'] = '{}'.format(cart.discount)
        c = 1
        for i in cart.items:
            data['itemId%d' % c] = '{0:06d}'.format(i.product.pk)
            data['itemDescription%d' % c] = '{0}'.format(i.product.nome.encode('ISO-8859-1'))
            data['itemAmount%d' % c] = '{0:.2f}'.format(i.price)
            data['itemQuantity%d' % c] = i.quantity
            data['itemWeight%d' % c] = '0'
            c += 1

        req = requests.post(url, data=data)
        data = parse(req.text)
        if req.status_code == 200:
            code = data['checkout']['code']
            ret['code'] = code
            # create_or_update_checkout(request, code)
        else:
            errs = []
            for key, value in data['errors'].iteritems():
                errs.append("{}: {}".format(value['code'], value['message']))
            ret['errors'] = errs
            ret['erro'] = True
    except Exception as e:
        ret['errors'] = [str(e)]
        ret['erro'] = True
    if request.method == 'GET':
        return HttpResponseRedirect('https://pagseguro.uol.com.br/v2/checkout/payment.html?code=%s' % ret['code'])

    return JsonResponse(ret)


@login_required
def pagseguro_set_transaction(request):
    # code = request.POST.get('trans')
    # create_or_update_checkout(request, code, True)
    Cart(request.session).clear()
    messages.success(
        request,
        'Seu pedido foi efetuado.<br>Assim que o PagSeguro confirmar o pagamento, iremos liberar o seu acesso. '
        '</br><strong>Obrigado!<strong>'
    )
    return JsonResponse({'code': 'success'})


@login_required
def pagseguro_transaction(request, code=None):
    aluno = request.user.aluno
    try:
        if code is None:
            code = request.GET.get['code']
        Cart(request.session).clear()
        chk = Checkout.objects.get(transaction_code=code)
        for item in chk.checkoutitens_set.all():
            curso = item.curso
            if curso.aluno:
                curso.status = 'F'
                curso.save()

    except Checkout.DoesNotExist:
        return HttpResponseRedirect('/')
    data = chk.get_transaction_status()
    ctx = {
        'checkout': chk,
        'data': data,
    }
    try:
        ctx['link'] = data['transaction']['paymentLink']
    except:
        pass
    return render(request, 'website/transaction.html', ctx)


def checkout_itens(request):
    cart = Cart(request.session)
    if not cart.count:
        messages.error(request, 'Não há itens no carrinho.')
        return HttpResponseRedirect('/')
    if settings.PAGSEGURO_SANDBOX:
        url = 'https://ws.sandbox.pagseguro.uol.com.br/v2/checkout'
    else:
        url = 'https://ws.pagseguro.uol.com.br/v2/checkout'
    cart.update_session()
    ctx = {
        'pagseguro_url': url,
        'token': settings.PAGSEGURO_TOKEN,
        'sandbox': settings.PAGSEGURO_SANDBOX,
        'cart': cart
    }
    return render(request, 'website/checkout/base.html', ctx)


class ContextMixinView(ContextMixin):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context_data = super(ContextMixinView, self).get_context_data()
        context_data.update(self.extra_context)
        return context_data


class HomeView(TemplateView, ContextMixinView):
    template_name = 'website/front/home.html'
    extra_context = {
        'title': 'Home'
    }


class ProfessorView(TemplateView, ContextMixinView):
    template_name = 'professores.html'
    extra_context = {
        'title': 'Professores',
        'professores': Professor.objects.filter(publico=True).order_by('nome')
    }
