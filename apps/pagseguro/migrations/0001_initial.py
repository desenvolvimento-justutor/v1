# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text='C\xf3digo gerado para redirecionamento.', unique=True, max_length=100, verbose_name='c\xf3digo')),
                ('cpf', models.CharField(max_length=20, null=True, verbose_name='C.P.F', blank=True)),
                ('date', models.DateTimeField(help_text='Data em que o checkout foi realizado.', verbose_name='Data')),
                ('success', models.BooleanField(default=False, help_text='O checkout foi feito com sucesso?', db_index=True, verbose_name='Sucesso')),
                ('message', models.TextField(help_text='Mensagem apresentada no caso de erro no checkout.', verbose_name='Mensagem de erro', blank=True)),
                ('transaction_date', models.DateTimeField(null=True, verbose_name='Data da cria\xe7\xe3o da transa\xe7\xe3o', blank=True)),
                ('transaction_code', models.CharField(max_length=36, null=True, verbose_name='C\xf3digo identificador da transa\xe7\xe3o', blank=True)),
                ('transaction_reference', models.CharField(max_length=200, null=True, verbose_name='C\xf3digo de refer\xeancia da transa\xe7\xe3o', blank=True)),
                ('transaction_type', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Tipo da transa\xe7\xe3o', choices=[(1, 'Pagamento')])),
                ('transaction_status', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Status da Transa\xe7\xe3o', choices=[(1, 'Aguardando pagamento'), (2, 'Em an\xe1lise'), (3, 'Paga'), (4, 'Dispon\xedvel'), (5, 'Em disputa'), (6, 'Devolvida'), (7, 'Cancelada')])),
                ('transaction_cancellation_source', models.CharField(choices=[('INTERNAL', 'PagSeguro'), ('EXTERNAL', 'Institui\xe7\xf5es Financeiras')], max_length=30, blank=True, help_text='Opcional (somente quando Status da Transa\xe7\xe3o igual a Cancelada)', null=True, verbose_name='Origem do cancelamento')),
                ('transaction_last_event_date', models.DateTimeField(null=True, verbose_name='Data do \xfaltimo evento', blank=True)),
                ('transaction_payment_method_type', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Tipo do meio de pagamento', choices=[(1, 'Cart\xe3o de cr\xe9dito'), (2, 'Boleto'), (3, 'D\xe9bito online (TEF)'), (4, 'Saldo PagSeguro'), (5, 'Oi Paggo'), (6, 'Dep\xf3sito em conta')])),
                ('transaction_payment_code', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='C\xf3digo identificador do meio de pagamento', choices=[(101, 'Cart\xe3o de cr\xe9dito Visa'), (102, 'Cart\xe3o de cr\xe9dito MasterCard'), (103, 'Cart\xe3o de cr\xe9dito American Express'), (104, 'Cart\xe3o de cr\xe9dito Diners'), (105, 'Cart\xe3o de cr\xe9dito Hipercard'), (106, 'Cart\xe3o de cr\xe9dito Aura'), (107, 'Cart\xe3o de cr\xe9dito Elo'), (108, 'Cart\xe3o de cr\xe9dito PLENOCard'), (190, 'Cart\xe3o de cr\xe9dito PersonalCard'), (110, 'Cart\xe3o de cr\xe9dito JCB'), (111, 'Cart\xe3o de cr\xe9dito Discover'), (113, 'Cart\xe3o de cr\xe9dito BrasilCard'), (113, 'Cart\xe3o de cr\xe9dito FORTBRASIL'), (114, 'Cart\xe3o de cr\xe9dito CARDBAN'), (115, 'Cart\xe3o de cr\xe9dito VALECARD'), (116, 'Cart\xe3o de cr\xe9dito Cabal'), (117, 'Cart\xe3o de cr\xe9dito Mais!'), (118, 'Cart\xe3o de cr\xe9dito Avista'), (119, 'Cart\xe3o de cr\xe9dito GRANDCARD'), (120, 'Cart\xe3o de cr\xe9dito Sorocred'), (201, 'Boleto Bradesco'), (202, 'Boleto Santander'), (301, 'D\xe9bito online Bradesco'), (302, 'D\xe9bito online Ita\xfa'), (303, 'D\xe9bito online Unibanco'), (304, 'D\xe9bito online Banco do Brasil'), (305, 'D\xe9bito online Banco Real'), (306, 'D\xe9bito online Banrisul'), (307, 'D\xe9bito online HSBC'), (401, 'Saldo PagSeguro'), (501, 'Oi Paggo'), (701, 'Dep\xf3sito em conta - Banco do Brasil'), (702, 'Dep\xf3sito em conta - HSBC')])),
                ('transaction_gross_amount', models.DecimalField(null=True, verbose_name='Valor bruto da transa\xe7\xe3o', max_digits=9, decimal_places=2, blank=True)),
                ('transaction_discount_amount', models.DecimalField(null=True, verbose_name='Valor do desconto dado', max_digits=9, decimal_places=2, blank=True)),
                ('transaction_net_amount', models.DecimalField(null=True, verbose_name='Valor l\xedquido da transa\xe7\xe3o', max_digits=9, decimal_places=2, blank=True)),
                ('transaction_extra_amount', models.DecimalField(null=True, verbose_name='Valor extra', max_digits=9, decimal_places=2, blank=True)),
                ('transaction_escrow_end_date', models.DateTimeField(null=True, verbose_name='Data de cr\xe9dito', blank=True)),
                ('transaction_installment_count', models.PositiveSmallIntegerField(null=True, verbose_name='N\xfamero de parcelas', blank=True)),
                ('transaction_item_count', models.PositiveSmallIntegerField(null=True, verbose_name='N\xfamero de itens da transa\xe7\xe3o', blank=True)),
                ('transaction_sender_email', models.EmailField(max_length=60, null=True, verbose_name='E-mail do comprador', blank=True)),
                ('transaction_sender_name', models.CharField(max_length=50, null=True, verbose_name='Nome completo do comprador', blank=True)),
                ('transaction_sender_phone_area_code', models.CharField(max_length=50, null=True, verbose_name='DDD do comprador', blank=True)),
                ('transaction_sender_phone_number', models.CharField(max_length=50, null=True, verbose_name='N\xfamero de telefone do comprador', blank=True)),
                ('aluno', models.ForeignKey(verbose_name='Aluno', to='aluno.Aluno', null=True)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Checkout',
                'verbose_name_plural': 'Checkouts',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text='O c\xf3digo da transa\xe7\xe3o.', unique=True, max_length=100, verbose_name='c\xf3digo', db_index=True)),
                ('reference', models.CharField(help_text='A refer\xeancia passada na transa\xe7\xe3o.', max_length=200, verbose_name='refer\xeancia', db_index=True, blank=True)),
                ('status', models.CharField(default='aguardando', choices=[('aguardando', 'Aguardando'), ('em_analise', 'Em an\xe1lise'), ('pago', 'Pago'), ('disponivel', 'Dispon\xedvel'), ('em_disputa', 'Em disputa'), ('devolvido', 'Devolvido'), ('cancelado', 'Cancelado')], max_length=20, help_text='Status atual da transa\xe7\xe3o.', verbose_name='Status', db_index=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, help_text='Data em que a transa\xe7\xe3o foi criada.', verbose_name='Data')),
                ('last_event_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Data da \xfaltima altera\xe7\xe3o na transa\xe7\xe3o.', verbose_name='\xdaltima altera\xe7\xe3o')),
                ('content', models.TextField(default={}, help_text='Transa\xe7\xe3o no formato json.', verbose_name='Transa\xe7\xe3o')),
                ('checkout', models.OneToOneField(null=True, verbose_name='Checkout', to='pagseguro.Checkout')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Transa\xe7\xe3o',
                'verbose_name_plural': 'Transa\xe7\xf5es',
            },
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(help_text='Status da transa\xe7\xe3o.', max_length=20, verbose_name='Status', choices=[('aguardando', 'Aguardando'), ('em_analise', 'Em an\xe1lise'), ('pago', 'Pago'), ('disponivel', 'Dispon\xedvel'), ('em_disputa', 'Em disputa'), ('devolvido', 'Devolvido'), ('cancelado', 'Cancelado')])),
                ('date', models.DateTimeField(verbose_name='Data')),
                ('transaction', models.ForeignKey(verbose_name='Transa\xe7\xe3o', to='pagseguro.Transaction')),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'Hist\xf3rico da transa\xe7\xe3o',
                'verbose_name_plural': 'Hist\xf3ricos de transa\xe7\xf5es',
            },
        ),
    ]
