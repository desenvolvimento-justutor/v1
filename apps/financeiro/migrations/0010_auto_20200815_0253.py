# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0009_credito_checkout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacotedesconto',
            name='ate',
            field=models.PositiveSmallIntegerField(verbose_name='at\xe9'),
        ),
    ]
