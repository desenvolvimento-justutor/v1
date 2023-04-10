# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20220822_2239'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerFooter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagem', sorl.thumbnail.fields.ImageField(help_text='Escolha uma imagem com tamanho de 1874x720 pixels.', upload_to=b'banner-img', verbose_name='Imagem')),
                ('titulo', models.CharField(max_length=150, verbose_name='T\xedtulo do banner')),
                ('texto', models.TextField(verbose_name='Texto')),
                ('link', models.URLField(help_text='Insira o link do banner', verbose_name='Link')),
                ('order', models.PositiveIntegerField(verbose_name='Ordem')),
            ],
            options={
                'verbose_name': 'Banner Footer',
                'verbose_name_plural': 'Banner FooterBanners Footer',
            },
        ),
    ]
