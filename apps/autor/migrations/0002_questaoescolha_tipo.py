# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questaoescolha',
            name='tipo',
            field=models.CharField(default='N', verbose_name='Tipo', max_length=1, editable=False, choices=[('N', 'Multipla'), ('C', 'Correta'), ('E', 'Errada')]),
        ),
    ]
