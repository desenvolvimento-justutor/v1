# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pix', '0002_cobranca_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cobranca',
            name='checkout',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, verbose_name='Checkout', to='pagseguro.Checkout'),
        ),
    ]
