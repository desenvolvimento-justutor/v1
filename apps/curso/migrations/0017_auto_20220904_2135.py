# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0016_auto_20220822_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='omie_id',
            field=models.BigIntegerField(null=True, verbose_name='C\xf3digo Omie', blank=True),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'2F7-F7F', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
    ]
