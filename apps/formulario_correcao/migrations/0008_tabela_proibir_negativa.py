# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario_correcao', '0007_auto_20221123_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabela',
            name='proibir_negativa',
            field=models.BooleanField(default=False, verbose_name=b'Proibir nota negativa?'),
        ),
    ]
