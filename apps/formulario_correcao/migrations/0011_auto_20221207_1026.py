# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formulario_correcao', '0010_auto_20221207_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tabela',
            name='nota_tabela',
        ),
        migrations.AddField(
            model_name='notatabela',
            name='tabela',
            field=models.ForeignKey(related_name='notas_tabela', default=1, to='formulario_correcao.Tabela'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='notatabela',
            name='nota',
        ),
        migrations.AddField(
            model_name='notatabela',
            name='nota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=1, to='formulario_correcao.Nota'),
            preserve_default=False,
        ),
    ]
