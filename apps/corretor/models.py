# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django_localflavor_br import br_states
from sorl.thumbnail.fields import ImageField

from libs.util.tipos import DDDS


@python_2_unicode_compatible
class Corretor(models.Model):
    class Meta:
        verbose_name_plural = "Corretores"

    user = models.OneToOneField(
        verbose_name="Usuário", to="auth.User", blank=True, null=True
    )
    nome = models.CharField(
        verbose_name="Nome", max_length=200,help_text="Nome completo"
    )
    cpf = models.CharField(
        verbose_name="C.P.F", max_length=14, blank=True, null=True
    )
    rg = models.CharField(
        verbose_name="RG", max_length=50, blank=True, null=True
    )
    pis = models.CharField(
        verbose_name="PIS/PASEP", max_length=50, blank=True, null=True
    )
    email = models.EmailField(
        verbose_name="E-Mail", unique=True
    )
    foto = ImageField(
        verbose_name="Foto", blank=True, null=True, upload_to='profile/corretor/', help_text="Foto do perfil."
    )
    ddd_telefone = models.CharField(
        verbose_name="DDD", max_length=2, choices=DDDS, blank=True, null=True
    )
    telefone = models.CharField(
        verbose_name="Telefone", max_length=9, blank=True, null=True
    )
    ddd_celular = models.CharField(
        verbose_name="DDD", max_length=2, choices=DDDS, blank=True, null=True
    )
    celular = models.CharField(
        verbose_name="Celular", max_length=9, blank=True, null=True
    )
    ocupacao = models.CharField(
        verbose_name="Ocupação atual", max_length=255, help_text="Cargo/Profissão"
    )
    curriculo = models.TextField(
        verbose_name="Currículo", help_text="Escreva um breve currículo, apenas para conhecermos você um pouco melhor"
    )
    data_cadastro = models.DateField(
        verbose_name="Data do cadastro", editable=False, blank=True, auto_now_add=True
    )
    questao = models.BooleanField(
        verbose_name="Questões discurssivas", default=False
    )
    peca = models.BooleanField(
        verbose_name="Peças práticas", default=False,
        help_text="(pareceres, contestações, petições iniciais, recursos etc.)"
    )
    sentenca = models.BooleanField(
        verbose_name="Sentenças", default=False
    )
    disciplinas = models.ManyToManyField(
        verbose_name="Disciplinas", to='enunciado.Disciplina'
    )
    # Endereço
    cep = models.CharField(
        verbose_name=u"CEP", max_length=10, blank=True, null=True
    )
    logradouro = models.CharField(
        verbose_name="Logradouro", max_length=100, blank=True, null=True
    )
    bairro = models.CharField(
        verbose_name=u"Bairro", max_length=100, blank=True, null=True
    )
    numero = models.CharField(
        verbose_name=u"Número", max_length=5, blank=True, null=True
    )
    complemento = models.CharField(
        verbose_name=u"Complemento", max_length=100, blank=True, null=True
    )
    cidade = models.CharField(
        verbose_name=u"Cidade", max_length=100, blank=True, null=True
    )
    uf = models.CharField(
        verbose_name=u"Estado", max_length=2, blank=True, null=True, choices=br_states.STATE_CHOICES
    )

    def __str__(self):
        return self.nome


@python_2_unicode_compatible
class Banco(models.Model):
    corretor = models.ForeignKey(
        verbose_name="Correto", to=Corretor
    )
    banco = models.CharField(
        verbose_name="Banco", max_length=150, help_text="Ex: Banco do Brasil"
    )
    codigo = models.CharField(
        verbose_name="Código", max_length=5
    )
    agencia = models.CharField(
        verbose_name="Agência", max_length=40
    )
    conta = models.CharField(
        verbose_name="Conta", max_length=40
    )

    def __str__(self):
        return self.banco
