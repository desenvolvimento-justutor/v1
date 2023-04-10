# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0020_auto_20221021_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='is_video_curso',
            field=models.BooleanField(default=False, help_text='Informe se o curso \xe9 em primordialmente em v\xeddeo', verbose_name='Curso em V\xeddeo'),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'D10-7A0', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
    ]
