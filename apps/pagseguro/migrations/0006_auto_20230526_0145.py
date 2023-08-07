# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagseguro', '0005_checkout_data_nfse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='data_nfse',
            field=models.TextField(null=True, verbose_name='Dados da NFSE', blank=True),
        ),
    ]
