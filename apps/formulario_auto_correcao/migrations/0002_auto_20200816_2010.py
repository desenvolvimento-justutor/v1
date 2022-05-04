# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario_auto_correcao', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formulario',
            name='valor',
        ),
        migrations.AddField(
            model_name='formulario',
            name='creditos',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Cr\xe9ditos', blank=True),
        ),
    ]
