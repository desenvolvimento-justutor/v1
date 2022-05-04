# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracao',
            name='politica',
            field=models.OneToOneField(related_name='politicas', null=True, blank=True, to='website.Institucional', verbose_name='Pol\xedtica de uso'),
        ),
        migrations.AddField(
            model_name='configuracao',
            name='termos',
            field=models.OneToOneField(related_name='termos', null=True, blank=True, to='website.Institucional', verbose_name='Termos'),
        ),
    ]
