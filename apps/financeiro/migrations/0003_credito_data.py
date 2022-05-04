# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0002_auto_20200807_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='credito',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Data'),
        ),
    ]
