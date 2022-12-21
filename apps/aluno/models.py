# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Avg
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import linebreaksbr
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import mark_safe
from django_localflavor_br import br_states
from pysendy import Sendy, AlreadySubscribedException
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.fields import ImageField

from apps.enunciado import FLAG_PONTOS_RESPONDER, FLAG_PONTOS_CORRIGIR, FLAG_PONTOS_CORRIGIREM
from apps.enunciado.models import (EnunciadoProposta, AvaliacaoCorrecao, NotaResposta, Correcao, NotificacoesAluno,
                                   Resposta)
from apps.financeiro.models import Credito
from justutorial.settings import SMARTWEB_MMKT_URL, SMARTWEB_MMKT_LIST_ID, SENDY_API_KEY
from libs.db import raw_sql
from libs.util.format import pretty_date
from omie.api import OmieAPI
import logging

logger = logging.getLogger("apps")
omie_api = OmieAPI()


class AlunoManager(models.Manager):
    def get_queryset(self):
        return super(AlunoManager, self).get_queryset().filter(usuario__is_active=True)


@python_2_unicode_compatible
class Aluno(models.Model):
    class Meta:
        ordering = ['nome']

    sexo = models.CharField(
        verbose_name='Sexo', max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')]
    )
    nome = models.CharField(
        verbose_name="Apelido", max_length=150
    )
    nome_completo = models.CharField(
        verbose_name="Nome Completo", max_length=150
    )
    email = models.EmailField(
        verbose_name="e-Mail", unique=True
    )
    usuario = models.OneToOneField(
        User, verbose_name="Usuário"
    )
    email_publico = models.BooleanField(
        verbose_name="Tornar e-mail público", default=False
    )
    # SOCIAL
    cargo = models.CharField(
        verbose_name=u'Ocupação atual', max_length=80, blank=True, null=True
    )
    frase = models.CharField(
        verbose_name='Frase', max_length=140, blank=True, null=True,
        help_text=u'Diga algo sobre você para a comunidade JusTutor'
    )
    url_facebook = models.URLField(
        verbose_name=u'Facebook', blank=True, null=True
    )
    url_flicker = models.URLField(
        verbose_name=u'Flicker', blank=True, null=True
    )
    url_twitter = models.URLField(
        verbose_name=u'Twitter', blank=True, null=True
    )
    url_instagram = models.URLField(
        verbose_name=u'Instagram', blank=True, null=True
    )
    foto = ImageField(
        verbose_name="Foto", blank=True, null=True, upload_to='profile/', help_text="Foto do perfil."
    )
    cpf = models.CharField(
        verbose_name="C.P.F", max_length=14, blank=True, null=True
    )
    rg = models.CharField(
        verbose_name=u"RG", max_length=50, blank=True, null=True
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
    telefone = models.CharField(
        verbose_name=u"Telefone", max_length=15, blank=True, null=True
    )
    celular = models.CharField(
        verbose_name=u"Celular", max_length=15, blank=True, null=True
    )
    newsletter = models.BooleanField(
        verbose_name=u"Newsletter", default=False,
        help_text=u"Receber no e-mail novidades, notícias e promoções especiais."
    )
    termo = models.BooleanField(
        verbose_name=u"Aceitou termo de uso?", default=False,
        help_text=u"Se o Aluno concordou com os Termo e Política de Privacidade do Site."
    )
    data_cadastro = models.DateTimeField(
        verbose_name='Data do Cadastro', default=timezone.now
    )
    # NOTIFICAÇÕES
    notificar_correcao = models.BooleanField(
        verbose_name=u'Notificar Correção', default=True,
        help_text=u'Receber E-mail quando um aluno Corrigir sua Resposta?'
    )
    notificar_comentario = models.BooleanField(
        verbose_name=u'Notificar Comentários', default=True,
        help_text=u'Receber E-mail quando um aluno Comentar sua Correção?'
    )
    notificar_avaliacao = models.BooleanField(
        verbose_name=u'Notificar Avaliação', default=True,
        help_text=u'Receber E-mail quando um aluno Curtir sua Correção?'
    )
    notificar_seguir = models.BooleanField(
        verbose_name=u'Notificar ao ser seguido', default=True,
        help_text=u'Receber E-mail quando um aluno começar a te seguir?'
    )
    notificar_responder_seguir = models.BooleanField(
        verbose_name=u'Notificar ao aluno responder', default=True,
        help_text=u'Receber e-mail toda vez que outro(a) aluno(a) que eu sigo responder uma questão?'
    )
    codigo_cliente_omie = models.BigIntegerField(
        verbose_name=u"Código Omie", blank=True, null=True
    )

    def __str__(self):
        if not self.usuario.is_active:
            return 'Aluno %d' % self.pk
        return self.nome

    @property
    def get_creditos_detalhe(self):
        totais = Credito.totais(self.pk)
        return totais

    def get_creditos(self):
        return self.credito_set.filter(expire_date__lte=timezone.now().date())

    @property
    def get_nome(self):
        if not self.usuario.is_active:
            return 'Aluno %d' % self.pk
        return self.nome_completo or self.nome

    @property
    def get_creditos_amount(self):
        creditos = self.get_creditos_detalhe.get('disponiveis')
        return creditos

    @models.permalink
    def get_absolute_url(self):
        return 'aluno:perfil-aluno', ([self.id])

    def omie_incluir(self, **kwargs):
        result = None
        try:
            result = omie_api.incluir_cliente(
                codigo_interno=self.pk,
                email=self.email,
                nome_completo=self.nome_completo or self.nome,
                cpf_cnpj=self.cpf,
                **kwargs
            )
            codigo_omie = result.get("codigo_cliente_omie")
            if codigo_omie:
                self.codigo_cliente_omie = codigo_omie
                self.save()
        except Exception as err:
            logger.error('%s' % err)
        return result

    @property
    def get_cupons_ativos(self):
        return self.cupom_set.filter(ativo=True, data_limite__gte=timezone.now())

    @property
    def msg_para_naolidas(self):
        return self.mensagem_paraaluno.filter(lido=False)

    @property
    def msg_de_naolidas(self):
        return self.mensagem_dealuno.filter(lido=False)

    @property
    def foto_url(self):
        url = '/static/images/logos/icone24-borda.svg'
        if self.foto:
            url = get_thumbnail(self.foto, '50x50', crop='center', quality=99).url
        return url

    @property
    def minhas_respostas(self):
        return self.resposta_set.filter(concluido=True, ativo=True)

    @property
    def get_notificacoes(self):
        notificacoes = NotificacoesAluno.objects.filter(~Q(aluno=self) & Q(para=self)).order_by('-data')
        return notificacoes

    @property
    def nome_resumido(self):
        if not self.usuario.is_active:
            return 'Aluno %d' % self.pk

        split = self.nome.split()
        if len(split) >= 3:
            return u'{0} {1}. {2}'.format(split[0].capitalize(), split[1][0].upper(), split[2].capitalize())
        elif len(split) >= 2:
            return u'{0} {1}'.format(split[0].capitalize(), split[1].capitalize())
        return u'{0}'.format(self.nome)

    @property
    def minhas_correcoes(self):
        return Correcao.objects.filter(aluno=self)

    @property
    def correcoes_recebidas(self):
        return Correcao.objects.filter(resposta__aluno=self)

    @property
    def minhas_correcoes(self):
        return Correcao.objects.filter(aluno=self)

    def get_total_respondidos(self, datai=False, dataf=False, tipo=False):
        """
        Total de respostas do aluno agrupado por classificação/tipo enunciado
        :return: [{'classificacao': u'QD', 'total': 4}, {'classificacao': u'PP', 'total': 1}]
        """
        args = [Q(resposta__aluno=self), Q(resposta__ativo=True), Q(resposta__concluido=True)]
        if datai and dataf:
            args.append(Q(resposta__data_termino__range=[datai, dataf]))
        if tipo:
            args.append(Q(classificacao=tipo))

        ep = EnunciadoProposta.objects.filter(*args).values('classificacao').annotate(total=Count('classificacao'))
        return ep

    def get_pontos_respondidos(self, datai=False, dataf=False, tipo=False):
        tot = self.get_total_respondidos(datai, dataf, tipo)
        return sum(map(lambda x: x.get('total') * FLAG_PONTOS_RESPONDER.get(x.get('classificacao')), tot))

    def get_total_corrigir(self, datai=False, dataf=False, tipo=False):
        """
        Total de correções do aluno agrupado por classificação/tipo enunciado
        :return: [{'classificacao': u'QD', 'total': 4}, {'classificacao': u'PP', 'total': 1}]
        """
        args = [Q(resposta__correcao__aluno=self), Q(resposta__concluido=True)]
        if datai and dataf:
            args.append(Q(resposta__correcao__data__range=[datai, dataf]))
        if tipo:
            args.append(Q(classificacao=tipo))

        ep = EnunciadoProposta.objects.filter(*args).values('classificacao').annotate(
            total=Count('classificacao')
        )
        return ep

    def get_pontos_corrigir(self, datai=False, dataf=False, tipo=False):
        tot = self.get_total_corrigir(datai, dataf, tipo)
        return sum(map(lambda x: x.get('total') * FLAG_PONTOS_CORRIGIR.get(x.get('classificacao')), tot))

    def get_pontos_avaliar(self, datai=False, dataf=False, tipo=False):
        tot = self.notaresposta_set.all().count()
        return tot

    def get_total_corrigirem(self, datai=False, dataf=False, tipo=False):
        """
        Total de correcoes dos respostas aluno agrupado por classificação/tipo enunciado
        :return: [{'classificacao': u'QD', 'total': 4}, {'classificacao': u'PP', 'total': 1}]
        """
        args = [Q(resposta__correcao__isnull=False), Q(resposta__aluno=self)]
        if datai and dataf:
            args.append(Q(resposta__data_termino__range=[datai, dataf]))
        if tipo:
            args.append(Q(classificacao=tipo))

        ep = EnunciadoProposta.objects.filter(*args).values('classificacao').annotate(total=Count('classificacao'))
        # ep = EnunciadoProposta.objects.filter(*args).\
        #     exclude(resposta__correcao__aluno=self, resposta__concluido=True).values(
        #     'classificacao').annotate(total=Count('classificacao'))
        return ep

    def get_pontos_corrigirem(self, datai=False, dataf=False, tipo=False):
        tot = self.get_total_corrigirem(datai, dataf, tipo)
        try:
            return sum(map(lambda x: x.get('total') * FLAG_PONTOS_CORRIGIREM.get(x.get('classificacao')), tot))
        except:
            return 0

    def get_pontos_avaliacao(self, datai=False, dataf=False, tipo=False):
        args = [Q(correcao__aluno=self)]
        if datai and dataf:
            args.append(Q(data__range=[datai, dataf]))
        if tipo:
            args.append(Q(correcao__resposta__enunciado__classificacao=tipo))

        return AvaliacaoCorrecao.objects.filter(*args).count()

    def get_pontos_total(self, datai=False, dataf=False, tipo=False):
        if dataf and not datai:
            datai = timezone.datetime(2015, 1, 1, 0, 0, 0)
        p = [
            self.get_pontos_corrigir(datai, dataf, tipo),
            self.get_pontos_avaliacao(datai, dataf, tipo),
            self.get_pontos_corrigirem(datai, dataf, tipo),
            self.get_pontos_respondidos(datai, dataf, tipo)
        ]
        return sum(p)

    @property
    def get_media_respostas(self):
        avg = NotaResposta.objects.filter(resposta__aluno=self).aggregate(Avg('nota'))
        if not avg.get('nota__avg'):
            return 0.0
        return avg.get('nota__avg')

    def imagem(self):
        if self.foto:
            return u'<img src="%s" />' % get_thumbnail(self.foto, "50x50", crop='center', quality=95).url
        return

    def subscribe(self):
        res = True
        try:
            s = Sendy(base_url=SMARTWEB_MMKT_URL, api_key=SENDY_API_KEY)
            s.subscribe(
                NomeCompleto=self.nome,
                name=self.nome.split()[0],
                email=self.email,
                list_id=SMARTWEB_MMKT_LIST_ID,
                api_key=SENDY_API_KEY
            )
        except AlreadySubscribedException as e1:
            res = True
        except Exception as e2:
            res = False
            raise e2
        self.newsletter = res
        self.save()
        return res

    imagem.short_description = 'Foto'
    imagem.allow_tags = True


@receiver(post_save, sender=Aluno)
def aluno_save(sender, **kwargs):
    from apps.website.utils import enviar_email
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        aluno = instance
        enviar_email(
            'email/email-cadastro-aluno.html',
            "Seja bem-vindo ao JusTutor!",
            [aluno.email], {}
        )

        # t = loader.get_template('email/email-cadastro-aluno.html')
        # c = Context({
        #     'dominio': SITEADD,
        # })
        # rendered = t.render(c)
        # send_mail(
        #     u'Seja bem-vindo ao JusTutor!',
        #     '',
        #     EMAIL_HOST_USER,
        #     [aluno.email],
        #     html=rendered
        # )


def aluno_from_user_request(request):
    aluno = False
    try:
        aluno = request.user.aluno
    except:
        pass
    return aluno


class Seguir(models.Model):
    class Meta:
        unique_together = [('de_aluno', 'para_aluno'), ('para_aluno', 'de_aluno')]

    de_aluno = models.ForeignKey(
        verbose_name='De', to=Aluno, related_name='get_seguindo'
    )
    para_aluno = models.ForeignKey(
        verbose_name='Para', to=Aluno, related_name='get_seguidores'
    )

    def __unicode__(self):
        return u'<de: {0}> <para: {1}>'.format(self.de_aluno.nome, self.para_aluno.nome)


@python_2_unicode_compatible
class Mensagem(models.Model):
    class Meta:
        ordering = ['-data']

    de_aluno = models.ForeignKey(
        verbose_name='De', to=Aluno, help_text='Aluno que enviou a mensagem.', related_name='mensagem_dealuno'
    )
    para_aluno = models.ForeignKey(
        verbose_name='Para', to=Aluno, help_text='Aluno que recebeu a mensagem.', related_name='mensagem_paraaluno'
    )
    mensagem = models.TextField(
        verbose_name='Mensagem'
    )
    lido = models.BooleanField(
        default=False
    )
    data = models.DateTimeField(
        verbose_name='Data', default=timezone.now
    )

    def __str__(self):
        return "<de: {0}> - <para: {1}>".format(self.de_aluno, self.para_aluno)

    @property
    def str_data(self):
        return pretty_date(self.data)

    @property
    def html(self):
        return mark_safe(linebreaksbr(self.mensagem))


class FormacaoAcademica(models.Model):
    class Meta:
        verbose_name = u"Formação Acadêmica"
        verbose_name = u"Formações Acadêmicas"

    aluno = models.ForeignKey(
        verbose_name="Aluno", to=Aluno
    )
    instituicao = models.CharField(
        verbose_name=u"Instituição", max_length=100
    )
    ano_inicio = models.PositiveIntegerField(
        verbose_name=u"Início", blank=True, null=True, help_text=u"Ano de início"
    )
    ano_termino = models.PositiveIntegerField(
        verbose_name=u"Termino", blank=True, null=True, help_text=u"Ano de Término ou Previsão de Graduação"
    )
    formacao = models.CharField(
        verbose_name=u"Formação", max_length=100, blank=True, null=True
    )


# ---------------------------------------------
# FILTROS
# ---------------------------------------------
class Filtro(models.Model):
    _anos = map(lambda x: (x, str(x)), range(2000, timezone.now().year + 1))

    aluno = models.ForeignKey(
        verbose_name="Aluno", to=Aluno
    )
    nome = models.CharField(
        verbose_name="Nome", unique=True, max_length=100
    )
    # desatualizado = models.BooleanField(
    #     verbose_name="Desatualizado", default=False, blank=True
    # )
    # respondidas = models.BooleanField(
    #     verbose_name="Respondidas", default=False, blank=True
    # )
    # corrigidas = models.BooleanField(
    #     verbose_name="Corrigidas", default=False, blank=True
    # )
    # avaliadas = models.BooleanField(
    #     verbose_name="Avaliadas", default=False, blank=True
    # )
    # classificacao = models.CharField(
    #     verbose_name=u"Classificação", max_length=2,
    #     choices=[("ST", u"Sentença"), ("PP", u"Peça Prática"), ("QD", u"Questão Discursiva")]
    # )
    esfera_geral = models.ForeignKey(
        verbose_name="Esfera Geral", to='enunciado.EsferaGeral', blank=True, null=True
    )
    esfera_especifica = models.ForeignKey(
        verbose_name=u"Esfera Específica", to='enunciado.EsferaEspecifica', blank=True, null=True
    )
    cargo = models.ForeignKey(
        verbose_name="Cargo", to='enunciado.Cargo', blank=True, null=True
    )
    area_profissional = models.ForeignKey(
        verbose_name=u"Área Profissional", to='enunciado.AreaProfissional',
        blank=True, null=True
    )
    orgao_entidade = models.ForeignKey(
        verbose_name=u"Órgao/Entidade", to='enunciado.OrgaoEntidade', blank=True, null=True
    )
    concurso = models.ForeignKey(
        verbose_name="Concurso", to='enunciado.Concurso', blank=True, null=True
    )
    data_prova = models.PositiveSmallIntegerField(
        verbose_name="Data da Prova", choices=_anos, blank=True, null=True
    )
    disciplina = models.ForeignKey(
        verbose_name=u"Discíplina", to='enunciado.Disciplina', blank=True, null=True
    )
    tipo_procedimento = models.ForeignKey(
        verbose_name="Tipo de Procedimento", to='enunciado.TipoProcedimento', blank=True, null=True
    )
    tipo_sentenca = models.ForeignKey(
        verbose_name=u"Tipo de Sentença", to='enunciado.TipoPecaSentenca', blank=True, null=True
    )
    tipo_peca_pratica = models.ForeignKey(
        verbose_name=u"Tipo de Peça Prática", to='enunciado.TipoPecaPratica', blank=True, null=True
    )
    num_questao_caderno = models.PositiveSmallIntegerField(
        verbose_name=u"Numero da Questão", blank=True, null=True
    )
    organizador = models.ForeignKey(
        verbose_name="Organizador(a)", to='enunciado.Organizador', blank=True, null=True
    )
    localidade = models.ForeignKey(
        verbose_name="Localidade", to='enunciado.Localidade', blank=True, null=True
    )
    texto = models.CharField(
        verbose_name="Texto", blank=True, null=True, max_length=100
    )

    def __unicode__(self):
        return self.nome


def verificar_email(email):
    """
    Verifica se o email esta cadastrado para um usuário
    :param email:
    :return: Boolean
    """
    email_user = User.objects.filter(email=email).exists()
    email_aluno = Aluno.objects.filter(email=email).exists()
    return email_user | email_aluno


def _ranking_top_pontos():
    sql = """
        SELECT
          enunciado_resposta.aluno_id as id,
          CASE enunciado_enunciadoproposta.classificacao
          WHEN 'PP'
            THEN 20 * COUNT(enunciado_enunciadoproposta.classificacao)
          WHEN 'QD'
            THEN 8 * COUNT(enunciado_enunciadoproposta.classificacao)
          WHEN 'ST'
            THEN 20 * COUNT(enunciado_enunciadoproposta.classificacao)
          END                                                  AS total
        FROM enunciado_resposta
          INNER JOIN enunciado_enunciadoproposta ON (enunciado_resposta.enunciado_id = enunciado_enunciadoproposta.id)
        GROUP BY enunciado_resposta.aluno_id, enunciado_enunciadoproposta.classificacao
        ORDER BY aluno_id;
    """
    qry = raw_sql(sql)
    group_aluno = {}
    for row in qry:
        group_aluno.update({
            row.get('id'): (group_aluno.get('id') or 0) + row.get('total')
        })
    return sorted(group_aluno.items(), key=operator.itemgetter(1))


def ranking_top_pontos():
    aluno_ids = []
    alunos_respostas = Resposta.objects.filter().values('aluno').annotate(total=Count('aluno')).order_by('-total')
    aluno_ids += map(lambda x: x.get('aluno'), alunos_respostas)

    alunos_correcoes = Correcao.objects.filter().values('aluno').annotate(total=Count('aluno')).order_by('-total')
    aluno_ids += map(lambda x: x.get('aluno'), alunos_correcoes)

    alunos_avaliacoes = AvaliacaoCorrecao.objects.filter().values('aluno').annotate(total=Count('aluno')).order_by(
        '-total')
    aluno_ids += map(lambda x: x.get('aluno'), alunos_avaliacoes)
    new = []

    for x in aluno_ids:
        if not x in new:
            new.append(x)
    alunos = Aluno.objects.filter(id__in=new)
    r = []
    inc = 0
    for aluno in alunos:
        p = aluno.get_pontos_total()
        if not p:
            continue
        r.append((aluno, p))
        inc += 1
    r = sorted(r, key=lambda aluno: aluno[1])
    r.reverse()
    ret = map(lambda x: x[0], r)
    return ret[:12]
