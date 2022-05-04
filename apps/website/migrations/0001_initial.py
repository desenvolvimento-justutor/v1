# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import mptt.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('titulo', models.CharField(max_length=150, verbose_name='T\xedtulo')),
                ('imagem', sorl.thumbnail.fields.ImageField(help_text='Escolha uma imagem com tamanho de 1874x720 pixels.', upload_to=b'anuncions', verbose_name='Imagem')),
                ('link', models.URLField(help_text='Insira o link do an\xfancio', verbose_name='Link')),
                ('pag_atividades', models.BooleanField(default=False, verbose_name='P\xe1g. de Atividades')),
                ('pag_curso_gratis', models.BooleanField(default=False, verbose_name='P\xe1g. de Cursos Gr\xe1tis')),
                ('pag_cursos', models.BooleanField(default=False, verbose_name='P\xe1g. de Cursos')),
                ('pag_enunciados', models.BooleanField(default=False, verbose_name='P\xe1g. de Enunciados')),
                ('pag_resultado_busca', models.BooleanField(default=False, verbose_name='P\xe1g. do Resultado da Busca')),
                ('pag_conteudo', models.BooleanField(default=False, verbose_name='P\xe1g. de Conte\xfados')),
                ('pag_videos', models.BooleanField(default=False, verbose_name='P\xe1g. de V\xeddeos')),
                ('pag_roteiro', models.BooleanField(default=False, verbose_name='P\xe1g. de Roteiro')),
                ('pag_noticias', models.BooleanField(default=False, verbose_name='P\xe1g. de Not\xedcias')),
                ('pag_temas', models.BooleanField(default=False, verbose_name='P\xe1g. Temas Abordados')),
                ('pag_populares', models.BooleanField(default=False, verbose_name='P\xe1g. Mais Populares')),
            ],
            options={
                'verbose_name': 'An\xfancio',
            },
        ),
        migrations.CreateModel(
            name='Artigo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=150, verbose_name='T\xedtulo')),
                ('conteudo', models.TextField(verbose_name='Conte\xfado')),
                ('autor', models.CharField(max_length=150, null=True, verbose_name=b'Autor', blank=True)),
                ('data', models.DateField(default=django.utils.timezone.now, verbose_name=b'Data cadastro')),
                ('slug', models.SlugField(max_length=150, editable=False)),
            ],
            options={
                'verbose_name': 'Texto & Artigo',
                'verbose_name_plural': 'Textos & Artigos',
            },
        ),
        migrations.CreateModel(
            name='ArtigoIndice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='T\xedtulo')),
                ('descricao', models.TextField(null=True, verbose_name='Descri\xe7\xe3o', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', verbose_name='\xcdndice Superior', blank=True, to='website.ArtigoIndice', null=True)),
            ],
            options={
                'verbose_name': '\xcdndice',
                'verbose_name_plural': '\xcdndices',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exibir_caixa', models.BooleanField(default=False, verbose_name='Exibir caixa de legendas')),
                ('titulo', models.CharField(max_length=150, null=True, verbose_name='T\xedtulo do banner', blank=True)),
                ('legendas', models.TextField(help_text='Uma por linha', null=True, verbose_name='Legendas', blank=True)),
                ('order', models.PositiveIntegerField(verbose_name='Ordem')),
                ('imagem', sorl.thumbnail.fields.ImageField(help_text='Escolha uma imagem com tamanho de 1874x720 pixels.', upload_to=b'banner-img', verbose_name='Imagem')),
                ('link', models.URLField(help_text='Insira o link do banner', null=True, verbose_name='Link', blank=True)),
                ('texto_link', models.CharField(default='Saiba+', help_text='Se informado o link, informe o texto que ser\xe1 exibido no bot\xe3o', max_length=15, verbose_name='Texto do Link')),
                ('ativo_inicio', models.DateTimeField(default=django.utils.timezone.now, help_text='A partir dessa data o sistema automaticamente colocar\xe1 o banner no site', verbose_name='In\xedcio')),
                ('ativo_fim', models.DateTimeField(help_text='A partir dessa data o sistema automaticamente ir\xe1 retirar o banner do site', null=True, verbose_name='Fim', blank=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Banner',
                'verbose_name_plural': "Banner's",
            },
        ),
        migrations.CreateModel(
            name='Configuracao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ativo', models.BooleanField(default=False, help_text='Somente uma configura\xe7\xe3o estar\xe1 ativa. \xc9 obrigat\xf3rio que haja uma configura\xe7\xe3o ativa para o funcionamento adequado do site', verbose_name='Ativo')),
                ('titulo', models.CharField(help_text='Crie um titulo para ser padr\xe3o do site e utilize, de prefer\xeancia no come\xe7o da frase, a palavra-chave mais importante dessa p\xe1gina. Procure utilizar de 3 a 9 palavras.', max_length=70, verbose_name='T\xedtulo do Site')),
                ('logo', sorl.thumbnail.fields.ImageField(help_text='Insira o logotipo para o cabecalho do site', upload_to=b'images', null=True, verbose_name='Logotipo', blank=True)),
                ('favicon', sorl.thumbnail.fields.ImageField(help_text='\xcdcone do site', upload_to=b'images', null=True, verbose_name='\xcdcone', blank=True)),
                ('subs_ativo', models.BooleanField(default=False, help_text=b'Se ativo ser\xc3\xa1 exibido a janela SUBSCRIBE na p\xc3\xa1gina inicial.', verbose_name=b'Ativo')),
                ('subs_titulo', models.CharField(max_length=150, null=True, verbose_name='T\xedtulo', blank=True)),
                ('subs_texto', models.TextField(null=True, verbose_name=b'Texto', blank=True)),
                ('subs_texto_botao', models.CharField(max_length=20, null=True, verbose_name='Texto do Bot\xe3o', blank=True)),
                ('subs_texto_sucesso', models.CharField(help_text='Texto que ser\xe1 exibido no final, caso o usu\xe1rio assine o newsletter.', max_length=150, null=True, verbose_name=b'Texto Conclu\xc3\xaddo', blank=True)),
                ('subs_texto_inferior', models.CharField(help_text='Acrescenta uma linha de texto na parte inferior da janela com texto reduzido. (ex: uma observa\xe7\xe3o)', max_length=50, null=True, verbose_name=b'Texto Inferior', blank=True)),
                ('subs_animacao', models.CharField(default=b'slide', choices=[(b'slide', b'Slide'), (b'rotatein', 'Rota\xe7\xe3o'), (b'perspectivein', b'Perspectiva'), (b'scalein', b'Escala')], max_length=13, blank=True, help_text='Efeito de Anima\xe7\xe3o que ser\xe1 executado na exibi\xe7\xe3o da janela.', null=True, verbose_name='Efeito de Anima\xe7\xe3o')),
                ('subs_posicao', models.CharField(default=b'centercenter', choices=[(b'lefttop', b'Canto Superior Esquerdo'), (b'leftcenter', b'Centralizado \xc3\xa0 Esquerda'), (b'leftbottom', b'Canto Inferior Esquerdo'), (b'centertop', b'Centralizado no Topo'), (b'centercenter', b'Centralizado ao Meio'), (b'centerbottom', b'Centralizado Abaixo'), (b'righttop', b'Canto Superior Direito'), (b'rightcenter', b'Centralizado \xc3\xa0 Direita'), (b'rightbottom', b'Canto Inferior Direito')], max_length=12, blank=True, help_text='Posi\xe7\xe3o da janela em rela\xe7\xe3o \xe0 p\xe1gina.', null=True, verbose_name='Posi\xe7\xe3o da Janela')),
                ('subs_bgcolor', models.CharField(default=b'#000', max_length=15, blank=True, help_text='Padr\xe3o: #000', null=True, verbose_name='Cor do Fundo')),
                ('subs_buttonbgcolor', models.CharField(default=b'#d71b1b', max_length=15, blank=True, help_text='Padr\xe3o: #d71b1b', null=True, verbose_name='Cor do Bot\xe3o')),
                ('subs_buttoncolor', models.CharField(default=b'#000', max_length=15, blank=True, help_text='Padr\xe3o: #000', null=True, verbose_name='Cor do Texto Bot\xe3o')),
                ('subs_closecolor', models.CharField(default=b'#d71b1b', max_length=15, blank=True, help_text='Padr\xe3o: #d71b1b', null=True, verbose_name='Cor do Bot\xe3o Fechar')),
                ('subs_color', models.CharField(default=b'#ccc', max_length=15, blank=True, help_text='Padr\xe3o: #ccc', null=True, verbose_name='Cor do t\xedtulo')),
                ('subs_contentcolor', models.CharField(default=b'#000', max_length=15, blank=True, help_text='Padr\xe3o: #000', null=True, verbose_name='Cor do Texto')),
                ('subs_imagem', sorl.thumbnail.fields.ImageField(upload_to=b'images', null=True, verbose_name='Imagem', blank=True)),
                ('url_facebook', models.URLField(null=True, verbose_name='Facebook', blank=True)),
                ('url_flicker', models.URLField(null=True, verbose_name='Flicker', blank=True)),
                ('url_twitter', models.URLField(null=True, verbose_name='Twitter', blank=True)),
                ('url_youtube', models.URLField(null=True, verbose_name='Youtube', blank=True)),
                ('url_instagram', models.URLField(null=True, verbose_name='Instagram', blank=True)),
                ('email', models.EmailField(help_text='Email que receber\xe1 c\xf3pia dos formul\xe1rios enviados pelo site.', max_length=200, null=True, verbose_name='Email Principal', blank=True)),
                ('telefone', models.CharField(max_length=15, verbose_name='Telefone Comercial')),
                ('cep', models.CharField(max_length=10, null=True, verbose_name='CEP', blank=True)),
                ('endereco', models.CharField(max_length=100, verbose_name='Endere\xe7o')),
                ('numero', models.CharField(max_length=5, verbose_name='N\xfamero')),
                ('bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                ('cidade', models.CharField(max_length=100, verbose_name='Cidade')),
                ('uf', models.CharField(max_length=2, verbose_name='Estado')),
                ('sobre_drm', models.TextField(null=True, verbose_name=b'Sobre DRM', blank=True)),
                ('meta_description', models.CharField(help_text='Resumo geral do site. Frase que descreva muito bem o site. Quando o site for buscado, essa ser\xe1 a frase que aparecer\xe1 \xe0 quem buscar. Melhor utilizar de 25 a 30 palavras com 160 a 180 caracteres.', max_length=160, null=True, verbose_name='Meta Description', blank=True)),
                ('meta_keywords', models.CharField(help_text='Procure usar umas poucas palavras que descrevam o conte\xfado do site. Exemplo: clim\xe1tica, previs\xe3o clim\xe1tica,desenvolvimento, tempo, clima. \xc9 importante que as palavras estejam no T\xedtulo e nas Meta Description.', max_length=100, null=True, verbose_name='Meta Keywords', blank=True)),
                ('meta_geo_position', models.CharField(help_text='Coordenada de Localiza\xe7\xe3o - Utilizado geralmente o local do escrit\xf3rio. Ex: -13.85089,-40.0877', max_length=20, null=True, verbose_name='Meta Geo Position', blank=True)),
                ('meta_geo_place', models.CharField(help_text='Localiza\xe7\xe3o Geogr\xe1fica - Utilizado geralmente o local do escrit\xf3rio. Ex: Campinas, S\xe3o Paulo', max_length=40, null=True, verbose_name='Meta Geo Placename', blank=True)),
                ('meta_geo_region', models.CharField(help_text='C\xf3digo da regi\xe3o geogr\xe1fica (Sigla do P\xe1is e do estado). Ex: BR-MG', max_length=5, null=True, verbose_name='Meta Geo Region', blank=True)),
            ],
            options={
                'verbose_name': 'Configura\xe7\xe3o',
                'verbose_name_plural': 'Configura\xe7\xf5es',
            },
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100, verbose_name='T\xedtulo')),
                ('telefone', models.CharField(max_length=15, null=True, verbose_name='Telefone Comercial', blank=True)),
                ('mapa', models.TextField(help_text='C\xf3digo HTML do Google Maps.', null=True, verbose_name='Mapa Embutido', blank=True)),
                ('cep', models.CharField(max_length=10, null=True, verbose_name='CEP', blank=True)),
                ('endereco', models.CharField(max_length=100, verbose_name='Endere\xe7o')),
                ('bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                ('numero', models.CharField(max_length=5, verbose_name='N\xfamero')),
                ('complemento', models.CharField(max_length=100, null=True, verbose_name='Complemento', blank=True)),
                ('cidade', models.CharField(max_length=100, verbose_name='Cidade')),
                ('uf', models.CharField(max_length=2, verbose_name='Estado')),
                ('configuracao', models.ForeignKey(related_name='endereco+', verbose_name='Endere\xe7os', to='website.Configuracao')),
            ],
            options={
                'verbose_name': 'Endere\xe7o',
                'verbose_name_plural': 'Endere\xe7os',
            },
        ),
        migrations.CreateModel(
            name='Imagem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagem', sorl.thumbnail.fields.ImageField(upload_to=b'img_site/', verbose_name='Imagem')),
                ('configuracao', models.ForeignKey(verbose_name='Configura\xe7\xe3o', blank=True, to='website.Configuracao', null=True)),
            ],
            options={
                'verbose_name_plural': 'Imagens',
            },
        ),
        migrations.CreateModel(
            name='Institucional',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50, verbose_name='T\xedtulo')),
                ('conteudo', models.TextField(verbose_name='Conte\xfado')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('slug', models.SlugField(max_length=150, editable=False)),
                ('order', models.PositiveIntegerField(verbose_name='Ordem')),
                ('meta_description', models.CharField(help_text='Resumo geral do site. Frase que descreva muito bem o Institucional. Quando o site for buscado, essa ser\xe1 a frase que aparecer\xe1 \xe0 quem buscar. Melhor utilizar de 25 a 30 palavras com 160 a 180 caracteres.', max_length=160, null=True, verbose_name='Meta Description', blank=True)),
                ('meta_keywords', models.CharField(help_text='Procure usar umas poucas palavras que descrevam o conte\xfado da Not\xedcia. Exemplo: clim\xe1tica, previs\xe3o clim\xe1tica,desenvolvimento, tempo, clima. \xc9 importante que as palavras estejam no T\xedtulo e nas Meta Description.', max_length=100, null=True, verbose_name='Meta Keywords', blank=True)),
                ('configuracao', models.ForeignKey(verbose_name='Configura\xe7\xe3o', to='website.Configuracao')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Institucional',
                'verbose_name_plural': 'Institucionais',
            },
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200, verbose_name='T\xedtulo')),
                ('conteudo', models.TextField(verbose_name='Conte\xfado')),
                ('ativo_inicio', models.DateTimeField(default=django.utils.timezone.now, help_text='A partir dessa data o sistema automaticamente exibi a Not\xedcia nosite', verbose_name='In\xedcio')),
                ('ativo_fim', models.DateTimeField(help_text='A partir dessa data o sistema automaticamente remove a Not\xedcia do site', null=True, verbose_name='Fim', blank=True)),
                ('slug', models.SlugField(max_length=150, editable=False)),
                ('meta_description', models.CharField(help_text='Resumo geral da. Frase que descreva muito bem a not\xedcia. Quando o site for buscado, essa ser\xe1 a frase que aparecer\xe1 \xe0 quem buscar. Melhor utilizar de 25 a 30 palavras com 160 a 180 caracteres.', max_length=160, null=True, verbose_name='Meta Description', blank=True)),
                ('meta_keywords', models.CharField(help_text='Procure usar umas poucas palavras que descrevam o conte\xfado da Not\xedcia. Exemplo: clim\xe1tica, previs\xe3o clim\xe1tica,desenvolvimento, tempo clima. \xc9 importante que as palavras estejam no T\xedtulo e nas Meta Description.', max_length=100, null=True, verbose_name='Meta Keywords', blank=True)),
                ('configuracao', models.ForeignKey(verbose_name='Configura\xe7\xe3o', to='website.Configuracao')),
            ],
            options={
                'ordering': ['-ativo_inicio'],
            },
        ),
        migrations.CreateModel(
            name='NoticiaLida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.IPAddressField()),
                ('noticia', models.ForeignKey(to='website.Noticia')),
            ],
        ),
        migrations.CreateModel(
            name='PacoteDesconto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qtda', models.SmallIntegerField(verbose_name=b'Quantidade')),
                ('desconto', models.DecimalField(help_text=b'Percentual do Desconto', verbose_name=b'Desconto', max_digits=5, decimal_places=2)),
                ('configuracao', models.ForeignKey(verbose_name='Configura\xe7\xe3o', to='website.Configuracao')),
            ],
            options={
                'ordering': ['qtda'],
            },
        ),
        migrations.CreateModel(
            name='VideoJusTutor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200, verbose_name='T\xedtulo')),
                ('descricao', models.TextField(null=True, verbose_name='Apresenta\xe7\xe3o', blank=True)),
                ('data_ini', models.DateTimeField(default=django.utils.timezone.now, help_text='A partir dessa data o sistema automaticamente colocar\xe1 o v\xeddeo no site', null=True, verbose_name='Data \xednicio', blank=True)),
                ('video', models.URLField(verbose_name='V\xeddeo URL')),
            ],
            options={
                'ordering': ['-data_ini'],
                'verbose_name': 'V\xeddeo JusTutor',
                'verbose_name_plural': 'V\xeddeos JusTutor',
            },
        ),
        migrations.AddField(
            model_name='configuracao',
            name='regulamento_premios',
            field=models.ForeignKey(related_name='get_institucional', blank=True, to='website.Institucional', help_text='Regulamento para concorrer a pr\xeamios', null=True, verbose_name='Regulamento Pr\xeamios'),
        ),
        migrations.AddField(
            model_name='configuracao',
            name='regulamento_sentenca_avulsa',
            field=models.ForeignKey(related_name='get_institucional_set', blank=True, to='website.Institucional', help_text='Regulamento para concorrer a pr\xeamios', null=True, verbose_name='Regulamento Atividade Avulsa'),
        ),
        migrations.AddField(
            model_name='banner',
            name='configuracao',
            field=models.ForeignKey(default=1, verbose_name='Configura\xe7\xe3o', to='website.Configuracao'),
        ),
        migrations.AddField(
            model_name='artigo',
            name='indice',
            field=mptt.fields.TreeForeignKey(verbose_name='\xcdndice', to='website.ArtigoIndice'),
        ),
        migrations.AddField(
            model_name='anuncio',
            name='configuracao',
            field=models.ForeignKey(default=1, verbose_name='Configura\xe7\xe3o', to='website.Configuracao'),
        ),
        migrations.AlterUniqueTogether(
            name='noticialida',
            unique_together=set([('noticia', 'ip')]),
        ),
        migrations.AlterUniqueTogether(
            name='configuracao',
            unique_together=set([('ativo',)]),
        ),
    ]
