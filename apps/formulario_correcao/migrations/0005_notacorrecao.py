# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0003_auto_20220822_2239'),
        ('formulario_correcao', '0004_auto_20221118_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotaCorrecao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aluno', models.ForeignKey(verbose_name='Aluno', to='aluno.Aluno')),
                ('nota', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Nota', to='formulario_correcao.Nota')),
            ],
        ),
    ]
