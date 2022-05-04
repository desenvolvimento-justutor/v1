# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0006_auto_20200812_1831'),
        ('financeiro', '0007_credito_pacote'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracaopacote',
            name='curso',
            field=models.ForeignKey(default=3, verbose_name=b'Curso', to='curso.CursoCredito'),
            preserve_default=False,
        ),
    ]
