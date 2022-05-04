# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enunciado', '0001_initial'),
        ('aluno', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filtro',
            name='area_profissional',
            field=models.ForeignKey(verbose_name='\xc1rea Profissional', blank=True, to='enunciado.AreaProfissional', null=True),
        ),
        migrations.AddField(
            model_name='filtro',
            name='cargo',
            field=models.ForeignKey(verbose_name='Cargo', blank=True, to='enunciado.Cargo', null=True),
        ),
        migrations.AddField(
            model_name='filtro',
            name='concurso',
            field=models.ForeignKey(verbose_name='Concurso', blank=True, to='enunciado.Concurso', null=True),
        ),
        migrations.AddField(
            model_name='filtro',
            name='disciplina',
            field=models.ForeignKey(verbose_name='Disc\xedplina', blank=True, to='enunciado.Disciplina', null=True),
        ),
        migrations.AddField(
            model_name='filtro',
            name='esfera_especifica',
            field=models.ForeignKey(verbose_name='Esfera Espec\xedfica', blank=True, to='enunciado.EsferaEspecifica', null=True),
        ),
        migrations.AddField(
            model_name='filtro',
            name='esfera_geral',
            field=models.ForeignKey(verbose_name='Esfera Geral', blank=True, to='enunciado.EsferaGeral', null=True),
        ),
        migrations.AddField(
            model_name='filtro',
            name='localidade',
            field=models.ForeignKey(verbose_name='Localidade', blank=True, to='enunciado.Localidade', null=True),
        ),
        migrations.AddField(
            model_name='filtro',
            name='organizador',
            field=models.ForeignKey(verbose_name='Organizador(a)', blank=True, to='enunciado.Organizador', null=True),
        ),
        migrations.AddField(
            model_name='filtro',
            name='orgao_entidade',
            field=models.ForeignKey(verbose_name='\xd3rgao/Entidade', blank=True, to='enunciado.OrgaoEntidade', null=True),
        ),
        migrations.AddField(
            model_name='filtro',
            name='tipo_peca_pratica',
            field=models.ForeignKey(verbose_name='Tipo de Pe\xe7a Pr\xe1tica', blank=True, to='enunciado.TipoPecaPratica', null=True),
        ),
        migrations.AddField(
            model_name='filtro',
            name='tipo_procedimento',
            field=models.ForeignKey(verbose_name='Tipo de Procedimento', blank=True, to='enunciado.TipoProcedimento', null=True),
        ),
        migrations.AddField(
            model_name='filtro',
            name='tipo_sentenca',
            field=models.ForeignKey(verbose_name='Tipo de Senten\xe7a', blank=True, to='enunciado.TipoPecaSentenca', null=True),
        ),
        migrations.AddField(
            model_name='aluno',
            name='usuario',
            field=models.OneToOneField(verbose_name='Usu\xe1rio', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='seguir',
            unique_together=set([('para_aluno', 'de_aluno'), ('de_aluno', 'para_aluno')]),
        ),
    ]
