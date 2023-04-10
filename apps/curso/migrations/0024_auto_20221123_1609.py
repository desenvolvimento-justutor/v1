# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0023_auto_20221118_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'0AC-133', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
    ]
