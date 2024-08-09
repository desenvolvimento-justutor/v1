# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0034_auto_20240806_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividade',
            name='enable_gpt',
            field=models.BooleanField(default=False, help_text='Habilitar corre\xe7\xe3o pelo GPT', verbose_name='Habilitar GPT'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='instrucoes_recurso',
            field=models.TextField(help_text='Instru\xe7\xf5es para an\xe1lise do recurso', null=True, verbose_name='Instru\xe7\xf5es GPT', blank=True),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='instrucoes_gpt',
            field=models.TextField(help_text='Instru\xe7\xf5es para o GPT', null=True, verbose_name='Instru\xe7\xf5es GPT', blank=True),
        ),
    ]
