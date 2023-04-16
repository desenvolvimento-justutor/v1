# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagseguro', '0004_auto_20230414_0536'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='data_nfse',
            field=models.TextField(verbose_name='Dados da NFSE', null=True, editable=False, blank=True),
        ),
    ]
