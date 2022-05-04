# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields
import sorl.thumbnail.fields
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcompanharResposta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField(default=django.utils.timezone.now, verbose_name=b'Data')),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
            ],
            options={
                'ordering': ['-data', '-id'],
                'verbose_name': 'Acompanhar resposta',
                'verbose_name_plural': 'Respostas acompanhadas',
            },
        ),
        migrations.CreateModel(
            name='AreaProfissional',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=60, verbose_name=b'Nome')),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name': '\xc1rea Profissional',
                'verbose_name_plural': '\xc1reas Profissionais',
            },
        ),
        migrations.CreateModel(
            name='AvaliacaoCorrecao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.SmallIntegerField(default=1, help_text='Informe se a Avalia\xe7\xe3o foi Negativa/Positiva', verbose_name=b'Tipo', choices=[(0, b'Negativa'), (1, b'Positiva')])),
                ('data', models.DateTimeField(help_text='Data da Avalia\xe7\xe3o.', verbose_name=b'Data', auto_now_add=True)),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
            ],
            options={
                'verbose_name': 'Avalia\xe7\xe3o da Corre\xe7\xe3o',
                'verbose_name_plural': 'Avalia\xe7\xf5es das Corre\xe7\xf5es',
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=60, verbose_name=b'Nome')),
            ],
            options={
                'ordering': ['esfera_especifica', 'nome'],
                'verbose_name': 'Cargo',
            },
        ),
        migrations.CreateModel(
            name='Coletania',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
            ],
            options={
                'verbose_name': 'Colet\xe2nea',
                'verbose_name_plural': 'Colet\xe2neas',
            },
        ),
        migrations.CreateModel(
            name='ComentarioCorrecao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comentario', models.TextField(verbose_name='Nota')),
                ('data', models.DateTimeField(help_text='Data de cria\xe7\xe3o.', verbose_name=b'Data', auto_now_add=True)),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
            ],
            options={
                'ordering': ['-data'],
                'verbose_name': 'Coment\xe1rio da Resposta',
                'verbose_name_plural': 'Coment\xe1rios das Respostas',
            },
        ),
        migrations.CreateModel(
            name='Concurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=200, verbose_name=b'Nome')),
                ('cargo', models.ForeignKey(verbose_name=b'Cargo', to='enunciado.Cargo')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Correcao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField(help_text='Texto contendo a Corre\xe7\xe3o da Resposta.', verbose_name=b'Texto')),
                ('data', models.DateTimeField(help_text='Data de corre\xe7\xe3o.', verbose_name=b'Data', auto_now_add=True)),
                ('excluir', models.BooleanField(default=False, help_text='Marque para excluir a resposta e enviar um email informando o motivo.', verbose_name=b'Excluir')),
                ('excluir_motivo', models.TextField(help_text='Mensagem que ser\xe1 enviada informando o motivo da exclus\xe3o da corre\xe7\xe3o.', null=True, verbose_name=b'Motivo', blank=True)),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
            ],
            options={
                'ordering': ['-data'],
                'verbose_name': 'Corre\xe7\xe3o',
                'verbose_name_plural': 'Corre\xe7\xf5es',
            },
        ),
        migrations.CreateModel(
            name='CurtirComentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
            ],
            options={
                'verbose_name': 'Curtit Coment\xe1rio',
                'verbose_name_plural': 'Curtir Coment\xe1rios',
            },
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=60, verbose_name=b'Nome')),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name': 'D\xedsciplina',
            },
        ),
        migrations.CreateModel(
            name='DisciplinaLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('legislacao', models.BooleanField(default=False, verbose_name='Legisla\xe7\xe3o')),
                ('titulo', models.CharField(max_length=150, verbose_name='T\xedtulo')),
                ('link', models.URLField()),
                ('disciplina', models.ForeignKey(to='enunciado.Disciplina')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': "Link's",
            },
        ),
        migrations.CreateModel(
            name='EnunciadoProposta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desatualizado', models.BooleanField(default=False, help_text='Marque caso o Enunciado esteja desatualizado.', verbose_name=b'Desatualizado?')),
                ('classificacao', models.CharField(help_text=b"Informe se o Enunciado/Proposta \xc3\xa9 uma 'Senten\xc3\xa7a', 'Pe\xc3\xa7a Pr\xc3\xa1tica' ou uma 'Quest\xc3\xa3o Discursiva'.", max_length=2, verbose_name='Classifica\xe7\xe3o', choices=[(b'ST', 'Senten\xe7a'), (b'PP', 'Pe\xe7a Pr\xe1tica'), (b'QD', 'Quest\xe3o Discursiva')])),
                ('data_prova', models.PositiveSmallIntegerField(verbose_name=b'Data da Prova', choices=[(1989, b'1989'), (1990, b'1990'), (1991, b'1991'), (1992, b'1992'), (1993, b'1993'), (1994, b'1994'), (1995, b'1995'), (1996, b'1996'), (1997, b'1997'), (1998, b'1998'), (1999, b'1999'), (2000, b'2000'), (2001, b'2001'), (2002, b'2002'), (2003, b'2003'), (2004, b'2004'), (2005, b'2005'), (2006, b'2006'), (2007, b'2007'), (2008, b'2008'), (2009, b'2009'), (2010, b'2010'), (2011, b'2011'), (2012, b'2012'), (2013, b'2013'), (2014, b'2014'), (2015, b'2015'), (2016, b'2016'), (2017, b'2017'), (2018, b'2018'), (2019, b'2019'), (2020, b'2020')])),
                ('num_questao_caderno', models.PositiveSmallIntegerField(help_text='N\xfamero da Quest\xe3o no Caderno de Provas.', null=True, verbose_name='Numero da Quest\xe3o', blank=True)),
                ('linhas', models.PositiveSmallIntegerField(null=True)),
                ('texto', models.TextField(help_text='Formule um texto para o seu Enunciado.', null=True, verbose_name=b'Texto', blank=True)),
                ('audio', models.TextField(help_text=b'C\xc3\xb3digo embutido do Soundcloud', null=True, verbose_name=b'\xc3\x81udio', blank=True)),
                ('autor', models.CharField(blank=True, max_length=1, null=True, verbose_name=b'Autor do Gabarito', choices=[(b'B', b'Banca examinadora'), (b'J', b'Justutor')])),
                ('gabarito_file', models.FileField(help_text=b'Arquivo contendo o Gabarito.', upload_to=b'', null=True, verbose_name=b'Arquivo', blank=True)),
                ('gabarito', models.TextField(help_text=b'Texto do Gabarito.', null=True, verbose_name=b'Gabarito', blank=True)),
                ('area_profissional', models.ForeignKey(related_name='get_enunciados', verbose_name='\xc1rea Profissional', blank=True, to='enunciado.AreaProfissional', null=True)),
                ('cargo', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'esfera_especifica', related_name='get_enunciados', chained_field=b'esfera_especifica', verbose_name=b'Cargo', to='enunciado.Cargo')),
                ('concurso', models.ForeignKey(related_name='get_enunciados', verbose_name=b'Concurso', blank=True, to='enunciado.Concurso', null=True)),
                ('disciplina', models.ForeignKey(related_name='get_enunciados', verbose_name='Disc\xedplina', blank=True, to='enunciado.Disciplina', null=True)),
            ],
            options={
                'verbose_name': 'Enunciado/Proposta',
                'verbose_name_plural': 'Enunciados/Propostas',
            },
        ),
        migrations.CreateModel(
            name='EsferaEspecifica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=60, verbose_name=b'Nome')),
            ],
            options={
                'ordering': ['esfera_geral', 'nome'],
                'verbose_name': 'Esfera Espec\xedfica',
                'verbose_name_plural': 'Esferas Especificas',
            },
        ),
        migrations.CreateModel(
            name='EsferaGeral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=60, verbose_name=b'Nome')),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name': 'Esfera Geral',
                'verbose_name_plural': 'Esferas Gerais',
            },
        ),
        migrations.CreateModel(
            name='Localidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=60, verbose_name=b'Nome')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='NotaResposta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nota', models.PositiveSmallIntegerField(verbose_name='Nota')),
                ('data', models.DateTimeField(help_text='Data de cria\xe7\xe3o.', verbose_name=b'Data', auto_now_add=True)),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
            ],
            options={
                'verbose_name': 'Nota da Resposta',
                'verbose_name_plural': 'Notas das Respostas',
            },
        ),
        migrations.CreateModel(
            name='NotificacoesAluno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=1, verbose_name=b'Tipo', choices=[(b'R', b'Resposta'), (b'C', 'Corre\xe7\xe3o'), (b'M', 'Coment\xe1rio'), (b'L', b'Like'), (b'G', b'Mensagem')])),
                ('status_resposta', models.CharField(blank=True, max_length=1, null=True, verbose_name=b'Tipo', choices=[(b'I', b'Iniciou'), (b'F', 'Finalizou'), (b'C', 'Cancelou')])),
                ('lido', models.BooleanField(default=False, help_text='Marque para informar que voc\xea visualizou a Notifica\xe7\xe3o', verbose_name=b'Lido')),
                ('data', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Data')),
                ('aluno', models.ForeignKey(related_name='get_notificacao_de', verbose_name=b'Aluno', to='aluno.Aluno')),
                ('comentario', models.ForeignKey(blank=True, to='enunciado.ComentarioCorrecao', null=True)),
                ('correcao', models.ForeignKey(blank=True, to='enunciado.Correcao', null=True)),
                ('nota', models.ForeignKey(blank=True, to='enunciado.NotaResposta', null=True)),
                ('para', models.ForeignKey(related_name='get_notificacao_para', verbose_name=b'Para', blank=True, to='aluno.Aluno', null=True)),
            ],
            options={
                'verbose_name': 'Notifica\xe7\xe3o',
                'verbose_name_plural': 'Notifica\xe7\xf5es',
            },
        ),
        migrations.CreateModel(
            name='Organizador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=60, verbose_name=b'Nome')),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name': 'Organizador',
                'verbose_name_plural': 'Organizadoras',
            },
        ),
        migrations.CreateModel(
            name='OrgaoEntidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=60, verbose_name=b'Nome')),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name': '\xd3rg\xe3o/Entidade',
                'verbose_name_plural': '\xd3rg\xe3os/Entidades',
            },
        ),
        migrations.CreateModel(
            name='RankingPremiado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200, verbose_name='T\xedtulo')),
                ('tipo_ranking', models.CharField(max_length=1, verbose_name=b'Tipo de Ranking', choices=[(b'T', b'Todos'), (b'R', b'Elaborar Respostas'), (b'C', b'Corrigir Respostas')])),
                ('tipo_enunciado', models.CharField(max_length=2, verbose_name=b'Tipo de Enunciado', choices=[(b'T', b'Todos'), (b'QD', 'Quest\xe3o'), (b'PP', 'Pe\xe7a'), (b'ST', 'Senten\xe7a')])),
                ('texto', models.TextField(verbose_name='Conte\xfado')),
                ('data_ini', models.DateTimeField(verbose_name='Data de \xednicio')),
                ('data_fim', models.DateTimeField(verbose_name='Data de t\xe9rmino')),
                ('premio', models.CharField(max_length=255, verbose_name='Pr\xeamio')),
                ('imagem', sorl.thumbnail.fields.ImageField(help_text=b'Imagem do pr\xc3\xaamio', upload_to=b'premios/', null=True, verbose_name=b'Imagem', blank=True)),
                ('encerrado', models.BooleanField(default=False, help_text=b'Quando est\xc3\xa1 op\xc3\xa7\xc3\xa3o estiver marcada, o Ranking ser\xc3\xa1 exibido no site.', verbose_name=b'Encerrado')),
                ('slug', models.SlugField(max_length=150, editable=False)),
            ],
            options={
                'ordering': ['-data_ini', '-data_fim', 'encerrado'],
                'verbose_name': 'Ranking Premiado',
                'verbose_name_plural': "Ranking's Premiado",
            },
        ),
        migrations.CreateModel(
            name='RankingPremiadoPremio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('premio', models.CharField(max_length=255, verbose_name='Pr\xeamio')),
                ('imagem', sorl.thumbnail.fields.ImageField(help_text=b'Imagem do pr\xc3\xaamio', upload_to=b'premios/', null=True, verbose_name=b'Imagem', blank=True)),
                ('ranking_premiado', models.ForeignKey(verbose_name=b'Ranking Premiado', to='enunciado.RankingPremiado')),
            ],
            options={
                'verbose_name': ' Premia\xe7\xe3o - Ranking Premiado',
                'verbose_name_plural': 'Premia\xe7\xf5es - Ranking Premiado',
            },
        ),
        migrations.CreateModel(
            name='RankingPremiadoRanking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pontos', models.PositiveSmallIntegerField(verbose_name=b'Pontos')),
                ('total', models.PositiveSmallIntegerField(verbose_name=b'Total Pontos')),
                ('dt_cadastro', models.DateTimeField(verbose_name=b'Data Cadastro')),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
                ('ranking_premiado', models.ForeignKey(verbose_name=b'Ranking Premiado', to='enunciado.RankingPremiado')),
            ],
            options={
                'ordering': ['-pontos', '-total', '-dt_cadastro'],
                'verbose_name': 'Ranking',
                'verbose_name_plural': 'Ranking',
            },
        ),
        migrations.CreateModel(
            name='ResponderDepois',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField(default=django.utils.timezone.now, verbose_name=b'Data')),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
                ('enunciado', models.ForeignKey(verbose_name='Enunciado', to='enunciado.EnunciadoProposta')),
            ],
            options={
                'ordering': ['-data'],
                'verbose_name': 'Responder depois',
            },
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField(help_text='Texto contendo a Resposta do Enunciado.', verbose_name=b'Texto')),
                ('data_inicio', models.DateTimeField(help_text='Data/Hora que iniciou a corre\xe7\xe3o', verbose_name='In\xedcio', auto_now_add=True)),
                ('tempo', models.TimeField(default=b'00:00:00', null=True, verbose_name='Tempo', blank=True)),
                ('data_termino', models.DateTimeField(auto_now_add=True, help_text='Data/Hora que concluiu a corre\xe7\xe3o', null=True, verbose_name='T\xe9rmino')),
                ('concluido', models.BooleanField(default=False, verbose_name='Conclu\xeddo')),
                ('ativo', models.BooleanField(default=True, help_text='Se a resposta for desativada ela n\xe3o aparecer\xe1 mais no Site.', verbose_name=b'Ativo')),
                ('ativo_motivo', models.TextField(help_text='Mensagem que ser\xe1 enviada informando o motivo da inativa\xe7\xe3o da resposta.', null=True, verbose_name=b'Motivo', blank=True)),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
                ('enunciado', models.ForeignKey(verbose_name='Enunciado', to='enunciado.EnunciadoProposta')),
            ],
            options={
                'ordering': ['-data_termino'],
            },
        ),
        migrations.CreateModel(
            name='RespostaComentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comentario', models.TextField(verbose_name=b'Coment\xc3\xa1rio')),
                ('data', models.DateTimeField(help_text='Data de cria\xe7\xe3o.', verbose_name=b'Data', auto_now_add=True)),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
                ('resposta', models.ForeignKey(related_name='comentarios', verbose_name=b'Resposta', to='enunciado.Resposta')),
            ],
            options={
                'ordering': ['-data'],
            },
        ),
        migrations.CreateModel(
            name='RoteiroEstudo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=150, verbose_name=b'T\xc3\xadtulo')),
                ('edital', models.BooleanField(verbose_name=b'\xc3\x89 edital?')),
                ('slug', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name': 'Roteiro',
                'verbose_name_plural': 'Roteiros',
            },
        ),
        migrations.CreateModel(
            name='RoteiroEstudoItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=150, verbose_name='T\xedtulo')),
                ('slug', models.CharField(max_length=200)),
                ('roteiro', models.ForeignKey(related_name='itens', verbose_name=b'Roteiro', to='enunciado.RoteiroEstudo')),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name': 'Item',
                'verbose_name_plural': 'Itens',
            },
        ),
        migrations.CreateModel(
            name='RoteiroEstudoSubItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=150, verbose_name='T\xedtulo')),
                ('order', models.PositiveIntegerField(verbose_name=b'Ordem')),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'nome', editable=False, blank=True)),
                ('item', models.ForeignKey(related_name='subitens', verbose_name=b'Item', to='enunciado.RoteiroEstudoItem')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Sub-Item',
                'verbose_name_plural': 'Sub-Itens',
            },
        ),
        migrations.CreateModel(
            name='SeguirComentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
                ('resposta', models.ForeignKey(verbose_name=b'Resposta', to='enunciado.Resposta')),
            ],
            options={
                'verbose_name': 'Seguir Coment\xe1rio',
                'verbose_name_plural': 'Seguir Coment\xe1rios',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50, verbose_name=b'Nome da Tag')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='TagLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('legislacao', models.BooleanField(default=False, verbose_name='Legisla\xe7\xe3o')),
                ('titulo', models.CharField(max_length=150, verbose_name='T\xedtulo')),
                ('link', models.URLField()),
                ('tag', models.ForeignKey(to='enunciado.Tag')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': "Link's",
            },
        ),
        migrations.CreateModel(
            name='TipoPecaPratica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=60, verbose_name=b'Nome')),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name': 'Tipo de Pe\xe7a Pr\xe1tica',
                'verbose_name_plural': 'Tipos de Pe\xe7as Pr\xe1ticas',
            },
        ),
        migrations.CreateModel(
            name='TipoPecaSentenca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=60, verbose_name=b'Nome')),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name': 'Tipo de Senten\xe7a',
                'verbose_name_plural': 'Tipos de Senten\xe7as',
            },
        ),
        migrations.CreateModel(
            name='TipoProcedimento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=60, verbose_name=b'Nome')),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name': 'Tipo de Procedimento',
                'verbose_name_plural': 'Tipos de Procedimentos',
            },
        ),
        migrations.AddField(
            model_name='roteiroestudosubitem',
            name='tags',
            field=models.ManyToManyField(to='enunciado.Tag', verbose_name=b'Tags', blank=True),
        ),
        migrations.AddField(
            model_name='notificacoesaluno',
            name='resposta',
            field=models.ForeignKey(blank=True, to='enunciado.Resposta', null=True),
        ),
        migrations.AddField(
            model_name='notaresposta',
            name='resposta',
            field=models.ForeignKey(verbose_name='Resposta', to='enunciado.Resposta'),
        ),
        migrations.AddField(
            model_name='esferaespecifica',
            name='esfera_geral',
            field=models.ForeignKey(related_name='get_especificas', verbose_name='Esfera Geral', to='enunciado.EsferaGeral'),
        ),
        migrations.AddField(
            model_name='enunciadoproposta',
            name='esfera_especifica',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'esfera_geral', related_name='get_enunciados', chained_field=b'esfera_geral', verbose_name='Esfera Espec\xedfica', to='enunciado.EsferaEspecifica'),
        ),
        migrations.AddField(
            model_name='enunciadoproposta',
            name='esfera_geral',
            field=models.ForeignKey(related_name='get_enunciados', verbose_name=b'Esfera Geral', to='enunciado.EsferaGeral'),
        ),
        migrations.AddField(
            model_name='enunciadoproposta',
            name='localidade',
            field=models.ForeignKey(verbose_name=b'Localidade', to='enunciado.Localidade'),
        ),
        migrations.AddField(
            model_name='enunciadoproposta',
            name='organizador',
            field=models.ForeignKey(verbose_name=b'Organizador(a)', to='enunciado.Organizador'),
        ),
        migrations.AddField(
            model_name='enunciadoproposta',
            name='orgao_entidade',
            field=models.ForeignKey(related_name='get_enunciados', verbose_name='\xd3rgao/Entidade', to='enunciado.OrgaoEntidade'),
        ),
        migrations.AddField(
            model_name='enunciadoproposta',
            name='tags',
            field=models.ManyToManyField(to='enunciado.Tag', verbose_name=b'Tag', blank=True),
        ),
        migrations.AddField(
            model_name='enunciadoproposta',
            name='tipo_peca_pratica',
            field=models.ForeignKey(verbose_name='Tipo de Pe\xe7a Pr\xe1tica', blank=True, to='enunciado.TipoPecaPratica', null=True),
        ),
        migrations.AddField(
            model_name='enunciadoproposta',
            name='tipo_procedimento',
            field=models.ForeignKey(verbose_name=b'Tipo de Procedimento', blank=True, to='enunciado.TipoProcedimento', null=True),
        ),
        migrations.AddField(
            model_name='enunciadoproposta',
            name='tipo_sentenca',
            field=models.ForeignKey(verbose_name='Tipo de Senten\xe7a', blank=True, to='enunciado.TipoPecaSentenca', null=True),
        ),
        migrations.AddField(
            model_name='curtircomentario',
            name='comentario',
            field=models.ForeignKey(verbose_name=b'Coment\xc3\xa1rio', to='enunciado.RespostaComentario'),
        ),
        migrations.AddField(
            model_name='correcao',
            name='resposta',
            field=models.ForeignKey(verbose_name=b'Resposta', to='enunciado.Resposta'),
        ),
        migrations.AddField(
            model_name='comentariocorrecao',
            name='correcao',
            field=models.ForeignKey(verbose_name='Resposta', to='enunciado.Correcao'),
        ),
        migrations.AddField(
            model_name='coletania',
            name='resposta',
            field=models.ForeignKey(verbose_name='Resposta', to='enunciado.Resposta'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='esfera_especifica',
            field=models.ForeignKey(related_name='get_cargos', verbose_name='Esfera Espec\xedfica', to='enunciado.EsferaEspecifica'),
        ),
        migrations.AddField(
            model_name='avaliacaocorrecao',
            name='correcao',
            field=models.ForeignKey(verbose_name='Corre\xe7\xe3o', to='enunciado.Correcao'),
        ),
        migrations.AddField(
            model_name='acompanharresposta',
            name='enunciado',
            field=models.ForeignKey(verbose_name='Enunciado', to='enunciado.EnunciadoProposta'),
        ),
        migrations.CreateModel(
            name='EnunciadoPropostaDiscursiva',
            fields=[
            ],
            options={
                'verbose_name': 'Quest\xe3o Discursiva',
                'proxy': True,
                'verbose_name_plural': 'Quest\xf5es Discursivas',
            },
            bases=('enunciado.enunciadoproposta',),
        ),
        migrations.CreateModel(
            name='EnunciadoPropostaPratica',
            fields=[
            ],
            options={
                'verbose_name': 'Pe\xe7a Pr\xe1tica',
                'proxy': True,
                'verbose_name_plural': 'Pe\xe7as Pr\xe1ticas',
            },
            bases=('enunciado.enunciadoproposta',),
        ),
        migrations.CreateModel(
            name='EnunciadoPropostaSentenca',
            fields=[
            ],
            options={
                'verbose_name': 'Senten\xe7a',
                'proxy': True,
            },
            bases=('enunciado.enunciadoproposta',),
        ),
        migrations.AlterUniqueTogether(
            name='seguircomentario',
            unique_together=set([('aluno', 'resposta')]),
        ),
        migrations.AlterUniqueTogether(
            name='roteiroestudosubitem',
            unique_together=set([('nome', 'item')]),
        ),
        migrations.AlterUniqueTogether(
            name='resposta',
            unique_together=set([('enunciado', 'aluno', 'ativo', 'ativo_motivo')]),
        ),
        migrations.AlterUniqueTogether(
            name='responderdepois',
            unique_together=set([('aluno', 'enunciado')]),
        ),
        migrations.AlterUniqueTogether(
            name='notaresposta',
            unique_together=set([('aluno', 'resposta')]),
        ),
        migrations.AlterUniqueTogether(
            name='esferaespecifica',
            unique_together=set([('nome', 'esfera_geral')]),
        ),
        migrations.AlterUniqueTogether(
            name='curtircomentario',
            unique_together=set([('aluno', 'comentario')]),
        ),
        migrations.AlterUniqueTogether(
            name='coletania',
            unique_together=set([('aluno', 'resposta')]),
        ),
        migrations.AlterUniqueTogether(
            name='cargo',
            unique_together=set([('nome', 'esfera_especifica')]),
        ),
        migrations.AlterUniqueTogether(
            name='avaliacaocorrecao',
            unique_together=set([('aluno', 'correcao')]),
        ),
        migrations.AlterUniqueTogether(
            name='acompanharresposta',
            unique_together=set([('aluno', 'enunciado')]),
        ),
    ]
