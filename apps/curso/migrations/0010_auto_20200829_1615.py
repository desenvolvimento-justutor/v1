# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0009_auto_20200816_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'94D-E67', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
    ]
