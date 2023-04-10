# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagseguro', '0002_checkout_omie_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='omie_id',
            field=models.BigIntegerField(null=True, verbose_name='Omie ID', blank=True),
        ),
    ]
