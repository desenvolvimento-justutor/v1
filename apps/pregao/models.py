# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class SolicitarCorrecao(models.Model):
    class Meta:
        verbose_name = "Solicitar Correção"
        verbose_name_plural = "Solicitar Correções"

    resposta = models.OneToOneField(
        to='enunciado.Resposta'
    )
    data_hora = models.DateTimeField(
        "Data/Hora", auto_now_add=True
    )
    corretores = models.ManyToManyField(
        to='corretor.Corretor', related_name='get_corretores'
    )
    corretor = models.ForeignKey(
        to='corretor.Corretor', blank=True, null=True, related_name='get_corretor'
    )
    status = models.CharField(
        choices=[
            ("A", "Aguardando"),
            ("C", "Corrigido"),
            ("E", "Esboço"),
            ("I", "Iniciado"),
        ], default="E", max_length=1
    )
    correcao = models.TextField(
        "Correção", blank=True, null=True
    )
