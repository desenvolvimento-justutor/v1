# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from collections import OrderedDict
from decimal import Decimal

import pycep_correios
import xmltodict
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView, FormView

from apps.curso.models import Curso
from apps.financeiro.models import Credito
from apps.pagseguro.api import PagSeguroApiTransparent, PagSeguroItem
from apps.pagseguro.models import Checkout
from carton.cart import Cart
from .forms import CartForm
from .utils import adicionar_cupom

ERRORS = {
    '5003': "Falha de comunicação com a instituição financeira.",
    '10000': "Bandeira inválida.",
    '10001': "Número do cartão inválido.",
    '10002': "Data no formato inválido.",
    '10003': "Código de segurança inválido.",
    '10004': "Código de segurança obrigatório.",
    '10006': "Código de segurança inválido.",
    '11007': "URL de redirecionamento inválida.",
    '13001': "Valor do código de notificação inválido.",
    '13005': "a data inicial deve ser inferior ao limite permitido.",
    '13009': "A data final deve ser inferior ao limite permitido.",
    '13013': "Valor inválido da página.",
    '13014': "Resultados máximos da página inválido (deve estar entre 1 e 1000).",
    '13020': "Página é maior que o número total de páginas retornadas.",
    '53004': "Quantidade de ítens inválido.",
    '53005': "Moeda obrigatória.",
    '53006': "Moeda inválida.",
    '53007': "Tamanho do campo referência inválido.",
    '53008': "URL de notificação inválida.",
    '53009': "Tamanho da URL de notificação inválida.",
    '53010': "Email do comprador inválido.",
    '53011': "Email do comprador inválido.",
    '53012': "Tamanho do campo email do comprador inválido.",
    '53013': "Nome do comprador obrigatório.",
    '53014': "Nome do comprador inválido.",
    '53015': "Tamanho do campo nome do comprador inválido.",
    '53017': "CPF do comprador inválido.",
    '53018': "Código de área do telefone inválido.",
    '53019': "Tamanho do campo código de área do telefone inválido.",
    '53020': "Telefone obrigatório.",
    '53021': "Telefone inválido.",
    '53022': "CEP obrigatório.",
    '53023': "CEP inválido.",
    '53024': "Rua do endereço obrigatório.",
    '53025': "Rua do endereço inválido.",
    '53026': "Número do endereço obrigatório.",
    '53027': "Número do endereço inválido.",
    '53028': "Complemento do endereço inválido.",
    '53029': "Bairro do endereço obrigatório.",
    '53030': "Bairro do endereço inválido.",
    '53031': "Cidade do endereço obrigatória.",
    '53032': "Cidade do endereço inválida.",
    '53033': "Estado do endereço obrigatório.",
    '53034': "Estado do endereço inválido.",
    '53035': "País do endereço obrigatório.",
    '53036': "País do endereço inválido.",
    '53037': "Token do cartão de crédito obrigatório.",
    '53038': "Quantidade de parcelas obrigatória.",
    '53039': "Quantidade de parcelas inválida.",
    '53040': "Valor da parcela obrigatória.",
    '53041': "Valor da parcela inválida.",
    '53042': "Portador do cartão obrigatório.",
    '53043': "Portador do cartão inválido.",
    '53044': "Tamanho do campo portador do cartão inválido.",
    '53045': "CPF do portador do cartão obrigatório.",
    '53046': "CPF do portador do cartão inválido.",
    '53047': "Data de nascimento do portador do cartão obrigatório.",
    '53048': "Data de nascimento do portador do cartão inválido.",
    '53049': "Código de área do portador do cartão obrigatório.",
    '53050': "Código de área do portador do cartão inválido.",
    '53051': "Telefone do portador do cartão obrigatório.",
    '53052': "Telefone  do portador do cartão inválido.",
    '53053': "CEP do portador do cartão obrigatório.",
    '53054': "CEP do portador do cartão inválido.",
    '53055': "Rua do portador do cartão obrigatório.",
    '53056': "Rua do portador do cartão inválido.",
    '53057': "Número do endereço do portador do cartão obrigatório.",
    '53058': "Número do endereço do portador do cartão inválido.",
    '53059': "Tamanho do campo complemento do endereço do portador do cartão inválido.",
    '53060': "Bairro do portador do cartão obrigatório.",
    '53061': "Tamanho do campo bairro do portador do cartão inválido.",
    '53062': "Cidade do portador do cartão obrigatório.",
    '53063': "Tamanho do campo cidade do portador do cartão inválido.",
    '53064': "Estado do portador do cartão obrigatório.",
    '53065': "Estado do portador do cartão inválido.",
    '53066': "País do portador do cartão obrigatório.",
    '53067': "Tamanho do campo país do portador do cartão inválido.",
    '53068': "Tamanho do email do vendedor inválido.",
    '53069': "Email do vendedor inválido.",
    '53070': "Código do ítem obrigatório.",
    '53071': "Tamanho do código do ítem inválido.",
    '53072': "Descrição do ítem obrigatório.",
    '53073': "Tamanho do campo ítem inválido.",
    '53074': "Quantidade de ítens obrigatória.",
    '53075': "Quantidade de ítens fora do limite.",
    '53076': "Quantidade de ítens inválido.",
    '53077': "Montante do ítem obrigatório.",
    '53078': "Montante do ítem inválido.",
    '53079': "Montante fora do limite.",
    '53081': "Comprador é igual ao vendedor.",
    '53084': "Vendedor inválido, verifique se é uma conta com status de vendedor.",
    '53085': "Método de pagamento indisponível.",
    '53086': "Montante total acima do limite do cartão.",
    '53087': "Dados do cartão inválidos.",
    '53091': "Hash do comprador inválido.",
    '53092': "Bandeira do cartão não aceita.",
    '53095': "Tipo de entrega inválido.",
    '53096': "Custo de entrega inválido.",
    '53097': "Custo da entrega fora do limite.",
    '53098': "Valor total é negatívo.",
    '53099': "Montante extra inválido.",
    '53101': "Modo de pagamento inválido, valores válidos são default e gateway.",
    '53102': "Método de pagamento inválido, valores válidos são creditCard, boleto e eft.",
    '53104': "Custo de entrega informado, endereço de entrega deve ser completo.",
    '53105': "Informações do comprador informado, email também deve ser informado.",
    '53106': "Portador do cartão incompleto.",
    '53109': "Endereço do comprador informado, email do comprador também deve ser informado.",
    '53110': "Banco eft obrigatório.",
    '53111': "Banco eft não aceito.",
    '53115': "Data de nascimento do comprador inválida.",
    '53117': "CPNJ do comprador inválido.",
    '53122': "Domínio do email do comprador inválido. Você deve usar um email @sandbox.pagseguro.com.br.",
    '53140': "Quantidade de parcelas fora do limite. O valor deve ser maior que zero.",
    '53141': "Comprador bloqueado.",
    '53142': "Token do cartão de crédito inválido.",
    '14007': "Status da transação não permite reembolso.",
    '53149': "IP inválido.",
}


class CartView(FormView):
    template_name = 'checkout/cart.html'
    template_name_empty = 'checkout/cart_empty.html'
    success_url = reverse_lazy('checkout:cart')
    form_class = CartForm

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        cart = Cart(self.request.session)
        cursos = Curso.objects.none()
        if cart.is_empty:
            now = timezone.now()
            args = [Q(data_fim__gte=now) | Q(data_fim__isnull=True)]
            cursos = Curso.objects.filter(aluno__isnull=True, *args)[:10]
        context.update(cart=cart, title='Carrinho', cursos=cursos)
        return context

    def get_template_names(self):
        cart = Cart(self.request.session)
        template_names = super(CartView, self).get_template_names()
        if cart.is_empty:
            template_names = [self.template_name_empty]
        return template_names

    def form_valid(self, form):
        valido = adicionar_cupom(self.request, codigo=form.cleaned_data['codigo'])
        if not valido:
            form.add_error('codigo', ValidationError('Cupom inválido.'))
            return self.form_invalid(form)
        return super(CartView, self).form_valid(form)

    def form_invalid(self, form):
        invalido = super(CartView, self).form_invalid(form)
        remover = form.data['remover']
        if remover == 'True':
            cart = Cart(self.request.session)
            cart.discount = 0
            cart.cupom = False
            cart.update_session()
            messages.error(self.request, 'Cupom removido!')
            return HttpResponseRedirect(self.success_url)
        return invalido

    def get(self, request, *args, **kwargs):
        return super(CartView, self).get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super(CartView, self).get_form(form_class)
        cart = Cart(self.request.session)
        if cart.cupom:
            atrs = form.fields['codigo'].widget.attrs
            atrs.update(disabled='disabled')
            form.fields['codigo'].widget.attrs = atrs
            form.fields['codigo'].initial = cart.cupom
            form.fields['remover'].initial = True
        return form


class PersonalInfomationView(TemplateView):
    template_name = 'checkout/personal_information.html'

    def render_to_response(self, context):
        self.get_context_data()
        cart = Cart(self.request.session)
        context.update(cart=cart, title='Dados Pessoais')
        pagseguro_session = PagSeguroApiTransparent().get_session_id()
        response = super(PersonalInfomationView, self).render_to_response(context)
        response.set_cookie('pagseguro_session', value=pagseguro_session['session_id'])
        return response


class PaymentView(TemplateView):
    template_name = 'checkout/payment.html'

    def render_to_response(self, context):
        self.get_context_data()
        cart = Cart(self.request.session)
        pagseguro_session = PagSeguroApiTransparent().get_session_id()
        context.update(cart=cart, title='Pagamento', session_id=pagseguro_session['session_id'])
        response = super(PaymentView, self).render_to_response(context)
        response.set_cookie('pagseguro_session', value=pagseguro_session['session_id'])
        return response


class StatusView(TemplateView):
    template_name = 'checkout/status.html'

    def render_to_response(self, context, **response_kwargs):
        code = context.get('code')
        checkout = get_object_or_404(Checkout, code=code)
        context.update(checkout=checkout, title='Conclusão', code=code)
        return super(StatusView, self).render_to_response(context, **response_kwargs)

    def get(self, request, *args, **kwargs):
        return super(StatusView, self).get(request, *args, **kwargs)


def ajax_cupom_actions(request):
    data = request.POST
    action = data.get('action')
    if action == 'add':
        adicionar_cupom()
    return JsonResponse({'data': 'data'})


def ajax_busca_cep(request):
    data = request.GET
    ret = {
        'erro': False,
        'message': 'CEP Encontrado'
    }
    try:
        endereco = pycep_correios.consultar_cep(data.get('cep'))
        ret.update(endereco)
    except Exception as e:
        ret.update(message=str(e), erro=True)
    return JsonResponse(ret)


def somente_numeros(text):
    return re.sub('[^0-9]', '', text)


def ajax_checkout(request):
    aluno = request.user.aluno
    ret = {}
    data = request.POST
    payment_method = data['paymentmethod']
    print("*" * 100)
    print(data)
    print("*" * 100)
    raise Exception("Pass")
    celular = somente_numeros(data.get('celular'))
    ddd = celular[:2] if celular else ''
    phone = celular[2:] if celular else ''

    cart = Cart(request.session)
    api = PagSeguroApiTransparent()
    api.set_notification_url('https://www.justutor.com.br/pagseguro/')
    api.set_reference(
        '{}:{}'.format(
            aluno.pk, somente_numeros(data['cpf'])
        )
    )

    if Decimal(cart.discount):
        api.set_extra_amount(Decimal(cart.discount) * -1)
    for i in cart.items:
        item = PagSeguroItem(
            id='{0:06d}'.format(i.product.pk),
            description=u'{0}'.format(i.product.nome)[:100],
            amount='{0:.2f}'.format(i.price),
            quantity='{}'.format(i.quantity)
        )
        api.add_item(item)

    # SENDER
    sender = {
        'name': data['name_on_card'] or data['nome'] or request.user.aluno,
        'area_code': ddd,
        'phone': phone,
        'email': data['email'],
        'cpf': re.sub('[^0-9]', '', data['cpf'])
    }
    # SHIPPING
    shipping = {
        'street': data['logradouro'],
        'number': data['numero'],
        'complement': data['complemento'],
        'district': data['bairro'],
        'postal_code': re.sub('[^0-9]', '', data['cep']),
        'city': data['cidade'],
        'state': data['uf'],
        'country': 'BRA'
    }

    api.set_sender(**sender)
    api.set_shipping(**shipping)
    if payment_method == 'creditcard':
        # CREDITCARD DATA
        quantity, value = data['cc_parcelas'].split(':')

        creditcard_data = {
            'quantity': int(quantity),
            'value': '%.02f' % float(value),
            'name': data['name_on_card'],
            'birth_date': data['nascimento'],
            'cpf': re.sub('[^0-9]', '', data['cpf']),
            'area_code': ddd,
            'phone': phone
        }
        api.set_creditcard_data(**creditcard_data)
        api.set_creditcard_billing_address(**shipping)
        api.set_creditcard_token(data['token'])
    api.set_sender_hash(data['senderHash'])
    api.set_payment_method(payment_method)
    data_api = api.checkout()
    success = data_api.get('success')
    message = data_api.get('message')

    if not success:

        message = xmltodict.parse(message)

        errors = message.get('errors').get('error')
        errors_messages = []
        if isinstance(errors, OrderedDict):
            errors = [errors]
        for erro in errors:
            errors_messages.append(ERRORS.get(erro.get('code')))
        ret.update({
            'error': errors_messages
        })
    else:
        code = data_api.get('code')
        ret.update({
            'link': '/checkout/status/%s' % code,
            'code': code
        })
        # try:
        #     chk = Checkout.objects.get(code=code)
        #     chk.aluno = request.user.aluno
        #     chk.date = data_api.get('date')
        #     chk.success = data_api.get('success')
        #     chk.message = data_api.get('response')
        #     chk.cpf = data['cpf']
        #     chk.save()
        # except Checkout.DoesNotExist:
        #     chk = Checkout(
        #         code=data_api.get('code'),
        #         aluno=request.user.aluno,
        #         date=data_api.get('date'),
        #         success=data_api.get('success'),
        #         message=data_api.get('response'),
        #         cpf=data['cpf']
        #     )
        #     chk.save()
        #     for i in cart.items:
        #         item = CheckoutItens(
        #             checkout=chk,
        #             curso=i.product,
        #             valor=i.price,
        #             qtda=i.quantity
        #         )
        #         item.save()
        #         # p = item.product
        #         # if p.aluno:
        #         #     p.state = 'F'
        #         #     p.save()
        for item in cart.items:
            if item.configuracao_pacote:
                credito = Credito(
                    aluno=aluno,
                    quantidade=item.quantidade,
                    origem="compra",
                    # checkout=Checkout.objects.get(code=code)
                )
                if item.pacote and item.pacote != 'false':
                    credito.pacote_id = item.pacote
                credito.save()
        cart.clear()
    return JsonResponse(ret)


def ajax_check_checkout(request):
    try:
        checkout = Checkout.objects.get(code=request.GET['code']).code
    except Checkout.DoesNotExist:
        checkout = False
    return JsonResponse({'checkout': checkout})
