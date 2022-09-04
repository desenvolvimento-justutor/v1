import locale
from decimal import Decimal

from django import template
from django.db import connection
from django.db.models import Count, Q
from django.db.models import Sum
from django.utils import timezone

from apps.formulario_correcao.models import TabelaCorrecaoAluno, TabelaAluno, Formulario
from apps.pagseguro.models import Checkout
from apps.website.models import PacoteDesconto
from ..models import (
    TarefaAtividade, Categoria, Serie, ComboAluno,
    Curso, LiberarCompraCurso, SentencaAvulsaAluno,
    CheckoutItens
)

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_correcao_pendentes(context, curso):
    try:
        aluno = context['request'].user.aluno
        tarefas_total = TarefaAtividade.objects.filter(
            atividade__tipo_retorno='C',
            atividade__curso=curso,
            aluno=aluno,
            corrigido=True
        )
        limitar_correcao = curso.limitar_correcao
        if tarefas_total:
            if tarefas_total.count() >= limitar_correcao:
                total = 0
            else:
                total = limitar_correcao - tarefas_total.count()
        else:
            total = limitar_correcao
    except TarefaAtividade.DoesNotExist:
        total = 0
    return total


@register.assignment_tag
def get_correcao_tarefa(atividade, aluno):
    try:
        tarefa = TarefaAtividade.objects.get(
            atividade=atividade,
            aluno=aluno,
            corrigido=True
        )
    except TarefaAtividade.DoesNotExist:
        tarefa = False
    return tarefa


@register.assignment_tag
def get_tarefa(atividade, aluno):
    try:
        tarefa = TarefaAtividade.objects.get(
            atividade=atividade,
            aluno=aluno,
        )
    except:
        tarefa = False
    return tarefa


@register.assignment_tag
def get_sentenca(sentenca, aluno):
    try:
        sentenca = SentencaAvulsaAluno.objects.get(
            sentenca_avulsa=sentenca,
            aluno=aluno,
        )
    except:
        sentenca = False
    return sentenca


@register.assignment_tag(takes_context=True)
def get_recursos_abertos(context, tipo='A'):
    try:
        args = [
            Q(formulario__atividade__isnull=False) | Q(formulario__sentenca_avulca__isnull=False)
        ]
        p = context['request'].user.professor
        return TabelaCorrecaoAluno.objects.filter(status='solicitado', professor=p, *args).count()
    except:
        return None


@register.assignment_tag
def get_tabela_correcao_aluno(atividade, aluno, corrigido=True):
    try:
        formulario = Formulario.objects.get(atividade=atividade)
        tabela_correcao = TabelaCorrecaoAluno.objects.filter(
            aluno=aluno, formulario=formulario, corrigido=corrigido
        ).first()
    except Formulario.DoesNotExist as exc:
        tabela_correcao = None
    return tabela_correcao


@register.assignment_tag
def get_tabela_correcao_aluno_st(sentenca, aluno, corrigido=True):
    try:
        formulario = Formulario.objects.get(sentenca_avulca=sentenca)
        tabela_correcao = TabelaCorrecaoAluno.objects.filter(
            aluno=aluno, formulario=formulario, corrigido=corrigido
        ).first()
    except Formulario.DoesNotExist as exc:
        tabela_correcao = None
    return tabela_correcao


@register.assignment_tag
def get_atividades(curso, professor=None):
    f = []
    if professor:
        return curso.atividade_set.filter(professores=professor)
    return curso.atividade_set.all()


@register.assignment_tag
def get_tarefa_nota(atividade):
    formulario = atividade.get_formulario()
    tot = 0
    if formulario:
        tabela = TabelaAluno.objects.filter(
            tabela_correcao__aluno=atividade.aluno,
            tabela_correcao__formulario=formulario
        ).aggregate(total=Sum('nota'))
        tot = tabela.get('total')
    return tot


@register.assignment_tag
def get_checkout_years():
    truncate_date = connection.ops.date_trunc_sql('year', 'date')
    qs = Checkout.objects.extra({
        'year': truncate_date}
    )
    ret = qs.values('year').annotate(Count('pk')).order_by('year')
    return ret


@register.filter(is_safe=True)
def moeda(value):
    if not value:
        return value
    if isinstance(value, unicode):
        value = Decimal(value)
    return locale.currency(value, grouping=True)


@register.filter(is_safe=True)
def moeda_nosymbol(value):
    if not value:
        return value
    if isinstance(value, unicode):
        value = Decimal(value)
    return locale.currency(value, symbol=False, grouping=True)


@register.filter(is_safe=True)
def moeda_slice(value):
    m = moeda(value)
    return m.split(',')


@register.assignment_tag
def get_categorias(tipo="C"):
    qs = Categoria.objects.filter(tipo=tipo)
    return qs


@register.assignment_tag
def get_series():
    qs = Serie.objects.all()
    return qs


@register.assignment_tag
def get_last_livro():
    qs = Curso.objects.filter(categoria__tipo="L").last()
    return qs


@register.assignment_tag
def get_cursos_lancamento():
    now = timezone.now()
    qs = Curso.objects.filter(Q(data_ini__lte=now), Q(data_fim__gte=now) | Q(data_fim=None)).order_by('-data_ini')[:5]
    # qs = Curso.objects.all().order_by('data_fim')[:4]
    return qs


@register.assignment_tag
def get_codigo_liberacao(aluno, curso):
    now = timezone.now().date()
    try:
        codigo = LiberarCompraCurso.objects.get(
            aluno=aluno, curso=curso, data__gte=now, ativo=True
        )
    except:
        codigo = None
    return codigo


@register.assignment_tag(takes_context=True)
def get_sentencas_aluno_aguardando(context):
    try:
        professor = context['request'].user.professor
        return SentencaAvulsaAluno.objects.filter(
            status='A',
            sentenca_avulsa__professor=professor
        ).count()
    except:
        return None


@register.assignment_tag
def get_pacotes_desconto():
    return PacoteDesconto.objects.all()


@register.assignment_tag(takes_context=True)
def get_combo_aluno(context, status='A'):
    try:
        aluno = context['request'].user.aluno
        combo_aluno = ComboAluno.objects.filter(status=status, aluno=aluno).first()
    except:
        combo_aluno = None
    return combo_aluno


@register.assignment_tag(takes_context=True)
def check_curso_in_pct(context, curso):
    try:
        aluno = context['request'].user.aluno
        combo_aluno = ComboAluno.objects.filter(status__in=['A', 'C'], aluno=aluno, cursos=curso).first()
    except:
        combo_aluno = None
    return combo_aluno


@register.assignment_tag(takes_context=True)
def check_curso_in_checkout(context, curso):
    aluno = context['request'].user.aluno
    checkout_item = CheckoutItens.objects.filter(
        checkout__aluno=aluno,
        curso=curso,
        checkout__transaction_status__in=[3, 4]
    ).last()
    return checkout_item


@register.assignment_tag(takes_context=True)
def get_materiais_curso(context, curso, ativo=False):
    if ativo:
        now = timezone.now()
        docs = curso.doccurso_set.filter(data_ativo__lte=now)
    else:
        docs = curso.doccurso_set.all()
    return docs
