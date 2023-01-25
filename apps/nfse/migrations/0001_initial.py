# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0003_auto_20220822_2239'),
        ('pagseguro', '0003_auto_20220608_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='NSFe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_emissao', models.DateTimeField(verbose_name='Data de emiss\xe3o')),
                ('ref', models.UUIDField(null=True, verbose_name=b'Ref', blank=True)),
                ('status', models.CharField(max_length=24, null=True, verbose_name=b'Status', blank=True)),
                ('numero_rps', models.CharField(max_length=20, null=True, verbose_name='N\xfamero RPS', blank=True)),
                ('serie_rps', models.CharField(max_length=20, null=True, verbose_name='S\xe9rie RPS', blank=True)),
                ('numero', models.CharField(max_length=20, null=True, verbose_name='N\xfamero', blank=True)),
                ('codigo_verificacao', models.CharField(max_length=20, null=True, verbose_name=b'C\xc3\xb3digo de verifica\xc3\xa7\xc3\xa3o', blank=True)),
                ('url', models.URLField(null=True, verbose_name=b'URL', blank=True)),
                ('caminho_xml_nota_fiscal', models.CharField(max_length=255, null=True, verbose_name=b'Caminho XML', blank=True)),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
                ('checkout', models.ForeignKey(verbose_name=b'Checkout', to='pagseguro.Checkout')),
            ],
            options={
                'ordering': ['data_emissao'],
                'verbose_name': 'NFSe',
                'verbose_name_plural': "NFSe's",
            },
        ),
    ]
