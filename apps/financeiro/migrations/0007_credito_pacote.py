# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.financeiro.models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0006_auto_20200812_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='credito',
            name='pacote',
            field=models.ForeignKey(verbose_name=apps.financeiro.models.Pacote, blank=True, to='financeiro.Pacote', null=True),
        ),
    ]
