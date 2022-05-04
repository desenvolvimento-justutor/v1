# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sexo', models.CharField(max_length=1, verbose_name='Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino')])),
                ('nome', models.CharField(max_length=150, verbose_name='Apelido')),
                ('nome_completo', models.CharField(max_length=150, verbose_name='Nome Completo')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='e-Mail')),
                ('email_publico', models.BooleanField(default=False, verbose_name='Tornar e-mail p\xfablico')),
                ('cargo', models.CharField(max_length=80, null=True, verbose_name='Ocupa\xe7\xe3o atual', blank=True)),
                ('frase', models.CharField(help_text='Diga algo sobre voc\xea para a comunidade JusTutor', max_length=140, null=True, verbose_name='Frase', blank=True)),
                ('url_facebook', models.URLField(null=True, verbose_name='Facebook', blank=True)),
                ('url_flicker', models.URLField(null=True, verbose_name='Flicker', blank=True)),
                ('url_twitter', models.URLField(null=True, verbose_name='Twitter', blank=True)),
                ('url_instagram', models.URLField(null=True, verbose_name='Instagram', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(help_text='Foto do perfil.', upload_to='profile/', null=True, verbose_name='Foto', blank=True)),
                ('cpf', models.CharField(max_length=14, null=True, verbose_name='C.P.F', blank=True)),
                ('rg', models.CharField(max_length=50, null=True, verbose_name='RG', blank=True)),
                ('cep', models.CharField(max_length=10, null=True, verbose_name='CEP', blank=True)),
                ('logradouro', models.CharField(max_length=100, null=True, verbose_name='Logradouro', blank=True)),
                ('bairro', models.CharField(max_length=100, null=True, verbose_name='Bairro', blank=True)),
                ('numero', models.CharField(max_length=5, null=True, verbose_name='N\xfamero', blank=True)),
                ('complemento', models.CharField(max_length=100, null=True, verbose_name='Complemento', blank=True)),
                ('cidade', models.CharField(max_length=100, null=True, verbose_name='Cidade', blank=True)),
                ('uf', models.CharField(blank=True, max_length=2, null=True, verbose_name='Estado', choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amap\xe1'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Cear\xe1'), ('DF', 'Distrito Federal'), ('ES', 'Esp\xedrito Santo'), ('GO', 'Goi\xe1s'), ('MA', 'Maranh\xe3o'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Par\xe1'), ('PB', 'Para\xedba'), ('PR', 'Paran\xe1'), ('PE', 'Pernambuco'), ('PI', 'Piau\xed'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rond\xf4nia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'S\xe3o Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')])),
                ('telefone', models.CharField(max_length=15, null=True, verbose_name='Telefone', blank=True)),
                ('celular', models.CharField(max_length=15, null=True, verbose_name='Celular', blank=True)),
                ('newsletter', models.BooleanField(default=False, help_text='Receber no e-mail novidades, not\xedcias e promo\xe7\xf5es especiais.', verbose_name='Newsletter')),
                ('termo', models.BooleanField(default=False, help_text='Se o Aluno concordou com os Termo e Pol\xedtica de Privacidade do Site.', verbose_name='Aceitou termo de uso?')),
                ('data_cadastro', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data do Cadastro')),
                ('notificar_correcao', models.BooleanField(default=True, help_text='Receber E-mail quando um aluno Corrigir sua Resposta?', verbose_name='Notificar Corre\xe7\xe3o')),
                ('notificar_comentario', models.BooleanField(default=True, help_text='Receber E-mail quando um aluno Comentar sua Corre\xe7\xe3o?', verbose_name='Notificar Coment\xe1rios')),
                ('notificar_avaliacao', models.BooleanField(default=True, help_text='Receber E-mail quando um aluno Curtir sua Corre\xe7\xe3o?', verbose_name='Notificar Avalia\xe7\xe3o')),
                ('notificar_seguir', models.BooleanField(default=True, help_text='Receber E-mail quando um aluno come\xe7ar a te seguir?', verbose_name='Notificar ao ser seguido')),
                ('notificar_responder_seguir', models.BooleanField(default=True, help_text='Receber e-mail toda vez que outro(a) aluno(a) que eu sigo responder uma quest\xe3o?', verbose_name='Notificar ao aluno responder')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Filtro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=100, verbose_name='Nome')),
                ('data_prova', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Data da Prova', choices=[(2000, b'2000'), (2001, b'2001'), (2002, b'2002'), (2003, b'2003'), (2004, b'2004'), (2005, b'2005'), (2006, b'2006'), (2007, b'2007'), (2008, b'2008'), (2009, b'2009'), (2010, b'2010'), (2011, b'2011'), (2012, b'2012'), (2013, b'2013'), (2014, b'2014'), (2015, b'2015'), (2016, b'2016'), (2017, b'2017'), (2018, b'2018'), (2019, b'2019'), (2020, b'2020')])),
                ('num_questao_caderno', models.PositiveSmallIntegerField(null=True, verbose_name='Numero da Quest\xe3o', blank=True)),
                ('texto', models.CharField(max_length=100, null=True, verbose_name='Texto', blank=True)),
                ('aluno', models.ForeignKey(verbose_name='Aluno', to='aluno.Aluno')),
            ],
        ),
        migrations.CreateModel(
            name='FormacaoAcademica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instituicao', models.CharField(max_length=100, verbose_name='Institui\xe7\xe3o')),
                ('ano_inicio', models.PositiveIntegerField(help_text='Ano de in\xedcio', null=True, verbose_name='In\xedcio', blank=True)),
                ('ano_termino', models.PositiveIntegerField(help_text='Ano de T\xe9rmino ou Previs\xe3o de Gradua\xe7\xe3o', null=True, verbose_name='Termino', blank=True)),
                ('formacao', models.CharField(max_length=100, null=True, verbose_name='Forma\xe7\xe3o', blank=True)),
                ('aluno', models.ForeignKey(verbose_name='Aluno', to='aluno.Aluno')),
            ],
            options={
                'verbose_name': 'Forma\xe7\xf5es Acad\xeamicas',
            },
        ),
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mensagem', models.TextField(verbose_name='Mensagem')),
                ('lido', models.BooleanField(default=False)),
                ('data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data')),
                ('de_aluno', models.ForeignKey(related_name='mensagem_dealuno', verbose_name='De', to='aluno.Aluno', help_text='Aluno que enviou a mensagem.')),
                ('para_aluno', models.ForeignKey(related_name='mensagem_paraaluno', verbose_name='Para', to='aluno.Aluno', help_text='Aluno que recebeu a mensagem.')),
            ],
            options={
                'ordering': ['-data'],
            },
        ),
        migrations.CreateModel(
            name='Seguir',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('de_aluno', models.ForeignKey(related_name='get_seguindo', verbose_name='De', to='aluno.Aluno')),
                ('para_aluno', models.ForeignKey(related_name='get_seguidores', verbose_name='Para', to='aluno.Aluno')),
            ],
        ),
    ]
