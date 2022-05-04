# coding=utf-8
from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django_extensions.db.models import TimeStampedModel, ActivatorModel, AutoSlugField

from libs.util.unique_id import get_unique_id


def get_uuid():
    return get_unique_id(length=6).upper()


@python_2_unicode_compatible
class ConfiguracaoPacote(TimeStampedModel):
    ativo = models.BooleanField(
        verbose_name="Ativo", default=True
    )
    titulo = models.CharField(
        verbose_name=u"Titulo", max_length=50, unique=True
    )
    curso = models.ForeignKey(
        verbose_name="Curso", to='curso.CursoCredito', on_delete=models.CASCADE
    )
    valor_unitario = models.DecimalField(
        verbose_name=u"Valor unitário",
        decimal_places=2, max_digits=5
    )
    qtda_min = models.PositiveSmallIntegerField(
        verbose_name=u"Qtda. mínima"
    )
    qtda_max = models.PositiveSmallIntegerField(
        verbose_name=u"Qtda. máxima"
    )
    slug = AutoSlugField(
        populate_from='titulo'
    )

    class Meta:
        verbose_name = u"Configuração de Pacote"
        verbose_name_plural = u"Configurações de Pacote"

    def __str__(self):
        return self.titulo


@python_2_unicode_compatible
class Pacote(TimeStampedModel):
    configuracao = models.ForeignKey(
        verbose_name=u"Configuração", related_name='pacotes',
        to=ConfiguracaoPacote, on_delete=models.CASCADE
    )
    quantidade = models.PositiveSmallIntegerField(
        verbose_name=u"Quantidade",
    )
    desconto = models.FloatField(
        verbose_name="Desconto", null=True, blank=True,
        help_text="%"
    )

    class Meta:
        verbose_name = u"Pacote"
        verbose_name_plural = u"Pacotes"
        unique_together = [
            'configuracao',
            'quantidade'
        ]
        ordering = [
            'quantidade'
        ]

    def __str__(self):
        return str(self.quantidade)

    @property
    def valor_liquido(self):
        return self.configuracao.valor_unitario * self.quantidade

    @property
    def vlr_desconto(self):
        vlr = 0
        if self.desconto:
            vlr = self.valor_liquido * Decimal(self.desconto) / 100
        return vlr

    @property
    def valor(self):
        vlr = self.valor_liquido
        if self.vlr_desconto:
            vlr -= self.vlr_desconto
        return vlr

    @property
    def valor_unitario(self):
        return self.valor / self.quantidade


@python_2_unicode_compatible
class PacoteDesconto(TimeStampedModel):
    pacote = models.ForeignKey(
        verbose_name=u"Configuração", related_name='descontos',
        to=ConfiguracaoPacote, on_delete=models.CASCADE
    )
    de = models.PositiveSmallIntegerField(
        verbose_name="de"
    )
    ate = models.PositiveSmallIntegerField(
        verbose_name=u"até"
    )
    desconto = models.FloatField(
        verbose_name="Desconto", help_text="%"
    )

    class Meta:
        verbose_name = u"Desconto"
        verbose_name_plural = u"Descontos"

    def __str__(self):
        return u"%.d-%.d (%.2f %%)" % (self.de, self.ate, self.desconto)


@python_2_unicode_compatible
class Credito(TimeStampedModel):
    uuid = models.CharField(
        verbose_name="Código", default=get_uuid, unique=True, max_length=36
    )
    aluno = models.ForeignKey(
        to='aluno.Aluno', on_delete=models.CASCADE
    )
    quantidade = models.PositiveSmallIntegerField(
        verbose_name='Quantidade'
    )
    expire_date = models.DateField(
        verbose_name="Expiração", help_text="Data de expiração do crédito se não utilizado",
        blank=True, null=True
    )
    origem = models.CharField(
        verbose_name="Origem", max_length=6,
        choices=[
            ("bonus", u"Bônus"),
            ("compra", u"Compra")
        ]
    )
    pacote = models.ForeignKey(
        verbose_name=Pacote, to=Pacote, on_delete=models.CASCADE,
        blank=True, null=True
    )
    checkout = models.ForeignKey(
        verbose_name='Checkout', to='pagseguro.Checkout', on_delete=models.CASCADE,
        blank=True, null=True
    )

    class Meta:
        verbose_name = u"Crédito"
        verbose_name_plural = u"Créditos"

    def __str__(self):
        return self.uuid

    @property
    def utilizados(self):
        return sum(
            map(lambda x: x.quantidade, self.creditoresgate_set.all())
        )

    @property
    def disponivel(self):
        return self.quantidade - self.utilizados

    @property
    def status(self):
        now = timezone.now().date()
        st = u'Disponível'
        if now > self.expire_date:
            st = 'Expirado'
        return st

    @classmethod
    def totais(cls, aluno_id):
        c = Credito.objects.filter(aluno_id=aluno_id).aggregate(Sum("quantidade"))
        r = CreditoResgate.objects.filter(credito__aluno_id=aluno_id).aggregate(Sum("quantidade"))
        c_sum = c.get('quantidade__sum') or 0
        r_sum = r.get('quantidade__sum') or 0
        d = c_sum - r_sum

        return dict(
            creditos=c,
            resgates=r,
            quantidade=c_sum,
            utilizados=r_sum,
            disponiveis=d
        )


class CreditoResgate(TimeStampedModel):
    credito = models.ForeignKey(
        verbose_name=u"Crédito", to=Credito, on_delete=models.CASCADE
    )
    quantidade = models.PositiveSmallIntegerField(
        verbose_name='Quantidade'
    )
    data = models.DateTimeField(
        verbose_name="Data", default=timezone.now
    )
    formulario = models.ForeignKey(
        verbose_name="Formulario", blank=True, null=True,
        to='formulario_auto_correcao.Formulario', on_delete=models.PROTECT,
        related_name='creditos_resgate'
    )

    class Meta:
        verbose_name = u"Resgate de Crédito"
        verbose_name_plural = u"Resgate de Créditos"
        ordering = [
            '-data'
        ]

    def __str__(self):
        return '%09dx' % self.pk
