# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('professor', '0001_initial'),
        ('curso', '0002_auto_20200807_1644'),
        ('aluno', '0002_auto_20200807_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formulario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200, verbose_name=b'T\xc3\xadtulo')),
                ('texto', models.TextField(verbose_name=b'Texto')),
                ('atividade', models.OneToOneField(related_name='formulario', null=True, blank=True, to='curso.Atividade', verbose_name=b'Atividade')),
                ('sentenca_avulca', models.OneToOneField(related_name='formulario', null=True, blank=True, to='curso.SentencaAvulsa', verbose_name=b'Senten\xc3\xa7a')),
            ],
            options={
                'verbose_name': 'Fomul\xe1rio',
                'verbose_name_plural': 'Fomul\xe1rios',
            },
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(help_text=b'Texto da op\xc3\xa7\xc3\xa3o.', max_length=200, verbose_name=b'T\xc3\xadtulo')),
                ('texto', models.TextField(verbose_name=b'Texto', blank=True)),
                ('valor', models.DecimalField(help_text=b'Nota padr\xc3\xa3o que o usu\xc3\xa1rio receber\xc3\xa1.', verbose_name=b'Valor', max_digits=4, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Nota padr\xe3o',
                'verbose_name_plural': 'Notas padr\xe3o',
            },
        ),
        migrations.CreateModel(
            name='Tabela',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.TextField(verbose_name=b'Item')),
                ('valor', models.DecimalField(verbose_name=b'Valor', max_digits=4, decimal_places=2)),
                ('comentarios', models.TextField(null=True, verbose_name=b'Coment\xc3\xa1rios', blank=True)),
                ('order', models.PositiveIntegerField(verbose_name='Ordem')),
                ('formulario', models.ForeignKey(related_name='tabelas', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Formul\xe1rio', blank=True, to='formulario_correcao.Formulario', null=True)),
                ('nota', models.ManyToManyField(to='formulario_correcao.Nota', verbose_name=b'Nota')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Tabela de corre\xe7\xe3o',
                'verbose_name_plural': 'Tabelas de corre\xe7\xe3o',
            },
        ),
        migrations.CreateModel(
            name='TabelaAluno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField(null=True, verbose_name=b'Texto', blank=True)),
                ('nota', models.DecimalField(decimal_places=2, default=0, max_digits=4, blank=True, null=True, verbose_name=b'Nota')),
                ('nota_calc', models.BooleanField(default=False, verbose_name=b'Nota professor')),
                ('texto_recurso', models.TextField(null=True, verbose_name=b'Recurso')),
                ('texto_justificativa', models.TextField(null=True, verbose_name=b'Justificativa')),
                ('notas', models.ManyToManyField(to='formulario_correcao.Nota', verbose_name=b'Notas', blank=True)),
                ('tabela', models.ForeignKey(related_name='tabela_aluno', verbose_name=b'Tabela', to='formulario_correcao.Tabela')),
            ],
            options={
                'ordering': ['tabela'],
            },
        ),
        migrations.CreateModel(
            name='TabelaCorrecaoAluno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('corrigido', models.BooleanField(default=False)),
                ('texto', models.TextField(null=True, verbose_name=b'Texto', blank=True)),
                ('data_solicitacao', models.DateTimeField(null=True, verbose_name='Data da Solicita\xe7\xe3o', blank=True)),
                ('data_correcao', models.DateTimeField(null=True, verbose_name='Data da Corre\xe7\xe3o')),
                ('status', models.CharField(default=b'corrigido', max_length=10, verbose_name='Situa\xe7\xe3o', choices=[(b'corrigido', b'Corrigido'), (b'solicitado', b'Recurso Solicitado'), (b'analise', b'Recurso em An\xc3\xa1lise'), (b'analisado', b'Recurso Analisado')])),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Aluno', to='aluno.Aluno')),
                ('formulario', models.ForeignKey(verbose_name='Formul\xe1rio', to='formulario_correcao.Formulario')),
                ('professor', models.ForeignKey(verbose_name=b'Corrigido por', blank=True, to='professor.Professor', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='tabelaaluno',
            name='tabela_correcao',
            field=models.ForeignKey(related_name='tabelas', verbose_name=b'Correcao', to='formulario_correcao.TabelaCorrecaoAluno'),
        ),
    ]
