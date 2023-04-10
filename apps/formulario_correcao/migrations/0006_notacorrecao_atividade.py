# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0024_auto_20221123_1609'),
        ('formulario_correcao', '0005_notacorrecao'),
    ]

    operations = [
        migrations.AddField(
            model_name='notacorrecao',
            name='atividade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=1, verbose_name=b'Atividade', to='curso.Atividade'),
            preserve_default=False,
        ),
    ]
