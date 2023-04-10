# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0025_auto_20221123_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividade',
            name='mural',
            field=models.TextField(help_text=b'Mural de avisos', null=True, verbose_name=b'Mural', blank=True),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'371-DBB', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
    ]
