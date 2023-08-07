# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pix', '0003_auto_20230414_0540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cobranca',
            name='checkout',
            field=models.OneToOneField(related_name='pix', on_delete=django.db.models.deletion.PROTECT, verbose_name='Checkout', to='pagseguro.Checkout'),
        ),
    ]
