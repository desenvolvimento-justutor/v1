# -*- coding: utf-8 -*-
# @Filename : utils
# @Date : 2019-12-14-08-14
# @Poject: justutor
# @AUTHOR : Christian Douglas <christian.douglas.alcantara@gmail.com>
# from __future__ import unicode_literals
from django.contrib import messages
import json
from carton.cart import Cart
from apps.curso.models import Curso, LiberarCompraCurso
from apps.cupom.ajax import valida_cupom, regras_cupom
from apps.cupom.models import Cupom


def add_to_cart(request, curso_id, codigo=False):
    cart = Cart(request.session)
    try:
        exist = False
        for item in cart.products:
            if item.pk == curso_id:
                exist = True
                break
        curso = Curso.objects.get(id=curso_id)
        tipo_curso = 'Livro' if curso.categoria.tipo == 'L' else 'Curso'
        if exist:
            msg = u"msg_erro('{1}: {0}, já está no seu carrinho!')".format(curso, tipo_curso)
            messages.error(request, msg)
        else:
            if curso.aluno:
                curso.status = 'C'
                curso.save()
            if codigo:
                try:
                    liberar_compra = LiberarCompraCurso.objects.get(codigo=codigo)
                    liberar_compra.ativo = False
                    liberar_compra.save()
                    cart.add(curso, price=curso.valor)
                    msg = u"{1}: {0}, adicionado com sucesso!".format(curso, tipo_curso)
                    messages.success(request, msg)
                except LiberarCompraCurso.DoesNotExist:
                    msg = u"msg_erro('Código de liberação invalido: %s.')" % codigo
                    messages.error(request, msg)
            else:
                cart.add(curso, price=curso.valor)
                msg = u"{1}: {0}, adicionado com sucesso!".format(curso, tipo_curso)
                messages.success(request, msg)
    except Exception as e:
        msg = u"msg_erro('Não foi possível adicionar o %s ao Carrinho.')" % tipo_curso
        messages.error(request, msg)
    return True


def adicionar_cupom(request, codigo):
    try:
        codigo = codigo.upper()
        cupom = Cupom.objects.get(codigo=codigo, ativo=True)
    except Cupom.DoesNotExist:
        cupom = False

    cart = Cart(request.session)
    if valida_cupom(cupom, cart, request):
        codigo = codigo.upper()
        cart.discount = regras_cupom[cupom.tipo](cupom, cart)
        cart.cupom = codigo
        cart.update_session()

        messages.success(request, 'Cupom validado com sucesso. Desconto aplicado!')
    else:
        messages.error(request, 'Cupom inválido')
    return cupom
