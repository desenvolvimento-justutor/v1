# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0003_auto_20220822_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtro',
            name='data_prova',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Data da Prova', choices=[(2000, b'2000'), (2001, b'2001'), (2002, b'2002'), (2003, b'2003'), (2004, b'2004'), (2005, b'2005'), (2006, b'2006'), (2007, b'2007'), (2008, b'2008'), (2009, b'2009'), (2010, b'2010'), (2011, b'2011'), (2012, b'2012'), (2013, b'2013'), (2014, b'2014'), (2015, b'2015'), (2016, b'2016'), (2017, b'2017'), (2018, b'2018'), (2019, b'2019'), (2020, b'2020'), (2021, b'2021'), (2022, b'2022'), (2023, b'2023')]),
        ),
    ]
