# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autor', '0002_questaoescolha_tipo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questaoescolha',
            options={'ordering': ['order', 'questao'], 'verbose_name': 'Escolha', 'verbose_name_plural': 'Escolhas'},
        ),
    ]
