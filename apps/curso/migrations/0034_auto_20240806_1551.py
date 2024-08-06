# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0033_auto_20230907_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividade',
            name='enunciado',
            field=models.TextField(null=True, verbose_name='Enunciado', blank=True),
        ),
        migrations.AddField(
            model_name='atividade',
            name='exemplos_correcao',
            field=models.TextField(null=True, verbose_name='Exemplos de Corre\xe7\xe3o', blank=True),
        ),
        migrations.AddField(
            model_name='atividade',
            name='frequency_penalty',
            field=models.DecimalField(default=0.0, help_text='Penalidade para a frequ\xeancia de termos repetidos. Valores entre 0 e 1 s\xe3o aceitos. Ex.: 0.50', max_digits=4, decimal_places=2),
        ),
        migrations.AddField(
            model_name='atividade',
            name='gpt_model',
            field=models.CharField(default='GPT-3', help_text='Selecione o modelo GPT a ser usado.', max_length=20, choices=[('GPT-2', 'GPT-2'), ('GPT-3', 'GPT-3'), ('GPT-3.5', 'GPT-3.5'), ('GPT-4', 'GPT-4')]),
        ),
        migrations.AddField(
            model_name='atividade',
            name='instrucoes_gpt',
            field=models.TextField(help_text='Instru\xe7\xf5es para o GPT', null=True, verbose_name='Instru\xe7\xf5es', blank=True),
        ),
        migrations.AddField(
            model_name='atividade',
            name='max_tokens',
            field=models.IntegerField(default=256, help_text='Especifique o n\xfamero m\xe1ximo de tokens na resposta. Deve ser um n\xfamero inteiro.'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='padrao_resposta',
            field=models.TextField(null=True, verbose_name='Padr\xe3o de Resposta', blank=True),
        ),
        migrations.AddField(
            model_name='atividade',
            name='parametros_correcao',
            field=models.TextField(null=True, verbose_name='Par\xe2metros de Corre\xe7\xe3o', blank=True),
        ),
        migrations.AddField(
            model_name='atividade',
            name='presence_penalty',
            field=models.DecimalField(default=0.0, help_text='Penalidade para a presen\xe7a de termos espec\xedficos. Valores entre 0 e 1 s\xe3o aceitos. Ex.: 0.50', max_digits=4, decimal_places=2),
        ),
        migrations.AddField(
            model_name='atividade',
            name='temperature',
            field=models.DecimalField(default=0.7, help_text='Define a aleatoriedade da resposta. Valores entre 0 e 1 s\xe3o aceitos. Ex.: 0.50', max_digits=4, decimal_places=2),
        ),
        migrations.AddField(
            model_name='atividade',
            name='top_p',
            field=models.DecimalField(default=0.9, help_text='Especifica a fra\xe7\xe3o da probabilidade cumulativa a ser considerada paraa resposta. Valores entre 0  e 1 s\xe3o aceitos. Ex.: 0.50', max_digits=4, decimal_places=2),
        ),
    ]
