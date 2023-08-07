# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from apps.aluno.models import Aluno
from decimal import Decimal
from django.db.models import Sum
from datetime import timedelta


@python_2_unicode_compatible
class Nota(models.Model):
    unica = models.BooleanField(verbose_name="Única", default=False)
    titulo = models.CharField(
        verbose_name='Título', max_length=200,
        help_text='Texto da opção.'
    )
    texto = models.TextField(
        verbose_name='Texto',
        blank=True
    )
    valor = models.DecimalField(
        verbose_name='Valor', decimal_places=2, max_digits=4,
        help_text='Nota padrão que o usuário receberá.'
    )

    class Meta:
        verbose_name = 'Nota padrão'
        verbose_name_plural = 'Notas padrão'

    def __str__(self):
        return self.titulo

    def __str__(self):
        return u'%s (%.2f)' % (self.titulo, self.valor)

    def get_dot_valor(self):
        return str(self.valor).replace(',', '.')

    @property
    def tipo(self):
        return "U" if self.unica else "M"


@python_2_unicode_compatible
class Formulario(models.Model):
    atividade = models.OneToOneField(
        verbose_name='Atividade', to='curso.Atividade', on_delete=models.CASCADE,
        null=True, blank=True, related_name='formulario'
    )
    sentenca_avulca = models.OneToOneField(
        verbose_name='Sentença', to='curso.SentencaAvulsa', on_delete=models.CASCADE,
        null=True, blank=True, related_name='formulario'
    )
    titulo = models.CharField(
        verbose_name='Título', max_length=200
    )
    texto = models.TextField(
        verbose_name='Texto'
    )

    class Meta:
        verbose_name = u'Fomulário'
        verbose_name_plural = u'Fomulários'

    def __str__(self):
        return self.titulo

    @property
    def total(self):
        return 0

    @property
    def tipo_display(self):
        if self.atividade:
            return self.atividade.nome
        elif self.sentenca_avulca:
            return self.sentenca_avulca.titulo
        else:
            return '?'


@python_2_unicode_compatible
class Tabela(models.Model):
    formulario = models.ForeignKey(
        verbose_name=u'Formulário', to=Formulario, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='tabelas'
    )
    item = models.TextField(
        verbose_name='Item'
    )
    valor = models.DecimalField(
        verbose_name='Valor', decimal_places=2, max_digits=4
    )
    proibir_negativa = models.BooleanField(
        verbose_name="Proibir nota negativa?", default=False
    )
    nota = models.ManyToManyField(
        verbose_name='Nota', to=Nota
    )
    # notas = models.ManyToManyField(
    #     verbose_name='Notas', through="TabelaNota"
    # )
    comentarios = models.TextField(
        verbose_name='Comentários', blank=True, null=True
    )
    order = models.PositiveIntegerField(
        verbose_name=u'Ordem'
    )

    class Meta:
        verbose_name = u'Tabela de correção'
        verbose_name_plural = u'Tabelas de correção'
        ordering = ["order"]

    def __str__(self):
        return self.item

    def get_dot_valor(self):
        return str(self.valor).replace(',', '.')

    @property
    def total(self):
        t = self.tabela_aluno.aggregate(total=Sum('nota'))
        return t.get('total')


@python_2_unicode_compatible
class TabelaNota(models.Model):
    tabela = models.ForeignKey(verbose_name="Tabela", to=Tabela, on_delete=models.CASCADE, related_name="tbnota_tabelas")
    nota = models.ForeignKey(verbose_name="Nota", to=Nota, on_delete=models.CASCADE, related_name="tbnota_notas")

    class Meta:
        verbose_name = u'Tabela de Nota'
        verbose_name_plural = u'Tabelas de Notas'

    def __str__(self):
        return self.nota.valor


@python_2_unicode_compatible
class TabelaCorrecaoAluno(models.Model):
    corrigido = models.BooleanField(
        default=False
    )
    professor = models.ForeignKey(
        verbose_name='Corrigido por', to='professor.Professor',
        blank=True, null=True
    )
    aluno = models.ForeignKey(
        verbose_name='Aluno', to=Aluno, on_delete=models.PROTECT,
    )
    formulario = models.ForeignKey(
        verbose_name=u'Formulário', to=Formulario, on_delete=models.CASCADE
    )
    texto = models.TextField(
        verbose_name='Texto', blank=True, null=True
    )
    data_solicitacao = models.DateTimeField(
        verbose_name=u'Data da Solicitação', null=True, blank=True
    )
    data_correcao = models.DateTimeField(
        verbose_name=u'Data da Correção', null=True
    )
    status = models.CharField(
        verbose_name=u'Situação', max_length=10,
        choices=[
            ('corrigido', 'Corrigido'),
            ('solicitado', 'Recurso Solicitado'),
            ('analise', 'Recurso em Análise'),
            ('analisado', 'Recurso Analisado'),
        ], default='corrigido'
    )
    pago = models.BooleanField(default=False)

    def total(self):
        tabelas = self.tabelas.all()
        valor = sum(map(lambda x: x.tabela.valor, tabelas))
        notas = sum(map(lambda x: x.total_notas(), tabelas))
        nota = sum(map(lambda x: x.nota, tabelas))
        media = Decimal(nota) - Decimal(notas)
        total = {
            'valor': valor,
            'notas': notas,
            'nota': nota,
            'media': '%.2f' % media
        }
        return total

    @property
    def status_texto(self):
        vals = {
            'corrigido': '',
            'solicitado': u'Seu recurso foi enviado ao professor e está em fase de análise. Assim que concluída a '
                          u'avaliação de seu recurso, você receberá uma notificação por e-mail.',
            'analise': u'Seu recurso foi enviado ao professor e está em fase de análise. Assim que concluída a '
                       u'avaliação de seu recurso, você receberá uma notificação por e-mail.',
            'analisado': u'Seu recurso foi analisado. Confira o resultado abaixo.'
        }
        return vals.get(self.status)

    @property
    def status_color(self):
        vals = {
            'corrigido': 'info',
            'solicitado': 'danger',
            'analise': 'warning',
            'analisado': 'success'
        }
        return vals.get(self.status)

    @property
    def pode_recorrer(self):
        if self.data_correcao:
            return timezone.now() <= self.data_correcao + timedelta(days=5)
        return False

    @property
    def total_aluno(self):
        return self.tabelas.aggregate(total=Sum('nota')).get('total')

    def get_tabelas_recorridas(self):
        if self.status == 'corrigido':
            qs = self.tabelas.all()
        else:
            qs = self.tabelas.filter(texto_recurso__isnull=False)
        return qs

    def __str__(self):
        return self.aluno.nome


class TabelaAluno(models.Model):
    tabela_correcao = models.ForeignKey(
        verbose_name='Correcao', to=TabelaCorrecaoAluno, on_delete=models.CASCADE,
        related_name='tabelas'
    )
    tabela = models.ForeignKey(
        verbose_name='Tabela', to=Tabela, on_delete=models.CASCADE,
        related_name='tabela_aluno'
    )
    texto = models.TextField(
        verbose_name='Texto', blank=True, null=True
    )
    notas = models.ManyToManyField(
        verbose_name='Notas', to=Nota, blank=True
    )
    nota = models.DecimalField(
        verbose_name='Nota', blank=True, null=True, default=0,
        max_digits=4, decimal_places=2
    )
    nota_calc = models.BooleanField(
        verbose_name='Nota professor', default=False
    )
    texto_recurso = models.TextField(
        verbose_name='Recurso', null=True
    )
    texto_justificativa = models.TextField(
        verbose_name='Justificativa', null=True
    )

    @property
    def recorrido(self):
        return 'Sim' if self.texto_recurso else u'Não'

    def get_notas(self):
        vals = []
        for nota in self.tabela.nota.all().order_by('id'):
            vals.append({
                'nota': nota,
                'ativo': self.notas.filter(tabelaaluno=self, tabelaaluno__notas=nota).exists(),
                'title': nota.texto
            })
        return vals

    def total_notas(self):
        return sum(map(lambda x: x.valor, self.notas.all()))

    def get_dot_nota(self):
        return str(self.nota).replace(',', '.')

    class Meta:
        ordering = ['tabela']


@python_2_unicode_compatible
class NotaCorrecao(models.Model):
    tabela = models.ForeignKey(
        verbose_name="Tabela", to=Tabela, on_delete=models.PROTECT
    )
    nota = models.ForeignKey(
        verbose_name=u"Nota", to=Nota, on_delete=models.PROTECT, related_name="nota_correcao"
    )
    aluno = models.ForeignKey(
        verbose_name=u"Aluno", to=Aluno, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.nota.valor)
