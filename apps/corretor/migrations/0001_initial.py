# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enunciado', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banco', models.CharField(help_text='Ex: Banco do Brasil', max_length=150, verbose_name='Banco')),
                ('codigo', models.CharField(max_length=5, verbose_name='C\xf3digo')),
                ('agencia', models.CharField(max_length=40, verbose_name='Ag\xeancia')),
                ('conta', models.CharField(max_length=40, verbose_name='Conta')),
            ],
        ),
        migrations.CreateModel(
            name='Corretor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text='Nome completo', max_length=200, verbose_name='Nome')),
                ('cpf', models.CharField(max_length=14, null=True, verbose_name='C.P.F', blank=True)),
                ('rg', models.CharField(max_length=50, null=True, verbose_name='RG', blank=True)),
                ('pis', models.CharField(max_length=50, null=True, verbose_name='PIS/PASEP', blank=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='E-Mail')),
                ('foto', sorl.thumbnail.fields.ImageField(help_text='Foto do perfil.', upload_to='profile/corretor/', null=True, verbose_name='Foto', blank=True)),
                ('ddd_telefone', models.CharField(blank=True, max_length=2, null=True, verbose_name='DDD', choices=[(b'11', b'(11) S\xc3\xa3o Paulo'), (b'12', b'(12) S\xc3\xa3o Paulo'), (b'13', b'(13) S\xc3\xa3o Paulo'), (b'14', b'(14) S\xc3\xa3o Paulo'), (b'15', b'(15) S\xc3\xa3o Paulo'), (b'16', b'(16) S\xc3\xa3o Paulo'), (b'17', b'(17) S\xc3\xa3o Paulo'), (b'18', b'(18) S\xc3\xa3o Paulo'), (b'19', b'(19) S\xc3\xa3o Paulo'), (b'21', b'(21) Rio de Janeiro'), (b'22', b'(22) Rio de Janeiro'), (b'24', b'(24) Rio de Janeiro'), (b'27', b'(27) Esp\xc3\xadrito Santo'), (b'28', b'(28) Esp\xc3\xadrito Santo'), (b'31', b'(31) Minas Gerais'), (b'32', b'(32) Minas Gerais'), (b'33', b'(33) Minas Gerais'), (b'34', b'(34) Minas Gerais'), (b'35', b'(35) Minas Gerais'), (b'37', b'(37) Minas Gerais'), (b'38', b'(38) Minas Gerais'), (b'41', b'(41) Paran\xc3\xa1'), (b'42', b'(42) Paran\xc3\xa1'), (b'43', b'(43) Paran\xc3\xa1'), (b'44', b'(44) Paran\xc3\xa1'), (b'45', b'(45) Paran\xc3\xa1'), (b'46', b'(46) Paran\xc3\xa1'), (b'47', b'(47) Santa Catarina'), (b'48', b'(48) Santa Catarina'), (b'49', b'(49) Santa Catarina'), (b'51', b'(51) Rio Grande do Sul'), (b'53', b'(53) Rio Grande do Sul'), (b'54', b'(54) Rio Grande do Sul'), (b'55', b'(55) Rio Grande do Sul'), (b'61', b'(61) Distrito Federal e Goi\xc3\xa1s'), (b'62', b'(62) Goi\xc3\xa1s'), (b'63', b'(63) Tocantins'), (b'64', b'(64) Goi\xc3\xa1s'), (b'65', b'(65) Mato Grosso'), (b'66', b'(66) Mato Grosso'), (b'67', b'(67) Mato Grosso do Sul'), (b'68', b'(68) Acre'), (b'69', b'(69) Rond\xc3\xb4nia'), (b'71', b'(71) Bahia'), (b'73', b'(73) Bahia'), (b'74', b'(74) Bahia'), (b'75', b'(75) Bahia'), (b'77', b'(77) Bahia'), (b'79', b'(79) Sergipe'), (b'81', b'(81) Pernambuco'), (b'82', b'(82) Alagoas'), (b'83', b'(83) Para\xc3\xadba'), (b'84', b'(84) Rio Grande do Norte'), (b'85', b'(85) Cear\xc3\xa1'), (b'86', b'(86) Piau\xc3\xad'), (b'87', b'(87) Pernambuco'), (b'88', b'(88) Cear\xc3\xa1'), (b'89', b'(89) Piau\xc3\xad'), (b'91', b'(91) Par\xc3\xa1'), (b'92', b'(92) Amazonas'), (b'93', b'(93) Par\xc3\xa1'), (b'94', b'(94) Par\xc3\xa1'), (b'95', b'(95) Roraima'), (b'96', b'(96) Amap\xc3\xa1'), (b'97', b'(97) Amazonas'), (b'98', b'(98) Maranh\xc3\xa3o'), (b'99', b'(99) Maranh\xc3\xa3o')])),
                ('telefone', models.CharField(max_length=9, null=True, verbose_name='Telefone', blank=True)),
                ('ddd_celular', models.CharField(blank=True, max_length=2, null=True, verbose_name='DDD', choices=[(b'11', b'(11) S\xc3\xa3o Paulo'), (b'12', b'(12) S\xc3\xa3o Paulo'), (b'13', b'(13) S\xc3\xa3o Paulo'), (b'14', b'(14) S\xc3\xa3o Paulo'), (b'15', b'(15) S\xc3\xa3o Paulo'), (b'16', b'(16) S\xc3\xa3o Paulo'), (b'17', b'(17) S\xc3\xa3o Paulo'), (b'18', b'(18) S\xc3\xa3o Paulo'), (b'19', b'(19) S\xc3\xa3o Paulo'), (b'21', b'(21) Rio de Janeiro'), (b'22', b'(22) Rio de Janeiro'), (b'24', b'(24) Rio de Janeiro'), (b'27', b'(27) Esp\xc3\xadrito Santo'), (b'28', b'(28) Esp\xc3\xadrito Santo'), (b'31', b'(31) Minas Gerais'), (b'32', b'(32) Minas Gerais'), (b'33', b'(33) Minas Gerais'), (b'34', b'(34) Minas Gerais'), (b'35', b'(35) Minas Gerais'), (b'37', b'(37) Minas Gerais'), (b'38', b'(38) Minas Gerais'), (b'41', b'(41) Paran\xc3\xa1'), (b'42', b'(42) Paran\xc3\xa1'), (b'43', b'(43) Paran\xc3\xa1'), (b'44', b'(44) Paran\xc3\xa1'), (b'45', b'(45) Paran\xc3\xa1'), (b'46', b'(46) Paran\xc3\xa1'), (b'47', b'(47) Santa Catarina'), (b'48', b'(48) Santa Catarina'), (b'49', b'(49) Santa Catarina'), (b'51', b'(51) Rio Grande do Sul'), (b'53', b'(53) Rio Grande do Sul'), (b'54', b'(54) Rio Grande do Sul'), (b'55', b'(55) Rio Grande do Sul'), (b'61', b'(61) Distrito Federal e Goi\xc3\xa1s'), (b'62', b'(62) Goi\xc3\xa1s'), (b'63', b'(63) Tocantins'), (b'64', b'(64) Goi\xc3\xa1s'), (b'65', b'(65) Mato Grosso'), (b'66', b'(66) Mato Grosso'), (b'67', b'(67) Mato Grosso do Sul'), (b'68', b'(68) Acre'), (b'69', b'(69) Rond\xc3\xb4nia'), (b'71', b'(71) Bahia'), (b'73', b'(73) Bahia'), (b'74', b'(74) Bahia'), (b'75', b'(75) Bahia'), (b'77', b'(77) Bahia'), (b'79', b'(79) Sergipe'), (b'81', b'(81) Pernambuco'), (b'82', b'(82) Alagoas'), (b'83', b'(83) Para\xc3\xadba'), (b'84', b'(84) Rio Grande do Norte'), (b'85', b'(85) Cear\xc3\xa1'), (b'86', b'(86) Piau\xc3\xad'), (b'87', b'(87) Pernambuco'), (b'88', b'(88) Cear\xc3\xa1'), (b'89', b'(89) Piau\xc3\xad'), (b'91', b'(91) Par\xc3\xa1'), (b'92', b'(92) Amazonas'), (b'93', b'(93) Par\xc3\xa1'), (b'94', b'(94) Par\xc3\xa1'), (b'95', b'(95) Roraima'), (b'96', b'(96) Amap\xc3\xa1'), (b'97', b'(97) Amazonas'), (b'98', b'(98) Maranh\xc3\xa3o'), (b'99', b'(99) Maranh\xc3\xa3o')])),
                ('celular', models.CharField(max_length=9, null=True, verbose_name='Celular', blank=True)),
                ('ocupacao', models.CharField(help_text='Cargo/Profiss\xe3o', max_length=255, verbose_name='Ocupa\xe7\xe3o atual')),
                ('curriculo', models.TextField(help_text='Escreva um breve curr\xedculo, apenas para conhecermos voc\xea um pouco melhor', verbose_name='Curr\xedculo')),
                ('data_cadastro', models.DateField(auto_now_add=True, verbose_name='Data do cadastro')),
                ('questao', models.BooleanField(default=False, verbose_name='Quest\xf5es discurssivas')),
                ('peca', models.BooleanField(default=False, help_text='(pareceres, contesta\xe7\xf5es, peti\xe7\xf5es iniciais, recursos etc.)', verbose_name='Pe\xe7as pr\xe1ticas')),
                ('sentenca', models.BooleanField(default=False, verbose_name='Senten\xe7as')),
                ('cep', models.CharField(max_length=10, null=True, verbose_name='CEP', blank=True)),
                ('logradouro', models.CharField(max_length=100, null=True, verbose_name='Logradouro', blank=True)),
                ('bairro', models.CharField(max_length=100, null=True, verbose_name='Bairro', blank=True)),
                ('numero', models.CharField(max_length=5, null=True, verbose_name='N\xfamero', blank=True)),
                ('complemento', models.CharField(max_length=100, null=True, verbose_name='Complemento', blank=True)),
                ('cidade', models.CharField(max_length=100, null=True, verbose_name='Cidade', blank=True)),
                ('uf', models.CharField(blank=True, max_length=2, null=True, verbose_name='Estado', choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amap\xe1'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Cear\xe1'), ('DF', 'Distrito Federal'), ('ES', 'Esp\xedrito Santo'), ('GO', 'Goi\xe1s'), ('MA', 'Maranh\xe3o'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Par\xe1'), ('PB', 'Para\xedba'), ('PR', 'Paran\xe1'), ('PE', 'Pernambuco'), ('PI', 'Piau\xed'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rond\xf4nia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'S\xe3o Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')])),
                ('disciplinas', models.ManyToManyField(to='enunciado.Disciplina', verbose_name='Disciplinas')),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Usu\xe1rio')),
            ],
            options={
                'verbose_name_plural': 'Corretores',
            },
        ),
        migrations.AddField(
            model_name='banco',
            name='corretor',
            field=models.ForeignKey(verbose_name='Correto', to='corretor.Corretor'),
        ),
    ]
