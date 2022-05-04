# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('curso', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(to='curso.Curso'),
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='checkout.OrderProduct', blank=True),
        ),
    ]
