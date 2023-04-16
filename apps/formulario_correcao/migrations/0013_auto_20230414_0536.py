# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario_correcao', '0012_auto_20221207_1029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notatabela',
            name='nota',
        ),
        migrations.RemoveField(
            model_name='tabela',
            name='nota_tabela',
        ),
        migrations.DeleteModel(
            name='NotaTabela',
        ),
    ]
