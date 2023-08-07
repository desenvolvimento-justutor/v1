# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario_correcao', '0013_auto_20230414_0536'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabelacorrecaoaluno',
            name='pago',
            field=models.BooleanField(default=False),
        ),
    ]
