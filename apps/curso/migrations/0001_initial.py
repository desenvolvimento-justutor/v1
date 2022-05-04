# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import datetime
import filebrowser.fields
import apps.curso.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0002_auto_20200807_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=150, verbose_name=b'T\xc3\xadtulo')),
                ('descricao', models.TextField(help_text=b'Breve descri\xc3\xa7\xc3\xa3o da atividade', null=True, verbose_name=b'Descri\xc3\xa7\xc3\xa3o', blank=True)),
                ('gabarito', models.TextField(null=True, verbose_name=b'Gabarito', blank=True)),
                ('data', models.DateField(default=datetime.datetime.today, verbose_name=b'Data de Cria\xc3\xa7\xc3\xa3o')),
                ('data_ini', models.DateTimeField(null=True, verbose_name=b'Data de in\xc3\xadcio')),
                ('data_fim', models.DateTimeField(null=True, verbose_name=b'Data de t\xc3\xa9rmino')),
                ('tipo_retorno', models.CharField(max_length=1, verbose_name=b'Tipo de retorno do professor', choices=[(b'F', b'Apenas discuss\xc3\xa3o no f\xc3\xb3rum'), (b'R', b'Apenas Gabarito'), (b'C', b'Corre\xc3\xa7\xc3\xa3o individual')])),
                ('tarefa', models.TextField(null=True, verbose_name=b'Tarefa', blank=True)),
                ('resposta_padra', models.FileField(upload_to=b'respostas', null=True, verbose_name=b'Resposta padr\xc3\xa3o', blank=True)),
                ('resposta_padrao_data', models.DateTimeField(help_text=b'Data em que a resposta padr\xc3\xa3o estar\xc3\xa1 dispon\xc3\xadvel', null=True, verbose_name=b'Data dispon\xc3\xadvel', blank=True)),
                ('resolucao_obrigatorio', models.BooleanField(default=False, help_text=b'Marque se essa Atividade se for de Resolu\xc3\xa7\xc3\xa3o Obrigat\xc3\xb3ria para a emiss\xc3\xa3o do Certificado.', verbose_name=b'Resolu\xc3\xa7\xc3\xa3o Obrigat\xc3\xb3ria?')),
                ('caracteres', models.PositiveIntegerField(default=20000)),
            ],
        ),
        migrations.CreateModel(
            name='AtividadeModelo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=b'atividade-modelo', verbose_name=b'Arquivo')),
            ],
            options={
                'verbose_name': 'Atividade Modelo',
                'verbose_name_plural': 'Atividades Modelo',
            },
        ),
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100, verbose_name=b'Nome')),
                ('foto', sorl.thumbnail.fields.ImageField(upload_to=b'professor/', null=True, verbose_name=b'Foto', blank=True)),
                ('sobre', models.TextField(null=True, verbose_name=b'Sobre', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Autores',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('titulo', models.CharField(help_text="T\xedtulo que ser\xe1 exibido no menu. Caso n\xe3o informe ser\xe1 exibido o 'Nome'.", max_length=50, null=True, verbose_name='T\xedtulo', blank=True)),
                ('tipo', models.CharField(default=b'C', max_length=1, verbose_name=b'Tipo', choices=[(b'C', b'Curso'), (b'S', b'Atividade Avulsa'), (b'O', b'OAB 2\xc2\xaa Fase'), (b'L', b'Livro'), (b'B', b'Combo'), (b'D', b'Simulado')])),
                ('slug', models.SlugField(max_length=60, editable=False)),
                ('order', models.PositiveIntegerField(verbose_name='Ordem')),
            ],
            options={
                'verbose_name': 'Categoria',
            },
        ),
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chave', models.CharField(unique=True, max_length=32, verbose_name=b'Chave')),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutItens',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qtda', models.PositiveSmallIntegerField()),
                ('valor', models.DecimalField(max_digits=9, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Colecao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=100, verbose_name=b'Nome')),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name': 'Cole\xe7\xe3o',
                'verbose_name_plural': 'Cole\xe7\xf5es',
            },
        ),
        migrations.CreateModel(
            name='Cortesia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(default=apps.curso.models.uuid5, max_length=150, verbose_name=b'C\xc3\xb3digo')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name=b'Email', blank=True)),
                ('utilizado', models.BooleanField(default=False, verbose_name=b'Utilizado?')),
            ],
            options={
                'ordering': ['id', 'utilizado', 'aluno'],
                'verbose_name': 'Cortesia',
                'verbose_name_plural': 'Cortesias',
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('limitar_correcao', models.SmallIntegerField(default=0, help_text=b'Limitar quantidade de corre\xc3\xa7\xc3\xb5es individuais a que o aluno tem direito?', verbose_name=b'Limitar corre\xc3\xa7\xc3\xb5es')),
                ('nome', models.CharField(max_length=250, verbose_name='T\xedtulo')),
                ('video', filebrowser.fields.FileBrowseField(help_text='Selecione um v\xeddeo no fotmat .MP4', max_length=200, null=True, verbose_name='V\xeddeo Demonstra\xe7\xe3o', blank=True)),
                ('thumbnail', sorl.thumbnail.fields.ImageField(help_text='Miniatura que ser\xe1 exibido, se n\xe3o escolher ser\xe1 gerado automaticamente', upload_to=b'videos_thumb/', null=True, verbose_name=b'Capa', blank=True)),
                ('imagem', sorl.thumbnail.fields.ImageField(help_text='Selecione um imagem de capa que ser\xe1 exibida na listagem dos curso (Tam. 270x170).', upload_to=b'img_thumb/', null=True, verbose_name='Imagem', blank=True)),
                ('descricao', models.TextField(verbose_name='Apresenta\xe7\xe3o')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=15, decimal_places=2)),
                ('disponivel', models.BooleanField(default=True, verbose_name='Turma Dispon\xedvel?')),
                ('inicio_gratis', models.BooleanField(default=False, help_text='Informe caso o curso tenha in\xedcio gr\xe1tis.', verbose_name='In\xedcio Gr\xe1tis?')),
                ('data_ini', models.DateTimeField(default=django.utils.timezone.now, help_text='A partir dessa data o sistema automaticamente colocar\xe1 o curso no site', null=True, verbose_name='Data \xednicio')),
                ('data_fim', models.DateTimeField(help_text='A partir dessa data o sistema automaticamente ir\xe1 marcar o curso como encerrado', null=True, verbose_name='Data final', blank=True)),
                ('saiba_mais', models.TextField(null=True, verbose_name=b'Saiba+', blank=True)),
                ('cronograma', models.TextField(null=True, verbose_name=b'Cronograma', blank=True)),
                ('certificado_formato', models.CharField(default=b'landscape', choices=[(b'portrait', b'Retrato'), (b'landscape', b'Paisagem')], max_length=20, blank=True, null=True, verbose_name=b'Orienta\xc3\xa7\xc3\xa3o da P\xc3\xa1gina')),
                ('certificado', models.TextField(null=True, verbose_name=b'Certificado', blank=True)),
                ('certificado_data_ini', models.DateField(help_text=b'Data para \xc3\xadnicio da emiss\xc3\xa3o do Certificado', null=True, verbose_name=b'Data emiss\xc3\xa3o', blank=True)),
                ('slug', models.SlugField(max_length=150)),
                ('order', models.PositiveIntegerField(verbose_name='Ordem')),
                ('meta_description', models.CharField(help_text='Resumo geral do site. Frase que descreva muito bem o Curso. Quando o site for buscado, essa ser\xe1 a frase que aparecer\xe1 \xe0 quem buscar. Melhor utilizar de 25 a 30 palavras com 160 a 180 caracteres.', max_length=160, null=True, verbose_name='Meta Description', blank=True)),
                ('meta_keywords', models.CharField(help_text='Procure usar umas poucas palavras que descrevam o conte\xfado do Curso. Exemplo: clim\xe1tica, previs\xe3o clim\xe1tica,desenvolvimento, tempo, clima. \xc9 importante que as palavras estejam no T\xedtulo e nas Meta Description.', max_length=100, null=True, verbose_name='Meta Keywords', blank=True)),
                ('formato', models.CharField(default=b'D', max_length=10, verbose_name=b'Formato', choices=[(b'D', b'Digital'), (b'F', b'F\xc3\xadsico')])),
                ('livro', models.FileField(upload_to=b'livros/amostra/', null=True, verbose_name=b'Livro', blank=True)),
                ('isbn', models.CharField(max_length=13, unique=True, null=True, verbose_name=b'ISBN', blank=True)),
                ('amostra', models.FileField(upload_to=b'livros/amostra/', null=True, verbose_name=b'Amostra', blank=True)),
                ('sumario', models.FileField(upload_to=b'livros/sumario/', null=True, verbose_name=b'Sum\xc3\xa1rio', blank=True)),
                ('edicao', models.SmallIntegerField(null=True, verbose_name=b'Edi\xc3\xa7\xc3\xa3o', blank=True)),
                ('ano', models.SmallIntegerField(null=True, verbose_name=b'Ano', blank=True)),
                ('paginas', models.SmallIntegerField(help_text=b'Quantidade de P\xc3\xa1ginas', null=True, verbose_name=b'P\xc3\xa1ginas', blank=True)),
                ('economia', models.DecimalField(null=True, verbose_name=b'Economia', max_digits=9, decimal_places=2, blank=True)),
                ('status', models.CharField(default=b'A', max_length=1, verbose_name=b'Status', choices=[(b'A', b'Aberto'), (b'C', b'Carrinho'), (b'F', b'Finalizado')])),
            ],
            options={
                'ordering': ['-data_ini'],
                'verbose_name': 'Curso',
            },
        ),
        migrations.CreateModel(
            name='CursoAvaliacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avaliacao', models.CharField(max_length=1, verbose_name='Avalia\xe7\xe3o', choices=[(b'O', '\xd3timo'), (b'B', b'Bom'), (b'R', b'Ruim')])),
            ],
        ),
        migrations.CreateModel(
            name='CursoGratis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50, verbose_name='T\xedtulo')),
                ('thumbnail', sorl.thumbnail.fields.ImageField(help_text='Miniatura que ser\xe1 exibido.', upload_to=b'videos_thumb/', null=True, verbose_name=b'Capa', blank=True)),
                ('video', models.URLField(help_text='V\xeddeo de Apresenta\xe7\xe3o.', verbose_name='V\xeddeo URL')),
                ('descricao', models.TextField(verbose_name='Apresenta\xe7\xe3o')),
                ('data_cadastro', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data \xednicio', editable=False)),
                ('slug', models.SlugField(max_length=150, editable=False)),
                ('order', models.PositiveIntegerField(verbose_name='Ordem')),
                ('meta_description', models.CharField(help_text='Resumo geral do site. Frase que descreva muito bem o Curso. Quando o site for buscado, essa ser\xe1 a frase que aparecer\xe1 \xe0 quem buscar. Melhor utilizar de 25 a 30 palavras com 160 a 180 caracteres.', max_length=160, null=True, verbose_name='Meta Description', blank=True)),
                ('meta_keywords', models.CharField(help_text='Procure usar umas poucas palavras que descrevam o conte\xfado do Curso. Exemplo: clim\xe1tica, previs\xe3o clim\xe1tica,desenvolvimento, tempo, clima. \xc9 importante que as palavras estejam no T\xedtulo e nas Meta Description.', max_length=100, null=True, verbose_name='Meta Keywords', blank=True)),
            ],
            options={
                'verbose_name': 'Cursos Gr\xe1tis',
            },
        ),
        migrations.CreateModel(
            name='Destaque',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_ini', models.DateTimeField(default=django.utils.timezone.now, help_text='A partir dessa data o sistema automaticamente colocar\xe1 o curso em destaque', verbose_name='Data \xednicio')),
                ('data_fim', models.DateTimeField(help_text='A partir dessa data o sistema automaticamente ir\xe1 retirar o curso em destaque', null=True, verbose_name='Data final', blank=True)),
                ('order', models.PositiveIntegerField(verbose_name='Ordem')),
            ],
        ),
        migrations.CreateModel(
            name='Discussao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=150, verbose_name=b'T\xc3\xadtulo')),
                ('descricao', models.TextField(null=True, verbose_name=b'Descri\xc3\xa7\xc3\xa3o', blank=True)),
                ('data_ini', models.DateField(help_text=b'Data que ser\xc3\xa1 iniciada as discuss\xc3\xb5es.', verbose_name=b'Data de in\xc3\xadcio')),
                ('data_fim', models.DateField(help_text=b'Data em que ser\xc3\xa1 encerrada as discuss\xc3\xb5es.', verbose_name=b'Data de t\xc3\xa9rmino')),
            ],
            options={
                'verbose_name': 'Discuss\xe3o',
                'verbose_name_plural': 'Discuss\xf5es',
            },
        ),
        migrations.CreateModel(
            name='DocCurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=50, verbose_name='T\xedtulo')),
                ('file', models.FileField(upload_to=b'materiais', verbose_name='Documento')),
                ('data_ativo', models.DateField(help_text=b'Data em que arquivo ser\xc3\xa1 disponibilizado', null=True, verbose_name=b'Data ativo', blank=True)),
                ('order', models.PositiveIntegerField(verbose_name='Ordem')),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materiais',
            },
        ),
        migrations.CreateModel(
            name='LiberarCompraCurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(default=b'8D1-589', unique=True, max_length=7, verbose_name='C\xf3digo', db_index=True)),
                ('data', models.DateField(help_text=b'Ap\xc3\xb3s essa data n\xc3\xa3o ser\xc3\xa1 mais possivel utilizar o C\xc3\xb3digo', verbose_name=b'Data de V\xc3\xa1lidade')),
                ('ativo', models.BooleanField(default=True, verbose_name=b'Ativo')),
            ],
            options={
                'verbose_name': 'Liberar Compra de Curso',
                'verbose_name_plural': 'Liberar Compra de Cursos',
            },
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=60, verbose_name=b'Nome')),
                ('order', models.PositiveIntegerField(verbose_name=b'Ordem')),
            ],
            options={
                'verbose_name': 'M\xf3dulo',
            },
        ),
        migrations.CreateModel(
            name='PdfModulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=50, verbose_name='T\xedtulo')),
                ('pdf', filebrowser.fields.FileBrowseField(help_text='Selecione um arquivo no fotmat .PDF', max_length=200, null=True, verbose_name='Arquivo PDF', blank=True)),
            ],
            options={
                'verbose_name': 'V\xeddeo',
            },
        ),
        migrations.CreateModel(
            name='SentencaAvulsa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(help_text=b'Identifica\xc3\xa7\xc3\xa3o', max_length=150, verbose_name=b'T\xc3\xadtulo')),
                ('cod_youtube', models.CharField(default=b'0', help_text=b'C\xc3\xb3digo do v\xc3\xaddeo no Youtube', max_length=50, verbose_name=b'C\xc3\xb3d. Youtube')),
                ('nivel', models.CharField(max_length=1, verbose_name=b'N\xc3\xadvel', choices=[(b'F', b'F\xc3\xa1cil'), (b'M', b'M\xc3\xa9dio'), (b'D', b'Dif\xc3\xadcil')])),
                ('amostra', models.TextField(null=True, verbose_name=b'Amostra da Senten\xc3\xa7a', blank=True)),
                ('conteudo', models.TextField(help_text=b'Conte\xc3\xbado integral da proposta de senten\xc3\xa7a', verbose_name=b'Conte\xc3\xbado')),
                ('comentario', models.TextField(help_text=b'Coment\xc3\xa1rios do professor sobre a proposta de senten\xc3\xa7a ', null=True, verbose_name=b'Coment\xc3\xa1rios', blank=True)),
                ('gabarito', models.FileField(upload_to=b'gabaritos-sentenca', null=True, verbose_name=b'Gabarito', blank=True)),
            ],
            options={
                'ordering': ['titulo'],
                'verbose_name': 'Atividade Avulsa',
                'verbose_name_plural': 'Atividades Avulsas',
            },
        ),
        migrations.CreateModel(
            name='SentencaAvulsaAluno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resposta', models.TextField(default=b'', verbose_name=b'Resposta', blank=True)),
                ('correcao_individual', models.TextField(default=b'', verbose_name='Corre\xe7\xe3o individual', blank=True)),
                ('status', models.CharField(default=b'I', max_length=1, verbose_name=b'Status', choices=[(b'I', b'Iniciada'), (b'A', b'Aguardando Corre\xc3\xa7\xc3\xa3o'), (b'C', b'Corrigido')])),
                ('tempo', models.PositiveSmallIntegerField(default=0, verbose_name=b'Tempo')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name=b'Data de cria\xc3\xa7\xc3\xa3o')),
                ('data_modificacao', models.DateTimeField(auto_now=True, verbose_name=b'Data de altera\xc3\xa7\xc3\xa3o')),
                ('correcao', models.FileField(upload_to=b'correcao_sentenca', null=True, verbose_name=b'Corre\xc3\xa7\xc3\xa3o', blank=True)),
                ('data_conclusao', models.DateTimeField(null=True, verbose_name=b'Data de conclus\xc3\xa3o', blank=True)),
                ('arquivo', models.FileField(upload_to=b'sentenca-avulsa-aluno', null=True, verbose_name=b'Arquivo', blank=True)),
                ('data_upload', models.DateTimeField(null=True, verbose_name=b'Data Upload', blank=True)),
            ],
            options={
                'verbose_name': 'Atividade Avulsa do Aluno',
                'verbose_name_plural': 'Atividades Avulsas dos Alunos',
            },
        ),
        migrations.CreateModel(
            name='SentencaModelo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=b'correcao-sentenca-modelo', verbose_name=b'Arquivo')),
            ],
            options={
                'verbose_name': 'Senten\xe7a Modelo',
                'verbose_name_plural': 'Senten\xe7as Modelo',
            },
        ),
        migrations.CreateModel(
            name='SentencaModeloOAB',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=b'correcao-sentenca-modelo-oab', verbose_name=b'Arquivo')),
            ],
            options={
                'verbose_name': 'Senten\xe7a Modelo',
                'verbose_name_plural': 'Senten\xe7as Modelo',
            },
        ),
        migrations.CreateModel(
            name='SentencaOAB',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(help_text=b'Identifica\xc3\xa7\xc3\xa3o', max_length=150, verbose_name=b'T\xc3\xadtulo')),
                ('cod_youtube', models.CharField(default=b'0', help_text=b'C\xc3\xb3digo do v\xc3\xaddeo no Youtube', max_length=50, verbose_name=b'C\xc3\xb3d. Youtube')),
                ('nivel', models.CharField(max_length=1, verbose_name=b'N\xc3\xadvel', choices=[(b'F', b'F\xc3\xa1cil'), (b'M', b'M\xc3\xa9dio'), (b'D', b'Dif\xc3\xadcil')])),
                ('amostra', models.TextField(null=True, verbose_name=b'Amostra da Senten\xc3\xa7a', blank=True)),
                ('conteudo', models.TextField(help_text=b'Conte\xc3\xbado integral da proposta de senten\xc3\xa7a', verbose_name=b'Conte\xc3\xbado')),
                ('comentario', models.TextField(help_text=b'Coment\xc3\xa1rios do professor sobre a proposta de senten\xc3\xa7a ', null=True, verbose_name=b'Coment\xc3\xa1rios', blank=True)),
                ('gabarito', models.FileField(upload_to=b'gabaritos-oab', null=True, verbose_name=b'Gabarito', blank=True)),
            ],
            options={
                'ordering': ['titulo'],
                'verbose_name': 'OAB 2\xaa Fase',
                'verbose_name_plural': 'OAB 2\xaa Fase',
            },
        ),
        migrations.CreateModel(
            name='SentencaOABAvulsaAluno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resposta', models.TextField(default=b'', verbose_name=b'Resposta', blank=True)),
                ('status', models.CharField(default=b'I', max_length=1, verbose_name=b'Status', choices=[(b'I', b'Iniciada'), (b'A', b'Aguardando Corre\xc3\xa7\xc3\xa3o'), (b'C', b'Corrigido')])),
                ('tempo', models.PositiveSmallIntegerField(default=0, verbose_name=b'Tempo')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name=b'Data de cria\xc3\xa7\xc3\xa3o')),
                ('data_modificacao', models.DateTimeField(auto_now=True, verbose_name=b'Data de altera\xc3\xa7\xc3\xa3o')),
                ('correcao', models.FileField(upload_to=b'correcao_sentenca', null=True, verbose_name=b'Corre\xc3\xa7\xc3\xa3o')),
            ],
            options={
                'verbose_name': 'Senten\xe7a OAB do Aluno',
                'verbose_name_plural': 'Senten\xe7as OAB dos Alunos',
            },
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('slug', models.SlugField(max_length=60, editable=False)),
                ('order', models.PositiveIntegerField(verbose_name='Ordem')),
            ],
            options={
                'verbose_name': 'S\xe9rie',
            },
        ),
        migrations.CreateModel(
            name='TarefaAtividade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resposta', models.TextField(default=b'', verbose_name=b'Resposta', blank=True)),
                ('concluido', models.BooleanField(default=False, verbose_name=b'Conclu\xc3\xaddo?')),
                ('tempo', models.PositiveSmallIntegerField(default=0, verbose_name=b'Tempo')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name=b'Data de cria\xc3\xa7\xc3\xa3o')),
                ('data_modificacao', models.DateTimeField(auto_now=True, verbose_name=b'Data de altera\xc3\xa7\xc3\xa3o')),
                ('data_conclusao', models.DateTimeField(null=True, verbose_name=b'Data de conclus\xc3\xa3o', blank=True)),
                ('data_upload', models.DateTimeField(null=True, verbose_name=b'Data Upload', blank=True)),
                ('correcao', models.FileField(upload_to=b'correcao', null=True, verbose_name=b'Corre\xc3\xa7\xc3\xa3o', blank=True)),
                ('gabarito', models.TextField(help_text=b'Corre\xc3\xa7\xc3\xa3o a partir do gabarito.', null=True, verbose_name=b'Gabarito', blank=True)),
                ('corrigido', models.BooleanField(default=False, verbose_name=b'Corrigido?')),
                ('limitada', models.BooleanField(default=False, verbose_name=b'Limitada')),
                ('arquivo', models.FileField(upload_to=b'atividades', null=True, verbose_name=b'Selecione o arquivo', blank=True)),
                ('aluno', models.ForeignKey(verbose_name=b'Aluno', to='aluno.Aluno')),
                ('atividade', models.ForeignKey(verbose_name=b'Atividade', to='curso.Atividade')),
            ],
        ),
        migrations.CreateModel(
            name='VideoGratis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200, verbose_name='T\xedtulo')),
                ('descricao', models.TextField(null=True, verbose_name='Apresenta\xe7\xe3o', blank=True)),
                ('data_ini', models.DateTimeField(default=django.utils.timezone.now, help_text='A partir dessa data o sistema automaticamente colocar\xe1 o v\xeddeo no site', null=True, verbose_name='Data \xednicio', blank=True)),
                ('video', models.URLField(verbose_name='V\xeddeo URL')),
                ('order', models.PositiveIntegerField(verbose_name='Ordem')),
                ('curso', models.ForeignKey(verbose_name=b'Curso', to='curso.CursoGratis')),
            ],
            options={
                'ordering': ['-data_ini'],
                'verbose_name': 'V\xeddeo Gr\xe1tis',
                'verbose_name_plural': 'V\xeddeos Gr\xe1tis',
            },
        ),
        migrations.CreateModel(
            name='VideoModulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=50, verbose_name='T\xedtulo')),
                ('descricao', models.CharField(max_length=250, null=True, verbose_name='Descri\xe7\xe3o', blank=True)),
                ('video', filebrowser.fields.FileBrowseField(help_text='Selecione um v\xeddeo no fotmat .MP4', max_length=200, null=True, verbose_name='V\xeddeo', blank=True)),
                ('thumbnail', sorl.thumbnail.fields.ImageField(upload_to=b'videos_thumb/', editable=False, blank=True, help_text='Miniatura que ser\xe1 exibido, se n\xe3o escolher ser\xe1 gerado automaticamente', null=True, verbose_name=b'Capa')),
                ('modulo', models.ForeignKey(verbose_name='M\xf3dulo', blank=True, to='curso.Modulo', null=True)),
            ],
            options={
                'verbose_name': 'V\xeddeo',
            },
        ),
    ]
