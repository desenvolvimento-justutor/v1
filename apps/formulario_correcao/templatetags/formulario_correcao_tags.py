# -*- coding: utf-8 -*-
# Autor: christian
from decimal import Decimal

from django import template

from apps.formulario_correcao.models import NotaCorrecao, Formulario

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_nota_selecionada(context, nota, tabela):
    aluno = context['request'].user.aluno
    try:
        return NotaCorrecao.objects.get(aluno=aluno, nota=nota, tabela=tabela)
    except NotaCorrecao.DoesNotExist:
        return False


@register.assignment_tag(takes_context=True)
def get_soma_correcao(context, tabela):
    aluno = context['request'].user.aluno
    notas_obj = NotaCorrecao.objects.filter(aluno=aluno, tabela=tabela)
    sum_notas = sum(map(lambda x: x.nota.valor, notas_obj))
    sum_total = tabela.valor - sum_notas
    if (sum_total < 0 and tabela.proibir_negativa):
        return 0.00
    elif sum_notas == Decimal(0):
        return tabela.valor
    return sum_total


def soma_notas(aluno, atividade):
    soma_notas = []
    try:
        tabelas = atividade.formulario.tabelas.all()
        for tabela in tabelas:
            try:
                notas_obj = NotaCorrecao.objects.filter(aluno=aluno, tabela=tabela)
                sum_notas = sum(map(lambda x: x.nota.valor, notas_obj))
                sum_total = tabela.valor - sum_notas
                if (sum_total < 0 and tabela.proibir_negativa):
                    sum_total = Decimal(0)
                elif sum_notas == Decimal(0):
                    sum_total = tabela.valor
                soma_notas.append(sum_total)
            except:
                pass
    except Formulario.DoesNotExist:
        pass
    return sum(soma_notas)


@register.assignment_tag(takes_context=True)
def get_soma_notas(context, atividade):
    aluno = context['request'].user.aluno
    return soma_notas(aluno, atividade)
