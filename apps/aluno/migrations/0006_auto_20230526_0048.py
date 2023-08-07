# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0005_cursos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cursos',
            options={'managed': False, 'verbose_name': 'Curso'},
        ),
    ]
