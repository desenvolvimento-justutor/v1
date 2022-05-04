# -*- coding: utf-8 -*-
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from .models import CursoAvaliacao, Curso, LiberarCompraCurso
from carton.cart import Cart
from django.contrib import messages
from apps.website.utils import CPF
from decimal import Decimal


@dajaxice_register(method='POST')
def avaliar(request, curso_id, avaliacao):
    x = Dajax()
    try:
        try:
            aluno = request.user.aluno
        except:
            aluno = False
        if not aluno:
            x.script("BootstrapDialog.alert('Efetue login para poder Avaliar!');")
        else:
            res_avaliacao = CursoAvaliacao.objects.filter(user_id=aluno.usuario.id, curso_id=curso_id).last()
            if not res_avaliacao:
                curso_avaliacao = CursoAvaliacao(
                    user_id=aluno.usuario.id,
                    curso_id=curso_id,
                    avaliacao=avaliacao
                )
                tipo_curso = 'Livro' if curso_avaliacao.curso.categoria.tipo == 'L' else 'Curso'
                curso_avaliacao.save()
                if avaliacao == 'O':
                    total = CursoAvaliacao.objects.filter(curso_id=curso_id, avaliacao='O').count()
                    x.clear('#id_otimo', 'innerHTML')
                    x.append('#id_otimo', 'innerHTML', total)
                elif avaliacao == 'B':
                    total = CursoAvaliacao.objects.filter(curso_id=curso_id, avaliacao='B').count()
                    x.clear('#id_bom', 'innerHTML')
                    x.append('#id_bom', 'innerHTML', total)
                else:
                    total = CursoAvaliacao.objects.filter(curso_id=curso_id, avaliacao='R').count()
                    x.clear('#id_ruim', 'innerHTML')
                    x.append('#id_ruim', 'innerHTML', total)
                total_avaliacao = CursoAvaliacao.objects.filter(curso_id=curso_id).count()
                x.clear('#aval-total', 'innerHTML')
                x.append('#aval-total', 'innerHTML', total_avaliacao)
                x.script(u"BootstrapDialog.alert('obrigado por avaliar nosso %s!');" % tipo_curso)
            else:
                tipo_curso = 'Livro' if res_avaliacao.curso.categoria.tipo == 'L' else 'Curso'
                avaliacao_aluno = res_avaliacao
                x.script(u"BootstrapDialog.alert('Você já avaliou este {1} como <b>{0}</b>!');".format(
                    avaliacao_aluno, tipo_curso))
            return x.json()
    except Exception as e:
        x.script(u"BootstrapDialog.alert('Erro ao avaliar');")
        return x.json()


@dajaxice_register(method='POST')
def add_to_cart(request, curso_id, codigo=False):
    djx = Dajax()
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
            djx.script(msg)
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
                    djx.script("window.location = '/carrinho/'")
                except LiberarCompraCurso.DoesNotExist:
                    msg = u"msg_erro('Código de liberação invalido: %s.')" % codigo
                    djx.script(msg)
            else:
                cart.add(curso, price=curso.valor)
                msg = u"{1}: {0}, adicionado com sucesso!".format(curso, tipo_curso)
                messages.success(request, msg)
                djx.script("window.location = '/carrinho/'")
    except Exception as e:
        print 'ERRO:', e
        msg = u"msg_erro('Não foi possível adicionar o %s ao Carrinho.')" % tipo_curso
        djx.script(msg)
    djx.script('$.unblockUI()')
    return djx.json()


@dajaxice_register(method='POST')
def set_qtda(request, curso_id, qtda):
    djx = Dajax()
    cart = Cart(request.session)
    try:
        curso = Curso.objects.get(id=curso_id)
        cart.set_quantity(curso, quantity=qtda)
        djx.script("location.reload();")
    except:
        msg = u"msg_erro('Não foi possível adicionar o Curso ao Carrinho.')"
        djx.script(msg)
    # djx.script('$.unblockUI()')
    return djx.json()


@dajaxice_register(method='POST')
def remove_item(request, curso_id):

    djx = Dajax()
    cart = Cart(request.session)
    try:
        curso = Curso.objects.get(id=curso_id)
        cart.remove(curso)
        if curso.aluno:
            curso.delete()
        cart.discount = Decimal(0)
        cart.cupom = False
        cart.update_session()
        djx.script("location.reload();")
        djx.script('swal("JusTutor!", "Item removido.", "success");')
    except:
        msg = u"msg_erro('Não foi possível adicionar o Curso ao Carrinho.')"
        djx.script(msg)
    djx.script('$.unblockUI()')
    return djx.json()


@dajaxice_register(method='POST')
def validar_cpf(request, cpf):
    djx = Dajax()
    try:
        valido = CPF(cpf).valid()
    except:
        valido = False
    if valido:
        cart = Cart(request.session)
        cart.cpf = cpf
        cart.update_session()
        djx.script("$('#helpBlock').addClass('hide')")
        djx.script("$('#cpfModal').modal('hide')")
        djx.script("pagar()")
    else:
        djx.script("$('#helpBlock').removeClass('hide')")
        djx.script("$('#helpBlock').pulsate({color: '#DE7A43', repeat: false});")
        djx.script("$('#idCPF').select();")
        djx.script("$('#idCPF').focus();")
    djx.script('$.unblockUI()')
    return djx.json()

