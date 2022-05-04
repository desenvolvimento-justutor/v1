# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formulario_auto_correcao', '0002_auto_20200816_2010'),
        ('financeiro', '0011_auto_20200831_1642'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='creditoresgate',
            options={'ordering': ['-data'], 'verbose_name': 'Resgate de Cr\xe9dito', 'verbose_name_plural': 'Resgate de Cr\xe9ditos'},
        ),
        migrations.AddField(
            model_name='creditoresgate',
            name='formulario',
            field=models.ForeignKey(related_name='creditos_resgate', on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Formulario', blank=True, to='formulario_auto_correcao.Formulario', null=True),
        ),
    ]
