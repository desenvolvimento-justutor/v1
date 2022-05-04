# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bloco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=160, verbose_name=b'T\xc3\xadtulo')),
                ('descricao', models.CharField(max_length=160, verbose_name=b'Descri\xc3\xa7\xc3\xa3o')),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comentario', models.TextField(verbose_name=b'Comentario')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name=b'Data')),
                ('aluno', models.ForeignKey(related_name='alunos_comentario', verbose_name=b'Aluno', to='aluno.Aluno')),
            ],
            options={
                'ordering': ['-data'],
            },
        ),
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.TextField(verbose_name=b'T\xc3\xadtulo')),
                ('correta', models.BooleanField(default=False, verbose_name=b'Correta')),
            ],
            options={
                'verbose_name': 'Op\xe7\xe3o',
                'verbose_name_plural': 'Op\xe7\xf5es',
            },
        ),
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.TextField(verbose_name=b'T\xc3\xadtulo')),
                ('comentario', models.TextField(null=True, verbose_name=b'Coment\xc3\xa1rio do professor', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RespostaAluno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aluno', models.ForeignKey(related_name='alunos', verbose_name=b'Aluno', to='aluno.Aluno')),
                ('questao', models.ForeignKey(related_name='respostas_questao', verbose_name=b'Quest\xc3\xa3o', to='quizz.Questao')),
                ('resposta', models.ForeignKey(related_name='respostas_aluno', verbose_name=b'Resposta', to='quizz.Pergunta')),
            ],
        ),
        migrations.AddField(
            model_name='pergunta',
            name='questao',
            field=models.ForeignKey(related_name='opcoes', verbose_name=b'Quest\xc3\xa3o', to='quizz.Questao'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='questao',
            field=models.ForeignKey(related_name='comentarios', verbose_name=b'Quest\xc3\xa3o', to='quizz.Questao'),
        ),
        migrations.AddField(
            model_name='bloco',
            name='questoes',
            field=models.ManyToManyField(to='quizz.Questao', blank=True),
        ),
    ]
