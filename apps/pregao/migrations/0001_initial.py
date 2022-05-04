# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretor', '0001_initial'),
        ('enunciado', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitarCorrecao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_hora', models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora')),
                ('status', models.CharField(default='E', max_length=1, choices=[('A', 'Aguardando'), ('C', 'Corrigido'), ('E', 'Esbo\xe7o'), ('I', 'Iniciado')])),
                ('correcao', models.TextField(null=True, verbose_name='Corre\xe7\xe3o', blank=True)),
                ('corretor', models.ForeignKey(related_name='get_corretor', blank=True, to='corretor.Corretor', null=True)),
                ('corretores', models.ManyToManyField(related_name='get_corretores', to='corretor.Corretor')),
                ('resposta', models.OneToOneField(to='enunciado.Resposta')),
            ],
            options={
                'verbose_name': 'Solicitar Corre\xe7\xe3o',
                'verbose_name_plural': 'Solicitar Corre\xe7\xf5es',
            },
        ),
    ]
