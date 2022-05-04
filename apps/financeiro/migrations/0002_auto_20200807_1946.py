# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditoResgate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('quantidade', models.PositiveSmallIntegerField(verbose_name=b'Quantidade')),
            ],
            options={
                'verbose_name': 'Resgate de Cr\xe9dito',
                'verbose_name_plural': 'Resgate de Cr\xe9ditos',
            },
        ),
        migrations.AlterModelOptions(
            name='credito',
            options={'verbose_name': 'Cr\xe9dito', 'verbose_name_plural': 'Cr\xe9ditos'},
        ),
        migrations.RemoveField(
            model_name='credito',
            name='active_date',
        ),
        migrations.RemoveField(
            model_name='credito',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='credito',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='credito',
            name='value',
        ),
        migrations.AddField(
            model_name='credito',
            name='origem',
            field=models.CharField(default='bonus', max_length=6, verbose_name=b'Origem', choices=[(b'bonus', 'B\xf4nus'), (b'compra', 'Compra')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='credito',
            name='quantidade',
            field=models.PositiveSmallIntegerField(default=0, verbose_name=b'Quantidade'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='creditoresgate',
            name='credito',
            field=models.ForeignKey(verbose_name='Cr\xe9dito', to='financeiro.Credito'),
        ),
    ]
