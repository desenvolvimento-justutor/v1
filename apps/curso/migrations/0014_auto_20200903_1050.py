# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0013_auto_20200903_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='autores',
            field=models.ManyToManyField(related_name='autores', verbose_name=b'Autores', to='curso.Autor', blank=True),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'252-EE8', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
    ]
