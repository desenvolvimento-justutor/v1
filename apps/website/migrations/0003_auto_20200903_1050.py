# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20200829_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticialida',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
    ]
