# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pix', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cobranca',
            name='info',
            field=models.TextField(null=True, verbose_name='Informa\xe7\xf5es', blank=True),
        ),
    ]
