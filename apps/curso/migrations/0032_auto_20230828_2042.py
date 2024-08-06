# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import datetime
import apps.curso.models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0031_auto_20230414_0540'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='videomodulo',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='modulo',
            name='thumbnail',
            field=sorl.thumbnail.fields.ImageField(help_text='Miniatura que ser\xe1 exibido, se n\xe3o escolher ser\xe1 gerado automaticamente', upload_to='videos_thumb/', null=True, verbose_name='Capa', blank=True),
        ),
        migrations.AddField(
            model_name='videomodulo',
            name='order',
            field=models.PositiveIntegerField(default=1, verbose_name='Ordem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='atividade',
            name='curso',
            field=models.ForeignKey(related_name='atividades', verbose_name='Curso', to='curso.Curso'),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='data',
            field=models.DateField(default=datetime.datetime.today, verbose_name='Data de Cria\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='data_fim',
            field=models.DateTimeField(null=True, verbose_name='Data de t\xe9rmino'),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='data_ini',
            field=models.DateTimeField(null=True, verbose_name='Data de in\xedcio'),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='descricao',
            field=models.TextField(help_text='Breve descri\xe7\xe3o da atividade', null=True, verbose_name='Descri\xe7\xe3o', blank=True),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='nome',
            field=models.CharField(max_length=150, verbose_name='T\xedtulo'),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='resolucao_obrigatorio',
            field=models.BooleanField(default=False, help_text='Marque se essa Atividade se for de Resolu\xe7\xe3o Obrigat\xf3ria para a emiss\xe3o do Certificado.', verbose_name='Resolu\xe7\xe3o Obrigat\xf3ria?'),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='resposta_padra',
            field=models.FileField(upload_to='respostas', null=True, verbose_name='Resposta padr\xe3o', blank=True),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='resposta_padrao_data',
            field=models.DateTimeField(help_text='Data em que a resposta padr\xe3o estar\xe1 dispon\xedvel', null=True, verbose_name='Data dispon\xedvel', blank=True),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='tipo_retorno',
            field=models.CharField(max_length=1, verbose_name='Tipo de retorno do professor', choices=[('F', 'Apenas discuss\xe3o no f\xf3rum'), ('R', 'Apenas Gabarito'), ('C', 'Corre\xe7\xe3o individual')]),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='tipo',
            field=models.CharField(default='C', max_length=1, verbose_name='Tipo', choices=[('C', 'Curso'), ('S', 'Atividade Avulsa'), ('O', 'OAB 2\xaa Fase'), ('L', 'Livro'), ('B', 'Combo'), ('D', 'Simulado'), ('P', 'Cr\xe9dito')]),
        ),
        migrations.AlterField(
            model_name='cortesia',
            name='codigo',
            field=models.CharField(default=apps.curso.models.uuid5, max_length=150, verbose_name='C\xf3digo'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='certificado_data_ini',
            field=models.DateField(help_text='Data para \xednicio da emiss\xe3o do Certificado', null=True, verbose_name='Data emiss\xe3o', blank=True),
        ),
        migrations.AlterField(
            model_name='curso',
            name='certificado_formato',
            field=models.CharField(default='landscape', choices=[('portrait', 'Retrato'), ('landscape', 'Paisagem')], max_length=20, blank=True, null=True, verbose_name='Orienta\xe7\xe3o da P\xe1gina'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='colecao',
            field=models.ForeignKey(related_name='colecoes', verbose_name='Cole\xe7\xe3o', blank=True, to='curso.Colecao', null=True),
        ),
        migrations.AlterField(
            model_name='curso',
            name='edicao',
            field=models.SmallIntegerField(null=True, verbose_name='Edi\xe7\xe3o', blank=True),
        ),
        migrations.AlterField(
            model_name='curso',
            name='formato',
            field=models.CharField(default='D', max_length=10, verbose_name='Formato', choices=[('D', 'Digital'), ('F', 'F\xedsico')]),
        ),
        migrations.AlterField(
            model_name='curso',
            name='limitar_correcao',
            field=models.SmallIntegerField(default=0, help_text='Limitar quantidade de corre\xe7\xf5es individuais a que o aluno tem direito?', verbose_name='Limitar corre\xe7\xf5es'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='paginas',
            field=models.SmallIntegerField(help_text='Quantidade de P\xe1ginas', null=True, verbose_name='P\xe1ginas', blank=True),
        ),
        migrations.AlterField(
            model_name='curso',
            name='sentenca_oab',
            field=models.OneToOneField(null=True, blank=True, to='curso.SentencaOAB', verbose_name='OAB 2\xaa Fase'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='sumario',
            field=models.FileField(upload_to='livros/sumario/', null=True, verbose_name='Sum\xe1rio', blank=True),
        ),
        migrations.AlterField(
            model_name='discussao',
            name='data_fim',
            field=models.DateField(help_text='Data em que ser\xe1 encerrada as discuss\xf5es.', verbose_name='Data de t\xe9rmino'),
        ),
        migrations.AlterField(
            model_name='discussao',
            name='data_ini',
            field=models.DateField(help_text='Data que ser\xe1 iniciada as discuss\xf5es.', verbose_name='Data de in\xedcio'),
        ),
        migrations.AlterField(
            model_name='discussao',
            name='descricao',
            field=models.TextField(null=True, verbose_name='Descri\xe7\xe3o', blank=True),
        ),
        migrations.AlterField(
            model_name='discussao',
            name='titulo',
            field=models.CharField(max_length=150, verbose_name='T\xedtulo'),
        ),
        migrations.AlterField(
            model_name='doccurso',
            name='data_ativo',
            field=models.DateField(help_text='Data em que arquivo ser\xe1 disponibilizado', null=True, verbose_name='Data ativo', blank=True),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='codigo',
            field=models.CharField(default='0FE-4BD', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True),
        ),
        migrations.AlterField(
            model_name='liberarcompracurso',
            name='data',
            field=models.DateField(help_text='Ap\xf3s essa data n\xe3o ser\xe1 mais possivel utilizar o C\xf3digo', verbose_name='Data de V\xe1lidade'),
        ),
        migrations.AlterField(
            model_name='sentencaavulsa',
            name='amostra',
            field=models.TextField(null=True, verbose_name='Amostra da Senten\xe7a', blank=True),
        ),
        migrations.AlterField(
            model_name='sentencaavulsa',
            name='cod_youtube',
            field=models.CharField(default='0', help_text='C\xf3digo do v\xeddeo no Youtube', max_length=50, verbose_name='C\xf3d. Youtube'),
        ),
        migrations.AlterField(
            model_name='sentencaavulsa',
            name='comentario',
            field=models.TextField(help_text='Coment\xe1rios do professor sobre a proposta de senten\xe7a ', null=True, verbose_name='Coment\xe1rios', blank=True),
        ),
        migrations.AlterField(
            model_name='sentencaavulsa',
            name='conteudo',
            field=models.TextField(help_text='Conte\xfado integral da proposta de senten\xe7a', verbose_name='Conte\xfado'),
        ),
        migrations.AlterField(
            model_name='sentencaavulsa',
            name='esfera_especifica',
            field=models.ForeignKey(verbose_name='Esfera Espec\xedfica', to='enunciado.EsferaEspecifica'),
        ),
        migrations.AlterField(
            model_name='sentencaavulsa',
            name='nivel',
            field=models.CharField(max_length=1, verbose_name='N\xedvel', choices=[('F', 'F\xe1cil'), ('M', 'M\xe9dio'), ('D', 'Dif\xedcil')]),
        ),
        migrations.AlterField(
            model_name='sentencaavulsa',
            name='titulo',
            field=models.CharField(help_text='Identifica\xe7\xe3o', max_length=150, verbose_name='T\xedtulo'),
        ),
        migrations.AlterField(
            model_name='sentencaavulsaaluno',
            name='correcao',
            field=models.FileField(upload_to='correcao_sentenca', null=True, verbose_name='Corre\xe7\xe3o', blank=True),
        ),
        migrations.AlterField(
            model_name='sentencaavulsaaluno',
            name='data_conclusao',
            field=models.DateTimeField(null=True, verbose_name='Data de conclus\xe3o', blank=True),
        ),
        migrations.AlterField(
            model_name='sentencaavulsaaluno',
            name='data_criacao',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data de cria\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='sentencaavulsaaluno',
            name='data_modificacao',
            field=models.DateTimeField(auto_now=True, verbose_name='Data de altera\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='sentencaavulsaaluno',
            name='status',
            field=models.CharField(default='I', max_length=1, verbose_name='Status', choices=[('I', 'Iniciada'), ('A', 'Aguardando Corre\xe7\xe3o'), ('C', 'Corrigido')]),
        ),
        migrations.AlterField(
            model_name='sentencaoab',
            name='amostra',
            field=models.TextField(null=True, verbose_name='Amostra da Senten\xe7a', blank=True),
        ),
        migrations.AlterField(
            model_name='sentencaoab',
            name='cod_youtube',
            field=models.CharField(default='0', help_text='C\xf3digo do v\xeddeo no Youtube', max_length=50, verbose_name='C\xf3d. Youtube'),
        ),
        migrations.AlterField(
            model_name='sentencaoab',
            name='comentario',
            field=models.TextField(help_text='Coment\xe1rios do professor sobre a proposta de senten\xe7a ', null=True, verbose_name='Coment\xe1rios', blank=True),
        ),
        migrations.AlterField(
            model_name='sentencaoab',
            name='conteudo',
            field=models.TextField(help_text='Conte\xfado integral da proposta de senten\xe7a', verbose_name='Conte\xfado'),
        ),
        migrations.AlterField(
            model_name='sentencaoab',
            name='nivel',
            field=models.CharField(max_length=1, verbose_name='N\xedvel', choices=[('F', 'F\xe1cil'), ('M', 'M\xe9dio'), ('D', 'Dif\xedcil')]),
        ),
        migrations.AlterField(
            model_name='sentencaoab',
            name='tipo_peca',
            field=models.ForeignKey(verbose_name='Tipo de Pe\xe7a Pr\xe1tica', to='enunciado.TipoPecaPratica'),
        ),
        migrations.AlterField(
            model_name='sentencaoab',
            name='titulo',
            field=models.CharField(help_text='Identifica\xe7\xe3o', max_length=150, verbose_name='T\xedtulo'),
        ),
        migrations.AlterField(
            model_name='sentencaoabavulsaaluno',
            name='correcao',
            field=models.FileField(upload_to='correcao_sentenca', null=True, verbose_name='Corre\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='sentencaoabavulsaaluno',
            name='data_criacao',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data de cria\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='sentencaoabavulsaaluno',
            name='data_modificacao',
            field=models.DateTimeField(auto_now=True, verbose_name='Data de altera\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='sentencaoabavulsaaluno',
            name='sentenca_oab',
            field=models.ForeignKey(verbose_name='OAB 2\xaa Fase', to='curso.SentencaOAB'),
        ),
        migrations.AlterField(
            model_name='sentencaoabavulsaaluno',
            name='status',
            field=models.CharField(default='I', max_length=1, verbose_name='Status', choices=[('I', 'Iniciada'), ('A', 'Aguardando Corre\xe7\xe3o'), ('C', 'Corrigido')]),
        ),
        migrations.AlterField(
            model_name='tarefaatividade',
            name='atividade',
            field=models.ForeignKey(related_name='tarefa_atividades', verbose_name='Atividade', to='curso.Atividade'),
        ),
        migrations.AlterField(
            model_name='tarefaatividade',
            name='concluido',
            field=models.BooleanField(default=False, verbose_name='Conclu\xeddo?'),
        ),
        migrations.AlterField(
            model_name='tarefaatividade',
            name='correcao',
            field=models.FileField(upload_to='correcao', null=True, verbose_name='Corre\xe7\xe3o', blank=True),
        ),
        migrations.AlterField(
            model_name='tarefaatividade',
            name='data_conclusao',
            field=models.DateTimeField(null=True, verbose_name='Data de conclus\xe3o', blank=True),
        ),
        migrations.AlterField(
            model_name='tarefaatividade',
            name='data_criacao',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data de cria\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='tarefaatividade',
            name='data_modificacao',
            field=models.DateTimeField(auto_now=True, verbose_name='Data de altera\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='tarefaatividade',
            name='gabarito',
            field=models.TextField(help_text='Corre\xe7\xe3o a partir do gabarito.', null=True, verbose_name='Gabarito', blank=True),
        ),
    ]
