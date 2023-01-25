# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfse', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nsfe',
            name='checkout',
            field=models.OneToOneField(verbose_name=b'Checkout', to='pagseguro.Checkout'),
        ),
    ]
