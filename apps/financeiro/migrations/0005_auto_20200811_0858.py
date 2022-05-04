# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0004_auto_20200807_2005'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracaoPacote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('ativo', models.BooleanField(default=True, verbose_name=b'Ativo')),
                ('titulo', models.CharField(unique=True, max_length=50, verbose_name='Titulo')),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unit\xe1rio', max_digits=5, decimal_places=2)),
                ('unitario', models.BooleanField(default=True, help_text='Se selecionado, permite a compra de cr\xe9ditos por unidade.', verbose_name='Unit\xe1rio')),
                ('qtda_minima', models.PositiveSmallIntegerField(default=1, verbose_name='Qtda. m\xednima')),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'titulo', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Configura\xe7\xe3o de Pacote',
                'verbose_name_plural': 'Configura\xe7\xf5es de Pacote',
            },
        ),
        migrations.CreateModel(
            name='Pacote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('quantidade', models.PositiveSmallIntegerField(verbose_name='Quantidade')),
                ('desconto', models.FloatField(help_text=b'%', verbose_name=b'Desconto')),
                ('configuracao', models.ForeignKey(verbose_name='Configura\xe7\xe3o', to='financeiro.ConfiguracaoPacote')),
            ],
            options={
                'verbose_name': 'Pacote',
                'verbose_name_plural': 'Pacotes',
            },
        ),
        migrations.AlterUniqueTogether(
            name='pacote',
            unique_together=set([('configuracao', 'quantidade')]),
        ),
    ]
