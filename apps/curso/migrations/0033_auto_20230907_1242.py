# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0032_auto_20230828_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default='133-937', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
        migrations.AlterField(
            model_name='modulo',
            name='curso',
            field=models.ForeignKey(verbose_name='Curso', to='curso.Curso', null=True),
        ),
    ]
