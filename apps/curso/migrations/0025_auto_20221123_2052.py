# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0024_auto_20221123_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='is_tutorial',
            field=models.BooleanField(default=False, verbose_name='Tutorial'),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'83B-CF1', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
    ]
