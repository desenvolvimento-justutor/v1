# -*- coding: utf-8 -*-
# Autor: christian
# try:
#     from django.db.models.loading import get_model
# except:
from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Q

get_model = apps.get_model

from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail.fields import ImageField
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from html2text import html2text
from mptt.models import MPTTModel
from smart_selects.db_fields import ChainedForeignKey
from django.template import loader, Context
import json
from django_extensions.db.fields import AutoSlugField
from libs.signals import create_slug
from libs.util.format import pretty_date
from libs.util.mail import send_mail
from apps.enunciado import FLAG_PONTOS_RESPONDER, FLAG_PONTOS_CORRIGIR, FLAG_PONTOS_CORRIGIREM, FLAG_TIPO_ENUNCIADO_P
from justutorial.settings import SITEADD, push, EMAIL_HOST_USER
from apps.website.utils import enviar_email
from apps.corretor.models import Corretor

TIPO_URL = {
    'QD': 'questao',
    'PP': 'peca',
    'ST': 'sentenca'
}


# ---------------------------------------------
# NOTIFICAÇÃO ALUNO
# ---------------------------------------------
class NotificacoesAluno(models.Model):
    class Meta:
        verbose_name = u'Notificação'
        verbose_name_plural = u'Notificações'

    aluno = models.ForeignKey(
        verbose_name='Aluno', to='aluno.Aluno', related_name='get_notificacao_de'
    )
    para = models.ForeignKey(
        verbose_name='Para', to='aluno.Aluno', related_name='get_notificacao_para', blank=True, null=True
    )
    tipo = models.CharField(
        verbose_name='Tipo', max_length=1,
        choices=[('R', 'Resposta'), ('C', u'Correção'), ('M', u'Comentário'), ('L', 'Like'), ('G', 'Mensagem')]
    )
    status_resposta = models.CharField(
        verbose_name='Tipo', max_length=1,
        choices=[('I', 'Iniciou'), ('F', u'Finalizou'), ('C', u'Cancelou')], blank=True, null=True
    )
    resposta = models.ForeignKey(to='enunciado.Resposta', blank=True, null=True)
    correcao = models.ForeignKey(to='enunciado.Correcao', blank=True, null=True)
    comentario = models.ForeignKey(to='enunciado.ComentarioCorrecao', blank=True, null=True)
    nota = models.ForeignKey(to='enunciado.NotaResposta', blank=True, null=True)
    lido = models.BooleanField(
        verbose_name='Lido', default=False, help_text=u'Marque para informar que você visualizou a Notificação'
    )
    data = models.DateTimeField(
        verbose_name='Data', default=timezone.now
    )

    @property
    def str_data(self):
        return pretty_date(self.data)

    @property
    def get_mensagem(self):
        ret = {}
        if self.tipo == 'C':
            if self.correcao.resposta.aluno != self.correcao.aluno:
                msg_html = u"""Efetuou uma <a data-toogle="tooltip" title="#{0}"
                target="_blank" href="{1}">Correção</a>""".format(
                    self.correcao, self.correcao.get_absolute_url(),
                )
            else:
                msg_html = u"""A <a data-toogle="tooltip" title={2} target="_blank" href="{0}">Resposta</a>
                recebeu uma <a data-toogle="tooltip" title="#{3}" target="_blank" href="{1}">Correção</a>
                e uma Nota <span class="text-success"><strong>+{4}</strong></span>.""".format(
                    self.correcao.resposta.get_absolute_url(), self.correcao.get_absolute_url(),
                    self.correcao.resposta.numero, self.correcao, self.correcao.get_nota_resposta
                )
            msg_simples = u'Nova Correção'
            ret = {'html': msg_html, 'plan': msg_simples}
        elif self.tipo == 'L':
            if self.aluno == self.para:
                msg_html = u"""Você fez uma avaliação positiva da <a data-toogle="tooltip" title={0}
                target="_blank" href="{1}">Correção</a> à <a target="_blank" href="{3}">Resposta {2}</a>""".format(
                    self.correcao, self.correcao.get_absolute_url(), self.correcao.resposta.numero,
                    self.correcao.resposta.get_absolute_url()
                )
            else:
                msg_html = u"""A sua <a data-toogle="tooltip" title={0} target="_blank" href="{1}">Correção</a>
                à <a target="_blank" href="{3}">Resposta {2}</a> recebeu uma avaliação
                positiva e você acumulou <span class="text-success"><strong>+1</strong></span>pt.""".format(
                    self.correcao, self.correcao.get_absolute_url(), self.correcao.resposta.numero,
                    self.correcao.resposta.get_absolute_url()
                )
            msg_simples = u'Avaliação Positiva'
            ret = {'html': msg_html, 'plan': msg_simples}
        elif self.tipo == 'M':
            msg_html = u"""A <a target="_blank" href="{1}">Correção</a> à <a data-toogle="tooltip" title="{2}"
            target="_blank" href="{3}">Resposta {2}</a> recebeu um Comentário.""".format(
                self.correcao, self.correcao.get_absolute_url(), self.correcao.resposta.numero,
                self.correcao.resposta.get_absolute_url()
            )
            msg_simples = u'Comentário'
            ret = {'html': msg_html, 'plan': msg_simples}
        elif self.tipo == 'G':
            msg_html = u"""<a target="_blank" href="{url_aluno}">{aluno}</a> te enviou uma mensagem.""".format(
                url_aluno=self.aluno.get_absolute_url(), aluno=self.aluno
            )
            msg_simples = u'Mensagem'
            ret = {'html': msg_html, 'plan': msg_simples}
        elif self.tipo == 'R':
            if self.status_resposta == 'F':
                if self.resposta.aluno == self.para:
                    msg_html = """
                    Finalizou a <a href="{url_resposta}">Resposta {resposta_numero}</a> ao
                    <a href="{url_enunciado}">Enunciado {nome_enunciado}</a>. Seu tempo foi de {tempo} e a média de
                    tempo para responder é de {media:.2f}. Parabéns! Você acumulou pontos no Ranking JusTutor!
                    """.format(
                        url_resposta=self.resposta.get_absolute_url(), resposta_numero=self.resposta.numero,
                        url_enunciado=self.resposta.enunciado.get_absolute_url(), nome_enunciado=self.resposta.enunciado,
                        tempo=self.resposta.tempo, media=self.resposta.enunciado.media_tempo,
                    )
                else:
                    msg_html = """
                    Finalizou a <a href="{url_resposta}">Resposta {resposta_numero}</a> ao
                    <a href="{url_enunciado}">Enunciado {nome_enunciado}</a>.
                    """.format(
                        url_resposta=self.resposta.get_absolute_url(), resposta_numero=self.resposta.numero,
                        url_enunciado=self.resposta.enunciado.get_absolute_url(), nome_enunciado=self.resposta.enunciado
                    )

                msg_simples = u'Finalizou uma Resposta.'
            elif self.status_resposta == 'I':
                msg_html = """
                Iniciou a <a href="{url_resposta}">Resposta #{resposta_numero}</a> ao
                <a href="{url_enunciado}">Enunciado {nome_enunciado}</a>.
                """.format(
                    url_resposta=self.resposta.get_absolute_url(), resposta_numero=self.resposta.numero,
                    url_enunciado=self.resposta.enunciado.get_absolute_url(), nome_enunciado=self.resposta.enunciado
                )
                msg_simples = u'Iniciou uma Resposta.'
            elif self.status_resposta == 'C':
                msg_html = """
                <del>Cancelou sua <a href="{url_resposta}">Resposta #{resposta_numero}</a> ao
                <a href="{url_enunciado}">Enunciado {nome_enunciado}</a>.</del>
                """.format(
                    url_resposta='javascript:void(0)', resposta_numero=self.resposta.numero,
                    url_enunciado=self.resposta.enunciado.get_absolute_url(), nome_enunciado=self.resposta.enunciado
                )
                msg_simples = u'Iniciou uma Resposta.'
            ret = {'html': msg_html, 'plan': msg_simples}
        return ret

    @property
    def icone(self):
        ret = {}
        if self.tipo == 'C':
            i = '<i class="fa fa-edit"></i>'
            i_lg = '<span class="text-danger"><i class="fa fa-edit fa-lg"></i></span>'
            ret = {'i': i, 'lg': i_lg}
        elif self.tipo == 'L':
            i = '<i class="fa fa-thumbs-o-up"></i>'
            i_lg = '<span class="text-success"><i class="fa fa-thumbs-o-up fa-lg"></i></span>'
            ret = {'i': i, 'lg': i_lg}
        elif self.tipo == 'M':
            i = '<i class="fa fa-comment-o"></i>'
            i_lg = '<span class="text-info"><i class="fa fa-comment-o fa-lg"></i></span>'
            ret = {'i': i, 'lg': i_lg}
        elif self.tipo == 'G':
            i = '<i class="fa fa-envelope-o"></i>'
            i_lg = '<span class="text-info"><i class="fa envelope-o fa-lg"></i></span>'
            ret = {'i': i, 'lg': i_lg}
        elif self.tipo == 'R':
            if self.status_resposta == 'F':
                i = '<i class="fa fa-check"></i>'
                i_lg = '<span class="text-success"><i class="fa fa-check fa-lg"></i></span>'
                ret = {'i': i, 'lg': i_lg}
            elif self.status_resposta == 'I':
                i = '<i class="fa fa-clock-o"></i>'
                i_lg = '<span class="text-primary"><i class="fa fa-clock-o fa-lg"></i></span>'
                ret = {'i': i, 'lg': i_lg}
            elif self.status_resposta == 'C':
                i = '<i class="fa fa-trash-o"></i>'
                i_lg = '<span class="text-danger"><i class="fa fa-trash-o fa-lg"></i></span>'
                ret = {'i': i, 'lg': i_lg}
        return ret


def criar_notificacao(aluno_id, para_id, tipo, **xargs):
    notificacao = None
    if tipo not in ['R', 'C', 'M', 'L', 'G']:
        raise Exception(u'Tipo {0} Inválido'.format(tipo))
    else:
        notificacao = NotificacoesAluno(
            aluno_id=aluno_id,
            para_id=para_id,
            tipo=tipo
        )

        resposta_id = xargs.get('resposta_id')
        correcao_id = xargs.get('correcao_id')
        status_resposta = xargs.get('status_resposta')
        if tipo in ['C', 'M'] and not correcao_id:
            raise Exception(u'É preciso informar o id do Comentário para tipo {0}.'.format(tipo))
        elif tipo == 'R' and not resposta_id:
            raise Exception(u'É preciso informar o id da Resposta para tipo {0}.'.format(tipo))
        else:
            if resposta_id:
                notificacao.resposta_id = resposta_id
            if correcao_id:
                notificacao.correcao_id = correcao_id
            if status_resposta:
                notificacao.status_resposta = status_resposta
        notificacao.save()
        if aluno_id != para_id:
            push.trigger('painel_channel', 'notificar_aluno', {
                'message': notificacao.get_mensagem.get('html'),
                'aluno_id': para_id
            })
    return notificacao
# ---------------------------------------------
# ESFERA GERAL
# ---------------------------------------------
class EsferaGeral(models.Model):
    """
    Cadastro de Esferas Gerais
    """
    class Meta:
        verbose_name = "Esfera Geral"
        verbose_name_plural = u"Esferas Gerais"
        ordering = ['nome']

    nome = models.CharField(
        verbose_name="Nome", unique=True, max_length=60
    )

    def __unicode__(self):
        return self.nome


# ---------------------------------------------
# ESFERA ESPECIFICA
# ---------------------------------------------
class EsferaEspecifica(models.Model):
    """
    Cadastro de Esferas Específicas
    """
    class Meta:
        verbose_name = "Esfera Específica"
        verbose_name_plural = U"Esferas Especificas"
        unique_together = ['nome', 'esfera_geral']
        ordering = ['esfera_geral', 'nome']

    esfera_geral = models.ForeignKey(
        verbose_name=u"Esfera Geral", to=EsferaGeral, related_name='get_especificas'
    )
    nome = models.CharField(
        verbose_name="Nome", max_length=60
    )

    def __unicode__(self):
        return u"{0} / {1}".format(self.esfera_geral, self.nome)


# ---------------------------------------------
# CARGO
# ---------------------------------------------
class Cargo(models.Model):
    """
    Cadastro de Cargos
    """
    class Meta:
        verbose_name = "Cargo"
        unique_together = ['nome', 'esfera_especifica']
        ordering = ['esfera_especifica', 'nome']

    esfera_especifica = models.ForeignKey(
        verbose_name=u"Esfera Específica",  to=EsferaEspecifica, related_name='get_cargos'
    )
    nome = models.CharField(
        verbose_name="Nome", max_length=60
    )

    def __unicode__(self):
        return self.nome


# ---------------------------------------------
# AREA PROFISSIONAL
# ---------------------------------------------
class AreaProfissional(models.Model):
    """
    Cadastro de Áreas Profissionais
    """
    class Meta:
        verbose_name = u"Área Profissional"
        verbose_name_plural = u"Áreas Profissionais"
        ordering = ['nome']

    nome = models.CharField(
        verbose_name="Nome", unique=True, max_length=60
    )

    def __unicode__(self):
        return self.nome


# ---------------------------------------------
# ORGAO/ENTIDADE
# ---------------------------------------------
class OrgaoEntidade(models.Model):
    """
    Cadastro de Órgãos e Entidades
    """
    class Meta:
        verbose_name = u"Órgão/Entidade"
        verbose_name_plural = u"Órgãos/Entidades"
        ordering = ['nome']

    nome = models.CharField(
        verbose_name="Nome", max_length=60, unique=True
    )

    def __unicode__(self):
        return self.nome


# ---------------------------------------------
# TIPO PROCEDIMENTO
# ---------------------------------------------
class TipoProcedimento(models.Model):
    """
    Cadastro Tipos de Procedimentos
    """
    class Meta:
        verbose_name = "Tipo de Procedimento"
        verbose_name_plural = "Tipos de Procedimentos"
        ordering = ['nome']

    nome = models.CharField(
        verbose_name="Nome", unique=True, max_length=60
    )

    def __unicode__(self):
        return self.nome


# ---------------------------------------------
# TIPO PECA PRATICA
# ---------------------------------------------
class TipoPecaPratica(models.Model):
    """
    Cadastro de Tipos de Peças Práticas
    """
    class Meta:
        verbose_name = u"Tipo de Peça Prática"
        verbose_name_plural = u"Tipos de Peças Práticas"
        ordering = ['nome']

    nome = models.CharField(
        verbose_name="Nome", unique=True, max_length=60
    )

    def __unicode__(self):
        return self.nome


# ---------------------------------------------
# TIPO SENTENCA
# ---------------------------------------------
class TipoPecaSentenca(models.Model):
    """
    Cadastro de Tipos de Sentenças
    """
    class Meta:
        verbose_name = u"Tipo de Sentença"
        verbose_name_plural = u"Tipos de Sentenças"
        ordering = ['nome']

    nome = models.CharField(
        verbose_name="Nome", unique=True, max_length=60
    )

    def __unicode__(self):
        return self.nome


# ---------------------------------------------
# ORGANIZADOR
# ---------------------------------------------
class Organizador(models.Model):
    """
    Cadastro de Organizadoras
    """
    class Meta:
        verbose_name = "Organizador"
        verbose_name_plural = "Organizadoras"
        ordering = ['nome']

    nome = models.CharField(
        verbose_name="Nome", unique=True, max_length=60
    )

    def __unicode__(self):
        return self.nome


# ---------------------------------------------
# LOCALIDADE
# ---------------------------------------------
class Localidade(models.Model):
    """
    Cadastro de Localidade
    """
    class Meta:
        ordering = ['nome']

    nome = models.CharField(
        verbose_name="Nome", unique=True, max_length=60
    )

    def __unicode__(self):
        return self.nome


# ---------------------------------------------
# DISCIPLINA
# ---------------------------------------------
class Disciplina(models.Model):
    """
    Cadastro de Dísciplinas
    """
    class Meta:
        verbose_name = u"Dísciplina"
        ordering = ['nome']

    nome = models.CharField(
        verbose_name="Nome", unique=True, max_length=60
    )

    def __unicode__(self):
        return self.nome


class DisciplinaLinks(models.Model):
    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = "Link's"

    legislacao = models.BooleanField(
        verbose_name=u"Legislação", default=False
    )
    disciplina = models.ForeignKey(Disciplina)
    titulo = models.CharField(
        verbose_name=u"Título", max_length=150
    )
    link = models.URLField()

    def __unicode__(self):
        return self.titulo

    @property
    def title(self):
        ret = self.disciplina.nome
        if self.legislacao:
            ret = u'(Legislação)'
        return ret

# ---------------------------------------------
# CONCURSO
# ---------------------------------------------
class Concurso(models.Model):
    """
    Cadastro de Concursos
    """
    class Meta:
        ordering = ['nome']

    cargo = models.ForeignKey(
        verbose_name="Cargo", to=Cargo
    )
    nome = models.CharField(
        verbose_name="Nome", unique=True, max_length=200
    )

    def __unicode__(self):
        return self.nome


# ---------------------------------------------
# TAG
# ---------------------------------------------
class Tag(models.Model):
    """
    Cadastro de Tag's
    """
    class Meta:
        ordering = ['nome']

    nome = models.CharField(
        verbose_name="Nome da Tag", max_length=50
    )

    def __unicode__(self):
        return self.nome


class TagLinks(models.Model):
    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = "Link's"

    legislacao = models.BooleanField(
        verbose_name=u"Legislação", default=False
    )
    tag = models.ForeignKey(Tag)
    titulo = models.CharField(
        verbose_name=u"Título", max_length=150
    )
    link = models.URLField()

    def __unicode__(self):
        return self.titulo

    @property
    def title(self):
        ret = self.tag.nome
        if self.legislacao:
            ret = u'(Legislação)'
        return ret


# ---------------------------------------------
# ENUNCIADO/PROPOSTA
# ---------------------------------------------
class EnunciadoProposta(models.Model):
    """
    Cadastro de Enunciados/Propostas
    --------------------------------
    * 'concurso somente' prencher se 'tipo_enunciado' in ['Peça Prática', 'Questão Discursiva']
    * 'tipo_procedimento' somente prencher se  'tipo_enunciado' = 'Sentença'
    * 'tipo_peca_pratica' somente prencher se  'tipo_enunciado' = 'Peça Prática'
    * 'num_questao_caderno' somente prencher se  'tipo_procedimento' = 'Questão Discursiva'
    """
    class Meta:
        verbose_name = "Enunciado/Proposta"
        verbose_name_plural = "Enunciados/Propostas"

    _anos = map(lambda x: (x, str(x)), range(1989, timezone.now().year+1))

    desatualizado = models.BooleanField(
        verbose_name="Desatualizado?", default=False, help_text=u"Marque caso o Enunciado esteja desatualizado."
    )
    classificacao = models.CharField(
        verbose_name=u"Classificação", max_length=2,
        choices=[("ST", u"Sentença"), ("PP", u"Peça Prática"), ("QD", u"Questão Discursiva")],
        help_text="Informe se o Enunciado/Proposta é uma 'Sentença', 'Peça Prática' ou uma 'Questão Discursiva'."
    )
    esfera_geral = models.ForeignKey(
        verbose_name="Esfera Geral", to=EsferaGeral, related_name='get_enunciados'
    )
    esfera_especifica = ChainedForeignKey(
        verbose_name=u"Esfera Específica", to=EsferaEspecifica, related_name='get_enunciados',
        chained_field='esfera_geral', chained_model_field='esfera_geral'
    )
    cargo = ChainedForeignKey(
        verbose_name="Cargo", to=Cargo, related_name='get_enunciados',
        chained_field='esfera_especifica', chained_model_field='esfera_especifica'
    )
    area_profissional = models.ForeignKey(
        verbose_name=u"Área Profissional", to=AreaProfissional, related_name='get_enunciados',
        blank=True, null=True
    )
    orgao_entidade = models.ForeignKey(
        verbose_name=u"Órgao/Entidade", to=OrgaoEntidade, related_name='get_enunciados'
    )
    concurso = models.ForeignKey(
        verbose_name="Concurso", to=Concurso, related_name='get_enunciados', blank=True, null=True
    )
    data_prova = models.PositiveSmallIntegerField(
        verbose_name="Data da Prova", choices=_anos
    )
    disciplina = models.ForeignKey(
        verbose_name=u"Discíplina", to=Disciplina, related_name='get_enunciados', blank=True, null=True
    )
    tipo_procedimento = models.ForeignKey(
        verbose_name="Tipo de Procedimento", to=TipoProcedimento, blank=True, null=True
    )  # Campo somente pra 'Classificação' = 'Sentença'
    tipo_sentenca = models.ForeignKey(
        verbose_name=u"Tipo de Sentença", to=TipoPecaSentenca, blank=True, null=True
    )  # Campo somente pra 'Classificação' = 'Sentença'
    tipo_peca_pratica = models.ForeignKey(
        verbose_name=u"Tipo de Peça Prática", to=TipoPecaPratica, blank=True, null=True
    )  # Campo somente pra 'Classificação' = 'Peça Prática'
    num_questao_caderno = models.PositiveSmallIntegerField(
        verbose_name=u"Numero da Questão", blank=True, null=True,
        help_text=u"Número da Questão no Caderno de Provas."
    )  # Campo somente pra Classificação = Questão Discursiva
    organizador = models.ForeignKey(
        verbose_name="Organizador(a)", to=Organizador
    )
    localidade = models.ForeignKey(
        verbose_name="Localidade", to=Localidade
    )
    linhas = models.PositiveSmallIntegerField(
        null=True
    )
    texto = models.TextField(
        verbose_name="Texto", help_text=u"Formule um texto para o seu Enunciado.", blank=True, null=True,
    )
    tags = models.ManyToManyField(
        verbose_name="Tag", to=Tag, blank=True
    )
    audio = models.TextField(
        verbose_name="Áudio", blank=True, null=True, help_text="Código embutido do Soundcloud"
    )
    autor = models.CharField(
        verbose_name="Autor do Gabarito", max_length=1,
        blank=True, null=True, choices=[
            ('B', 'Banca examinadora'),
            ('J', 'Justutor'),
        ]
    )
    gabarito_file = models.FileField(
        verbose_name="Arquivo", blank=True, null=True,
        help_text="Arquivo contendo o Gabarito."
    )
    gabarito = models.TextField(
        verbose_name="Gabarito", blank=True, null=True,
        help_text="Texto do Gabarito."
    )

    @property
    def range_lines(self):
        return range(1, self.linhas + 1)

    def __unicode__(self):
        return u"{0} {1:05d}".format(self.get_classificacao_display(), self.id)

    def titulo(self):
        return self.__unicode__()

    def css_class(self):
        ret = '1'
        if self.classificacao == 'ST':
            ret = '2'
        elif self.classificacao == 'PP':
            ret = '3'
        return ret

    def get_biblioteca(self):
        links = []
        for link in self.disciplina.disciplinalinks_set.all():
            links.append(link)
        for tag in self.tags.all():
            for link in tag.taglinks_set.all():
                links.append(link)
        return links

    @property
    def get_respostas(self):
        return self.resposta_set.filter(concluido=True, ativo=True)

    @property
    def count_respostas(self):
        return self.resposta_set.filter(concluido=True, ativo=True).count()

    @property
    def min_char(self):
        ret = 200
        if self.classificacao == 'ST':
            ret = 3000
        elif self.classificacao == 'PP':
            ret = 2000
        return ret

    @property
    def get_pontos_responder(self):
        """usado pra calcular o ranking do aluno"""
        return FLAG_PONTOS_RESPONDER.get(self.classificacao)

    @property
    def get_pontos_corrigir(self):
        """usado pra calcular o ranking do aluno"""
        ret = 10
        if self.classificacao == 'QD':
            ret = 4
        return ret

    @property
    def get_tipo_url(self):
        return TIPO_URL.get(self.classificacao)

    @models.permalink
    def get_absolute_url(self):
        return 'enunciado:tipo-id', ([self.get_tipo_url, self.id])

    @models.permalink
    def get_responder_absolute_url(self):
        return 'enunciado:responder', ([self.get_tipo_url, self.id])

    def get_respostas(self):
        respostas = self.resposta_set.filter(concluido=True, ativo=True)
        resps = sorted(respostas, key=lambda r: r.get_media)
        resps.reverse()
        return resps

    @property
    def media_tempo(self):
        avg = self.resposta_set.all().aggregate(Avg('tempo')).get('tempo__avg')
        if not avg:
            return 0.0
        return avg / 60

    def get_corretores(self):
        filtro = {
            "ST": Q(sentenca=True),
            "PP": Q(peca=True),
            "QD": Q(questao=True),
        }
        args = [Q(filtro.get(self.classificacao)), Q(disciplinas=self.disciplina)]
        return Corretor.objects.filter(*args)


class EnunciadoPropostaSentenca(EnunciadoProposta):
    class Meta:
        verbose_name = u"Sentença"
        proxy = True

    TIPO = 'ST'
    LIST_DISPLAY = [
        'titulo', 'esfera_geral', 'esfera_especifica', 'cargo', 'orgao_entidade',
        'concurso', 'data_prova', 'disciplina', 'tipo_procedimento', 'tipo_sentenca',
        'organizador', 'localidade', 'desatualizado'
    ]
    EXCLUDE = [
        'area_profissional', 'tipo_peca_pratica', 'num_questao_caderno', 'classificacao', 'gabarito_file'
    ]
    REQUIREDS = ['disciplina', 'concurso', 'tipo_procedimento', 'tipo_sentenca']


class EnunciadoPropostaPratica(EnunciadoProposta):
    class Meta:
        verbose_name = u"Peça Prática"
        verbose_name_plural = u"Peças Práticas"
        proxy = True

    TIPO = 'PP'
    LIST_DISPLAY = [
        'titulo', 'esfera_geral', 'esfera_especifica', 'cargo', 'area_profissional',
        'orgao_entidade', 'concurso', 'data_prova', 'disciplina', 'tipo_peca_pratica',
        'organizador', 'localidade', 'desatualizado'
    ]
    EXCLUDE = [
        'tipo_procedimento', 'num_questao_caderno', 'classificacao', 'tipo_sentenca', 'gabarito_file'
    ]
    REQUIREDS = ['concurso', 'area_profissional', 'disciplina', 'tipo_peca_pratica']


class EnunciadoPropostaDiscursiva(EnunciadoProposta):
    class Meta:
        verbose_name = u"Questão Discursiva"
        verbose_name_plural = u"Questões Discursivas"
        proxy = True

    TIPO = 'QD'
    LIST_DISPLAY = [
        'esfera_geral', 'esfera_especifica', 'cargo', 'area_profissional',
        'orgao_entidade', 'concurso', 'data_prova', 'disciplina', 'num_questao_caderno',
        'organizador', 'localidade', 'desatualizado'
    ]
    EXCLUDE = [
        'tipo_procedimento', 'tipo_peca_pratica', 'classificacao', 'tipo_sentenca', 'gabarito_file'
    ]
    REQUIREDS = ['concurso', 'area_profissional', 'disciplina', 'num_questao_caderno']


# ---------------------------------------------
# QUESTOES DOS ENUNCIADOS
# ---------------------------------------------
# class Conteudo(models.Model):
#     """
#     Cadastro de Enunciados
#     Utilizada para o cadastro de Enunciados que deve
#     ser relacionada a um EnunciadoProposta
#     """
#     class Meta:
#         verbose_name = u"Conteúdo"
#
#     user = models.ForeignKey(
#         verbose_name=u"Usuário", to=User, editable=False,
#     )
#     enunciado = models.ForeignKey(
#         verbose_name=u"Enunciado", to=EnunciadoProposta,
#         help_text=u"Enunciado a que este Texto pertence."
#     )
#     texto = models.TextField(
#         verbose_name="Texto", help_text=u"Formule um texto para o seu Enunciado."
#     )
#     data = models.DateTimeField(
#         verbose_name="Data", auto_now_add=True, blank=True, help_text=u"Data de criação."
#     )
#
#     def __unicode__(self):
#         return u"Conteúdo #{0:06d}".format(self.id)
#
#     def titulo(self):
#         return self.__unicode__()


# ---------------------------------------------
# RESPOSTAS DAS QUESTOES
# ---------------------------------------------
class Resposta(models.Model):
    """
    Cadastro de Respostas
    Utilizada para o cadastro de Respostas dos Enunciados
    """
    class Meta:
        ordering = ['-data_termino']
        unique_together = ['enunciado', 'aluno', 'ativo', 'ativo_motivo']

    send_mail = False

    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno'
    )
    enunciado = models.ForeignKey(
        verbose_name=u"Enunciado", to=EnunciadoProposta
    )
    texto = models.TextField(
        verbose_name="Texto", help_text=u"Texto contendo a Resposta do Enunciado."
    )
    data_inicio = models.DateTimeField(
        verbose_name=u"Início", auto_now_add=True, blank=True, help_text=u"Data/Hora que iniciou a correção"
    )
    tempo = models.TimeField(
        verbose_name=u"Tempo", blank=True, null=True, default='00:00:00'
    )
    data_termino = models.DateTimeField(
        verbose_name=u"Término", auto_now_add=True, blank=True, null=True,
        help_text=u"Data/Hora que concluiu a correção"
    )
    concluido = models.BooleanField(
        verbose_name=u"Concluído", default=False
    )
    media = models.FloatField(
        verbose_name='Media', blank=True, null=True, default=0.0
    )
    ativo = models.BooleanField(
        verbose_name='Ativo', default=True, help_text=u"Se a resposta for desativada ela não aparecerá mais no Site."
    )
    ativo_motivo = models.TextField(
        verbose_name="Motivo", blank=True, null=True,
        help_text=u'Mensagem que será enviada informando o motivo da inativação da resposta.'
    )


    def __unicode__(self):
        return u"#{0:06d}".format(self.id or 1)

    @property
    def str_data(self):
        return pretty_date(self.data_termino)

    @property
    def anterior(self):
        return Resposta.objects.filter(
            id__lt=self.id, enunciado=self.enunciado, concluido=True, ativo=True,
        ).exclude(id=self.id).order_by('id').last()

    @property
    def proxima(self):
        return Resposta.objects.filter(
            id__gt=self.id, enunciado=self.enunciado, concluido=True, ativo=True,
        ).order_by('id').exclude(id=self.id).first()

    @property
    def numero(self):
        return u"#{0:06d}".format(self.id)

    @property
    def qtda_char(self):
        return len(html2text(self.texto).replace('\n', ''))

    @models.permalink
    def get_absolute_url(self):
        return 'enunciado:resposta', ([self.id])

    def count_notas(self):
        """
        Conta a quantidade de notas que a resposta recebeu

        :rtype : list
        :return : [{'nota__count': 1, 'nota': 5}, {'nota__count': 1, 'nota': 7}]
        """
        qry_res = self.notaresposta_set.values('nota').annotate(Count('nota'))
        return qry_res.order_by('-nota')

    def media(self):
        return self.notaresposta_set.all().aggregate(media=Avg('nota')).get('media')

    @property
    def get_minutos(self):
        return (self.tempo.hour * 60. + self.tempo.minute) + self.tempo.second * .1

    @property
    def get_media(self):
        avg = self.notaresposta_set.aggregate(Avg('nota'))
        if not avg.get('nota__avg'):
            return 0.0
        return avg.get('nota__avg')

    @property
    def get_css_class(self):
        media = self.get_media
        if media == 0.0:
            css = "", "label-default"
        elif media <= 3.0 > 0.0:
            css = "status-vermelho", "label-danger"
        elif media <= 6.0 > 3.0:
            css = "status-amarelo", "label-warning"
        elif media <= 8.0 > 6.0:
            css = "status-azul", "label-primary"
        elif media <= 10.0 > 8.0:
            css = "status-verde", "label-success"
        return css


@receiver(post_save, sender=Resposta)
def resposta_save(sender, **kwargs):
    instance = kwargs.get('instance')
    enunciado = instance.enunciado
    status_resposta = 'I'
    if instance.concluido and instance.ativo:
        status_resposta = 'F'
    elif not instance.ativo:
        status_resposta = 'C'

    de = instance.aluno
    tipo = 'R'
    created = kwargs.get('created')
    if created:
        criar_notificacao(
            aluno_id=de.id,
            para_id=de.id,
            tipo=tipo,
            resposta_id=instance.id,
            status_resposta=status_resposta
        )
    # DESATIVAR RESPOSTA
    if not instance.ativo:
        enviar_email(
            'email/email-desativar-resposta.html', u'Resposta excluída do site JusTutor',
            [instance.aluno.email], {'resposta': instance}
        )
    # NOTIFICAR SEGUIDORES
    if instance.concluido and instance.send_mail:
        criar_notificacao(
            aluno_id=de.id,
            para_id=de.id,
            tipo=tipo,
            resposta_id=instance.id,
            status_resposta=status_resposta
        )
        for seguidor in de.get_seguidores.all():
            para = seguidor.de_aluno
            criar_notificacao(
                aluno_id=de.id,
                para_id=para.id,
                tipo=tipo,
                resposta_id=instance.id,
                status_resposta=status_resposta
            )
            if para.notificar_responder_seguir:
                ctx = {
                    'aluno': de,
                    'resposta': instance
                }
                enviar_email(
                    'email/email-responder-seguir.html',
                    u'{0} elaborou uma resposta no JusTutor'.format(de),
                    [para.email], ctx, ead=True
                )
        for resp in enunciado.acompanharresposta_set.all():
            aluno = resp.aluno
            ctx = {
                'aluno': aluno,
                'aluno_de': de,
                'resposta': instance
            }
            enviar_email(
                'email/acompanhar-enunciado.html',
                u'Nova resposta para o enunciado que você acompanha',
                [aluno.email], ctx, ead=True
            )


class RespostaComentario(models.Model):
    resposta = models.ForeignKey(
        verbose_name="Resposta", to=Resposta, related_name='comentarios'
    )
    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno'
    )
    comentario = models.TextField(
        verbose_name="Comentário"
    )
    data = models.DateTimeField(
        verbose_name="Data", auto_now_add=True, blank=True, help_text=u"Data de criação."
    )

    class Meta:
        ordering = ['-data']

    @property
    def str_data(self):
        return pretty_date(self.data)


# ---------------------------------------------
# NOTA DAS RESPOSTAS
# ---------------------------------------------
class NotaResposta(models.Model):
    """
    Cadastro de Notas
    O Aluno pode dar uma nota a Resposta, informando se ela está 'correta'
    se ela é 'razoável' ou se está 'errada'.
    """
    class Meta:
        verbose_name = u"Nota da Resposta"
        verbose_name_plural = u"Notas das Respostas"
        unique_together = ('aluno', 'resposta')

    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno'
    )
    resposta = models.ForeignKey(
        verbose_name=u"Resposta", to=Resposta
    )
    nota = models.PositiveSmallIntegerField(
        verbose_name=u"Nota"
    )
    data = models.DateTimeField(
        verbose_name="Data", auto_now_add=True, blank=True, help_text=u"Data de criação."
    )

    def __unicode__(self):
        return u'{0}'.format(self.nota)

    @property
    def str_data(self):
        return pretty_date(self.data)

    def get_color(self):
        nota = self.nota
        if isinstance(nota, (unicode, str)):
            nota = int(nota)
        if nota in [0, 1, 2, 3, 4, 5, 6]:
            ret = ''
        elif nota in [7, 8]:
            ret = 'orange'
        else:
            ret = 'greenc'
        return ret

@receiver(post_save, sender=NotaResposta)
def model_post_save(sender, **kwargs):
    instance = kwargs['instance']
    media = instance.resposta.get_media
    instance.resposta.media = media
    instance.resposta.save()


# ---------------------------------------------
# SEGUIR RESPOSTA
# ---------------------------------------------
@python_2_unicode_compatible
class SeguirComentario(models.Model):
    class Meta:
        verbose_name = "Seguir Comentário"
        verbose_name_plural = "Seguir Comentários"
        unique_together = ('aluno', 'resposta')

    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno'
    )
    resposta = models.ForeignKey(
        verbose_name="Resposta", to=Resposta
    )

    def __str__(self):
        return "S.{}".format(self.id)


# ---------------------------------------------
# CURTIR COMENTARIO
# ---------------------------------------------
@python_2_unicode_compatible
class CurtirComentario(models.Model):
    class Meta:
        verbose_name = "Curtit Comentário"
        verbose_name_plural = "Curtir Comentários"
        unique_together = ('aluno', 'comentario')

    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno'
    )
    comentario = models.ForeignKey(
        verbose_name="Comentário", to=RespostaComentario
    )

    def __str__(self):
        return "S.{}".format(self.id)


# ---------------------------------------------
# Coletania
# ---------------------------------------------
@python_2_unicode_compatible
class Coletania(models.Model):
    class Meta:
        verbose_name = "Coletânea"
        verbose_name_plural = "Coletâneas"
        unique_together = ('aluno', 'resposta')

    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno'
    )
    resposta = models.ForeignKey(
        verbose_name=u"Resposta", to=Resposta
    )

    def __str__(self):
        return "C.{}".format(self.resposta)


# ---------------------------------------------
# CORREÇÕES DAS RESPOSTAS
# ---------------------------------------------
class Correcao(models.Model):
    """
    Cadastro de Correções
    """
    class Meta:
        verbose_name = u"Correção"
        verbose_name_plural = u"Correções"
        ordering = ['-data']

    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno'
    )
    resposta = models.ForeignKey(
        verbose_name="Resposta", to=Resposta
    )
    texto = models.TextField(
        verbose_name="Texto", help_text=u"Texto contendo a Correção da Resposta."
    )
    data = models.DateTimeField(
        verbose_name="Data", auto_now_add=True, blank=True, help_text=u"Data de correção."
    )
    excluir = models.BooleanField(
        verbose_name='Excluir', default=False,
        help_text=u"Marque para excluir a resposta e enviar um email informando o motivo."
    )
    excluir_motivo = models.TextField(
        verbose_name="Motivo", blank=True, null=True,
        help_text=u'Mensagem que será enviada informando o motivo da exclusão da correção.'
    )


    def __unicode__(self):
        return u'{0:06d}'.format(self.id)

    @property
    def str_data(self):
        return pretty_date(self.data)

    @property
    def anterior(self):
        return Correcao.objects.filter(
            data__lt=self.data, resposta=self.resposta
        ).exclude(id=self.id).order_by('id').last()

    @property
    def proxima(self):
        return Correcao.objects.filter(
            data__gt=self.data, resposta=self.resposta
        ).order_by('id').exclude(id=self.id).first()

    @property
    def get_avaliacao_positiva(self):
        """
        Obtem a quantidade de avaliações positivas para essa correção
        :rtype : int
        """
        return self.avaliacaocorrecao_set.filter(tipo=1).count()

    @property
    def get_avaliacao_negativa(self):
        """
        Obtem a quantidade de avaliações negativas para essa correção
        :rtype : int
        """
        return self.avaliacaocorrecao_set.filter(tipo=0).count()

    @models.permalink
    def get_absolute_url(self):
        return 'enunciado:correcao', ([self.id])

    @property
    def qtda_char(self):
        return len(html2text(self.texto).replace('\n', ''))

    @property
    def get_nota_resposta(self):
        try:
            nota = NotaResposta.objects.get(aluno=self.aluno, resposta=self.resposta)
            nota = nota.nota
        except:
            nota = 0
        return nota

    def send_email_aluno(self):
        """
        envia email ao aluno dono da resposta avisando que ele recebeu uma correcao
        :return:
        """
        receber_email = self.resposta.aluno.notificar_correcao
        if receber_email:
            enviar_email(
                'email/acompanhar-enunciado.html',
                u'Alguém corrigiu sua resposta ao enunciado {0}'.format(self.resposta.enunciado),
                [self.resposta.aluno.email],
                {'correcao': self}, ead=True
            )
        return receber_email


@receiver(post_save, sender=Correcao)
def correcao_save(sender, **kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        de = instance.aluno
        para = instance.resposta.aluno
        tipo = 'C'
        criar_notificacao(
            aluno_id=de.id,
            para_id=para.id,
            tipo=tipo,
            correcao_id=instance.id
        )
        criar_notificacao(
            aluno_id=de.id,
            para_id=de.id,
            tipo=tipo,
            correcao_id=instance.id
        )
        # NOTIFICAR SEGUIDORES
        for seguidor in de.get_seguidores.all():
            if seguidor.de_aluno != instance.resposta.aluno:
                criar_notificacao(
                    aluno_id=de.id,
                    para_id=seguidor.de_aluno.id,
                    tipo=tipo,
                    correcao_id=instance.id
                )
        # ENVIAR EMAIL
        instance.resposta.send_mail = False
        instance.send_email_aluno()


# ---------------------------------------------
# COMENTÁRIO DAS RESPOSTAS
# ---------------------------------------------
class ComentarioCorrecao(models.Model):
    """
    Cadastro de Comentario das Coreções
    """
    class Meta:
        verbose_name = u"Comentário da Resposta"
        verbose_name_plural = u"Comentários das Respostas"
        ordering = ['-data']

    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno'
    )
    correcao = models.ForeignKey(
        verbose_name=u"Resposta", to=Correcao
    )
    comentario = models.TextField(
        verbose_name=u"Nota"
    )
    data = models.DateTimeField(
        verbose_name="Data", auto_now_add=True, blank=True, help_text=u"Data de criação."
    )

    @property
    def str_data(self):
        return pretty_date(self.data)

    def send_email_aluno(self):
        """
        envia email ao aluno dono da resposta avisando que ele recebeu uma curtida
        :return:
        """
        receber_email = self.correcao.aluno.notificar_comentario
        if receber_email:
            enviar_email(
                'email/email-comentario-avisar-aluno.html', u'Alguém comentou sua Correção #{0}'.format(self.correcao),
                [self.correcao.aluno.email], {'correcao': self.correcao, 'comentario': self.comentario}, ead=True
            )
        return receber_email


@receiver(post_save, sender=ComentarioCorrecao)
def comentario_correcao_save(sender, **kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        de = instance.aluno
        para = instance.correcao.aluno
        tipo = 'M'

        criar_notificacao(
            aluno_id=de.id,
            para_id=para.id,
            tipo=tipo,
            correcao_id=instance.correcao.id
        )
        criar_notificacao(
            aluno_id=de.id,
            para_id=de.id,
            tipo=tipo,
            correcao_id=instance.correcao.id
        )
        # NOTIFICAR SEGUIDORES
        for seguidor in de.get_seguidores.all():
            criar_notificacao(
                aluno_id=de.id,
                para_id=seguidor.de_aluno.id,
                tipo=tipo,
                correcao_id=instance.correcao.id
            )
        # ENVIAR EMAIL
        instance.send_email_aluno()


# ---------------------------------------------
# AVALIAÇÃO DA CORREÇÃO
# ---------------------------------------------
class AvaliacaoCorrecao(models.Model):
    """
    Cadastro de Correções
    """
    class Meta:
        verbose_name = u"Avaliação da Correção"
        verbose_name_plural = u"Avaliações das Correções"
        unique_together = ('aluno', 'correcao')

    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno'
    )
    correcao = models.ForeignKey(
        verbose_name=u"Correção", to=Correcao
    )
    tipo = models.SmallIntegerField(
        verbose_name="Tipo", choices=[(0, 'Negativa'), (1, 'Positiva')], default=1,
        help_text=u"Informe se a Avaliação foi Negativa/Positiva"
    )
    data = models.DateTimeField(
        verbose_name="Data", auto_now_add=True, blank=True, help_text=u"Data da Avaliação."
    )

    def send_email_aluno(self):
        """
        envia email ao aluno dono da resposta avisando que ele recebeu uma curtida
        :return:
        """
        receber_email = self.correcao.aluno.notificar_avaliacao
        if receber_email:
            t = loader.get_template('email/email-avaliacao-avisar-aluno.html')
            c = Context({'avaliacao': self, 'dominio': SITEADD})
            rendered = t.render(c)
            send_mail(
                u'Alguém curtiu sua Correção #{0}'.format(self.correcao),
                '',
                EMAIL_HOST_USER,
                [self.correcao.aluno.email],
                html=rendered
            )
        return receber_email


@receiver(post_save, sender=AvaliacaoCorrecao)
def avaliacao_correcao_save(sender, **kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        de = instance.aluno
        para = instance.correcao.aluno
        tipo = 'L'

        criar_notificacao(
            aluno_id=de.id,
            para_id=para.id,
            tipo=tipo,
            correcao_id=instance.correcao.id
        )
        criar_notificacao(
            aluno_id=de.id,
            para_id=de.id,
            tipo=tipo,
            correcao_id=instance.correcao.id
        )
        # ENVIAR EMAIL
        instance.send_email_aluno()


@python_2_unicode_compatible
class RoteiroEstudo(models.Model):
    class Meta:
        verbose_name = "Roteiro"
        verbose_name_plural = "Roteiros"
        ordering = ['nome']

    nome = models.CharField(
        verbose_name="Título", max_length=150, unique=True
    )
    edital = models.BooleanField(
        verbose_name="É edital?"
    )
    slug = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

    @models.permalink
    def get_absolute_url(self):
        return 'enunciado:roteiro', (self.slug,)

    @property
    def get_total(self):
        total = 0
        for item in self.itens.all():
            total += item.get_total_enunciados()
        return total


@python_2_unicode_compatible
class RoteiroEstudoItem(models.Model):
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"
        ordering = ['nome']

    nome = models.CharField(
        verbose_name=u'Título', max_length=150, unique=True
    )
    roteiro = models.ForeignKey(
        verbose_name="Roteiro", to=RoteiroEstudo, related_name='itens'
    )
    slug = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

    @models.permalink
    def get_absolute_url(self):
        return 'enunciado:roteiro-item', (self.roteiro.slug, self.slug)

    def tags(self):
        tags = []
        for sub in self.subitens.all():
            for tag in sub.tags.all():
                if tag not in tags:
                    tags.append(tag)
        return tags

    def get_enunciados(self):
        tags = self.tags
        if tags:
            ret = EnunciadoProposta.objects.filter(tags__in=tags)
        else:
            ret = None
        return ret

    def get_total_enunciados(self):
        enun = self.get_enunciados()
        ret = 0
        if enun:
            ret = enun.count()
        return ret


@python_2_unicode_compatible
class RoteiroEstudoSubItem(models.Model):
    class Meta:
        verbose_name = "Sub-Item"
        verbose_name_plural = "Sub-Itens"
        ordering = ['order']
        unique_together = ['nome', 'item']

    nome = models.CharField(verbose_name=u'Título', max_length=150)
    item = models.ForeignKey(
        verbose_name="Item", to=RoteiroEstudoItem, related_name='subitens'
    )
    tags = models.ManyToManyField(
        verbose_name="Tags", to=Tag, blank=True
    )
    order = models.PositiveIntegerField(
        verbose_name="Ordem"
    )
    slug = AutoSlugField(populate_from='nome')

    @models.permalink
    def get_absolute_url(self):
        return 'enunciado:roteiro-sub-item', (self.item.roteiro.slug, self.item.slug, self.slug)

    def __str__(self):
        return self.nome

    def get_enunciados(self):
        tags = self.tags.all()
        if tags:
            ret = EnunciadoProposta.objects.filter(tags__in=tags)
        else:
            ret = None
        return ret

    def get_total_enunciados(self):
        enun = self.get_enunciados()
        ret = 0
        if enun:
            ret = enun.count()
        return ret


class RankingPremiado(models.Model):
    class Meta:
        verbose_name = "Ranking Premiado"
        verbose_name_plural = "Ranking's Premiado"
        ordering = ['-data_ini', '-data_fim', 'encerrado']

    nome = models.CharField(
            verbose_name=u'Título', max_length=200
    )
    tipo_ranking = models.CharField(
        verbose_name='Tipo de Ranking', max_length=1,
        choices=[('T', 'Todos'), ('R', 'Elaborar Respostas'), ('C', 'Corrigir Respostas')]
    )
    tipo_enunciado = models.CharField(
        verbose_name='Tipo de Enunciado', max_length=2,
        choices=[('T', 'Todos'), ('QD', u'Questão'), ('PP', u'Peça'), ('ST', u'Sentença')]
    )
    texto = models.TextField(verbose_name=u'Conteúdo')
    data_ini = models.DateTimeField(verbose_name=u'Data de ínicio')
    data_fim = models.DateTimeField(
            verbose_name=u'Data de término'
    )
    premio = models.CharField(
            verbose_name=u'Prêmio', max_length=255
    )
    imagem = ImageField(
            verbose_name="Imagem", blank=True, null=True, upload_to='premios/', help_text="Imagem do prêmio"
    )
    encerrado = models.BooleanField(
        verbose_name='Encerrado', default=False,
            help_text='Quando está opção estiver marcada, o Ranking será exibido no site.'
    )
    slug = models.SlugField(max_length=150, editable=False)

    @property
    def get_status(self):
        now = timezone.now()
        display = '?'
        computar = False
        if self.encerrado:
            display = '<span class="label label-danger pull-right">Finalizado</lanel>'
        else:
            if (self.data_ini <= now) and (self.data_fim >= now):
                display = '<span class="label label-success pull-right">Iniciado</lanel>'
                computar = True
            elif self.data_ini > now:
                display = '<span class="label label-warning pull-right">A ser iniciado</lanel>'
            elif self.data_fim < now:
                display = '<span class="label label-info pull-right   ">Em finalização</lanel>'
                computar = True

        return {
            'display': display,
            'computar': computar
        }

    @property
    def get_tipo(self):
        ret = ''
        if self.tipo_ranking == 'T':
            if self.tipo_enunciado == 'T':
                ret = u'Quem tiver maior produtividade geral no JusTutor, de acordo com a tabela de pontuação'
            else:
                ret = u'Quem mais Elaborar e Responder qualquer tipo de Enunciado {0}'.format(
                    self.get_tipo_enunciado_display()
                )
        else:
            if self.tipo_enunciado == 'T':
                ret = u'{0} de todos os tipos'.format(self.get_tipo_ranking_display())
            else:
                ret = u'Quem mais {0} do tipo {1}'.format(self.get_tipo_ranking_display(),
                                                          self.get_tipo_enunciado_display())
        return ret

    def __unicode__(self):
        return self.nome

    def get_premios(self):
        ret = []
        inc = 2
        for premio in self.rankingpremiadopremio_set.all():
            ret.append({
                'pos': inc,
                'premio': premio
            })
            inc += 1
        return ret

    def ranking(self, computar=False):
        if not self.get_status.get('computar') and not computar:
            return []

        model_aluno = get_model('aluno', 'Aluno')
        aluno_ids = []
        alunos_respostas = Resposta.objects.filter().values('aluno').annotate(total=Count('aluno')).order_by('-total')
        aluno_ids += map(lambda x: x.get('aluno'), alunos_respostas)

        alunos_correcoes = Correcao.objects.filter().values('aluno').annotate(total=Count('aluno')).order_by('-total')
        aluno_ids += map(lambda x: x.get('aluno'), alunos_correcoes)

        # alunos_avaliacoes = AvaliacaoCorrecao.objects.filter().values('aluno').annotate(total=Count('aluno')).order_by('-total')
        # aluno_ids += map(lambda x: x.get('aluno'), alunos_avaliacoes)
        new = []

        for x in aluno_ids:
            if not x in new:
                new.append(x)

        alunos = model_aluno.objects.filter(id__in=list(aluno_ids))
        ret_dict = []

        for aluno in alunos:
            ret = []
            total_pontos = 0
            datai = self.data_ini
            dataf = self.data_fim
            tipo = False
            if self.tipo_enunciado != 'T':
                tipo = self.tipo_enunciado

            if self.tipo_ranking == 'T':
                # PONTOS POR CORRIGIREM
                for pt in aluno.get_total_corrigirem(datai=datai, dataf=dataf, tipo=tipo):
                    total = pt.get('total') * FLAG_PONTOS_CORRIGIREM.get(pt.get('classificacao'))
                    total_pontos += total
                    ret.append({
                        'y': total,
                        'name': u'{1} - Correções recebidas ({0})'.format(
                            pt.get('total'), FLAG_TIPO_ENUNCIADO_P.get(pt.get('classificacao'))
                        )
                    })

                pt_aval = aluno.get_pontos_avaliacao(datai=datai, dataf=dataf, tipo=tipo)
                if pt_aval:
                    total = pt_aval
                    total_pontos += total
                    ret.append({
                        'y': total,
                        'name': u'Avaliações úteis ({0})'.format(pt_aval)
                    })

            if self.tipo_ranking in ['T', 'R']:
                # PONTOS POR RESPONDER
                for pt in aluno.get_total_respondidos(datai=datai, dataf=dataf, tipo=tipo):
                    total = pt.get('total') * FLAG_PONTOS_RESPONDER.get(pt.get('classificacao'))
                    total_pontos += total
                    ret.append({
                        'y': total,
                        'name': u'{1} - Respostas elaboradas ({0})'.format(
                            pt.get('total'), FLAG_TIPO_ENUNCIADO_P.get(pt.get('classificacao'))
                        )
                    })
            # PONTOS POR CORRIGIR
            if self.tipo_ranking in ['T', 'C']:
                for pt in aluno.get_total_corrigir(datai=datai, dataf=dataf, tipo=tipo):
                    total = pt.get('total') * FLAG_PONTOS_CORRIGIR.get(pt.get('classificacao'))
                    total_pontos += total
                    ret.append({
                        'y': total,
                        'name': u'{1} - Correções de respostas ({0})'.format(
                            pt.get('total'), FLAG_TIPO_ENUNCIADO_P.get(pt.get('classificacao'))
                        )
                    })
            if total_pontos:
                ret_dict.append({'pieData': json.dumps(ret), 'aluno': aluno, 'total': total_pontos})
        return sorted(ret_dict, key=lambda x: x.get('total'), reverse=True)


class RankingPremiadoPremio(models.Model):
    class Meta:
        verbose_name = u" Premiação - Ranking Premiado"
        verbose_name_plural = u"Premiações - Ranking Premiado"

    premio = models.CharField(
            verbose_name=u'Prêmio', max_length=255
    )
    imagem = ImageField(
            verbose_name="Imagem", blank=True, null=True, upload_to='premios/', help_text="Imagem do prêmio"
    )
    ranking_premiado = models.ForeignKey(
        verbose_name='Ranking Premiado', to=RankingPremiado
    )

    def __unicode__(self):
        return self.premio


class RankingPremiadoRanking(models.Model):
    class Meta:
        verbose_name = u"Ranking"
        verbose_name_plural = u"Ranking"
        ordering = ['-pontos', '-total', '-dt_cadastro']

    ranking_premiado = models.ForeignKey(
        verbose_name='Ranking Premiado', to=RankingPremiado
    )
    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno'
    )
    pontos = models.PositiveSmallIntegerField(
        verbose_name='Pontos'
    )
    total = models.PositiveSmallIntegerField(
        verbose_name='Total Pontos'
    )
    dt_cadastro = models.DateTimeField(
        verbose_name='Data Cadastro'
    )

    def __unicode__(self):
        return self.ranking_premiado.nome


class ResponderDepois(models.Model):

    class Meta:
        verbose_name = 'Responder depois'
        unique_together = ['aluno', 'enunciado']
        ordering = ['-data']

    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno'
    )
    enunciado = models.ForeignKey(
        verbose_name=u"Enunciado", to=EnunciadoProposta
    )
    data = models.DateField(
        verbose_name='Data', default=timezone.now
    )

    def __unicode__(self):
        return u'{0}'.format(self.enunciado)

    @property
    def respondido(self):
        return Resposta.objects.filter(aluno=self.aluno, enunciado=self.enunciado, ativo=True, concluido=True).first()


class AcompanharResposta(models.Model):

    class Meta:
        verbose_name = 'Acompanhar resposta'
        verbose_name_plural = 'Respostas acompanhadas'
        unique_together = ['aluno', 'enunciado']
        ordering = ['-data', '-id']

    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno'
    )
    enunciado = models.ForeignKey(
        verbose_name=u"Enunciado", to=EnunciadoProposta
    )
    data = models.DateField(
        verbose_name='Data', default=timezone.now
    )

    def __unicode__(self):
        return u'{0}'.format(self.enunciado)

    @property
    def respondidos(self):
        return Resposta.objects.filter(enunciado=self.enunciado, ativo=True, concluido=True).count()


@receiver(post_save, sender=RankingPremiado)
def rankingpremiado_post_save(sender, **kwargs):
    instance = kwargs['instance']
    encerrado = instance.encerrado
    if encerrado:
        if not instance.rankingpremiadoranking_set.count():
            for r in instance.ranking(True):
                aluno = r.get('aluno')
                rkg = RankingPremiadoRanking(
                    ranking_premiado=instance,
                    aluno=aluno,
                    pontos=r.get('total'),
                    total=aluno.get_pontos_total(dataf=instance.data_fim),
                    dt_cadastro=aluno.usuario.date_joined
                )
                rkg.save()
    else:
        r2 = RankingPremiadoRanking.objects.filter(ranking_premiado=instance)
        if r2:
            r2.delete()


models.signals.post_save.connect(create_slug, sender=RankingPremiado)
