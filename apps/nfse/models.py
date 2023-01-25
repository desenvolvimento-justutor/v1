# -*- coding: utf-8 -*-
import uuid

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from apps.aluno.models import Aluno


@python_2_unicode_compatible
class NSFe(models.Model):
    STATUS = [
        ("autorizado", "Autorizado"),
        ("cancelado", "Cancelado"),
        ("erro_autorizacao", u"Erro na autorização"),
        ("processando_autorizacao", u"Processando autorização"),
        ("substituido", u"Substituído")
    ]
    aluno = models.ForeignKey(
        verbose_name="Aluno", to=Aluno, on_delete=models.CASCADE
    )
    checkout = models.OneToOneField(
        verbose_name="Checkout", to="pagseguro.Checkout"
    )
    data_emissao = models.DateTimeField(verbose_name=u"Data de emissão", auto_now=True)
    ref = models.UUIDField(verbose_name="Ref", default=uuid.uuid4)
    status = models.CharField(verbose_name="Status", max_length=24, null=True, blank=True, choices=STATUS)
    numero_rps = models.CharField(verbose_name=u"Número RPS", max_length=20, null=True, blank=True)
    serie_rps = models.CharField(verbose_name=u"Série RPS", max_length=20, null=True, blank=True)
    numero = models.CharField(verbose_name=u"Número", max_length=20, null=True, blank=True)
    codigo_verificacao = models.CharField(verbose_name="Código de verificação", max_length=20, null=True, blank=True)
    url = models.URLField(verbose_name="URL", null=True, blank=True)
    caminho_xml_nota_fiscal = models.CharField(verbose_name="Caminho XML", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "NFSe"
        verbose_name_plural = "NFSe's"
        ordering = ["-data_emissao"]

    def __str__(self):
        return str(self.id)
