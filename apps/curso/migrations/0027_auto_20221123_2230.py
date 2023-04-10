# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0026_auto_20221123_2227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atividade',
            name='mural',
        ),
        migrations.AddField(
            model_name='curso',
            name='mural',
            field=models.TextField(null=True, verbose_name=b'Mural', blank=True),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'CFE-0DF', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
    ]
