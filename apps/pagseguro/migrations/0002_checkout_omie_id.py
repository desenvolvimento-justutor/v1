# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagseguro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='omie_id',
            field=models.IntegerField(null=True, verbose_name='Omie ID', blank=True),
        ),
        migrations.RunSQL("UPDATE pagseguro_checkout SET omie_id = 0 WHERE id > 0;")
    ]
