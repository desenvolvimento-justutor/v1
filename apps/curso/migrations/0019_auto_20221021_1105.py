# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0018_auto_20220905_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='videomodulo',
            name='tipo',
            field=models.CharField(default=b'p', max_length=1, verbose_name=b'Tipo', choices=[(b'p', 'Padr\xe3o'), (b'v', b'VdoCipher'), (b'y', b'Youtube')]),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'2AD-E02', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
        migrations.AlterField(
            model_name='videomodulo',
            name='descricao',
            field=models.CharField(help_text='ID do v\xeddeo (VDOCipher/Youtube)', max_length=250, null=True, verbose_name='ID', blank=True),
        ),
    ]
