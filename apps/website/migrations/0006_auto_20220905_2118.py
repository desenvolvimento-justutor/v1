# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_bannerfooter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bannerfooter',
            options={'verbose_name': 'Banner Footer', 'verbose_name_plural': 'Banners Footer'},
        ),
        migrations.RemoveField(
            model_name='bannerfooter',
            name='texto',
        ),
        migrations.RemoveField(
            model_name='bannerfooter',
            name='titulo',
        ),
        migrations.AlterField(
            model_name='bannerfooter',
            name='imagem',
            field=sorl.thumbnail.fields.ImageField(help_text='Escolha uma imagem com tamanho de 400x300 pixels.', upload_to=b'banner-img', verbose_name='Imagem'),
        ),
    ]
