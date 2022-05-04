# coding=utf-8
from __future__ import unicode_literals
from decimal import Decimal

from django.template import RequestContext
from django.template.loader import render_to_string

from carton.cart import Cart
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from libs.util.templatetags.helpers import currency
from .models import Cupom


@csrf_protect
@dajaxice_register
def remover_cupom(request, codigo):
    cart = Cart(request.session)
    try:
        cupom = Cupom.objects.get(codigo=codigo, ativo=True)
    except Cupom.DoesNotExist:
        cupom = False
    cart.discount = 0
    cart.cupom = False
    cart.update_session()
    x = Dajax()
    messages.success(request, 'Cupom removido com sucesso!')
    x.script('location.reload();')
    return x.json()


@csrf_protect
@dajaxice_register
def desconto_cupom(request, codigo):
    try:
        cupom = Cupom.objects.get(codigo=codigo, ativo=True)
    except Cupom.DoesNotExist:
        cupom = False

    x = Dajax()

    cart = Cart(request.session)
    if valida_cupom(cupom, cart, request):
        cart.discount = regras_cupom[cupom.tipo](cupom, cart)
        cart.cupom = codigo
        cart.update_session()

        tpl = render_to_string('carrinho-pagamento-com-desconto.html', context_instance=RequestContext(request))
        x.assign('.discount', 'innerHTML', tpl)
        x.assign('.total-payment', 'innerHTML', str(cart.total_payment))
        # x.script("swal_alert('Parabéns', 'Cupom validado com sucesso. Desconto aplicado!', 'success')")
        messages.success(request, 'Cupom validado com sucesso. Desconto aplicado!')
        x.script('location.reload();')
    else:
        x.script("swal_alert('Ops...', 'Cupom inválido', 'error')")

    x.script('$.unblockUI();')
    return x.json()


def valida_cupom(cupom, cart, request):
    if cupom:
        if cupom.data_limite:
            if timezone.now() <= cupom.data_limite:
                pass
            else:
                return False

        if cupom.qte_max_uso:
            if cupom.qte_usada < cupom.qte_max_uso:
                pass
            else:
                return False

        if cupom.cliente:
            if cupom.cliente.pk == request.user.aluno.pk:
                pass
            else:
                return False

        if cupom.primeira_compra:
            if request.user.aluno.checkout_set.filter(aluno=request.user.aluno, success=True).exists():
                return False

        if cupom.produtos.all():
            prds = (set(prd.pk for prd in cupom.produtos.all()) &
                    set(item.pk for item in cart.products))
            if prds:
                pass
            else:
                return False
        return True
    else:
        return False


def desconto_valor(cupom, carrinho):
    return cupom.valor_desconto


def desconto_percentual(cupom, carrinho):
    total = cupom.percentual_desconto / 100 * carrinho.total
    return Decimal("{0:.2f}".format(total))


def desconto_zera_frete(cupom, carrinho):
    return carrinho.valor_frete


def desconto_percentual_frete(cupom, carrinho):
    total = cupom.percentual_desconto / 100 * carrinho.total
    return Decimal("{0:.2f}".format(total))


regras_cupom = {
    u'Nominal (Valor)': desconto_valor,
    u'Nominal (Percentual)': desconto_percentual,
    u'Zerar o Frete': desconto_zera_frete,
    u'Desconto no Frete (Percentual)': desconto_percentual_frete,
    u'Desconto no Frete (Valor)': desconto_valor,
    u'Desconto na compra (Percentual)': desconto_percentual,
    u'Desconto na Compra (Valor)': desconto_valor,
}