# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('aluno', '0002_auto_20200807_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('value', models.FloatField(verbose_name=b'Valor')),
                ('active_date', models.DateField(help_text=b'Data de ativa\xc3\xa7\xc3\xa3odo cr\xc3\xa9dito', null=True, verbose_name=b'Ativa\xc3\xa7\xc3\xa3o', blank=True)),
                ('expire_date', models.DateField(help_text=b'Data de expira\xc3\xa7\xc3\xa3o do cr\xc3\xa9dito se n\xc3\xa3o utilizado', null=True, verbose_name=b'Expira\xc3\xa7\xc3\xa3o', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('aluno', models.ForeignKey(to='aluno.Aluno')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Cr\xe9dito',
            },
        ),
    ]
