# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cupom', '0001_initial'),
        ('curso', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cupom',
            name='produtos',
            field=models.ManyToManyField(help_text='Selecione o(s) curso(s). Se necess\xe1rio.', to='curso.Curso', db_index=True, verbose_name='Curso(s)', blank=True),
        ),
    ]
