# -#- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Bloco(models.Model):
    titulo = models.CharField(
        verbose_name='Título', max_length=160
    )
    descricao = models.CharField(
        verbose_name='Descrição', max_length=160
    )

    questoes = models.ManyToManyField(
        'quizz.Questao', blank=True
    )

    def __str__(self):
        return self.titulo


@python_2_unicode_compatible
class Questao(models.Model):
    titulo = models.TextField(
        verbose_name='Título'
    )
    comentario = models.TextField(
        verbose_name='Comentário do professor', blank=True, null=True
    )

    def __str__(self):
        return self.titulo

    def proxima(self):
        return Questao.objects.filter(bloco=self.bloco, id__gt=self.pk).first()

    def get_correta(self):
        return self.opcoes.first(correta=True).first()


@python_2_unicode_compatible
class Pergunta(models.Model):
    questao = models.ForeignKey(
        verbose_name='Questão', related_name='opcoes',
        to=Questao, on_delete=models.CASCADE
    )
    titulo = models.TextField(
        verbose_name='Título'
    )
    correta = models.BooleanField(
        verbose_name='Correta',
        default=False
    )

    class Meta:
        verbose_name = 'Opção'
        verbose_name_plural = 'Opções'

    def __str__(self):
        return self.titulo


@python_2_unicode_compatible
class RespostaAluno(models.Model):
    questao = models.ForeignKey(
        verbose_name='Questão', related_name='respostas_questao',
        to=Questao, on_delete=models.CASCADE
    )
    resposta = models.ForeignKey(
        verbose_name='Resposta', related_name='respostas_aluno',
        to=Pergunta, on_delete=models.CASCADE
    )
    aluno = models.ForeignKey(
        verbose_name='Aluno', to='aluno.Aluno',
        related_name='alunos', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.resposta.titulo


@python_2_unicode_compatible
class Comentario(models.Model):
    questao = models.ForeignKey(
        verbose_name='Questão', related_name='comentarios',
        to=Questao, on_delete=models.CASCADE
    )
    comentario = models.TextField(
        verbose_name='Comentario'
    )
    aluno = models.ForeignKey(
        verbose_name='Aluno', to='aluno.Aluno',
        related_name='alunos_comentario', on_delete=models.CASCADE
    )
    data = models.DateTimeField(
        verbose_name='Data', auto_now_add=True
    )

    def __str__(self):
        return self.comentario

    class Meta:
        ordering = ['-data']


