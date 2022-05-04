# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from sorl.thumbnail.fields import ImageField
from libs.util.format import pretty_date
from sorl.thumbnail import get_thumbnail
from django.utils.html import mark_safe
from django.template.defaultfilters import linebreaksbr


@python_2_unicode_compatible
class Professor(models.Model):
    user = models.OneToOneField(
        verbose_name='Usuário', to=User
    )
    nome = models.CharField(
        verbose_name='Nome', max_length=100
    )
    graduacao = models.CharField(
        verbose_name='Graduação', max_length=150, blank=True, null=True
    )
    foto = ImageField(
        verbose_name='Foto', upload_to='professor/', blank=True, null=True
    )
    sobre = models.TextField(
        verbose_name='Sobre', blank=True, null=True
    )
    publico = models.BooleanField(
        verbose_name="Perfil público", default=False
    )
    class Meta:
        verbose_name_plural = 'Professores'

    @property
    def foto_url(self):
        url = '/static/images/logos/icone24-borda.svg'
        if self.foto:
            url = get_thumbnail(self.foto, '50x50', crop='center', quality=99).url
        return url

    def __str__(self):
        return self.nome

    def msg_naolidas(self):
        return self.mensagem_set.filter(resposta=False, lido=False, curso__isnull=False)


class Mensagem(models.Model):
    professor = models.ForeignKey(
        Professor
    )
    aluno = models.ForeignKey(
        'aluno.Aluno'
    )
    curso = models.ForeignKey(
        'curso.Curso', blank=True, null=True
    )
    mensagem = models.TextField()
    resposta = models.BooleanField(
        default=False
    )
    sentenca = models.BooleanField(
        default=False
    )
    oab = models.BooleanField(
        default=False
    )
    lido = models.BooleanField(
        default=False
    )
    data = models.DateTimeField(
        editable=False, blank=True, auto_now_add=True
    )

    class Meta:
        verbose_name_plural = 'Mensagens'
        ordering = ['-data']

    def __str__(self):
        return 'MSG:{0:05d} - {1}'.format(self.pk, self.aluno)

    @property
    def str_data(self):
        return pretty_date(self.data)

    @property
    def html(self):
        return mark_safe(linebreaksbr(self.mensagem))

    @property
    def is_professor(self):
        return self.resposta