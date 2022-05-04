# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0005_auto_20200807_2004'),
    ]

    operations = [
        migrations.CreateModel(
            name='CursoCredito',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('curso.curso',),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='tipo',
            field=models.CharField(default=b'C', max_length=1, verbose_name=b'Tipo', choices=[(b'C', b'Curso'), (b'S', b'Atividade Avulsa'), (b'O', b'OAB 2\xc2\xaa Fase'), (b'L', b'Livro'), (b'B', b'Combo'), (b'D', b'Simulado'), (b'P', 'Cr\xe9dito')]),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'A33-ACE', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
    ]
