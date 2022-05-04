# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aluno', '0002_auto_20200807_1644'),
        ('curso', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mensagem', models.TextField()),
                ('resposta', models.BooleanField(default=False)),
                ('sentenca', models.BooleanField(default=False)),
                ('oab', models.BooleanField(default=False)),
                ('lido', models.BooleanField(default=False)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('aluno', models.ForeignKey(to='aluno.Aluno')),
                ('curso', models.ForeignKey(blank=True, to='curso.Curso', null=True)),
            ],
            options={
                'ordering': ['-data'],
                'verbose_name_plural': 'Mensagens',
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100, verbose_name=b'Nome')),
                ('graduacao', models.CharField(max_length=150, null=True, verbose_name=b'Gradua\xc3\xa7\xc3\xa3o', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(upload_to=b'professor/', null=True, verbose_name=b'Foto', blank=True)),
                ('sobre', models.TextField(null=True, verbose_name=b'Sobre', blank=True)),
                ('publico', models.BooleanField(default=False, verbose_name=b'Perfil p\xc3\xbablico')),
                ('user', models.OneToOneField(verbose_name=b'Usu\xc3\xa1rio', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Professores',
            },
        ),
        migrations.AddField(
            model_name='mensagem',
            name='professor',
            field=models.ForeignKey(to='professor.Professor'),
        ),
    ]
