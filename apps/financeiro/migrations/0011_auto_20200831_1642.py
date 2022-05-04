# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0010_auto_20200815_0253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pacote',
            options={'ordering': ['quantidade'], 'verbose_name': 'Pacote', 'verbose_name_plural': 'Pacotes'},
        ),
    ]
