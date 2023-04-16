# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfse', '0004_auto_20230414_0536'),
        ('pagseguro', '0003_auto_20220608_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='omie_id',
        ),
        migrations.AddField(
            model_name='checkout',
            name='nfse',
            field=models.OneToOneField(null=True, editable=False, to='nfse.NSFe', verbose_name='NFSe'),
        ),
    ]
