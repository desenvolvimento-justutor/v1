# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('professor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enunciado', '0001_initial'),
        ('autor', '0001_initial'),
        ('aluno', '0002_auto_20200807_1644'),
        ('quizz', '0001_initial'),
        ('curso', '0001_initial'),
        ('pagseguro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarefaatividade',
            name='professor',
            field=models.ForeignKey(verbose_name=b'Corrigido por', blank=True, to='professor.Professor', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='serie',
            unique_together=set([('nome',)]),
        ),
        migrations.AddField(
            model_name='sentencaoabavulsaaluno',
            name='aluno',
            field=models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno'),
        ),
        migrations.AddField(
            model_name='sentencaoabavulsaaluno',
            name='sentenca_oab',
            field=models.ForeignKey(verbose_name=b'OAB 2\xc2\xaa Fase', to='curso.SentencaOAB'),
        ),
        migrations.AddField(
            model_name='sentencaoab',
            name='disciplina',
            field=models.ForeignKey(verbose_name=b'Disciplina', to='enunciado.Disciplina'),
        ),
        migrations.AddField(
            model_name='sentencaoab',
            name='professor',
            field=models.ForeignKey(to='professor.Professor'),
        ),
        migrations.AddField(
            model_name='sentencaoab',
            name='tipo_peca',
            field=models.ForeignKey(verbose_name=b'Tipo de Pe\xc3\xa7a Pr\xc3\xa1tica', to='enunciado.TipoPecaPratica'),
        ),
        migrations.AddField(
            model_name='sentencamodelooab',
            name='sentenca_oab',
            field=models.ForeignKey(to='curso.SentencaOAB'),
        ),
        migrations.AddField(
            model_name='sentencamodelo',
            name='sentenca_avulsa',
            field=models.ForeignKey(to='curso.SentencaAvulsa'),
        ),
        migrations.AddField(
            model_name='sentencaavulsaaluno',
            name='aluno',
            field=models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno'),
        ),
        migrations.AddField(
            model_name='sentencaavulsaaluno',
            name='sentenca_avulsa',
            field=models.ForeignKey(verbose_name=b'Atividade Avulsa', to='curso.SentencaAvulsa'),
        ),
        migrations.AddField(
            model_name='sentencaavulsa',
            name='disciplina',
            field=models.ForeignKey(verbose_name=b'Disciplina', to='enunciado.Disciplina', null=True),
        ),
        migrations.AddField(
            model_name='sentencaavulsa',
            name='esfera_especifica',
            field=models.ForeignKey(verbose_name=b'Esfera Espec\xc3\xadfica', to='enunciado.EsferaEspecifica'),
        ),
        migrations.AddField(
            model_name='sentencaavulsa',
            name='professor',
            field=models.ForeignKey(to='professor.Professor'),
        ),
        migrations.AddField(
            model_name='sentencaavulsa',
            name='tipo_procedimento',
            field=models.ForeignKey(verbose_name=b'Tipo de Procedimento', to='enunciado.TipoProcedimento', null=True),
        ),
        migrations.AddField(
            model_name='pdfmodulo',
            name='modulo',
            field=models.ForeignKey(verbose_name='M\xf3dulo', blank=True, to='curso.Modulo', null=True),
        ),
        migrations.AddField(
            model_name='modulo',
            name='curso',
            field=models.ForeignKey(verbose_name='Curso', to='curso.Curso'),
        ),
        migrations.AddField(
            model_name='liberarcompracurso',
            name='aluno',
            field=models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno'),
        ),
        migrations.AddField(
            model_name='liberarcompracurso',
            name='curso',
            field=models.ForeignKey(verbose_name=b'Curso', to='curso.Curso'),
        ),
        migrations.AddField(
            model_name='doccurso',
            name='curso',
            field=models.ForeignKey(verbose_name='Curso', to='curso.Curso'),
        ),
        migrations.AddField(
            model_name='discussao',
            name='curso',
            field=models.ForeignKey(verbose_name=b'Curso', to='curso.Curso'),
        ),
        migrations.AddField(
            model_name='destaque',
            name='curso',
            field=models.ForeignKey(verbose_name=b'Curso', to='curso.Curso'),
        ),
        migrations.AddField(
            model_name='cursogratis',
            name='serie',
            field=models.ForeignKey(verbose_name='Serie', to='curso.Serie'),
        ),
        migrations.AddField(
            model_name='cursoavaliacao',
            name='curso',
            field=models.ForeignKey(verbose_name=b'Curso', to='curso.Curso'),
        ),
        migrations.AddField(
            model_name='cursoavaliacao',
            name='user',
            field=models.ForeignKey(verbose_name='Usu\xe1rio', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='curso',
            name='aluno',
            field=models.ForeignKey(verbose_name=b'Aluno', blank=True, to='aluno.Aluno', null=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='autores',
            field=models.ManyToManyField(related_name='autores', null=True, verbose_name=b'Autores', to='curso.Autor', blank=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='blocos',
            field=models.ManyToManyField(to='quizz.Bloco', verbose_name=b'Quizz', blank=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='categoria',
            field=models.ForeignKey(verbose_name='Categoria', to='curso.Categoria'),
        ),
        migrations.AddField(
            model_name='curso',
            name='colecao',
            field=models.ForeignKey(related_name='colecoes', verbose_name=b'Cole\xc3\xa7\xc3\xa3o', blank=True, to='curso.Colecao', null=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='cursos',
            field=models.ManyToManyField(related_name='_curso_cursos_+', verbose_name=b'Cursos', to='curso.Curso'),
        ),
        migrations.AddField(
            model_name='curso',
            name='professores',
            field=models.ManyToManyField(to='professor.Professor', blank=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='sentenca_avulsa',
            field=models.OneToOneField(null=True, blank=True, to='curso.SentencaAvulsa', verbose_name=b'Atividade Avulsa'),
        ),
        migrations.AddField(
            model_name='curso',
            name='sentenca_oab',
            field=models.OneToOneField(null=True, blank=True, to='curso.SentencaOAB', verbose_name=b'OAB 2\xc2\xaa Fase'),
        ),
        migrations.AddField(
            model_name='curso',
            name='simulado',
            field=models.OneToOneField(null=True, blank=True, to='autor.Simulado', verbose_name=b'Simulado'),
        ),
        migrations.AddField(
            model_name='cortesia',
            name='aluno',
            field=models.ForeignKey(verbose_name=b'Aluno', blank=True, to='aluno.Aluno', null=True),
        ),
        migrations.AddField(
            model_name='checkoutitens',
            name='checkout',
            field=models.ForeignKey(to='pagseguro.Checkout'),
        ),
        migrations.AddField(
            model_name='checkoutitens',
            name='curso',
            field=models.ForeignKey(to='curso.Curso'),
        ),
        migrations.AddField(
            model_name='certificado',
            name='aluno',
            field=models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno'),
        ),
        migrations.AddField(
            model_name='certificado',
            name='curso',
            field=models.ForeignKey(related_name='certificados', verbose_name=b'Curso', to='curso.Curso'),
        ),
        migrations.AlterUniqueTogether(
            name='categoria',
            unique_together=set([('nome',)]),
        ),
        migrations.AddField(
            model_name='atividademodelo',
            name='atividade',
            field=models.ForeignKey(to='curso.Atividade'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='curso',
            field=models.ForeignKey(verbose_name='Curso', to='curso.Curso'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='professores',
            field=models.ManyToManyField(to='professor.Professor', blank=True),
        ),
        migrations.CreateModel(
            name='Combo',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('curso.curso',),
        ),
        migrations.CreateModel(
            name='ComboAluno',
            fields=[
            ],
            options={
                'verbose_name': 'Combo Personalizada',
                'proxy': True,
                'verbose_name_plural': 'Combos Personalizadas',
            },
            bases=('curso.curso',),
        ),
        migrations.CreateModel(
            name='Livro',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('curso.curso',),
        ),
        migrations.CreateModel(
            name='Simulado',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('curso.curso',),
        ),
        migrations.AlterUniqueTogether(
            name='sentencaoabavulsaaluno',
            unique_together=set([('sentenca_oab', 'aluno')]),
        ),
        migrations.AlterUniqueTogether(
            name='sentencaavulsaaluno',
            unique_together=set([('sentenca_avulsa', 'aluno')]),
        ),
        migrations.AlterUniqueTogether(
            name='liberarcompracurso',
            unique_together=set([('curso', 'aluno')]),
        ),
        migrations.AlterUniqueTogether(
            name='destaque',
            unique_together=set([('curso',)]),
        ),
        migrations.AlterUniqueTogether(
            name='cursogratis',
            unique_together=set([('nome',)]),
        ),
        migrations.AlterUniqueTogether(
            name='cursoavaliacao',
            unique_together=set([('user', 'curso')]),
        ),
        migrations.AlterUniqueTogether(
            name='curso',
            unique_together=set([('nome',)]),
        ),
        migrations.AddField(
            model_name='cortesia',
            name='curso',
            field=models.ForeignKey(related_name='cortesias', verbose_name=b'Curso', to='curso.Simulado'),
        ),
        migrations.AlterUniqueTogether(
            name='certificado',
            unique_together=set([('curso', 'aluno')]),
        ),
        migrations.AlterUniqueTogether(
            name='cortesia',
            unique_together=set([('curso', 'aluno')]),
        ),
    ]
