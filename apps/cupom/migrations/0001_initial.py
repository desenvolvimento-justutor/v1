# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0002_auto_20200807_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cupom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(default=b'Desconto na Compra (Valor)', help_text='Escolha o tipo de cupom.', max_length=35, verbose_name='Tipo de Cupom', choices=[('Nominal (Valor)', 'Nominal (Valor)'), ('Nominal (Percentual)', 'Nominal (Percentual)'), ('Desconto na compra (Percentual)', 'Desconto na Compra (Percentual)'), ('Desconto na Compra (Valor)', 'Desconto na Compra (Valor)')])),
                ('codigo', models.CharField(help_text='C\xf3digo do Cupom', max_length=10, null=True, verbose_name='C\xf3digo', blank=True)),
                ('valor_desconto', models.DecimalField(decimal_places=2, default=0, max_digits=9, blank=True, help_text='Valor que ser\xe1 descontado nas compras com esse cupom', null=True, verbose_name='Valor do Desconto')),
                ('percentual_desconto', models.DecimalField(decimal_places=2, max_digits=5, blank=True, help_text='Desconto em porcentagem.', null=True, verbose_name='Percentual de desconto (%)')),
                ('data_limite', models.DateTimeField(help_text='Data limite que o cupom estar\xe1 ativo', null=True, verbose_name='V\xe1lido at\xe9?', blank=True)),
                ('qte_max_uso', models.IntegerField(null=True, verbose_name='Quantidade M\xe1xima de Uso', blank=True)),
                ('primeira_compra', models.BooleanField(default=True, help_text='Aplicar esse cupom somente se for a primeira compra?<br><b>Cupons de primeira compra n\xe3o devem ser nominais, nem espec\xedficos a um curso.</b>', verbose_name='Primeira compra')),
                ('qte_usada', models.IntegerField(default=0, null=True, verbose_name='Quantidade Usada', blank=True)),
                ('ativo', models.BooleanField(default=True, help_text='Esse cupom est\xe1 ativo?', verbose_name='Ativo')),
                ('gerado', models.BooleanField(default=False, help_text='Cupom gerado automaticamente?', verbose_name='Gerado')),
                ('cliente', models.ForeignKey(blank=True, to='aluno.Aluno', help_text='Caso o cupom seja nominal, escolha o aluno que ser\xe1 beneficiados por esse cupom.', null=True, verbose_name='Aluno')),
            ],
            options={
                'verbose_name': 'Cupom',
                'verbose_name_plural': 'Cupons',
            },
        ),
        migrations.CreateModel(
            name='CupomMassa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_limite', models.DateTimeField(help_text='Data limite que o cupom estar\xe1 ativo', null=True, verbose_name='V\xe1lido at\xe9?', blank=True)),
            ],
            options={
                'verbose_name': 'Cupom em massa',
                'verbose_name_plural': 'Cupons em massa',
            },
        ),
        migrations.AddField(
            model_name='cupom',
            name='cupom_massa',
            field=models.ForeignKey(verbose_name=b'Cupom em massa', blank=True, to='cupom.CupomMassa', null=True),
        ),
    ]
