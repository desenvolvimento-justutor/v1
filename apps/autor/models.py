# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Q, Count, Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django_localflavor_br import br_states
from mptt.models import MPTTModel
from smart_selects.db_fields import ChainedForeignKey
from sorl.thumbnail.fields import ImageField

from apps.aluno.models import Aluno
from apps.enunciado.models import Disciplina, EsferaGeral, EsferaEspecifica, \
    Cargo, OrgaoEntidade, Concurso, AreaProfissional, Organizador, Localidade
from libs.util.format import timedelta_str, convert_timedelta
from libs.util.tipos import DDDS

ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'


@python_2_unicode_compatible
class Autor(models.Model):
    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = "Autores"

    user = models.OneToOneField(
        verbose_name=u"Usuário", to=User, related_name='autor'
    )
    nome = models.CharField(
        verbose_name="Nome", max_length=200, help_text="Nome completo"
    )
    cpf = models.CharField(
        verbose_name="C.P.F", max_length=14, blank=True, null=True
    )
    rg = models.CharField(
        verbose_name="RG", max_length=50, blank=True, null=True
    )
    rg_orgao = models.CharField(
        verbose_name=u"Orgão Expedidor", max_length=50, blank=True, null=True
    )
    pis = models.CharField(
        verbose_name="PIS/PASEP", max_length=50, blank=True, null=True
    )
    data_nascimento = models.DateField(
        verbose_name="Data Nascimento", blank=True, null=True
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
    # RECEBIMENOS
    tipo_recebimento = models.CharField(
        verbose_name=u"Tipo Recebimento", max_length=1, blank=True, null=True,
        choices=[
            ('F', 'Física'),
            ('J', 'Juridica')
        ], default='F'
    )
    cnpj = models.CharField(
        verbose_name="CNPJ", max_length=14, blank=True, null=True
    )
    endereco = models.TextField(
        verbose_name="Endereço", blank=True, null=True
    )

    def __str__(self):
        return self.nome


@python_2_unicode_compatible
class Banco(models.Model):
    autor = models.ForeignKey(
        verbose_name="Correto", to=Autor
    )
    banco_tipo_conta = models.CharField(
        verbose_name=u"Tipo Conta", max_length=1, blank=True, null=True,
        choices=[
            ('C', 'Corrente'),
            ('P', 'Poupança')
        ]
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


@python_2_unicode_compatible
class AssuntoGeral(models.Model):
    class Meta:
        verbose_name = u"Assunto Geral"
        verbose_name_plural = u"Assuntos Gerais"
        ordering = ['disciplina', 'nome']
        unique_together = [ordering]

    disciplina = models.ForeignKey(
        verbose_name='Disciplina', to=Disciplina,
        on_delete=models.PROTECT
    )
    nome = models.CharField(
        verbose_name="Nome", max_length=200
    )

    def __str__(self):
        return self.nome


@python_2_unicode_compatible
class AssuntoEspecifico(models.Model):
    class Meta:
        verbose_name = u"Assunto Específico"
        verbose_name_plural = u"Assuntos Específicos"
        ordering = ['assunto_geral', 'nome']
        unique_together = [['disciplina', 'assunto_geral', 'nome']]

    disciplina = models.ForeignKey(
        verbose_name='Disciplina', to=Disciplina,
        on_delete=models.PROTECT
    )
    assunto_geral = ChainedForeignKey(
        verbose_name="Assunto Geral", to=AssuntoGeral, related_name='assuntos_gerais',
        chained_field='disciplina', chained_model_field='disciplina'
    )
    nome = models.CharField(
        verbose_name="Nome", max_length=200
    )

    def __str__(self):
        return self.nome


@python_2_unicode_compatible
class Questao(models.Model):
    class Meta:
        verbose_name = "Todas"
        verbose_name_plural = "Todas"
        db_table = 'autor_questaoc'

    codigo = models.CharField(
        verbose_name=u"Código", max_length=10, blank=True
    )
    data_criacao = models.DateTimeField(
        verbose_name='Data de criaçãos', default=timezone.now
    )
    user = models.ForeignKey(
        verbose_name=u"Usuário", to=User, blank=True, null=True, related_name='questao_users'
    )
    autor = models.ForeignKey(
        verbose_name="Autor", to=Autor, related_name='questoe_autor',
        null=True, blank=True
    )
    disciplina = models.ForeignKey(
        verbose_name="Disciplina", to=Disciplina, related_name='questoes'
    )
    assunto_geral = ChainedForeignKey(
        verbose_name="Assunto Geral", to=AssuntoGeral, related_name='questoes_assuntos_gerais',
        chained_field='disciplina', chained_model_field='disciplina'
    )
    assunto_especifico = ChainedForeignKey(
        verbose_name="Assunto Específico", to=AssuntoEspecifico, related_name='questoes_assuntos_especificos',
        chained_field='assunto_geral', chained_model_field='assunto_geral', blank=True, null=True
    )
    tipo = models.CharField(
        verbose_name="Tipo", max_length=1,
        choices=[
            ('C', 'Certo/Errado'),
            ('M', 'Mútipla Escolha'),
        ], default='C'
    )
    nivel = models.CharField(
        verbose_name="Nível", max_length=1,
        choices=[
            ('F', 'Fácil'),
            ('M', 'Médio'),
            ('D', 'Dificil'),
        ], default='F'
    )
    correta = models.BooleanField(
        verbose_name='Correta', default=False,
        help_text='Usado para questões de \'Certo/Errado\'.'
    )
    enunciado = models.TextField(
        verbose_name='Enunciado'
    )
    comentario = models.TextField(
        verbose_name='Comentário', blank=True, null=True
    )
    situacao = models.CharField(
        verbose_name="Situação", max_length=1,
        choices=[
            ('E', 'Em Elaboração'),
            ('A', 'Aguardando Aprovação'),
            ('H', 'Habilitada'),
            ('D', 'Desabilitada'),
            ('N', 'Anulada'),
            ('R', 'Reabilitada após anulação'),
        ], default='E'
    )
    situacao_financeira = models.CharField(
        verbose_name="Situação Financeira", max_length=1,
        choices=[
            ('P', 'Pendente de Pagamento'),
            ('A', 'Paga'),
            ('S', 'Sem Custo')
        ], default='P'
    )
    data_pagamento = models.DateField(
        verbose_name='Data de Pagamento', blank=True, null=True
    )

    def opcoes(self):
        return self.escolhas.all().count()
    opcoes.short_description = u'Opções'

    def __str__(self):
        return self.codigo

    def get_simulados(self):
        simulados = map(
            lambda x: map(
                lambda y: y.simulado, x.disciplina_grupo.grupo_simulado.gruposs.filter(simulado__isnull=False)
            )[0],
            self.questoes_grupo.filter(disciplina_grupo__grupo_simulado__gruposs__isnull=False)
        )
        return simulados

    def simulados(self):
        q = self
        g = QuestaoGrupo.objects.filter(questao=q)
        grupos = GrupoSimulado.objects.filter(disciplinas__questoes__questao=q)
        simulados = []
        for grupo in grupos:
            for g in grupo.gruposs.all():
                s = g.simulado
                if s not in simulados:
                    simulados.append(s)
        return simulados

    def get_escolhas(self):
        return QuestaoEscolha.objects.filter(questao=self)

    @property
    def get_disciplina(self):
        return self.disciplina

    @property
    def anulada(self):
        return self.situacao == 'N'

    def get_correta(self):
        ret = {
            'numeracao': '?',
            'correta': False
        }
        if self.tipo == 'M':
            try:
                q = QuestaoEscolha.objects.get(questao=self, correta=True)
                ret.update(
                    numeracao=q.numeracao,
                    correta=q.correta
                )
            except QuestaoEscolha.DoesNotExist:
                q = QuestaoEscolha.objects.none()
            except QuestaoEscolha.MultipleObjectsReturned:
                raise Exception('>>>>> %s ', self.pk)
        else:
            ret = {
                'numeracao': 'a' if self.correta else 'b',
                'correta': self.correta
            }
        return ret


class QuestaoMManager(models.Manager):
    def get_queryset(self):
        return Questao.objects.get_queryset().filter(tipo='M')


class QuestaoM(Questao):
    class Meta:
        verbose_name = 'Mútipla Escolha'
        verbose_name_plural = 'Mútiplas Escolhas'
        proxy = True

    objects = QuestaoMManager()


class QuestaoCManager(models.Manager):
    def get_queryset(self):
        return Questao.objects.get_queryset().filter(tipo='C')


class QuestaoC(Questao):
    class Meta:
        verbose_name = "Certo ou Errado"
        verbose_name_plural = "Certas ou Erradas"
        proxy = True

    objects = QuestaoCManager()


@python_2_unicode_compatible
class QuestaoEscolha(models.Model):
    class Meta:
        verbose_name = u"Escolha"
        verbose_name_plural = u"Escolhas"
        ordering = ['order', 'questao']

    questao = models.ForeignKey(
        verbose_name="Questão", to=Questao, related_name='escolhas'
    )
    texto = models.TextField(
        verbose_name='Texto da Alternativa',
        help_text='Digite aqui o texto da alternativa'
    )
    comentario = models.TextField(
        verbose_name='Comentário', blank=True, null=True,
        help_text="Digite aqui o comentário do(a) autor(a) sobre a alternativa"
    )
    correta = models.BooleanField(
        verbose_name='Correta?', default=False
    )
    tipo = models.CharField(
        verbose_name='Tipo', max_length=1, choices=[
            ('N', 'Multipla'),
            ('C', 'Correta'),
            ('E', 'Errada'),
        ], default='N', editable=False
    )
    order = models.PositiveIntegerField(
        verbose_name=u'Ordem'
    )

    def __str__(self):
        return '{}'.format(self.texto)

    @property
    def numeracao(self):
        return '{}'.format(ascii_lowercase[self.order])


@python_2_unicode_compatible
class DisciplinaConcurso(models.Model):
    nome = models.CharField(
        verbose_name='Título',
        max_length=200
    )
    disciplinas = models.ManyToManyField(
        verbose_name='Disciplinas JusTutor',
        to=Disciplina
    )

    def __str__(self):
        return self.nome


PREVISTO, ANDAMENTO, ENCERRADO, INDEFINIDO = 'Aguardando', 'Andamento', 'Encerrado', 'Indefinido'
SIMULADO_FLAGS = {
    PREVISTO: {
        'title': 'Aguardando início do prazo',
        'tag': 'warning',
        'bg': 'esmerald'
    },
    ANDAMENTO: {
        'title': 'Simulado em andamento',
        'tag': 'success',
        'bg': 'green',
    },
    ENCERRADO: {
        'title': 'Prazo para resolução do simulado encerrado',
        'tag': 'danger',
        'bg': 'red',
    }
}


@python_2_unicode_compatible
class Simulado(models.Model):
    _anos = map(lambda x: (x, str(x)), range(1989, timezone.now().year + 1))

    nome = models.CharField(
        verbose_name='Título',
        max_length=200
    )
    tipo = models.CharField(
        verbose_name="Tipo", max_length=1,
        choices=[
            ('C', 'Certo/Errado'),
            ('M', 'Mútipla Escolha'),
        ]
    )
    data_inicio = models.DateTimeField(
        verbose_name="Data de início"
    )
    data_fim = models.DateTimeField(
        verbose_name="Data de fim"
    )
    duracao = models.DurationField(
        verbose_name="Duração",
        help_text="Ex: HH:MM / 3:45"
    )
    nota_minima = models.FloatField(
        verbose_name="Nota mínima", default=0,
        validators=[MaxValueValidator(100)],
        help_text="Porcentagem"
    )
    esfera_geral = models.ForeignKey(
        verbose_name="Esfera Geral", to=EsferaGeral, related_name='esferas_gerais_simulado'
    )
    esfera_especifica = ChainedForeignKey(
        verbose_name=u"Esfera Específica", to=EsferaEspecifica,
        chained_field='esfera_geral', chained_model_field='esfera_geral'
    )
    cargo = ChainedForeignKey(
        verbose_name="Cargo", to=Cargo,
        chained_field='esfera_especifica',
        chained_model_field='esfera_especifica',
        null=True
    )
    area_profissional = models.ForeignKey(
        verbose_name=u"Área Profissional", to=AreaProfissional,
        blank=True, null=True
    )
    orgao_entidade = models.ForeignKey(
        verbose_name=u"Órgao/Entidade", to=OrgaoEntidade,
    )
    concurso = models.ForeignKey(
        verbose_name="Concurso", to=Concurso, blank=True, null=True
    )
    data_prova = models.PositiveSmallIntegerField(
        verbose_name="Data da Prova", choices=_anos
    )
    organizador = models.ForeignKey(
        verbose_name="Organizador(a)", to=Organizador
    )
    localidade = models.ForeignKey(
        verbose_name="Localidade", to=Localidade
    )
    texto = models.TextField(
        verbose_name="Texto", help_text=u"Formule um texto para o seu Enunciado.", blank=True, null=True,
    )

    def __str__(self):
        return self.nome

    def get_grupos(self):
        return self.grupos.all().count()

    def get_classificados(self):
        quests = self.questionarios.filter(data_conclusao__isnull=False, aprovado__isnull=False).order_by(
            '-pontuacao', 'data_conclusao', 'aprovado'
        )
        return quests

    def get_questionarios(self):
        quest = self.questionarios.filter(
            data_conclusao__isnull=False
        )

    @property
    def status(self):
        now = timezone.now()
        if self.data_inicio <= now < self.data_fim:
            ret = ANDAMENTO
        elif self.data_inicio > now:
            ret = PREVISTO
        elif now > self.data_fim:
            ret = ENCERRADO
        else:
            ret = INDEFINIDO
        return ret

    @property
    def status_flags(self):
        return SIMULADO_FLAGS.get(self.status)

    @property
    def ativo(self):
        return self.status == ANDAMENTO

    @property
    def encerrado(self):
        return self.status == ENCERRADO

    @property
    def situacao(self):
        now = timezone.now()
        if self.data_inicio <= now < self.data_fim:
            s = "Em andamento"
        elif self.data_inicio > now:
            s = 'Inicio em: {}'.format(self.data_inicio)
        elif now > self.data_fim:
            s = 'Encerrado em: {}'.format(self.data_fim)
        else:
            s = 'Indefinido'
        return s

    @property
    def situacao(self):
        now = timezone.now()
        if now >= self.data_inicio and now < self.data_fim:
            s = "ativo"
        elif self.data_inicio > now:
            s = 'inicia'
        elif now > self.data_fim:
            s = 'encerrado'
        else:
            s = 'indefinido'
        return s

    @property
    def situacao_desc(self):
        situacao_dict = {
            'ativo': {
                'title': 'Simulado em andamento',
                'tag': 'success',
                'bg': 'green',
            },
            'inicia': {
                'title': 'Aguardando início do prazo',
                'tag': 'warning',
                'bg': 'esmerald'
            },
            'encerrado': {
                'title': 'Prazo para resolução do simulado encerrado',
                'tag': 'danger',
                'bg': 'red',
            }
        }
        return situacao_dict.get(self.situacao)

    @property
    def get_time_left(self):
        now = timezone.now()
        date_end = self.data_fim
        time_left = date_end - now
        minutes_left = time_left.total_seconds() / 60
        return {
            'left': time_left,
            'repr': convert_timedelta(time_left),
            'str': timedelta_str(time_left),
            'minutes': int(minutes_left),
            'end': minutes_left <= 0
        }

    def estatisticas(self):

        questionarios = quests = self.questionarios.filter(data_conclusao__isnull=False).order_by(
            'data_conclusao'
        )
        estatisticas = []
        for questionario in questionarios:
            estatisticas.append({
                'questionario': questionario,
                'estatistica': questionario.estatisticas()
            })
        return sorted(estatisticas, key=lambda i: (i['estatistica']['pontos'], i['estatistica']['tempo']), reverse=True)


@python_2_unicode_compatible
class GrupoSimulado(models.Model):
    active = models.BooleanField(
        verbose_name='Ativo',
        default=True
    )
    nome = models.CharField(
        verbose_name='Título',
        max_length=200
    )
    nota_minima = models.FloatField(
        verbose_name="Nota mínima", default=0,
        validators=[MaxValueValidator(100)],
        help_text="Porcentagem"
    )

    def __str__(self):
        return self.nome


@python_2_unicode_compatible
class GrupoDoSimulado(models.Model):
    class Meta:
        unique_together = [
            ['simulado', 'grupo']
        ]

    simulado = models.ForeignKey(
        verbose_name="Simulado", to=Simulado, related_name='grupos'
    )
    grupo = models.ForeignKey(
        verbose_name="Grupo", to=GrupoSimulado, related_name='gruposs'
    )

    def __str__(self):
        return self.grupo.nome

    def get_questoes(self):
        return QuestaoGrupo.objects.filter()


@python_2_unicode_compatible
class DisciplinaGrupo(models.Model):
    class Meta:
        unique_together = [
            ['disciplina', 'grupo_simulado']
        ]
        ordering = ['id']

    disciplina = models.ForeignKey(
        verbose_name="Disciplina", to=DisciplinaConcurso, related_name='disciplinas_grupos'
    )
    peso = models.PositiveSmallIntegerField(
        verbose_name='Peso'
    )
    nota_minima = models.FloatField(
        verbose_name="Nota mínima", default=0,
        validators=[MaxValueValidator(100)],
        help_text="Porcentagem"
    )
    grupo_simulado = models.ForeignKey(
        'GrupoSimulado',
        related_name='disciplinas'
    )

    def __str__(self):
        return self.disciplina.nome

    @property
    def peso_total(self):
        return self.peso + self.questoes.all().count()


@python_2_unicode_compatible
class QuestaoGrupo(models.Model):
    class Meta:
        unique_together = [
            ['questao', 'disciplina_grupo']
        ]
        ordering = ['numeracao']

    numeracao = models.PositiveSmallIntegerField(
        verbose_name="Numeração", default=0
    )
    questao = models.ForeignKey(
        verbose_name="Questão", to=Questao, related_name='questoes_grupo'
    )
    disciplina_grupo = models.ForeignKey(
        'DisciplinaGrupo',
        related_name='questoes'
    )

    def __str__(self):
        # self.objects.filter(disciplina_grupo__grupo_simulado_id=)
        try:
            return '{:02d} - {}'.format(self.numeracao, self.questao.codigo)
        except:
            return '?'

@python_2_unicode_compatible
class QuestionarioAluno(models.Model):
    class Meta:
        verbose_name = "Questionário do Aluno"
        verbose_name_plural = "Questionários do Aluno"

    aluno = models.ForeignKey(
        verbose_name="Aluno", to=Aluno,
        on_delete=models.CASCADE, related_name='aluno_questionario'
    )
    simulado = models.ForeignKey(
        verbose_name="Simulado", to=Simulado, related_name='questionarios'
    )
    data_criacao = models.DateTimeField(
        verbose_name='Data de criaçãos', auto_now_add=True
    )
    data_conclusao = models.DateTimeField(
        verbose_name='Data de conclusão', null=True, blank=True
    )
    timer = models.DurationField(
        verbose_name='Timer', default="00:00:00", editable=False
    )
    pontuacao = models.PositiveSmallIntegerField(
        verbose_name='Pontuação', default=0
    )
    status_questionario = models.CharField(
        verbose_name="Status", max_length=20,
        choices=[
            ('esboco', 'Esboço'),
            ('iniciado', 'Iniciado'),
            ('finalizado', 'Finalizado')
        ], default='esboco'
    )
    status_simulado = models.CharField(
        verbose_name="Status", max_length=20,
        choices=[
            (PREVISTO, PREVISTO),
            (ANDAMENTO, ANDAMENTO),
            (ENCERRADO, ENCERRADO),
            (INDEFINIDO, INDEFINIDO),
        ], null=True, blank=True
    )
    tempo_esgotado = models.BooleanField(
        verbose_name="Tempo esgotado", default=False
    )
    confirmar_visualizar_comentario = models.BooleanField(
        verbose_name="Visualizar confirmação", default=True
    )
    aprovado = models.NullBooleanField(
        verbose_name='Classificado'
    )

    def __str__(self):
        return '{} [{}]'.format(self.simulado.nome, self.aluno.nome)

    def resultado(self):
        return Resultado.objects.get(pk=self.pk)

    def estatisticas(self):
        questionario_aluno = self

        grupo_list = []
        total_pontos = 0
        simulado = questionario_aluno.simulado
        tempo = questionario_aluno.data_conclusao - questionario_aluno.data_criacao
        simulado_duracao = simulado.duracao
        simulado_nota_minima = simulado.nota_minima
        aprovado_geral = True
        # resumo geral
        rg_total_questoes = 0
        rg_total_corretas = 0
        rg_total_erradas = 0
        rg_total_porcento = 0
        rg_total_pontos_questao = 0
        rg_total_pontos = 0
        rg_total_pontos_porcento = 0

        total_pontos_grupo = 0
        simulado_grupos = questionario_aluno.simulado.grupos.all()

        aprovado_grupo = True
        for grupo_do_simulado in simulado_grupos:
            grupo_simulado = grupo_do_simulado.grupo
            args = [
                Q(questao_escolha__correta=True) |
                Q(questao_escolha__questao__situacao='N')
            ]
            grupo_simulado__nota_minima = grupo_simulado.nota_minima
            total_questao_grupo = questionario_aluno.respostas_aluno.filter(
                questao_grupo__disciplina_grupo__grupo_simulado=grupo_simulado
            )

            respostas_corretas_grupo = total_questao_grupo.filter(*args).count()
            porcentagem_acertos_grupo = 0

            if respostas_corretas_grupo:
                porcentagem_acertos_grupo = respostas_corretas_grupo * 100. / total_questao_grupo.count()
            aprovado_g = porcentagem_acertos_grupo >= grupo_simulado__nota_minima
            if not aprovado_g:
                aprovado_geral = False
            ret_grupo = {
                'grupo': grupo_simulado,
                'total_questoes': total_questao_grupo.count(),
                'nota_minima': grupo_simulado__nota_minima,
                'nota_minima_simulado': simulado_nota_minima,
                'respostas_corretas': respostas_corretas_grupo,
                'porcentage_acertos': porcentagem_acertos_grupo,
                'aprovado_grupo': aprovado_g,
                'aprovado_simulado': porcentagem_acertos_grupo >= simulado_nota_minima
            }
            rg_total_questoes += total_questao_grupo.count()  # RES
            rg_total_corretas += respostas_corretas_grupo
            rg_total_erradas += total_questao_grupo.count() - respostas_corretas_grupo

            pontos_grupo = 0
            disciplinas_list = []

            for disciplina_grupo in grupo_simulado.disciplinas.all():
                args_d = [
                    Q(questao_grupo__disciplina_grupo=disciplina_grupo),
                    Q(questao_escolha__correta=True) |
                    Q(questao__situacao='N')
                ]
                disciplina_grupo__nota_minima = disciplina_grupo.nota_minima
                disciplina_grupo__peso = disciplina_grupo.peso
                disciplina_grupo__questoes_total = disciplina_grupo.questoes.all().count()
                disciplina_grupo__peso_total = disciplina_grupo__questoes_total * disciplina_grupo__peso
                total_questao_corretas = questionario_aluno.respostas_aluno.filter(
                    *args_d
                ).count()
                pontos_disciplina = total_questao_corretas * disciplina_grupo__peso

                porcentagem_acertos = 0
                if total_questao_corretas:
                    porcentagem_acertos = total_questao_corretas * 100. / disciplina_grupo__questoes_total
                disciplina_aprovado = porcentagem_acertos >= disciplina_grupo__nota_minima

                total_pontos += pontos_disciplina
                total_pontos_grupo += pontos_disciplina
                if not disciplina_aprovado:
                    aprovado_geral = False
                pontos_grupo += pontos_disciplina

                rg_total_pontos_questao += disciplina_grupo__peso_total
                rg_total_pontos += pontos_disciplina

                args = [
                    Q(questionario_aluno__data_conclusao__isnull=False),
                    Q(questionario_aluno__simulado=simulado),
                    Q(acertou=True),
                    Q(disciplina_grupo=disciplina_grupo)
                ]
                respostas_disciplina_correta_outros = ResultadoResposta.objects.filter(*args). \
                    values('questionario_aluno').annotate(total=Count('questionario_aluno')). \
                    aggregate(total_outros=Avg('total') * 100 / disciplina_grupo__questoes_total)
                disciplina_porcento_outros = respostas_disciplina_correta_outros.get('total_outros')

                ret_disciplina = {
                    'disciplina': disciplina_grupo,
                    'peso': disciplina_grupo__peso,
                    'peso_total': disciplina_grupo__peso_total,
                    'pontos': pontos_disciplina,
                    'total_questoes': disciplina_grupo__questoes_total,
                    'respostas_corretas': total_questao_corretas,
                    'porcentage_acertos': porcentagem_acertos,
                    'aprovado': disciplina_aprovado,
                    'nota_minima': disciplina_grupo__nota_minima,
                    'porcentagem_outros': disciplina_porcento_outros,
                }
                disciplinas_list.append(ret_disciplina)

            # for q in total_questao_corretas:
            #     print q.questao.pk, q.questao_escolha.correta, q.questao.situacao
            # print 'disciplina_grupo__nota_minima', disciplina_grupo__nota_minima
            # print 'disciplina_grupo__peso_total', disciplina_grupo__peso_total
            # print 'disciplina_grupo__questoes', disciplina_grupo__questoes_total
            # print 'total_questao_corretas', total_questao_corretas
            # print 'pontos_disciplina', pontos_disciplina
            # print 'porcentagem_acertos', porcentagem_acertos
            # print 'disciplina_aprovado', disciplina_aprovado
            ret_grupo.update(
                disciplinas=disciplinas_list,
                pontos=pontos_grupo,
            )
            grupo_list.append(
                ret_grupo
            )

        for gs in grupo_list:

            # print 'GRUPO:', gs['grupo']
            # print '-' * 100
            for key, value in gs.iteritems():
                if key == 'disciplinas':
                    continue
                # print '{:<20}: {}'.format(key, value)
            for di in gs['disciplinas']:
                for k, v in di.iteritems():
                    pass
                    # print ' ', k, v

        if rg_total_corretas:
            # print '>>', rg_total_corretas, rg_total_questoes
            rg_total_porcento = rg_total_corretas * 100. / rg_total_questoes

        if rg_total_pontos:
            rg_total_pontos_porcento = rg_total_pontos * 100. / rg_total_pontos_questao
        if aprovado_geral:
            aprovado_geral = rg_total_porcento >= simulado_nota_minima

        ret = {
            'aprovado_geral': aprovado_geral,
            'total_questoes': rg_total_questoes,
            'corretas': rg_total_corretas,
            'erradas': rg_total_erradas,
            'porcento': rg_total_porcento,
            'grupos': grupo_list,
            'pontos': rg_total_pontos,
            'pontos_questao': rg_total_pontos_questao,
            'porcentage_acertos': rg_total_pontos_porcento,
            'tempo': tempo,
            'no_prazo': tempo <= simulado_duracao
        }

        return ret

    @property
    def position(self):
        if not self.data_conclusao:
            return 0
        lst = self.simulado.estatisticas()
        idx = next((index for (index, d) in enumerate(lst) if d["questionario"].pk == self.pk), None)
        return idx + 1

    def get_estatisticas(self):
        return self.estatistica_set.all()

    @property
    def classificado(self):
        return self.estatistica_set.filter(aprovado=True, estatisticadisciplina__aprovado=True).exists()

    @property
    def no_prazo(self):
        simulado_data_fim = self.simulado.data_fim
        if self.data_conclusao:
            return self.data_conclusao <= simulado_data_fim
        return False

    def ranking(self):
        try:
            ranking = QuestionarioAluno.objects.filter(
                pontuacao__lte=self.pontuacao, data_conclusao__lte=self.data_conclusao,
                simulado=self.simulado, data_conclusao__isnull=False
            ).order_by('-pontuacao', 'data_conclusao')
        except:
            ranking = QuestionarioAluno.objects.none()
        print '>>>>>>>.', ranking
        return ranking

    @property
    def edit(self):
        return self.simulado.ativo and not self.data_conclusao

    def create_resposta(self):
        for grupo in self.simulado.grupos.all():
            for disciplina in grupo.grupo.disciplinas.all():
                for questao in disciplina.questoes.all():
                    try:
                        RespostaQuestionarioAluno.objects.create(
                            questionario_aluno=self,
                            questao=questao.questao,
                            questao_grupo=questao,
                        )
                    except:
                        raise Exception('Questao: %d - %s' % (questao.pk, str(questao)))

    def get_respostas_corretas(self):
        return self.respostas_aluno.filter(Q(correta__isnull=False), Q(correta=True) | Q(questao__situacao='N'))

    def get_respostas_corretas_perc(self):
        try:
            ret = self.get_respostas_corretas().count() * 100. / self.get_respostas_total().count()
        except:
            ret = 0
        return ret

    def get_respostas_erradas(self):
        return self.respostas_aluno.filter(Q(correta=False), ~Q(questao__situacao='N'))

    def get_respostas_erradas_perc(self):
        try:
            ret = self.get_respostas_erradas().count() * 100. / self.get_respostas_total().count()
        except:
            ret = 0
        return ret

    def get_respostas_nulas(self):
        return self.respostas_aluno.filter(correta__isnull=True)

    def get_respostas_nulas_perc(self):
        try:
            ret = self.get_respostas_nulas().count() * 100. / self.get_respostas_total().count()
        except:
            ret = 0
        return ret

    def get_respostas_concluidas(self):
        return self.respostas_aluno.filter(Q(questao_escolha__isnull=False) | Q(viu_comentario=True))

    def get_respostas_restantes(self):
        return self.respostas_aluno.filter(Q(questao_escolha__isnull=True), Q(viu_comentario=False))

    def get_respostas_total(self):
        return self.respostas_aluno.all()

    @property
    def get_respostas_percent(self):
        ret = 0
        total = self.get_respostas_total().count()
        concluidas = self.get_respostas_concluidas().count()
        if concluidas:
            ret = concluidas * 100. / total
        return int(ret)

    @property
    def tempo_de_prova(self):
        now = timezone.now()
        if self.data_conclusao:
            return self.data_conclusao - self.data_criacao
        else:
            return now - self.data_criacao

    @property
    def tempo_de_prova_str(self):
        return timedelta_str(self.tempo_de_prova, False)

    @property
    def tempo_restante(self):
        return self.simulado.duracao - self.tempo_de_prova

    @property
    def tempo_restante_str(self):
        return timedelta_str(self.tempo_restante)

    @property
    def status(self):
        if self.data_conclusao:
            s = "finalizado"
        else:
            s = 'pendente'
        return s

    @property
    def finalizado(self):
        return bool(self.data_conclusao)

    @property
    def concluido(self):
        return self.get_respostas_restantes() == 0

    @property
    def status_flags(self):
        situacao_dict = {
            'finalizado': {
                'title': 'Resolução finalizada',
                'tag': 'success',
                'bg': 'green-bg'
            },
            'pendente': {
                'title': 'Resolução pendente',
                'tag': 'warning',
                'bg': 'red-bg'
            }
        }
        return situacao_dict.get(self.status)

    @property
    def pontuacao_final(self):
        q = GrupoDoSimulado.objects.filter(simulado__questionario_simulado=self.simulado)
        d = DisciplinaGrupo.objects.filter(questoes__questoes_grupo__questionario_aluno=self)
        return d

    def update_classificacao(self):
        if self.data_conclusao:
            self.gerar_estatistica()
            classificado = self.estatistica_set.filter(aprovado=True, estatisticadisciplina__aprovado=True)
            self.aprovado = classificado.exists()
            self.save()

    def update_pontos(self, verbose=False):
        self.gerar_estatistica(verbose=True)
        soma = []
        disciplinas = DisciplinaGrupo.objects.filter(grupo_simulado__gruposs__simulado=self.simulado)
        for disciplina in disciplinas:
            pontos = disciplina.peso
            args = [
                Q(questao_grupo__disciplina_grupo__disciplina=disciplina.disciplina),
                Q(correta__isnull=False),
                Q(correta=True) |
                Q(questao__situacao='N')
            ]
            corretas = self.respostas_aluno.filter(*args)
            soma.append(corretas.count() * pontos)
        self.pontuacao = sum(soma)
        r = self.estatistica_set.filter(aprovado=True).exists()
        e = EstatisticaDisciplina.objects.filter(estatistica__questionario_aluno=self, aprovado=True).exists()
        self.aprovado = r & e & sum(soma) >= self.simulado.nota_minima
        self.save()
        return soma

    def gerar_estatistica(self, verbose=False):
        args = [
            Q(correta__isnull=False),
            Q(correta=True) |
            Q(questao__situacao='N')
        ]
        quest = self
        for grupo in quest.simulado.grupos.all():
            verbose_text = []
            min_grupo = grupo.grupo.nota_minima
            total_questao = quest.respostas_aluno.filter(questao_grupo__disciplina_grupo__grupo_simulado=grupo.grupo)
            respostas_corretas = total_questao.filter(*args)
            grupo_perc = 0
            if respostas_corretas:
                grupo_perc = respostas_corretas.count() * 100. / total_questao.count()

            aprovado_q = grupo_perc >= min_grupo
            default_estatistica = dict(
                porcentagem_acertos=grupo_perc,
                aprovado=aprovado_q
            )
            estatistica, create = Estatistica.objects.update_or_create(
                questionario_aluno=quest,
                grupo_simulado=grupo.grupo,
                defaults=default_estatistica
            )
            verbose_text.append(u'ALUNO %s' % quest.aluno)
            verbose_text.append(u'------------------------ -------- --------------- ------------- --------')
            verbose_text.append(u'GRUPO                    Nota Min Total Perguntas Total Acertos Aprovado')
            verbose_text.append(u'------------------------ -------- --------------- ------------- --------')
            verbose_text.append(u'{:<24}{:>9}{:>16}{:>14}{:>9}'.format(
                grupo.grupo.nome[:20], min_grupo, total_questao.count(), grupo_perc,
                u'SIM' if aprovado_q else u'NAO'
            ))
            verbose_text.append(u'-' * 72)
            for disciplina in grupo.grupo.disciplinas.all():
                min_dis = disciplina.nota_minima
                perc = 0

                total = quest.respostas_aluno.filter(
                    questao__questoes_grupo__disciplina_grupo=disciplina
                )
                corretas = total.filter(*args)
                if corretas:
                    perc = corretas.count() * 100. / total.count()

                aprovado_d = perc >= min_dis
                EstatisticaDisciplina.objects.update_or_create(
                    estatistica=estatistica,
                    disciplina_grupo=disciplina,
                    defaults=dict(
                        porcentagem_acertos=perc,
                        aprovado=aprovado_d
                    )
                )
                verbose_text.append(u'{:<24}{:>9}{:>16}{:>14}{:>9}'.format(
                    disciplina.disciplina.nome[:20], min_dis, total_questao.count(), grupo_perc,
                    u'SIM' if aprovado_d else u'NAO'
                ))
            verbose_text.append(u'-' * 72)
            verbose_text.append(u'')
        if verbose:
            print u'\n'.join(verbose_text).encode('utf-8')


CORRETA, ERRADA, ANULADA, EMBRANCO = 'Correta', 'Errada', 'Anulada', 'Em branco'
STATUS_QUESTAO = {
    CORRETA: {
        'icon': 'fa-check',
        'title': CORRETA,
        'color': 'green',
        'correta': True
    },
    ERRADA: {
        'icon': 'fa-close',
        'title': ERRADA,
        'color': 'red',
        'correta': False
    },
    ANULADA: {
        'icon': 'fa-circle',
        'title': ANULADA,
        'color': 'green',
        'correta': True
    },
    EMBRANCO: {
        'icon': 'fa-clircle-o',
        'title': EMBRANCO,
        'color': 'lightgrey',
        'correta': False
    },
}


@python_2_unicode_compatible
class RespostaQuestionarioAluno(models.Model):
    class Meta:
        verbose_name = "Resposta do Questionário do Aluno"
        verbose_name_plural = "Resposta dos Questionários do Aluno"
        ordering = [
            'questao_grupo'
        ]

    questionario_aluno = models.ForeignKey(
        verbose_name="Questionário",
        to=QuestionarioAluno, related_name='respostas_aluno',
        on_delete=models.CASCADE
    )
    questao_grupo = models.ForeignKey(
        verbose_name="Questão Grupo", to=QuestaoGrupo, related_name='questoes_grupo'
    )
    questao = models.ForeignKey(
        verbose_name="Questao", to=Questao, related_name='questoes_f'
    )
    questao_escolha = models.ForeignKey(
        verbose_name="Questão Escolha", to=QuestaoEscolha, related_name='questoes_escolha',
        blank=True, null=True
    )
    correta = models.NullBooleanField(
        verbose_name='Correta', blank=True, null=True
    )
    questao_anulada = models.NullBooleanField(
        verbose_name='Anulada', blank=True, null=True
    )
    respondida = models.BooleanField(
        verbose_name='Respondida', default=False
    )
    viu_comentario = models.BooleanField(
        verbose_name='Respondida', default=False
    )
    data_criacao = models.DateTimeField(
        verbose_name='Data de criaçãos', default=timezone.now
    )

    def resultado(self):
        return ResultadoResposta.objects.get(pk=self.pk)

    def __str__(self):
        q = ''
        if self.questao_escolha:
            q = ': %s' % self.questao_escolha.questao.codigo
        return '{}{}'.format(self.status['title'], q)

    @property
    def status(self):
        if self.anulada:
            status = ANULADA
        elif not self.questao_escolha:
            status = EMBRANCO
        else:
            status = CORRETA if self.questao_escolha.correta else ERRADA
        return STATUS_QUESTAO.get(status)

    def get_correta(self):
        ret = {
            'numeracao': '?',
            'correta': False
        }
        if self.questao.tipo == 'M':
            if self.questao_escolha:
                ret.update(
                    numeracao=self.questao_escolha.numeracao,
                    correta=self.questao_escolha.correta
                )
        else:
            ret = {
                'numeracao': 'a' if self.correta else 'b',
                'correta': self.correta
            }
        return ret

    @property
    def anulada(self):
        return self.questao.situacao == 'N'

    def prev(self):
        try:
            ret = RespostaQuestionarioAluno.objects.filter(
                questionario_aluno=self.questionario_aluno,
                id__lt=self.id
            ).order_by('questao_grupo', 'questao').last()
        except RespostaQuestionarioAluno.DoesNotExist:
            ret = RespostaQuestionarioAluno.objects.none()
        return ret

    def next(self):
        try:
            ret = RespostaQuestionarioAluno.objects.filter(
                questionario_aluno=self.questionario_aluno,
                id__gt=self.id
            ).order_by('questao_grupo__disciplina_grupo__grupo_simulado', 'questao_grupo__numeracao').first()
        except RespostaQuestionarioAluno.DoesNotExist:
            ret = RespostaQuestionarioAluno.objects.none()
        return ret

    @property
    def contem_comentario(self):
        flag = False
        qtda = 0
        if self.questao.tipo == 'M':
            for escolha in self.questao.get_escolhas():
                if escolha.comentario:
                    flag = True
                    break
        else:
            flag = True if self.questao.comentario else False
        return flag

    def comentarios(self):
        args = dict(comentario__isnull=False)
        if self.questao.tipo == 'C':
            args.update(dict(correta=True))
        return self.questao.escolhas.filter(**args)


@receiver(post_save, sender=RespostaQuestionarioAluno)
def save_resposta_questionario_aluno(sender, instance, **kwargs):
    created = kwargs.get('created')
    if not created:
        instance.questionario_aluno.update_pontos()


@python_2_unicode_compatible
class Estatistica(models.Model):
    class Meta:
        unique_together = [
            'questionario_aluno', 'grupo_simulado'
        ]

    questionario_aluno = models.ForeignKey(
        verbose_name='Questionário', to=QuestionarioAluno
    )
    grupo_simulado = models.ForeignKey(
        verbose_name='Grupo', to=GrupoSimulado
    )
    porcentagem_acertos = models.FloatField(
        verbose_name='Acertos (%)', default=0
    )
    aprovado = models.BooleanField(
        verbose_name='Aprovado'
    )

    def __str__(self):
        return self.grupo_simulado.nome


class EstatisticaDisciplina(models.Model):
    class Meta:
        unique_together = [
            'estatistica', 'disciplina_grupo'
        ]

    estatistica = models.ForeignKey(
        verbose_name='Estatistica', to=Estatistica, on_delete=models.CASCADE
    )
    disciplina_grupo = models.ForeignKey(
        verbose_name='Disciplina Grupo', to=DisciplinaGrupo, on_delete=models.CASCADE
    )
    porcentagem_acertos = models.FloatField(
        verbose_name='Acertos (%)', default=0
    )
    aprovado = models.BooleanField(
        verbose_name='Aprovado'
    )


@python_2_unicode_compatible
class Resultado(models.Model):
    id = models.IntegerField(primary_key=True)
    data_criacao = models.DateTimeField(
        verbose_name='Data de criaçãos'
    )
    data_conclusao = models.DateTimeField(
        verbose_name='Data de conclusão'
    )
    aluno = models.ForeignKey(
        verbose_name="Aluno", to=Aluno,
        on_delete=models.CASCADE, related_name='ralunos'
    )
    simulado = models.ForeignKey(
        verbose_name="Simulado", to=Simulado, related_name='simulados'
    )

    class Meta:
        managed = False
        db_table = 'resultado'

    def __str__(self):
        return '{:06d} - {}: [{}]'.format(
            self.id, self.simulado.nome, self.aluno.nome
        )


@python_2_unicode_compatible
class ResultadoResposta(models.Model):
    id = models.IntegerField(primary_key=True)
    questionario_aluno = models.ForeignKey(
        verbose_name="Resultado",
        to=Resultado, related_name='rrespostas', to_field='id', on_delete=models.DO_NOTHING
    )
    questao_grupo = models.ForeignKey(
        verbose_name="Questão Grupo", to=QuestaoGrupo, related_name='rquestoes_grupo', on_delete=models.DO_NOTHING
    )
    questao = models.ForeignKey(
        verbose_name="Questao", to=Questao, related_name='rquestoes', on_delete=models.DO_NOTHING
    )
    questao_escolha = models.ForeignKey(
        verbose_name="Questão Escolha", to=QuestaoEscolha, related_name='rescolhas', on_delete=models.DO_NOTHING
    )
    numeracao = models.SmallIntegerField()
    codigo = models.CharField(max_length=10)
    anulada = models.BooleanField()
    em_branco = models.BooleanField()
    acertou = models.BooleanField()
    errou = models.BooleanField()
    correta = models.BooleanField()
    pontuacao = models.IntegerField()
    grupo_simulado = models.ForeignKey(
        verbose_name='Grupo', to=GrupoSimulado
    )
    grupo = models.ForeignKey(
        verbose_name="Grupo",
        to=GrupoSimulado, on_delete=models.DO_NOTHING,
        related_name='rgrupos'
    )
    disciplina_grupo = models.ForeignKey(
        to=DisciplinaGrupo, on_delete=models.DO_NOTHING,
        related_name='rdisciplinas'
    )
    disciplina_grupo = models.ForeignKey(
        to=DisciplinaGrupo, on_delete=models.DO_NOTHING,
        related_name='rdisciplina_grupos'
    )
    disciplina = models.ForeignKey(
        verbose_name="Disciplina",
        to=DisciplinaConcurso, on_delete=models.DO_NOTHING,
        related_name='rdisciplinas'
    )
    disciplina_peso = models.SmallIntegerField()
    disciplina_nota_minima = models.FloatField()

    class Meta:
        managed = False
        db_table = 'resultado_resposta'

    def __str__(self):
        return self.questionario_aluno.aluno.nome
