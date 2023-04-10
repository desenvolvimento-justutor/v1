# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario_correcao', '0003_auto_20221118_1823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nota',
            name='multipla',
        ),
        migrations.AddField(
            model_name='nota',
            name='unica',
            field=models.BooleanField(default=False, verbose_name=b'\xc3\x9anica'),
        ),
    ]
