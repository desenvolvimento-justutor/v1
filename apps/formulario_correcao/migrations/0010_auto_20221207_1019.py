# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario_correcao', '0009_auto_20221207_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notatabela',
            name='tabela',
        ),
        migrations.AddField(
            model_name='tabela',
            name='nota_tabela',
            field=models.OneToOneField(null=True, blank=True, to='formulario_correcao.NotaTabela', verbose_name=b'Notas'),
        ),
        migrations.RemoveField(
            model_name='notatabela',
            name='nota',
        ),
        migrations.AddField(
            model_name='notatabela',
            name='nota',
            field=models.ManyToManyField(to='formulario_correcao.Nota', verbose_name=b'Nota'),
        ),
    ]
