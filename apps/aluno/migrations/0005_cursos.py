# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0004_auto_20230414_0536'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cursos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'aluno_curso',
                'managed': False,
            },
        ),
        migrations.RunSQL("""
            CREATE or REPLACE VIEW aluno_curso AS
            select curso_id, pc.aluno_id, pc.transaction_status
            from curso_checkoutitens
                     inner join pagseguro_checkout pc on pc.id = curso_checkoutitens.id
            where pc.transaction_status = 3
        """)
    ]
