# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings
import smart_selects.db_fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enunciado', '0001_initial'),
        ('aluno', '0002_auto_20200807_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('data_criacao', models.DateTimeField(verbose_name='Data de cria\xe7\xe3os')),
                ('data_conclusao', models.DateTimeField(verbose_name='Data de conclus\xe3o')),
            ],
            options={
                'db_table': 'resultado',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ResultadoResposta',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('numeracao', models.SmallIntegerField()),
                ('codigo', models.CharField(max_length=10)),
                ('anulada', models.BooleanField()),
                ('em_branco', models.BooleanField()),
                ('acertou', models.BooleanField()),
                ('errou', models.BooleanField()),
                ('correta', models.BooleanField()),
                ('pontuacao', models.IntegerField()),
                ('disciplina_peso', models.SmallIntegerField()),
                ('disciplina_nota_minima', models.FloatField()),
            ],
            options={
                'db_table': 'resultado_resposta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssuntoEspecifico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
            ],
            options={
                'ordering': ['assunto_geral', 'nome'],
                'verbose_name': 'Assunto Espec\xedfico',
                'verbose_name_plural': 'Assuntos Espec\xedficos',
            },
        ),
        migrations.CreateModel(
            name='AssuntoGeral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Disciplina', to='enunciado.Disciplina')),
            ],
            options={
                'ordering': ['disciplina', 'nome'],
                'verbose_name': 'Assunto Geral',
                'verbose_name_plural': 'Assuntos Gerais',
            },
        ),
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text='Nome completo', max_length=200, verbose_name='Nome')),
                ('cpf', models.CharField(max_length=14, null=True, verbose_name='C.P.F', blank=True)),
                ('rg', models.CharField(max_length=50, null=True, verbose_name='RG', blank=True)),
                ('rg_orgao', models.CharField(max_length=50, null=True, verbose_name='Org\xe3o Expedidor', blank=True)),
                ('pis', models.CharField(max_length=50, null=True, verbose_name='PIS/PASEP', blank=True)),
                ('data_nascimento', models.DateField(null=True, verbose_name='Data Nascimento', blank=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='E-Mail')),
                ('foto', sorl.thumbnail.fields.ImageField(help_text='Foto do perfil.', upload_to='profile/corretor/', null=True, verbose_name='Foto', blank=True)),
                ('ddd_telefone', models.CharField(blank=True, max_length=2, null=True, verbose_name='DDD', choices=[(b'11', b'(11) S\xc3\xa3o Paulo'), (b'12', b'(12) S\xc3\xa3o Paulo'), (b'13', b'(13) S\xc3\xa3o Paulo'), (b'14', b'(14) S\xc3\xa3o Paulo'), (b'15', b'(15) S\xc3\xa3o Paulo'), (b'16', b'(16) S\xc3\xa3o Paulo'), (b'17', b'(17) S\xc3\xa3o Paulo'), (b'18', b'(18) S\xc3\xa3o Paulo'), (b'19', b'(19) S\xc3\xa3o Paulo'), (b'21', b'(21) Rio de Janeiro'), (b'22', b'(22) Rio de Janeiro'), (b'24', b'(24) Rio de Janeiro'), (b'27', b'(27) Esp\xc3\xadrito Santo'), (b'28', b'(28) Esp\xc3\xadrito Santo'), (b'31', b'(31) Minas Gerais'), (b'32', b'(32) Minas Gerais'), (b'33', b'(33) Minas Gerais'), (b'34', b'(34) Minas Gerais'), (b'35', b'(35) Minas Gerais'), (b'37', b'(37) Minas Gerais'), (b'38', b'(38) Minas Gerais'), (b'41', b'(41) Paran\xc3\xa1'), (b'42', b'(42) Paran\xc3\xa1'), (b'43', b'(43) Paran\xc3\xa1'), (b'44', b'(44) Paran\xc3\xa1'), (b'45', b'(45) Paran\xc3\xa1'), (b'46', b'(46) Paran\xc3\xa1'), (b'47', b'(47) Santa Catarina'), (b'48', b'(48) Santa Catarina'), (b'49', b'(49) Santa Catarina'), (b'51', b'(51) Rio Grande do Sul'), (b'53', b'(53) Rio Grande do Sul'), (b'54', b'(54) Rio Grande do Sul'), (b'55', b'(55) Rio Grande do Sul'), (b'61', b'(61) Distrito Federal e Goi\xc3\xa1s'), (b'62', b'(62) Goi\xc3\xa1s'), (b'63', b'(63) Tocantins'), (b'64', b'(64) Goi\xc3\xa1s'), (b'65', b'(65) Mato Grosso'), (b'66', b'(66) Mato Grosso'), (b'67', b'(67) Mato Grosso do Sul'), (b'68', b'(68) Acre'), (b'69', b'(69) Rond\xc3\xb4nia'), (b'71', b'(71) Bahia'), (b'73', b'(73) Bahia'), (b'74', b'(74) Bahia'), (b'75', b'(75) Bahia'), (b'77', b'(77) Bahia'), (b'79', b'(79) Sergipe'), (b'81', b'(81) Pernambuco'), (b'82', b'(82) Alagoas'), (b'83', b'(83) Para\xc3\xadba'), (b'84', b'(84) Rio Grande do Norte'), (b'85', b'(85) Cear\xc3\xa1'), (b'86', b'(86) Piau\xc3\xad'), (b'87', b'(87) Pernambuco'), (b'88', b'(88) Cear\xc3\xa1'), (b'89', b'(89) Piau\xc3\xad'), (b'91', b'(91) Par\xc3\xa1'), (b'92', b'(92) Amazonas'), (b'93', b'(93) Par\xc3\xa1'), (b'94', b'(94) Par\xc3\xa1'), (b'95', b'(95) Roraima'), (b'96', b'(96) Amap\xc3\xa1'), (b'97', b'(97) Amazonas'), (b'98', b'(98) Maranh\xc3\xa3o'), (b'99', b'(99) Maranh\xc3\xa3o')])),
                ('telefone', models.CharField(max_length=9, null=True, verbose_name='Telefone', blank=True)),
                ('ddd_celular', models.CharField(blank=True, max_length=2, null=True, verbose_name='DDD', choices=[(b'11', b'(11) S\xc3\xa3o Paulo'), (b'12', b'(12) S\xc3\xa3o Paulo'), (b'13', b'(13) S\xc3\xa3o Paulo'), (b'14', b'(14) S\xc3\xa3o Paulo'), (b'15', b'(15) S\xc3\xa3o Paulo'), (b'16', b'(16) S\xc3\xa3o Paulo'), (b'17', b'(17) S\xc3\xa3o Paulo'), (b'18', b'(18) S\xc3\xa3o Paulo'), (b'19', b'(19) S\xc3\xa3o Paulo'), (b'21', b'(21) Rio de Janeiro'), (b'22', b'(22) Rio de Janeiro'), (b'24', b'(24) Rio de Janeiro'), (b'27', b'(27) Esp\xc3\xadrito Santo'), (b'28', b'(28) Esp\xc3\xadrito Santo'), (b'31', b'(31) Minas Gerais'), (b'32', b'(32) Minas Gerais'), (b'33', b'(33) Minas Gerais'), (b'34', b'(34) Minas Gerais'), (b'35', b'(35) Minas Gerais'), (b'37', b'(37) Minas Gerais'), (b'38', b'(38) Minas Gerais'), (b'41', b'(41) Paran\xc3\xa1'), (b'42', b'(42) Paran\xc3\xa1'), (b'43', b'(43) Paran\xc3\xa1'), (b'44', b'(44) Paran\xc3\xa1'), (b'45', b'(45) Paran\xc3\xa1'), (b'46', b'(46) Paran\xc3\xa1'), (b'47', b'(47) Santa Catarina'), (b'48', b'(48) Santa Catarina'), (b'49', b'(49) Santa Catarina'), (b'51', b'(51) Rio Grande do Sul'), (b'53', b'(53) Rio Grande do Sul'), (b'54', b'(54) Rio Grande do Sul'), (b'55', b'(55) Rio Grande do Sul'), (b'61', b'(61) Distrito Federal e Goi\xc3\xa1s'), (b'62', b'(62) Goi\xc3\xa1s'), (b'63', b'(63) Tocantins'), (b'64', b'(64) Goi\xc3\xa1s'), (b'65', b'(65) Mato Grosso'), (b'66', b'(66) Mato Grosso'), (b'67', b'(67) Mato Grosso do Sul'), (b'68', b'(68) Acre'), (b'69', b'(69) Rond\xc3\xb4nia'), (b'71', b'(71) Bahia'), (b'73', b'(73) Bahia'), (b'74', b'(74) Bahia'), (b'75', b'(75) Bahia'), (b'77', b'(77) Bahia'), (b'79', b'(79) Sergipe'), (b'81', b'(81) Pernambuco'), (b'82', b'(82) Alagoas'), (b'83', b'(83) Para\xc3\xadba'), (b'84', b'(84) Rio Grande do Norte'), (b'85', b'(85) Cear\xc3\xa1'), (b'86', b'(86) Piau\xc3\xad'), (b'87', b'(87) Pernambuco'), (b'88', b'(88) Cear\xc3\xa1'), (b'89', b'(89) Piau\xc3\xad'), (b'91', b'(91) Par\xc3\xa1'), (b'92', b'(92) Amazonas'), (b'93', b'(93) Par\xc3\xa1'), (b'94', b'(94) Par\xc3\xa1'), (b'95', b'(95) Roraima'), (b'96', b'(96) Amap\xc3\xa1'), (b'97', b'(97) Amazonas'), (b'98', b'(98) Maranh\xc3\xa3o'), (b'99', b'(99) Maranh\xc3\xa3o')])),
                ('celular', models.CharField(max_length=9, null=True, verbose_name='Celular', blank=True)),
                ('cep', models.CharField(max_length=10, null=True, verbose_name='CEP', blank=True)),
                ('logradouro', models.CharField(max_length=100, null=True, verbose_name='Logradouro', blank=True)),
                ('bairro', models.CharField(max_length=100, null=True, verbose_name='Bairro', blank=True)),
                ('numero', models.CharField(max_length=5, null=True, verbose_name='N\xfamero', blank=True)),
                ('complemento', models.CharField(max_length=100, null=True, verbose_name='Complemento', blank=True)),
                ('cidade', models.CharField(max_length=100, null=True, verbose_name='Cidade', blank=True)),
                ('uf', models.CharField(blank=True, max_length=2, null=True, verbose_name='Estado', choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amap\xe1'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Cear\xe1'), ('DF', 'Distrito Federal'), ('ES', 'Esp\xedrito Santo'), ('GO', 'Goi\xe1s'), ('MA', 'Maranh\xe3o'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Par\xe1'), ('PB', 'Para\xedba'), ('PR', 'Paran\xe1'), ('PE', 'Pernambuco'), ('PI', 'Piau\xed'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rond\xf4nia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'S\xe3o Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')])),
                ('tipo_recebimento', models.CharField(default='F', choices=[('F', 'F\xedsica'), ('J', 'Juridica')], max_length=1, blank=True, null=True, verbose_name='Tipo Recebimento')),
                ('cnpj', models.CharField(max_length=14, null=True, verbose_name='CNPJ', blank=True)),
                ('endereco', models.TextField(null=True, verbose_name='Endere\xe7o', blank=True)),
                ('user', models.OneToOneField(related_name='autor', verbose_name='Usu\xe1rio', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Autor',
                'verbose_name_plural': 'Autores',
            },
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banco_tipo_conta', models.CharField(blank=True, max_length=1, null=True, verbose_name='Tipo Conta', choices=[('C', 'Corrente'), ('P', 'Poupan\xe7a')])),
                ('banco', models.CharField(help_text='Ex: Banco do Brasil', max_length=150, verbose_name='Banco')),
                ('codigo', models.CharField(max_length=5, verbose_name='C\xf3digo')),
                ('agencia', models.CharField(max_length=40, verbose_name='Ag\xeancia')),
                ('conta', models.CharField(max_length=40, verbose_name='Conta')),
                ('autor', models.ForeignKey(verbose_name='Correto', to='autor.Autor')),
            ],
        ),
        migrations.CreateModel(
            name='DisciplinaConcurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200, verbose_name='T\xedtulo')),
                ('disciplinas', models.ManyToManyField(to='enunciado.Disciplina', verbose_name='Disciplinas JusTutor')),
            ],
        ),
        migrations.CreateModel(
            name='DisciplinaGrupo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('peso', models.PositiveSmallIntegerField(verbose_name='Peso')),
                ('nota_minima', models.FloatField(default=0, help_text='Porcentagem', verbose_name='Nota m\xednima', validators=[django.core.validators.MaxValueValidator(100)])),
                ('disciplina', models.ForeignKey(related_name='disciplinas_grupos', verbose_name='Disciplina', to='autor.DisciplinaConcurso')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Estatistica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('porcentagem_acertos', models.FloatField(default=0, verbose_name='Acertos (%)')),
                ('aprovado', models.BooleanField(verbose_name='Aprovado')),
            ],
        ),
        migrations.CreateModel(
            name='EstatisticaDisciplina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('porcentagem_acertos', models.FloatField(default=0, verbose_name='Acertos (%)')),
                ('aprovado', models.BooleanField(verbose_name='Aprovado')),
                ('disciplina_grupo', models.ForeignKey(verbose_name='Disciplina Grupo', to='autor.DisciplinaGrupo')),
                ('estatistica', models.ForeignKey(verbose_name='Estatistica', to='autor.Estatistica')),
            ],
        ),
        migrations.CreateModel(
            name='GrupoDoSimulado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='GrupoSimulado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('nome', models.CharField(max_length=200, verbose_name='T\xedtulo')),
                ('nota_minima', models.FloatField(default=0, help_text='Porcentagem', verbose_name='Nota m\xednima', validators=[django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=10, verbose_name='C\xf3digo', blank=True)),
                ('data_criacao', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data de cria\xe7\xe3os')),
                ('tipo', models.CharField(default='C', max_length=1, verbose_name='Tipo', choices=[('C', 'Certo/Errado'), ('M', 'M\xfatipla Escolha')])),
                ('nivel', models.CharField(default='F', max_length=1, verbose_name='N\xedvel', choices=[('F', 'F\xe1cil'), ('M', 'M\xe9dio'), ('D', 'Dificil')])),
                ('correta', models.BooleanField(default=False, help_text="Usado para quest\xf5es de 'Certo/Errado'.", verbose_name='Correta')),
                ('enunciado', models.TextField(verbose_name='Enunciado')),
                ('comentario', models.TextField(null=True, verbose_name='Coment\xe1rio', blank=True)),
                ('situacao', models.CharField(default='E', max_length=1, verbose_name='Situa\xe7\xe3o', choices=[('E', 'Em Elabora\xe7\xe3o'), ('A', 'Aguardando Aprova\xe7\xe3o'), ('H', 'Habilitada'), ('D', 'Desabilitada'), ('N', 'Anulada'), ('R', 'Reabilitada ap\xf3s anula\xe7\xe3o')])),
                ('situacao_financeira', models.CharField(default='P', max_length=1, verbose_name='Situa\xe7\xe3o Financeira', choices=[('P', 'Pendente de Pagamento'), ('A', 'Paga'), ('S', 'Sem Custo')])),
                ('data_pagamento', models.DateField(null=True, verbose_name='Data de Pagamento', blank=True)),
                ('assunto_especifico', smart_selects.db_fields.ChainedForeignKey(chained_model_field='assunto_geral', related_name='questoes_assuntos_especificos', chained_field='assunto_geral', verbose_name='Assunto Espec\xedfico', blank=True, to='autor.AssuntoEspecifico', null=True)),
                ('assunto_geral', smart_selects.db_fields.ChainedForeignKey(chained_model_field='disciplina', related_name='questoes_assuntos_gerais', chained_field='disciplina', verbose_name='Assunto Geral', to='autor.AssuntoGeral')),
                ('autor', models.ForeignKey(related_name='questoe_autor', verbose_name='Autor', blank=True, to='autor.Autor', null=True)),
                ('disciplina', models.ForeignKey(related_name='questoes', verbose_name='Disciplina', to='enunciado.Disciplina')),
                ('user', models.ForeignKey(related_name='questao_users', verbose_name='Usu\xe1rio', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'autor_questaoc',
                'verbose_name': 'Todas',
                'verbose_name_plural': 'Todas',
            },
        ),
        migrations.CreateModel(
            name='QuestaoEscolha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField(help_text='Digite aqui o texto da alternativa', verbose_name='Texto da Alternativa')),
                ('comentario', models.TextField(help_text='Digite aqui o coment\xe1rio do(a) autor(a) sobre a alternativa', null=True, verbose_name='Coment\xe1rio', blank=True)),
                ('correta', models.BooleanField(default=False, verbose_name='Correta?')),
                ('order', models.PositiveIntegerField(verbose_name='Ordem')),
                ('questao', models.ForeignKey(related_name='escolhas', verbose_name='Quest\xe3o', to='autor.Questao')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Escolha',
                'verbose_name_plural': 'Escolhas',
            },
        ),
        migrations.CreateModel(
            name='QuestaoGrupo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numeracao', models.PositiveSmallIntegerField(default=0, verbose_name='Numera\xe7\xe3o')),
                ('disciplina_grupo', models.ForeignKey(related_name='questoes', to='autor.DisciplinaGrupo')),
                ('questao', models.ForeignKey(related_name='questoes_grupo', verbose_name='Quest\xe3o', to='autor.Questao')),
            ],
            options={
                'ordering': ['numeracao'],
            },
        ),
        migrations.CreateModel(
            name='QuestionarioAluno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de cria\xe7\xe3os')),
                ('data_conclusao', models.DateTimeField(null=True, verbose_name='Data de conclus\xe3o', blank=True)),
                ('timer', models.DurationField(default='00:00:00', verbose_name='Timer', editable=False)),
                ('pontuacao', models.PositiveSmallIntegerField(default=0, verbose_name='Pontua\xe7\xe3o')),
                ('status_questionario', models.CharField(default='esboco', max_length=20, verbose_name='Status', choices=[('esboco', 'Esbo\xe7o'), ('iniciado', 'Iniciado'), ('finalizado', 'Finalizado')])),
                ('status_simulado', models.CharField(blank=True, max_length=20, null=True, verbose_name='Status', choices=[('Aguardando', 'Aguardando'), ('Andamento', 'Andamento'), ('Encerrado', 'Encerrado'), ('Indefinido', 'Indefinido')])),
                ('tempo_esgotado', models.BooleanField(default=False, verbose_name='Tempo esgotado')),
                ('confirmar_visualizar_comentario', models.BooleanField(default=True, verbose_name='Visualizar confirma\xe7\xe3o')),
                ('aprovado', models.NullBooleanField(verbose_name='Classificado')),
                ('aluno', models.ForeignKey(related_name='aluno_questionario', verbose_name='Aluno', to='aluno.Aluno')),
            ],
            options={
                'verbose_name': 'Question\xe1rio do Aluno',
                'verbose_name_plural': 'Question\xe1rios do Aluno',
            },
        ),
        migrations.CreateModel(
            name='RespostaQuestionarioAluno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('correta', models.NullBooleanField(verbose_name='Correta')),
                ('questao_anulada', models.NullBooleanField(verbose_name='Anulada')),
                ('respondida', models.BooleanField(default=False, verbose_name='Respondida')),
                ('viu_comentario', models.BooleanField(default=False, verbose_name='Respondida')),
                ('data_criacao', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data de cria\xe7\xe3os')),
                ('questao', models.ForeignKey(related_name='questoes_f', verbose_name='Questao', to='autor.Questao')),
                ('questao_escolha', models.ForeignKey(related_name='questoes_escolha', verbose_name='Quest\xe3o Escolha', blank=True, to='autor.QuestaoEscolha', null=True)),
                ('questao_grupo', models.ForeignKey(related_name='questoes_grupo', verbose_name='Quest\xe3o Grupo', to='autor.QuestaoGrupo')),
                ('questionario_aluno', models.ForeignKey(related_name='respostas_aluno', verbose_name='Question\xe1rio', to='autor.QuestionarioAluno')),
            ],
            options={
                'ordering': ['questao_grupo'],
                'verbose_name': 'Resposta do Question\xe1rio do Aluno',
                'verbose_name_plural': 'Resposta dos Question\xe1rios do Aluno',
            },
        ),
        migrations.CreateModel(
            name='Simulado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200, verbose_name='T\xedtulo')),
                ('tipo', models.CharField(max_length=1, verbose_name='Tipo', choices=[('C', 'Certo/Errado'), ('M', 'M\xfatipla Escolha')])),
                ('data_inicio', models.DateTimeField(verbose_name='Data de in\xedcio')),
                ('data_fim', models.DateTimeField(verbose_name='Data de fim')),
                ('duracao', models.DurationField(help_text='Ex: HH:MM / 3:45', verbose_name='Dura\xe7\xe3o')),
                ('nota_minima', models.FloatField(default=0, help_text='Porcentagem', verbose_name='Nota m\xednima', validators=[django.core.validators.MaxValueValidator(100)])),
                ('data_prova', models.PositiveSmallIntegerField(verbose_name='Data da Prova', choices=[(1989, b'1989'), (1990, b'1990'), (1991, b'1991'), (1992, b'1992'), (1993, b'1993'), (1994, b'1994'), (1995, b'1995'), (1996, b'1996'), (1997, b'1997'), (1998, b'1998'), (1999, b'1999'), (2000, b'2000'), (2001, b'2001'), (2002, b'2002'), (2003, b'2003'), (2004, b'2004'), (2005, b'2005'), (2006, b'2006'), (2007, b'2007'), (2008, b'2008'), (2009, b'2009'), (2010, b'2010'), (2011, b'2011'), (2012, b'2012'), (2013, b'2013'), (2014, b'2014'), (2015, b'2015'), (2016, b'2016'), (2017, b'2017'), (2018, b'2018'), (2019, b'2019'), (2020, b'2020')])),
                ('texto', models.TextField(help_text='Formule um texto para o seu Enunciado.', null=True, verbose_name='Texto', blank=True)),
                ('area_profissional', models.ForeignKey(verbose_name='\xc1rea Profissional', blank=True, to='enunciado.AreaProfissional', null=True)),
                ('cargo', smart_selects.db_fields.ChainedForeignKey(chained_model_field='esfera_especifica', chained_field='esfera_especifica', verbose_name='Cargo', to='enunciado.Cargo', null=True)),
                ('concurso', models.ForeignKey(verbose_name='Concurso', blank=True, to='enunciado.Concurso', null=True)),
                ('esfera_especifica', smart_selects.db_fields.ChainedForeignKey(chained_model_field='esfera_geral', to='enunciado.EsferaEspecifica', chained_field='esfera_geral', verbose_name='Esfera Espec\xedfica')),
                ('esfera_geral', models.ForeignKey(related_name='esferas_gerais_simulado', verbose_name='Esfera Geral', to='enunciado.EsferaGeral')),
                ('localidade', models.ForeignKey(verbose_name='Localidade', to='enunciado.Localidade')),
                ('organizador', models.ForeignKey(verbose_name='Organizador(a)', to='enunciado.Organizador')),
                ('orgao_entidade', models.ForeignKey(verbose_name='\xd3rgao/Entidade', to='enunciado.OrgaoEntidade')),
            ],
        ),
        migrations.AddField(
            model_name='questionarioaluno',
            name='simulado',
            field=models.ForeignKey(related_name='questionarios', verbose_name='Simulado', to='autor.Simulado'),
        ),
        migrations.AddField(
            model_name='grupodosimulado',
            name='grupo',
            field=models.ForeignKey(related_name='gruposs', verbose_name='Grupo', to='autor.GrupoSimulado'),
        ),
        migrations.AddField(
            model_name='grupodosimulado',
            name='simulado',
            field=models.ForeignKey(related_name='grupos', verbose_name='Simulado', to='autor.Simulado'),
        ),
        migrations.AddField(
            model_name='estatistica',
            name='grupo_simulado',
            field=models.ForeignKey(verbose_name='Grupo', to='autor.GrupoSimulado'),
        ),
        migrations.AddField(
            model_name='estatistica',
            name='questionario_aluno',
            field=models.ForeignKey(verbose_name='Question\xe1rio', to='autor.QuestionarioAluno'),
        ),
        migrations.AddField(
            model_name='disciplinagrupo',
            name='grupo_simulado',
            field=models.ForeignKey(related_name='disciplinas', to='autor.GrupoSimulado'),
        ),
        migrations.AddField(
            model_name='assuntoespecifico',
            name='assunto_geral',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field='disciplina', related_name='assuntos_gerais', chained_field='disciplina', verbose_name='Assunto Geral', to='autor.AssuntoGeral'),
        ),
        migrations.AddField(
            model_name='assuntoespecifico',
            name='disciplina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Disciplina', to='enunciado.Disciplina'),
        ),
        migrations.CreateModel(
            name='QuestaoC',
            fields=[
            ],
            options={
                'verbose_name': 'Certo ou Errado',
                'proxy': True,
                'verbose_name_plural': 'Certas ou Erradas',
            },
            bases=('autor.questao',),
        ),
        migrations.CreateModel(
            name='QuestaoM',
            fields=[
            ],
            options={
                'verbose_name': 'M\xfatipla Escolha',
                'proxy': True,
                'verbose_name_plural': 'M\xfatiplas Escolhas',
            },
            bases=('autor.questao',),
        ),
        migrations.AlterUniqueTogether(
            name='questaogrupo',
            unique_together=set([('questao', 'disciplina_grupo')]),
        ),
        migrations.AlterUniqueTogether(
            name='grupodosimulado',
            unique_together=set([('simulado', 'grupo')]),
        ),
        migrations.AlterUniqueTogether(
            name='estatisticadisciplina',
            unique_together=set([('estatistica', 'disciplina_grupo')]),
        ),
        migrations.AlterUniqueTogether(
            name='estatistica',
            unique_together=set([('questionario_aluno', 'grupo_simulado')]),
        ),
        migrations.AlterUniqueTogether(
            name='disciplinagrupo',
            unique_together=set([('disciplina', 'grupo_simulado')]),
        ),
        migrations.AlterUniqueTogether(
            name='assuntogeral',
            unique_together=set([('disciplina', 'nome')]),
        ),
        migrations.AlterUniqueTogether(
            name='assuntoespecifico',
            unique_together=set([('disciplina', 'assunto_geral', 'nome')]),
        ),
    ]
