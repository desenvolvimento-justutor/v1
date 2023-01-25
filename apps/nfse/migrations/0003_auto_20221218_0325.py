# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('nfse', '0002_auto_20221218_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nsfe',
            name='data_emissao',
            field=models.DateTimeField(auto_now=True, verbose_name='Data de emiss\xe3o'),
        ),
        migrations.AlterField(
            model_name='nsfe',
            name='ref',
            field=models.UUIDField(default=uuid.uuid4, verbose_name=b'Ref'),
        ),
    ]
