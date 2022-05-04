# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0003_credito_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credito',
            name='data',
        ),
        migrations.AddField(
            model_name='creditoresgate',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Data'),
        ),
    ]
