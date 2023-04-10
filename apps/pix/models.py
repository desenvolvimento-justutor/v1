# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from apps.aluno.models import Aluno
from django_extensions.db.fields import CreationDateTimeField
from apps.pagseguro.models import Checkout
from django.utils import timezone


@python_2_unicode_compatible
class Cobranca(models.Model):
    txid = models.CharField(
        verbose_name="TXID", max_length=32
    )
    status = models.CharField(
        verbose_name="Status", max_length=31, choices=[
            ("ATIVA", "ATIVA"),
            ("CONCLUIDA", "CONCLUIDA"),
            ("REMOVIDO_PELO_USUARIO_RECEBEDOR", "REMOVIDO_PELO_USUARIO_RECEBEDOR"),
            ("REMOVIDO_PELO_PSP", "REMOVIDO_PELO_PSP")
        ], default="ATIVA"
    )
    checkout = models.ForeignKey(
        verbose_name='Checkout', to=Checkout, on_delete=models.PROTECT)

    response = models.TextField(
        verbose_name='Response'
    )
    info = models.TextField(verbose_name=u"Informações", null=True, blank=True)
    copia_cola = models.TextField(
        verbose_name=u'PIX Cópia e Cola'
    )
    qr_code = models.URLField(
        verbose_name="URL QR-Code"
    )
    valor = models.DecimalField(
        verbose_name="Valor",
        max_digits=9, decimal_places=2
    )
    data = models.DateTimeField(
        verbose_name='Data', default=timezone.now
    )

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return self.txid


a = {
    "status": "ATIVA",
    "calendario": {
        "expiracao": 3600,
        "criacao": "2023-03-03T18:48:27Z"
    },
    "location": "api.pagseguro.com/pix/v2/AA643AA3-5FF1-42BD-907E-724E8F11F260",
    "txid": "2f86a603a8aa43af927574e238f39f9a",
    "revisao": 0,
    "devedor": {
        "cpf": "88815935134",
        "nome": "Christian Douglas"
    },
    "loc": {
        "id": 4883583657504888605,
        "location": "api.pagseguro.com/pix/v2/AA643AA3-5FF1-42BD-907E-724E8F11F260",
        "tipoCob": "COB",
        "criacao": "2023-03-03T18:48:27Z"
    },
    "valor": {
        "original": "1.00"
    },
    "chave": "24181548000143",
    "solicitacaoPagador": "Serviço realizado.",
    "infoAdicionais": [
        {"nome": "Serviço", "valor": "Serviços Justutor"}
    ],
    "pixCopiaECola": "00020101021226830014br.gov.bcb.pix2561api.pagseguro.com/pix/v2/8D7D27E8-7167-4289-A1A7-90A18A26C12627600016BR.COM.PAGSEGURO01368D7D27E8-7167-4289-A1A7-90A18A26C12652048299530398654041.005802BR5922JUSTUTOR EDUCACAO LTDA6010Uberlandia62070503***6304CB09",
    "urlImagemQrCode": "https://api.pagseguro.com/qrcode/QRCO_8D7D27E8-7167-4289-A1A7-90A18A26C126/png"
}
