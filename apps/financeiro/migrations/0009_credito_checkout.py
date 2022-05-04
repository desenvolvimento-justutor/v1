# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagseguro', '0001_initial'),
        ('financeiro', '0008_configuracaopacote_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='credito',
            name='checkout',
            field=models.ForeignKey(verbose_name=b'Checkout', blank=True, to='pagseguro.Checkout', null=True),
        ),
    ]
