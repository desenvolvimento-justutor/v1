# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import re
from decimal import Decimal

import requests
import xmltodict
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Context, loader
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from xmltodict import parse

from apps.nfse.consumer import emitir
from apps.nfse.models import NSFe
from justutorial import settings
from justutorial.settings import EMAIL_HOST_USER, SITEADD
from libs.util.mail import send_mail
from .settings import PAGSEGURO_LOG_IN_MODEL
from .signals import notificacao_recebida, update_transaction

log_nfse = logging.getLogger("nfse")

TRANSACTION_STATUS_CHOICES = (
    ('aguardando', 'Aguardando'),
    ('em_analise', 'Em análise'),
    ('pago', 'Pago'),
    ('disponivel', 'Disponível'),
    ('em_disputa', 'Em disputa'),
    ('devolvido', 'Devolvido'),
    ('cancelado', 'Cancelado')
)


def ra(input_str):
    import unicodedata as ud
    nfkd_form = ud.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


@python_2_unicode_compatible
class Checkout(models.Model):

    code = models.CharField(
        'código',
        max_length=100,
        help_text='Código gerado para redirecionamento.',
        unique=True
    )

    aluno = models.ForeignKey(
        verbose_name='Aluno',
        to='aluno.Aluno',
        null=True
    )
    cpf = models.CharField(
        verbose_name='C.P.F',
        max_length=20, blank=True, null=True
    )
    date = models.DateTimeField(
        'Data',
        help_text='Data em que o checkout foi realizado.'
    )

    success = models.BooleanField(
        'Sucesso',
        db_index=True,
        help_text='O checkout foi feito com sucesso?',
        default=False
    )

    message = models.TextField(
        'Mensagem de erro',
        blank=True,
        help_text='Mensagem apresentada no caso de erro no checkout.'
    )
    # PAGSEGURO
    transaction_date = models.DateTimeField(
        verbose_name="Data da criação da transação", blank=True, null=True
    )
    transaction_code = models.CharField(
        verbose_name="Código identificador da transação", max_length=36, blank=True, null=True
    )
    transaction_reference = models.CharField(
        verbose_name="Código de referência da transação", max_length=200, blank=True, null=True
    )
    transaction_type = models.PositiveSmallIntegerField(
        verbose_name="Tipo da transação", blank=True, null=True,
        choices=[
            (1, "Pagamento")
        ]
    )

    transaction_status = models.PositiveSmallIntegerField(
        verbose_name="Status da Transação", null=True, blank=True,
        choices=[
            (1, "Aguardando pagamento"),
            (2, "Em análise"),
            (3, "Paga"),
            (4, "Disponível"),
            (5, "Em disputa"),
            (6, "Devolvida"),
            (7, "Cancelada")
        ]
    )
    transaction_cancellation_source = models.CharField(
        verbose_name="Origem do cancelamento", max_length=30, blank=True, null=True,
        choices=[
            ('INTERNAL', "PagSeguro"),
            ('EXTERNAL', "Instituições Financeiras")
        ], help_text="Opcional (somente quando Status da Transação igual a Cancelada)"
    )
    transaction_last_event_date = models.DateTimeField(
        verbose_name="Data do último evento", blank=True, null=True
    )
    transaction_payment_method_type = models.PositiveSmallIntegerField(
        verbose_name="Tipo do meio de pagamento", blank=True, null=True,
        choices=[
            (1, "Cartão de crédito"),
            (2, "Boleto"),
            (3, "Débito online (TEF)"),
            (4, "Saldo PagSeguro"),
            (5, "Oi Paggo"),
            (6, "Depósito em conta")
        ]
    )
    transaction_payment_code = models.PositiveSmallIntegerField(
        verbose_name="Código identificador do meio de pagamento", blank=True, null=True,
        choices=[
            (101, "Cartão de crédito Visa"), (102, "Cartão de crédito MasterCard"),
            (103, "Cartão de crédito American Express"), (104, "Cartão de crédito Diners"),
            (105, "Cartão de crédito Hipercard"), (106, "Cartão de crédito Aura"), (107, "Cartão de crédito Elo"),
            (108, "Cartão de crédito PLENOCard"), (190, "Cartão de crédito PersonalCard"),
            (110, "Cartão de crédito JCB"), (111, "Cartão de crédito Discover"), (113, "Cartão de crédito BrasilCard"),
            (113, "Cartão de crédito FORTBRASIL"), (114, "Cartão de crédito CARDBAN"),
            (115, "Cartão de crédito VALECARD"), (116, "Cartão de crédito Cabal"), (117, "Cartão de crédito Mais!"),
            (118, "Cartão de crédito Avista"), (119, "Cartão de crédito GRANDCARD"),
            (120, "Cartão de crédito Sorocred"), (201, "Boleto Bradesco"), (202, "Boleto Santander"),
            (301, "Débito online Bradesco"), (302, "Débito online Itaú"), (303, "Débito online Unibanco"),
            (304, "Débito online Banco do Brasil"), (305, "Débito online Banco Real"), (306, "Débito online Banrisul"),
            (307, "Débito online HSBC"), (401, "Saldo PagSeguro"), (501, "Oi Paggo"),
            (701, "Depósito em conta - Banco do Brasil"), (702, "Depósito em conta - HSBC"),
        ]
    )
    transaction_gross_amount = models.DecimalField(
        verbose_name="Valor bruto da transação", max_digits=9, decimal_places=2, blank=True, null=True
    )
    transaction_discount_amount = models.DecimalField(
        verbose_name="Valor do desconto dado", max_digits=9, decimal_places=2, blank=True, null=True
    )
    transaction_net_amount = models.DecimalField(
        verbose_name="Valor líquido da transação", max_digits=9, decimal_places=2, blank=True, null=True
    )
    transaction_extra_amount = models.DecimalField(
        verbose_name="Valor extra", max_digits=9, decimal_places=2, blank=True, null=True
    )
    transaction_escrow_end_date = models.DateTimeField(
        verbose_name="Data de crédito", blank=True, null=True
    )
    transaction_installment_count = models.PositiveSmallIntegerField(
        verbose_name="Número de parcelas", blank=True, null=True
    )
    transaction_item_count = models.PositiveSmallIntegerField(
        verbose_name="Número de itens da transação", blank=True, null=True
    )
    transaction_sender_email = models.EmailField(
        verbose_name="E-mail do comprador", max_length=60, blank=True, null=True
    )
    transaction_sender_name = models.CharField(
        verbose_name="Nome completo do comprador", max_length=50, blank=True, null=True
    )
    transaction_sender_phone_area_code = models.CharField(
        verbose_name="DDD do comprador", max_length=50, blank=True, null=True
    )
    transaction_sender_phone_number = models.CharField(
        verbose_name="Número de telefone do comprador", max_length=50, blank=True, null=True
    )
    nfse = models.OneToOneField(
        verbose_name="NFSe", to=NSFe, null=True, editable=False
    )
    data_nfse = models.TextField(
        verbose_name="Dados da NFSE", blank=True, null=True
    )


    def get_sender(self):
        data = None
        transaction = self.code
        # (u'sender', OrderedDict([(u'name', u'tiziana m viana'),
        # (u'email', u'tiziadv@yahoo.com.br'),
        # (u'phone', OrderedDict([(u'areaCode', u'27'), (u'number', u'998442866')]))])
        if transaction:
            if settings.PAGSEGURO_SANDBOX:
                url = 'https://ws.sandbox.pagseguro.uol.com.br/v3/transactions/%s'
            else:
                url = 'https://ws.pagseguro.uol.com.br/v3/transactions/%s'
            req = requests.get(url % transaction, params=settings.PAGSEGURO_DATA)
            if req.status_code == 200:
                data = parse(req.text)
                return data['transaction']['shipping']['address']

    def incluir_os(self):
        log_nfse.debug("transaction_status [{}]: {}".format(self.pk, self.transaction_status))
        if self.transaction_status in ["3", 3] and not self.nfse:
            if self.cpf:
                self.aluno.cpf = self.cpf
                self.aluno.save()
            # ==========================================================================================================
            # TOTAIS
            # ==========================================================================================================
            total = Decimal(self.total)
            s_total = "%.2f" % total
            gross_amount = Decimal(self.transaction_gross_amount)
            s_gross_amount = "%.2f" % gross_amount
            desconto = total - gross_amount
            s_desconto = "%.2f" % desconto
            # ==========================================================================================================
            # DADOS NA NOTA
            # ==========================================================================================================
            if self.transaction_payment_method_type == 6:
                try:
                    endereco = self.pix.get_endereco
                except:
                    endereco = {}
            else:
                sender = self.get_sender()
                endereco = {
                    "logradouro": ra(sender["street"]),
                    "numero": sender["number"],
                    "complemento": ra(sender["complement"] or "N/A"),
                    "bairro": ra(sender["district"]),
                    "codigo_municipio": "4106902",
                    "uf": sender["state"],
                    "cep": sender["postalCode"]
                }
            tomador = {
                "cpf": self.aluno.cpf,
                "razao_social": ra(self.aluno.nome_completo or self.aluno.nome),
                "email": self.aluno.email,
                "endereco": endereco
            }
            log_nfse.debug("Tomador %s" % tomador)
            # ==========================================================================================================
            # DESCRICAO
            # ==========================================================================================================
            descriminacao = ""
            itens = self.checkoutitens_set.all()
            for item in itens:
                valor = "%.2f" % item.valor
                descriminacao += "{curso:<50}: R${valor:>9}\n".format(
                    curso=item.curso, valor=valor
                )
            descriminacao += "\nValor bruto: R$ {:>10}".format(s_total)
            descriminacao += "\nDesconto   : R$ {:>10}".format(s_desconto)
            descriminacao += "\nTotal      : R$ {:>10}".format(s_gross_amount)
            # ==========================================================================================================
            # GERAR NFSE
            # ==========================================================================================================
            nfse = NSFe(aluno=self.aluno)
            code, response = emitir(nfse.ref.hex, tomador, ra(descriminacao), float(gross_amount))
            log_nfse.debug("nfse response: {}".format(response))
            if code == 202:
                nfse.status = response.get("status")
                nfse.numero_rps = response.get("numero_rps")
                nfse.serie_rps = response.get("serie_rps")
                nfse.save()
                self.nfse = nfse
                self.data_nfse = str(response)
                self.save()
        else:
            log_nfse.debug("nfse não gerada")

    def get_transaction_status(self):
        transaction = self.code

        if transaction:
            if settings.PAGSEGURO_SANDBOX:
                url = 'https://ws.sandbox.pagseguro.uol.com.br/v3/transactions/%s'
            else:
                url = 'https://ws.pagseguro.uol.com.br/v3/transactions/%s'
            req = requests.get(url % transaction, params=settings.PAGSEGURO_DATA)

            if req.status_code == 200:
                data = parse(req.text)
                transaction_status = int(data['transaction']['status'])

                self.transaction_date = data['transaction']['date']
                self.transaction_code = data['transaction']['code']
                self.transaction_reference = data['transaction']['reference']
                self.transaction_type = data['transaction']['type']
                self.transaction_status = data['transaction']['status']
                if transaction_status == 7:
                    self.transaction_cancellation_source = data['transaction']['cancellationSource']
                self.transaction_last_event_date = data['transaction']['lastEventDate']
                self.transaction_payment_method_type = data['transaction']['paymentMethod']['type']
                self.transaction_payment_code = data['transaction']['paymentMethod']['code']
                self.transaction_gross_amount = data['transaction']['grossAmount']
                self.transaction_discount_amount = data['transaction']['discountAmount']
                self.transaction_net_amount = data['transaction']['netAmount']
                self.transaction_escrow_end_date = data['transaction'].get('escrowEndDate')
                self.transaction_extra_amount = data['transaction']['extraAmount']
                self.transaction_installment_count = data['transaction']['installmentCount']
                self.transaction_item_count = data['transaction']['itemCount']
                self.transaction_sender_email = data['transaction']['sender']['email']
                self.transaction_sender_name = data['transaction']['sender']['name']
                try:
                    self.transaction_sender_phone_area_code = data['transaction']['sender']['phone']['areaCode']
                    self.transaction_sender_phone_number = data['transaction']['sender']['phone']['number']
                except:
                    pass
                if transaction_status == 3:
                    try:
                        tr = Transaction.objects.get(code=self.transaction_code)
                        tr.status = 'pago'
                        tr.save()
                    except Transaction.DoesNotExist:
                        pass
                elif transaction_status in [6, 7]:
                    try:
                        tr = Transaction.objects.get(code=self.transaction_code)
                        tr.status = 'cancelado'
                        tr.save()
                    except Transaction.DoesNotExist:
                        pass
                self.save()
                return data
        return transaction

    @property
    def link(self):
        from  .api import PagSeguroApi
        api = PagSeguroApi()
        data = api.get_transaction(self.code)
        t = data.get('transaction', {'paymentLink': '#'}).get('paymentLink', '#')
        return t

    @property
    def total(self):
        return (self.transaction_extra_amount * -1) + self.transaction_gross_amount

    @property
    def get_card_name(self):
        if self.transaction_payment_method_type == 1:
            return self.get_transaction_payment_code_display().replace('Cartão de crédito', '')
        return ''

    @property
    def status_color(self):
        status = {
            1: "warning",
            2: "info",
            3: "success",
            4: "success",
            5: "warning",
            6: "danger",
            7: "danger"
        }
        return status.get(self.transaction_status)

    def __str__(self):
        return '{0}'.format(self.code or self.transaction_code)

    # @property
    # def transaction(self):
    #     try:
    #         trans = Transaction.objects.get(code=self.code)
    #     except:
    #         trans = False
    #     return trans

    def get_dict_xml(self):
        return xmltodict.parse(self.message)

    @property
    def get_endereco_ps(self):
        try:
            root = self.get_dict_xml()
            ret = {
                'logradouro': root['transaction']['shipping']['address']['street'],
                'numero': root['transaction']['shipping']['address']['number'],
                'bairro': root['transaction']['shipping']['address']['district'],
                'cidade': root['transaction']['shipping']['address']['city'],
                'uf': root['transaction']['shipping']['address']['state'],
                'cep': root['transaction']['shipping']['address']['postalCode'],
            }
        except:
            ret = {
                'logradouro': '',
                'numero': '',
                'bairro': '',
                'cidade': '',
                'uf': '',
                'cep': '',
            }
        return ret

    @property
    def get_desconto(self):
        try:
            root = self.get_dict_xml()
            desc = float(root['transaction']['extraAmount'])
        except:
            desc = 0.00
            if self.transaction_extra_amount:
                desc = self.transaction_extra_amount
        return desc

    @property
    def total(self):
        t = map(lambda x: x.valor * x.qtda, self.checkoutitens_set.all())
        return sum(t)

    @property
    def get_cursos(self):

        return self.checkoutitens_set.filter(
            curso__sentenca_avulsa__isnull=True, curso__sentenca_oab__isnull=True,
            curso__categoria__tipo__in=['C', 'S', 'O']
        )


    @property
    def get_curso_ativo(self):
        ativo = False
        for item in self.get_cursos:
            if item.curso.disponivel:
                ativo = True
                break
        return ativo


    @property
    def get_livros(self):
        ret = self.checkoutitens_set.filter(
            curso__sentenca_avulsa__isnull=True, curso__sentenca_oab__isnull=True,
            curso__categoria__tipo='L'
        )
        return ret

    @property
    def get_sentencas(self):
        return self.checkoutitens_set.filter(curso__sentenca_avulsa__isnull=False)

    @property
    def get_simulados(self):
        return self.checkoutitens_set.filter(curso__simulado__isnull=False)

    @property
    def get_sentencas_oab(self):
        return self.checkoutitens_set.filter(curso__sentenca_oab__isnull=False)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkouts'


@python_2_unicode_compatible
class Transaction(models.Model):

    code = models.CharField(
        'código',
        max_length=100,
        unique=True,
        db_index=True,
        help_text='O código da transação.'
    )
    checkout = models.OneToOneField(
        verbose_name='Checkout', to=Checkout, null=True,
        on_delete=models.CASCADE
    )
    reference = models.CharField(
        'referência',
        max_length=200,
        db_index=True,
        blank=True,
        help_text='A referência passada na transação.'
    )

    status = models.CharField(
        'Status',
        max_length=20,
        db_index=True, default='aguardando',
        choices=TRANSACTION_STATUS_CHOICES,
        help_text='Status atual da transação.'
    )

    date = models.DateTimeField(
        'Data', default=timezone.now,
        help_text='Data em que a transação foi criada.'
    )

    last_event_date = models.DateTimeField(
        'Última alteração', default=timezone.now,
        help_text='Data da última alteração na transação.'
    )

    content = models.TextField(
        'Transação',
        help_text='Transação no formato json.', default={}
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'

    @property
    def link(self):
        return json.loads(self.content).get('paymentLink')

    @property
    def get_checkout(self):
        checkout = Checkout.objects.filter(code=self.code).first()
        return checkout

    def __str__(self):
        return '{0}'.format(self.code)


@receiver(post_save, sender=Transaction)
def aluno_save(sender, **kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if instance.status == 'pago':
        checkout = instance.checkout
        if checkout:
            try:
                if checkout.checkoutitens_set.filter(curso__categoria__tipo='L'):
                    aluno = checkout.aluno
                    t = loader.get_template('email/compra-livro.html')
                    if aluno.cpf:
                        cpf = aluno.cpf
                    else:
                        cpf = ''
                    c = Context({
                        'cpf': re.sub('[^0-9]', '', cpf),
                        'dominio': SITEADD,
                        'absolute_static_url': '{0}/static/'.format(SITEADD)
                    })
                    rendered = t.render(c)
                    send_mail(
                        u'Sua obra já está disponível para download!',
                        '',
                        EMAIL_HOST_USER,
                        [aluno.email],
                        html=rendered
                    )
            except:
                pass


@python_2_unicode_compatible
class TransactionHistory(models.Model):

    transaction = models.ForeignKey(
        Transaction,
        verbose_name='Transação',
        on_delete=models.CASCADE
    )

    status = models.CharField(
        'Status',
        max_length=20,
        choices=TRANSACTION_STATUS_CHOICES,
        help_text='Status da transação.'
    )

    date = models.DateTimeField(
        'Data'
    )

    def __str__(self):
        return '{0} - {1} - {2}'.format(
            self.transaction, self.status, self.date
        )

    class Meta:
        ordering = ['date']
        verbose_name = 'Histórico da transação'
        verbose_name_plural = 'Históricos de transações'


# Signals
if PAGSEGURO_LOG_IN_MODEL:
    # checkout_realizado.connect(save_checkout)
    notificacao_recebida.connect(update_transaction)
