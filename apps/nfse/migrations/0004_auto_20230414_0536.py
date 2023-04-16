# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfse', '0003_auto_20221218_0325'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nsfe',
            options={'ordering': ['-data_emissao'], 'verbose_name': 'NFSe', 'verbose_name_plural': "NFSe's"},
        ),
        migrations.RemoveField(
            model_name='nsfe',
            name='checkout',
        ),
        migrations.AlterField(
            model_name='nsfe',
            name='status',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name=b'Status', choices=[(b'autorizado', b'Autorizado'), (b'cancelado', b'Cancelado'), (b'erro_autorizacao', 'Erro na autoriza\xe7\xe3o'), (b'processando_autorizacao', 'Processando autoriza\xe7\xe3o'), (b'substituido', 'Substitu\xeddo')]),
        ),
    ]
