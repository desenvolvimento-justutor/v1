# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0028_auto_20221218_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cortesia',
            name='curso',
            field=models.ForeignKey(related_name='cortesias', verbose_name=b'Curso', to='curso.Curso'),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'E99-3DB', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
    ]
