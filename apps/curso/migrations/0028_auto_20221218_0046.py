# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0027_auto_20221123_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='professores',
            field=models.ManyToManyField(to='professor.Professor'),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'538-DC4', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
    ]
