# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario_correcao', '0002_tabela_multipla'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tabela',
            name='multipla',
        ),
        migrations.AddField(
            model_name='nota',
            name='multipla',
            field=models.BooleanField(default=False, verbose_name=b'M\xc3\xbaltipla'),
        ),
    ]
