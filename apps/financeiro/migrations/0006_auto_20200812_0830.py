# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.financeiro.models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0005_auto_20200811_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='PacoteDesconto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('de', models.PositiveSmallIntegerField(verbose_name=b'de')),
                ('ate', models.FloatField(verbose_name='at\xe9')),
                ('desconto', models.FloatField(help_text=b'%', verbose_name=b'Desconto')),
            ],
            options={
                'verbose_name': 'Desconto',
                'verbose_name_plural': 'Descontos',
            },
        ),
        migrations.RemoveField(
            model_name='configuracaopacote',
            name='qtda_minima',
        ),
        migrations.RemoveField(
            model_name='configuracaopacote',
            name='unitario',
        ),
        migrations.AddField(
            model_name='configuracaopacote',
            name='qtda_max',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Qtda. m\xe1xima'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuracaopacote',
            name='qtda_min',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Qtda. m\xednima'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='credito',
            name='uuid',
            field=models.CharField(default=apps.financeiro.models.get_uuid, unique=True, max_length=36, verbose_name=b'C\xc3\xb3digo'),
        ),
        migrations.AlterField(
            model_name='pacote',
            name='configuracao',
            field=models.ForeignKey(related_name='pacotes', verbose_name='Configura\xe7\xe3o', to='financeiro.ConfiguracaoPacote'),
        ),
        migrations.AlterField(
            model_name='pacote',
            name='desconto',
            field=models.FloatField(help_text=b'%', null=True, verbose_name=b'Desconto', blank=True),
        ),
        migrations.AddField(
            model_name='pacotedesconto',
            name='pacote',
            field=models.ForeignKey(related_name='descontos', verbose_name='Configura\xe7\xe3o', to='financeiro.ConfiguracaoPacote'),
        ),
    ]
