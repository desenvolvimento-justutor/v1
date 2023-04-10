# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pagseguro', '0003_auto_20220608_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cobranca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('txid', models.CharField(max_length=32, verbose_name='TXID')),
                ('status', models.CharField(default='ATIVA', max_length=31, verbose_name='Status', choices=[('ATIVA', 'ATIVA'), ('CONCLUIDA', 'CONCLUIDA'), ('REMOVIDO_PELO_USUARIO_RECEBEDOR', 'REMOVIDO_PELO_USUARIO_RECEBEDOR'), ('REMOVIDO_PELO_PSP', 'REMOVIDO_PELO_PSP')])),
                ('response', models.TextField(verbose_name='Response')),
                ('copia_cola', models.TextField(verbose_name='PIX C\xf3pia e Cola')),
                ('qr_code', models.URLField(verbose_name='URL QR-Code')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=9, decimal_places=2)),
                ('data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data')),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Checkout', to='pagseguro.Checkout')),
            ],
            options={
                'ordering': ['-data'],
            },
        ),
    ]
