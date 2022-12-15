# -*- coding: utf-8 -*-
# Autor: christian
from datetime import timedelta

from django import template
from django.utils import timezone

from apps.curso.models import SentencaAvulsaAluno, CheckoutItens, SentencaOABAvulsaAluno, Cortesia
from apps.financeiro.models import ConfiguracaoPacote
from apps.formulario_auto_correcao.models import RespostaAluno

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_cortesia(context, simulado):
    aluno = context['request'].user.aluno
    try:
        return Cortesia.objects.get(aluno=aluno, curso=simulado, utilizado=False)
    except Cortesia.DoesNotExist:
        return Cortesia.objects.none()


@register.assignment_tag(takes_context=True)
def get_sentenca(context, sentenca):
    aluno = context['request'].user.aluno
    return SentencaAvulsaAluno.objects.filter(aluno=aluno, sentenca_avulsa=sentenca).first()


@register.assignment_tag(takes_context=True)
def get_configuracao_pacote(context):
    configuracao_pacote = ConfiguracaoPacote.objects.filter(ativo=True).first()
    return configuracao_pacote


@register.assignment_tag(takes_context=True)
def get_resposta(context, tabela):
    aluno = context['request'].user.aluno
    try:
        return RespostaAluno.objects.get(
            aluno=aluno,
            tabela_id=tabela,
        )
    except RespostaAluno.DoesNotExist:
        return RespostaAluno.objects.none()


@register.assignment_tag()
def sentenca_data_limite(data_compra, check=False):
    if not data_compra:
        data_compra = timezone.now()
    data_limite = data_compra + timedelta(days=365)
    if check:
        now = timezone.now()
        return now > data_limite
    else:
        return data_limite


@register.assignment_tag(takes_context=True)
def get_sentenca_oab(context, sentenca):
    aluno = context['request'].user.aluno
    return SentencaOABAvulsaAluno.objects.filter(aluno=aluno, sentenca_oab=sentenca).first()


@register.assignment_tag(takes_context=True)
def get_transaction(context, curso):
    retval = {'check': False, 'trans': False}
    try:
        aluno = context['request'].user.aluno
        ci = CheckoutItens.objects.filter(checkout__aluno=aluno, curso_id=curso).last()
        trans = ci.checkout.transaction
        retval = {'check': ci, 'trans': trans}
    except:
        pass
    return retval

@register.assignment_tag(takes_context=True)
def get_checkoutitem(context, curso):
    checkoutiten = curso.checkoutitens_set.filter(
        curso__sentenca_avulsa__isnull=False,
        checkout__aluno_id=3,
        checkout__transaction__status__in=['pago', 'disponivel']
    ).distinct().first()
    return checkoutiten


@register.assignment_tag(takes_context=True)
def get_checkout_cursos(context, checkout, is_tutorial=False):
    return checkout.checkoutitens_set.filter(
        curso__sentenca_avulsa__isnull=True, curso__sentenca_oab__isnull=True,
        curso__categoria__tipo__in=['C', 'S', 'O'], curso__is_tutorial=is_tutorial
    )


@register.assignment_tag(takes_context=True)
def get_checkout_curso_ativo(context, checkout):
    ativo = False
    for item in checkout.get_cursos:
        if item.curso.disponivel:
            ativo = True
            break
    return ativo
