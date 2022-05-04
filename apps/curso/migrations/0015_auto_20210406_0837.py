# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0014_auto_20200903_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='cursos',
            field=models.ManyToManyField(related_name='_curso_cursos_+', null=True, verbose_name=b'Cursos', to='curso.Curso', blank=True),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'C4E-735', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
    ]
