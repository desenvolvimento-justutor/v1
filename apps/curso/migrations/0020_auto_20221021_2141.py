# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0019_auto_20221021_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default=b'30B-5C2', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
        migrations.AlterField(
            model_name='videomodulo',
            name='thumbnail',
            field=sorl.thumbnail.fields.ImageField(help_text='Miniatura que ser\xe1 exibido, se n\xe3o escolher ser\xe1 gerado automaticamente', upload_to=b'videos_thumb/', null=True, verbose_name=b'Capa', blank=True),
        ),
    ]
