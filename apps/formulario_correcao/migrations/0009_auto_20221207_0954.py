# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formulario_correcao', '0008_tabela_proibir_negativa'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotaTabela',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nota', models.ForeignKey(to='formulario_correcao.Nota', on_delete=django.db.models.deletion.PROTECT)),
                ('tabela', models.ForeignKey(related_name='notas_tabela', to='formulario_correcao.Tabela')),
            ],
        ),
        migrations.AlterField(
            model_name='notacorrecao',
            name='nota',
            field=models.ForeignKey(related_name='nota_correcao', on_delete=django.db.models.deletion.PROTECT, verbose_name='Nota', to='formulario_correcao.Nota'),
        ),
    ]
