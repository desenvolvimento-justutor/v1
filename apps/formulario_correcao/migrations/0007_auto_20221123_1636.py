# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formulario_correcao', '0006_notacorrecao_atividade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notacorrecao',
            name='atividade',
        ),
        migrations.AddField(
            model_name='notacorrecao',
            name='tabela',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=1, verbose_name=b'Tabela', to='formulario_correcao.Tabela'),
            preserve_default=False,
        ),
    ]
