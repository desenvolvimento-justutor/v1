# coding=utf-8
from django.db.models import (
    CharField, FloatField, BooleanField, DateTimeField, ManyToManyField, ForeignKey,
    IntegerField, Model, DecimalField, CASCADE
)
from libs.util.format import currency_format

TIPOS_CUPONS = (
    (u'Nominal (Valor)', u'Nominal (Valor)'),
    (u'Nominal (Percentual)', u'Nominal (Percentual)'),
    # (u'Zerar o Frete', u'Zerar o Frete'),
    # (u'Desconto no Frete (Percentual)', u'Desconto no Frete (Percentual)'),
    # (u'Desconto no Frete (Valor)', u'Desconto no Frete (Valor)'),
    (u'Desconto na compra (Percentual)', u'Desconto na Compra (Percentual)'),
    (u'Desconto na Compra (Valor)', u'Desconto na Compra (Valor)'),
)


class CupomMassa(Model):
    data_limite = DateTimeField(
        verbose_name=u'Válido até?', blank=True, null=True,
        help_text=u'Data limite que o cupom estará ativo'
    )

    class Meta:
        verbose_name = 'Cupom em massa'
        verbose_name_plural = 'Cupons em massa'

    def __str__(self):
        return u"Cupom em Massa #{:05d}".format(self.pk)

    @property
    def title(self):
        return self.__str__()


class Cupom(Model):
    class Meta:
        verbose_name = u'Cupom'
        verbose_name_plural = u'Cupons'

    tipo = CharField(
        verbose_name=u'Tipo de Cupom', blank=False, null=False,
        max_length=35, choices=TIPOS_CUPONS,
        default='Desconto na Compra (Valor)',
        help_text=u'Escolha o tipo de cupom.'
    )
    codigo = CharField(
        verbose_name=u'Código', blank=True, null=True,
        max_length=10, help_text=u'Código do Cupom'
    )
    valor_desconto = DecimalField(
        verbose_name=u'Valor do Desconto', max_digits=9,
        decimal_places=2, default=0, blank=True, null=True,
        help_text=u'Valor que será descontado nas compras com esse cupom'
    )
    percentual_desconto = DecimalField(
        verbose_name=u'Percentual de desconto (%)', max_digits=5,
        decimal_places=2, blank=True, null=True,
        help_text=u'Desconto em porcentagem.'
    )
    data_limite = DateTimeField(
        verbose_name=u'Válido até?', blank=True, null=True,
        help_text=u'Data limite que o cupom estará ativo'
    )
    produtos = ManyToManyField(
        'curso.Curso', verbose_name=u'Curso(s)', blank=True, db_index=True,
        help_text=u'Selecione o(s) curso(s). Se necessário.'
    )
    cliente = ForeignKey(
        'aluno.Aluno', verbose_name=u'Aluno', blank=True, db_index=True, null=True,
        help_text=u'Caso o cupom seja nominal, escolha o aluno que será beneficiados por esse cupom.'
    )
    qte_max_uso = IntegerField(
        verbose_name=u'Quantidade Máxima de Uso', blank=True, null=True)
    primeira_compra = BooleanField(
        default=True, verbose_name=u"Primeira compra",
        help_text=u'Aplicar esse cupom somente se for a primeira'
                  u' compra?<br><b>Cupons de primeira compra não '
                  u'devem ser nominais, nem específicos a um curso.</b>'
    )
    qte_usada = IntegerField(
        verbose_name=u'Quantidade Usada', blank=True, null=True, default=0
    )
    ativo = BooleanField(
        default=True, verbose_name=u"Ativo", help_text=u'Esse cupom está ativo?'
    )
    gerado = BooleanField(
        default=False, verbose_name=u"Gerado", help_text=u'Cupom gerado automaticamente?'
    )
    cupom_massa = ForeignKey(
        verbose_name='Cupom em massa', to=CupomMassa, on_delete=CASCADE,
        null=True, blank=True
    )

    def __unicode__(self):
        return u'%s' % self.codigo

    @classmethod
    def get_desconto_primeira_compra(cls):
        try:
            return cls.objects.filter(primeira_compra=True, cliente__isnull=True, ativo=True)
        except:
            return None

    @property
    def curso(self):
        return self.produtos.first()

    @property
    def get_valor(self):
        valor = currency_format(self.valor_desconto or self.percentual_desconto, False)
        monetary = 'R$ ' if 'Valor' in self.tipo else ''
        percent = '%' if 'Percentual' in self.tipo else ''
        return '{}{}{}'.format(
            monetary, valor, percent
        )

    def save(self, *args, **kwargs):
        if self.primeira_compra:
            Cupom.objects.filter(primeira_compra=True).update(primeira_compra=False)
        super(Cupom, self).save(*args, **kwargs)
