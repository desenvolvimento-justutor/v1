# -*- coding: utf-8 -*-
import os
import shlex
import socket
import subprocess
import time
import uuid
from datetime import datetime, timedelta

import django
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import mark_safe
from django_comments.signals import comment_was_posted
from filebrowser.fields import FileBrowseField
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.fields import ImageField

from apps.autor.models import Simulado
from apps.enunciado.models import EsferaEspecifica, TipoProcedimento, Disciplina, TipoPecaPratica
from apps.formulario_correcao.models import TabelaCorrecaoAluno
from apps.website.models import PacoteDesconto
from apps.website.utils import enviar_email
from justutorial.settings import MEDIA_ROOT
from libs.signals import create_slug
from libs.util import shortuuid
from libs.util.format import currency_format, pretty_date


def get_id():
    t = str(time.time())
    return uuid.uuid3(uuid.NAMESPACE_DNS, t).hex


def uuid5():
    return shortuuid.uuid()[:5].upper()


@python_2_unicode_compatible
class Categoria(models.Model):
    class Meta:
        verbose_name = u'Categoria'
        unique_together = ('nome',)

    nome = models.CharField(verbose_name=u'Nome', max_length=50)
    titulo = models.CharField(verbose_name=u'Título', max_length=50, blank=True, null=True,
                              help_text=u"Título que será exibido no menu. Caso não informe será exibido o 'Nome'.")
    # sentenca_avulsa = models.BooleanField(verbose_name="Atividade Avulsa", default=False,
    #                                       help_text="Marque para os cursos de Atividade Avulsa.")
    tipo = models.CharField(
        verbose_name="Tipo", max_length=1, default='C', choices=[
            ('C', 'Curso'),
            ('S', 'Atividade Avulsa'),
            ('O', 'OAB 2ª Fase'),
            ('L', 'Livro'),
            ('B', 'Combo'),
            ('D', 'Simulado'),
            ('P', u'Crédito'),
        ]
    )
    slug = models.SlugField(max_length=60, editable=False)
    order = models.PositiveIntegerField(verbose_name=u'Ordem')

    def __str__(self):
        return u'[{0}] {1}'.format(self.tipo, self.nome)

    @models.permalink
    def get_absolute_url(self):
        if self.tipo == 'L':
            return 'website:livraria', ([self.slug])
        else:
            return 'curso:categoria', ([self.slug])

    @property
    def get_cursos(self):
        now = django.utils.timezone.now()
        cursos = self.curso_set.filter(Q(data_ini__lte=now)).order_by('-data_ini')
        return cursos

    @property
    def get_last_curso(self):
        now = django.utils.timezone.now()
        curso = self.curso_set.filter(Q(data_ini__lte=now)).last()
        return curso

    @property
    def titulo_menu(self):
        return self.titulo or self.nome


@python_2_unicode_compatible
class Autor(models.Model):
    nome = models.CharField(
        verbose_name='Nome', max_length=100
    )
    foto = ImageField(
        verbose_name='Foto', upload_to='professor/', blank=True, null=True
    )
    sobre = models.TextField(
        verbose_name='Sobre', blank=True, null=True
    )

    class Meta:
        verbose_name_plural = 'Autores'

    @property
    def foto_url(self):
        url = '/static/images/logos/icone24-borda.svg'
        if self.foto:
            url = get_thumbnail(self.foto, '50x50', crop='center', quality=99).url
        return url

    def __str__(self):
        return self.nome


@python_2_unicode_compatible
class Colecao(models.Model):
    nome = models.CharField(
        verbose_name='Nome', max_length=100, unique=True
    )

    class Meta:
        verbose_name = 'Coleção'
        verbose_name_plural = 'Coleções'
        ordering = ['nome']

    def __str__(self):
        return self.nome


@python_2_unicode_compatible
class Curso(models.Model):
    class Meta:
        verbose_name = u"Curso"
        unique_together = ('nome',)
        ordering = ['-data_ini']

    categoria = models.ForeignKey(Categoria, verbose_name=u'Categoria')
    limitar_correcao = models.SmallIntegerField(
        verbose_name="Limitar correções", default=0,
        help_text='Limitar quantidade de correções individuais a que o aluno tem direito?'
    )
    sentenca_avulsa = models.OneToOneField(
        verbose_name="Atividade Avulsa", blank=True, null=True, to="SentencaAvulsa")
    sentenca_oab = models.OneToOneField(verbose_name="OAB 2ª Fase", blank=True, null=True, to="SentencaOAB")
    simulado = models.OneToOneField(
        verbose_name="Simulado", to=Simulado,
        blank=True, null=True
    )
    nome = models.CharField(verbose_name=u'Título', max_length=250)
    video = FileBrowseField(
        verbose_name=u"Vídeo Demonstração", max_length=200, extensions=['.mp4'], blank=True, null=True,
        help_text=u'Selecione um vídeo no fotmat .MP4', directory='videos/'
    )
    thumbnail = ImageField(
        verbose_name='Capa', upload_to='videos_thumb/', blank=True, null=True,
        help_text=u'Miniatura que será exibido, se não escolher será gerado automaticamente'
    )
    imagem = ImageField(
        verbose_name=u"Imagem", blank=True, null=True, upload_to='img_thumb/',
        help_text=u'Selecione um imagem de capa que será exibida na listagem dos curso (Tam. 270x170).',

    )
    descricao = models.TextField(verbose_name=u'Apresentação')
    valor = models.DecimalField(verbose_name=u'Valor', max_digits=15, decimal_places=2)
    disponivel = models.BooleanField(verbose_name=u'Turma Disponível?', default=True)
    inicio_gratis = models.BooleanField(verbose_name=u'Início Grátis?', default=False,
                                        help_text=u"Informe caso o curso tenha início grátis.")
    data_ini = models.DateTimeField(verbose_name=u'Data ínicio', default=django.utils.timezone.now, null=True, blank=False,
                                    help_text=u'A partir dessa data o sistema automaticamente '
                                              u'colocará o curso no site')
    data_fim = models.DateTimeField(verbose_name=u'Data final', blank=True, null=True,
                                    help_text=u'A partir dessa data o sistema automaticamente irá marcar o curso '
                                              u'como encerrado')
    professores = models.ManyToManyField(
        'professor.Professor', blank=True
    )
    blocos = models.ManyToManyField(
        verbose_name='Quizz', to='quizz.Bloco',
        blank=True
    )
    saiba_mais = models.TextField(
        verbose_name='Saiba+', null=True, blank=True
    )
    cronograma = models.TextField(
        verbose_name='Cronograma', null=True, blank=True
    )
    certificado_formato = models.CharField(
        verbose_name="Orientação da Página", max_length=20, choices=[
            ('portrait', 'Retrato'),
            ('landscape', 'Paisagem')
        ], blank=True, null=True, default='landscape'
    )
    certificado = models.TextField(
        verbose_name='Certificado', blank=True, null=True
    )
    certificado_data_ini = models.DateField(
        verbose_name="Data emissão", blank=True, null=True,
        help_text="Data para ínicio da emissão do Certificado"
    )
    slug = models.SlugField(max_length=150, editable=True)
    # Sortable property
    order = models.PositiveIntegerField(verbose_name=u'Ordem')
    # SEO
    meta_description = models.CharField(verbose_name=u'Meta Description', blank=True, null=True, max_length=160,
                                        help_text=u'Resumo geral do site. Frase que descreva muito bem o Curso. Quando'
                                                  u' o site for buscado, essa será a frase que aparecerá à quem '
                                                  u'buscar. Melhor utilizar de 25 a 30 palavras com 160 a 180 '
                                                  u'caracteres.')
    meta_keywords = models.CharField(verbose_name=u'Meta Keywords', blank=True, null=True, max_length=100,
                                     help_text=u'Procure usar umas poucas palavras que descrevam o conteúdo do Curso. '
                                               u'Exemplo: climática, previsão climática,desenvolvimento, tempo, '
                                               u'clima. É importante que as palavras estejam no Título e nas Meta '
                                               u'Description.')
    # Livro
    formato = models.CharField(
        verbose_name="Formato", choices=[('D', 'Digital'), ('F', "Físico")], max_length=10, default='D'
    )
    autores = models.ManyToManyField(
        verbose_name="Autores", to=Autor, related_name='autores', blank=True
    )
    colecao = models.ForeignKey(
        verbose_name="Coleção", to=Colecao, related_name='colecoes', blank=True, null=True
    )
    livro = models.FileField(
        verbose_name="Livro", upload_to='livros/amostra/', blank=True, null=True
    )
    isbn = models.CharField(
        verbose_name='ISBN', max_length=13, blank=True, null=True, unique=True
    )
    amostra = models.FileField(
        verbose_name="Amostra", upload_to='livros/amostra/', blank=True, null=True
    )
    sumario = models.FileField(
        verbose_name="Sumário", upload_to='livros/sumario/', blank=True, null=True
    )
    edicao = models.SmallIntegerField(
        verbose_name="Edição", blank=True, null=True
    )
    ano = models.SmallIntegerField(
        verbose_name="Ano", blank=True, null=True
    )
    paginas = models.SmallIntegerField(
        verbose_name="Páginas", blank=True, null=True,
        help_text="Quantidade de Páginas"
    )
    # combo
    economia = models.DecimalField(
        verbose_name="Economia", blank=True, null=True, max_digits=9, decimal_places=2
    )
    cursos = models.ManyToManyField(
        verbose_name="Cursos", to="self", blank=True, null=True
    )
    # COMBO ALUNO
    aluno = models.ForeignKey(
        verbose_name='Aluno', to='aluno.Aluno',
        blank=True, null=True
    )
    status = models.CharField(
        verbose_name='Status', max_length=1,
        choices=[
            ('A', 'Aberto'),
            ('C', 'Carrinho'),
            ('F', 'Finalizado')
        ], default='A'
    )

    def __str__(self):
        return u'{}'.format(self.nome)

    def matriculas(self):
        chk = self.checkoutitens_set.filter(
        )
        return chk.count()

    def matriculados(self):
        chk = self.checkoutitens_set.filter(
            checkout__transaction__status='pago'
        )
        return chk.count()

    matriculados.short_description = 'Pagantes'
    matriculas.short_description = 'Matriculados'

    def save(self):
        if self.video and not self.thumbnail:
            self.create_screenshot()
        super(Curso, self).save()

    def create_screenshot(self):
        video_file = self.video
        if video_file:
            png_filename = u'{0}.png'.format(video_file.filename)
            png_file = os.path.join(MEDIA_ROOT, 'videos_thumb', png_filename)
            if not os.path.exists(png_file):
                command = u"ffmpeg -y -i '{0:s}' -ss 00:00:05 -vframes 1 '{1:s}'".format(video_file.path_full, png_file)
                subprocess.call(shlex.split(command))
            self.thumbnail = os.path.join('videos_thumb', png_filename)

    @property
    def get_alunos(self):
        cks = self.checkoutitens_set.all().order_by('checkout__aluno')
        alunos = []
        for x in cks:
            try:
                trans = x.checkout.transaction
            except:
                continue
            if trans:
                if trans.status in ['pago', 'disponivel']:
                    alunos.append(x.checkout.aluno)
        return alunos

    @models.permalink
    def get_absolute_url(self):
        if self.categoria.tipo == 'L':
            return 'website:livro', ([self.slug])
        elif self.categoria.tipo == 'S':
            return 'curso:curso-sentenca', ([self.slug])
        elif self.categoria.tipo == 'O':
            return 'curso:curso-oab', ([self.slug])
        elif self.categoria.tipo == 'D':
            return 'curso:curso-simulado', ([self.slug])
        else:
            return 'curso:curso', ([self.slug])

    def get_atividade_correcao_individual(self):
        return self.atividade_set.filter(tipo_retorno='C')

    @property
    def meta_comment(self):
        return ', '.join(self.meta_keywords.split(',')[0:3])

    def get_parcelas(self):
        return currency_format(self.valor / self.parcelas)

    def get_valor(self):
        return currency_format(self.valor)

    @property
    def url(self):
        absolute_url = self.get_absolute_url()
        hostname = socket.getfqdn()
        return ''.join(['https://www.', hostname, absolute_url])

    @property
    def is_doc(self):
        return self.doccurso_set.count()

    @property
    def is_video(self):
        return self.doccurso_set.count()

    @property
    def ativo(self):
        now = django.utils.timezone.now()
        if not self.data_fim:
            return True
        return self.data_fim >= now

    @property
    def timeout(self):
        if not self.data_fim:
            return self.data_fim - timezone.now().date()
        return timezone.now().date()

    def materials(self):
        now = django.utils.timezone.now()
        docs = self.doccurso_set.filter(data_ativo__lte=now)
        return docs

    def atividades(self):
        now = django.utils.timezone.now()
        ativs = self.atividade_set.filter(data_ini__lte=now)
        return ativs

    @property
    def get_discuss(self):
        discuss = self.discussao_set.all().order_by('-data_ini')
        return discuss



class Livro(Curso):

    class Meta:
        proxy = True


class SimuladoManager(models.Manager):
    def get_queryset(self):
        return Curso.objects.filter(categoria__tipo='D')


class Simulado(Curso):

    class Meta:
        proxy = True

    object = SimuladoManager()

    def cortesias_check(self):
        cortesias = self.cortesias.all()
        return {
            'total': cortesias.count(),
            'utilizadas': cortesias.filter(utilizado=True).count(),
            'restantes': cortesias.filter(aluno__isnull=True).count()
        }


class Combo(Curso):
    class Meta:
        proxy = True


class CursoCredito(Curso):
    class Meta:
        proxy = True


class ComboAluno(Curso):
    class Meta:
        proxy = True
        verbose_name = 'Combo Personalizada'
        verbose_name_plural = 'Combos Personalizadas'

    @property
    def qtda_cursos(self):
        return self.cursos.count()

    @property
    def get_valor_cursos(self):
        valor = map(lambda x: x.valor, self.cursos.all())
        return sum(valor)

    def calc(self, safe=False):
        valor_cursos = self.get_valor_cursos
        msg = []
        desconto_valor = 0
        desconto_porcento = 0
        desconto = 0
        qtda_cursos = self.qtda_cursos
        pact_menor = PacoteDesconto.objects.filter(qtda__lt=qtda_cursos).last()
        pact_igual = PacoteDesconto.objects.filter(qtda=qtda_cursos).first()
        pact_maior = PacoteDesconto.objects.filter(qtda__gt=qtda_cursos).first()
        if pact_igual:
            msg.append(u'O seu desconto atual é de <b class="text-primary">{:.2f}%</b>.'.format(pact_igual.desconto))
            desconto_porcento = pact_igual.desconto
        elif pact_menor and pact_maior:
            if pact_menor.qtda < qtda_cursos < pact_maior.qtda:
                msg.append(u'O seu desconto atual é de <b class="text-primary">{:.2f}%</b>.'.format(pact_menor.desconto))
                desconto_porcento = pact_menor.desconto
        if pact_maior:
            resto = pact_maior.qtda - qtda_cursos
            msg.append(u'Adicione mais <b class="text-primary">{}</b> sentença(s) e seu desconto será de'
                       u' <b class="text-primary">{:.2f}%</b>.'.format(
                resto, pact_maior.desconto
            ))
        if desconto_porcento:
            desconto = valor_cursos - valor_cursos * desconto_porcento / 100
            desconto_valor = valor_cursos - desconto
        if safe:
            self.valor = desconto or valor_cursos
            self.economia = desconto_valor
            self.save()
        return dict(messages=msg, desconto_porcento=desconto_porcento, desconto_valor=desconto_valor)


@python_2_unicode_compatible
class CursoAvaliacao(models.Model):
    class Meta:
        unique_together = ('user', 'curso')

    curso = models.ForeignKey(
        verbose_name="Curso", to=Curso
    )
    user = models.ForeignKey(
        verbose_name=u"Usuário", to=User
    )
    avaliacao = models.CharField(
        verbose_name=u"Avaliação", max_length=1, choices=[('O', u'Ótimo'), ('B', 'Bom'), ('R', 'Ruim')]
    )

    def __str__(self):
        return self.get_avaliacao_display()


@python_2_unicode_compatible
class Cortesia(models.Model):
    class Meta:
        verbose_name = "Cortesia"
        verbose_name_plural = "Cortesias"
        ordering = [
            'id', 'utilizado', 'aluno'
        ]
        unique_together = [
            'curso', 'aluno'
        ]
    curso = models.ForeignKey(
        verbose_name="Curso", to=Simulado, related_name='cortesias'
    )
    codigo = models.CharField(
        "Código", max_length=150, default=uuid5
    )
    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno', null=True, blank=True
    )
    email = models.EmailField(
        verbose_name='Email', blank=True, null=True
    )
    utilizado = models.BooleanField(
        verbose_name='Utilizado?', default=False
    )

    def __str__(self):
        return self.codigo

    @property
    def codigo_copy(self):
        return mark_safe('<strong>%s</strong>' % self.codigo)


@python_2_unicode_compatible
class Discussao(models.Model):
    class Meta:
        verbose_name = "Discussão"
        verbose_name_plural = "Discussões"

    curso = models.ForeignKey(
        verbose_name="Curso", to=Curso
    )
    titulo = models.CharField(
        "Título", max_length=150
    )
    descricao = models.TextField(
        "Descrição", blank=True, null=True
    )
    data_ini = models.DateField(
        "Data de início", help_text="Data que será iniciada as discussões."
    )
    data_fim = models.DateField(
        "Data de término", help_text="Data em que será encerrada as discussões."
    )

    def __str__(self):
        return self.titulo

    def status(self):
        now = datetime.now().date()  # django.utils.timezone.now().date()
        dini = self.data_ini
        dfim = self.data_fim
        ret = 'Erro'
        label = 'danger'
        if dini <= now <= dfim:
            ret = 'Iniciado'
            label = 'success'
        elif dfim < now:
            ret = 'Encerrado'
            label = 'default'
        elif now < dini:
            ret = 'Aguarde'
            label = 'warning'
        return dict(
            status=ret, label=label
        )


def com1(sender, **kwargs):
    comment = kwargs.get('comment')
    parent = comment.parent
    discuss = comment.content_object
    if parent:
        aluno = parent.user.aluno
        enviar_email(
            'curso/email/resposta-comentario.html',
            "Sua postagem no fórum foi respondida",
            [aluno.email], {'discuss': discuss, 'comentario': comment}
        )


comment_was_posted.connect(com1)


class Modulo(models.Model):
    class Meta:
        verbose_name = u"Módulo"

    curso = models.ForeignKey(Curso, verbose_name=u'Curso')
    nome = models.CharField(verbose_name='Nome', max_length=60)
    order = models.PositiveIntegerField(verbose_name='Ordem')

    def __unicode__(self):
        return self.nome

    @property
    def is_pdf(self):
        return self.pdfmodulo_set.all().count()

    @property
    def is_video(self):
        return self.videomodulo_set.all().count()


class PdfModulo(models.Model):
    class Meta:
        verbose_name = u'Vídeo'

    modulo = models.ForeignKey(Modulo, verbose_name=u'Módulo', blank=True, null=True)
    titulo = models.CharField(verbose_name=u'Título', max_length=50)
    pdf = FileBrowseField(
        verbose_name=u"Arquivo PDF", max_length=200, extensions=['.pdf'], blank=True, null=True,
        help_text=u'Selecione um arquivo no fotmat .PDF',
    )


class Atividade(models.Model):
    curso = models.ForeignKey(
        verbose_name=u'Curso', to=Curso
    )
    professores = models.ManyToManyField(
        'professor.Professor', blank=True
    )
    nome = models.CharField(
        verbose_name='Título', max_length=150
    )
    descricao = models.TextField(
        verbose_name='Descrição', blank=True, null=True, help_text="Breve descrição da atividade"
    )
    gabarito = models.TextField(
        verbose_name='Gabarito', blank=True, null=True
    )
    data = models.DateField(
        verbose_name="Data de Criação", default=datetime.today
    )
    data_ini = models.DateTimeField(
        verbose_name='Data de início', null=True
    )
    data_fim = models.DateTimeField(
        verbose_name='Data de término', null=True
    )
    tipo_retorno = models.CharField(
        verbose_name='Tipo de retorno do professor', max_length=1,
        choices=[
            ('F', 'Apenas discussão no fórum'),
            ('R', 'Apenas Gabarito'),
            ('C', 'Correção individual')
        ]
    )
    tarefa = models.TextField(
        verbose_name='Tarefa', blank=True, null=True
    )
    resposta_padra = models.FileField(
        verbose_name='Resposta padrão', blank=True, null=True, upload_to='respostas'
    )
    resposta_padrao_data = models.DateTimeField(
        verbose_name='Data disponível', blank=True, null=True,
        help_text='Data em que a resposta padrão estará disponível'
    )
    resolucao_obrigatorio = models.BooleanField(
        verbose_name='Resolução Obrigatória?', default=False,
        help_text="Marque se essa Atividade se for de Resolução Obrigatória para a emissão do Certificado."
    )
    caracteres = models.PositiveIntegerField(
        default=20000
    )

    def __unicode__(self):
        return self.nome


    def get_resposta_padrao(self):
        ret = False
        if self.tipo_retorno == 'R' and self.resposta_padra and self.resposta_padrao_data:
            ret = self.gabarito_liberado
        return ret

    def gabarito_liberado(self):
        now = timezone.now()
        ret = False
        if self.resposta_padrao_data:
            ret = now >= self.resposta_padrao_data
        if not ret:
            ret = now >= self.data_fim
        return ret

    def get_status(self):
        now = timezone.now()
        dini = self.data_ini
        dfim = self.data_fim
        ret = 'Erro'
        label = 'danger'
        try:
            if dini <= now <= dfim:
                ret = 'Iniciado'
                label = 'success'
            elif dfim < now:
                ret = 'Encerrado'
                label = 'danger'
            elif now < dini:
                ret = 'Aguarde'
                label = 'warning'
        except:
            pass
        return dict(
            status=ret, label=label
        )

    @property
    def tipo_retorno_label(self):
        return {
            'F': 'info',
            'R': 'primary',
            'C': 'warning'
        }.get(self.tipo_retorno)


class AtividadeModelo(models.Model):
    class Meta:
        verbose_name = "Atividade Modelo"
        verbose_name_plural = "Atividades Modelo"

    atividade = models.ForeignKey(to=Atividade)
    arquivo = models.FileField(
        verbose_name='Arquivo', upload_to='atividade-modelo'
    )


class TarefaAtividade(models.Model):

    atividade = models.ForeignKey(
        verbose_name='Atividade', to=Atividade
    )
    aluno = models.ForeignKey(
        verbose_name='Aluno', to='aluno.Aluno'
    )
    resposta = models.TextField(
        verbose_name='Resposta', blank=True, default=''
    )
    concluido = models.BooleanField(
        verbose_name='Concluído?', default=False
    )
    tempo = models.PositiveSmallIntegerField(
        verbose_name='Tempo', default=0
    )
    data_criacao = models.DateTimeField(
        verbose_name='Data de criação', editable=False, blank=True, auto_now_add=True
    )
    data_modificacao = models.DateTimeField(
        verbose_name='Data de alteração', editable=False, blank=True, auto_now=True
    )
    data_conclusao = models.DateTimeField(
        verbose_name='Data de conclusão', blank=True, null=True
    )
    data_upload = models.DateTimeField(
        verbose_name='Data Upload', blank=True, null=True
    )
    correcao = models.FileField(
        verbose_name='Correção', upload_to='correcao', null=True, blank=True
    )
    professor = models.ForeignKey(
        verbose_name='Corrigido por', to='professor.Professor',
        blank=True, null=True
    )
    gabarito = models.TextField(
        verbose_name='Gabarito', blank=True, null=True, help_text="Correção a partir do gabarito."
    )
    corrigido = models.BooleanField(
        verbose_name='Corrigido?', default=False
    )
    limitada = models.BooleanField(
        verbose_name='Limitada', default=False
    )
    arquivo = models.FileField(
        verbose_name="Selecione o arquivo", upload_to='atividades', blank=True, null=True
    )

    def __unicode__(self):
        return u'{0}/{1}'.format(self.atividade, self.aluno)

    @property
    def time(self):
        return time.strftime('%H:%M:%S', time.gmtime(self.tempo))

    def get_formulario(self):
        try:
            formulario = self.atividade.formulario
        except:
            formulario = None
        return formulario

    def render_gabarito(self):
        br = u'<br/>'
        hr = u'<hr/>'
        tarefa_atividade = self
        texto = ''

        try:
            tabela_correcao = TabelaCorrecaoAluno.objects.get(
                formulario__atividade=tarefa_atividade.atividade, aluno=tarefa_atividade.aluno
            )
            texto = u'<h3><center>CORREÇÃO INDIVIDUALIZADA</center></h3>'
            texto += hr
            texto += tarefa_atividade.atividade.formulario.texto
            texto += br
            texto += u'<table style="border: 1px solid black;">'
            texto += u'    <tr style="border: 1px solid black;">'
            texto += u'        <th style="border: 1px solid black;" colspan="3">Correção individualizada</th>'
            texto += u'    </tr>'
            for tabela in tabela_correcao.tabelas.all():
                texto += u'    <tr style="border: 1px solid black;">'
                texto += u'        <td style="border: 1px solid black;"><center>Item</center></td>'
                texto += u'        <td style="border: 1px solid black;"><center>Valor</center></td>'
                texto += u'        <td style="border: 1px solid black;"><center>Nota</center></td>'
                texto += u'    </tr>'

                txt = u'<h4><strong>%s</strong></h4>' % tabela.tabela.item
                txt += tabela.tabela.comentarios
                for nota in tabela.notas.all().order_by('id'):
                    txt += nota.texto

                if tabela.texto:
                    txt += tabela.texto
                texto += u'    <tr style="border: 1px solid black;">'
                texto += u'        <td style="border: 1px solid black; padding: 0px 15px 15px 15px;">%s</td>' % txt
                texto += u'        <td style="padding-top: 20px; border: 1px solid black; font-size: 1em" valign="top"><center><strong>%.02f</strong></center></td>' % tabela.tabela.valor
                texto += u'        <td style="padding-top: 20px; border: 1px solid black; font-size: 1em" valign="top"><center><strong>%.02f</strong></center></td>' % tabela.nota
                texto += u'    </tr>'
            texto += u'</table>'
            if tabela_correcao.texto:
                texto += br
                texto += u'<h4><strong>Comentário final do professor:</strong></h4>'
                texto += tabela_correcao.texto
            texto += br
            texto += u'<h4>Nota obtida: <strong>%.02f</strong></h4>' % tabela_correcao.total().get('nota')
            self.gabarito = texto
            self.save()
        except TabelaCorrecaoAluno.DoesNotExist:
            pass
        return texto


class Certificado(models.Model):
    curso = models.ForeignKey(
        verbose_name='Curso', to=Curso, related_name='certificados'
    )
    aluno = models.ForeignKey(
        verbose_name='Aluno', to='aluno.Aluno'
    )
    chave = models.CharField(
        verbose_name="Chave", max_length=32, unique=True
    )

    def __unicode__(self):
        return u'{0}/{1}'.format(self.curso, self.aluno)

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise ValueError("Certificado não pode ser alterado")
        else:
            self.chave = get_id()
        super(Certificado, self).save(*args, **kwargs)

    class Meta:
        unique_together = ['curso', 'aluno']


class DocCurso(models.Model):
    class Meta:
        verbose_name = u'Material'
        verbose_name_plural = u'Materiais'

    curso = models.ForeignKey(
        Curso, verbose_name=u'Curso'
    )
    titulo = models.CharField(
        verbose_name=u'Título', max_length=50
    )
    file = models.FileField(
        verbose_name=u"Documento", upload_to='materiais'
    )
    data_ativo = models.DateField(
        verbose_name="Data ativo", blank=True, null=True, help_text="Data em que arquivo será disponibilizado"
    )
    order = models.PositiveIntegerField(verbose_name=u'Ordem')

    def __unicode__(self):
        return self.titulo

    @property
    def ativo(self):
        return timezone.now().date() >= self.data_ativo

    @property
    def file_extension(self):
        return os.path.splitext(self.file.name)[-1]

    @property
    def fileinfo(self):
        icon = 'fa-file-o'
        color = 'green'
        ext = self.file_extension
        if ext in ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']:
            icon = 'fa-file-photo-o'
        elif ext in ['.pdf']:
            icon = 'fa-file-pdf-o'
            color = 'red'
        elif ext in ['.doc', '.rtf', '.txt', '.xls', '.csv']:
            icon = ' fa-file-word-o'
        elif ext in ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm']:
            icon = 'fa-file-movie-o'
        elif ext in ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p']:
            icon = 'fa-file-audio-o'
        return {
            'icon': icon,
            'color': color
        }


class VideoModulo(models.Model):
    class Meta:
        verbose_name = u'Vídeo'

    modulo = models.ForeignKey(Modulo, verbose_name=u'Módulo', blank=True, null=True)
    titulo = models.CharField(verbose_name=u'Título', max_length=50)
    descricao = models.CharField(verbose_name=u'Descrição', max_length=250, blank=True, null=True)
    video = FileBrowseField(
        verbose_name=u"Vídeo", max_length=200, extensions=['.mp4'], blank=True, null=True,
        help_text=u'Selecione um vídeo no fotmat .MP4', directory='videos/'
    )
    thumbnail = ImageField(
        verbose_name='Capa', upload_to='videos_thumb/', blank=True, null=True, editable=False,
        help_text=u'Miniatura que será exibido, se não escolher será gerado automaticamente'
    )

    def __unicode__(self):
        return self.titulo

    def create_screenshot(self):
        video_file = self.video
        png_filename = u'{0}.png'.format(video_file.filename)
        png_file = os.path.join(MEDIA_ROOT, 'videos_thumb', png_filename)
        if not os.path.exists(png_file):
            command = u"ffmpeg -y -i '{0:s}' -ss 00:00:01 -vframes 1 '{1:s}'".format(video_file.path_full, png_file)
            subprocess.call(shlex.split(command))
        self.thumbnail = os.path.join('videos_thumb', png_filename)

    def save(self):
        if self.video:
            self.create_screenshot()
        super(VideoModulo, self).save()


class Destaque(models.Model):
    class Meta:
        unique_together = ('curso',)
    curso = models.ForeignKey(Curso, verbose_name='Curso')
    data_ini = models.DateTimeField(verbose_name=u'Data ínicio', default=django.utils.timezone.now,
                                    help_text=u'A partir dessa data o sistema automaticamente '
                                              u'colocará o curso em destaque')
    data_fim = models.DateTimeField(verbose_name=u'Data final', blank=True, null=True,
                                    help_text=u'A partir dessa data o sistema automaticamente irá retirar o curso '
                                              u'em destaque')
    # Sortable property
    order = models.PositiveIntegerField(verbose_name=u'Ordem')

    def __unicode__(self):
        return self.curso.nome


class Serie(models.Model):
    class Meta:
        verbose_name = u'Série'
        unique_together = ('nome',)

    nome = models.CharField(verbose_name=u'Nome', max_length=50)
    slug = models.SlugField(max_length=60, editable=False)
    order = models.PositiveIntegerField(verbose_name=u'Ordem')

    def __unicode__(self):
        return self.nome

    @models.permalink
    def get_absolute_url(self):
        return 'curso:serie', ([self.slug])


class CursoGratis(models.Model):
    class Meta:
        verbose_name = u"Curso Grátis"
        verbose_name = u"Cursos Grátis"
        unique_together = ('nome',)

    serie = models.ForeignKey(
        verbose_name=u'Serie', to=Serie
    )
    nome = models.CharField(verbose_name=u'Título', max_length=50)
    thumbnail = ImageField(
        verbose_name='Capa', upload_to='videos_thumb/', blank=True, null=True,
        help_text=u'Miniatura que será exibido.'
    )
    video = models.URLField(
        verbose_name=u'Vídeo URL', help_text=u'Vídeo de Apresentação.'
    )
    descricao = models.TextField(verbose_name=u'Apresentação')
    data_cadastro = models.DateTimeField(verbose_name=u'Data ínicio', default=django.utils.timezone.now, editable=False)
    slug = models.SlugField(max_length=150, editable=False)
    # Sortable property
    order = models.PositiveIntegerField(verbose_name=u'Ordem')
    # SEO
    meta_description = models.CharField(verbose_name=u'Meta Description', blank=True, null=True, max_length=160,
                                        help_text=u'Resumo geral do site. Frase que descreva muito bem o Curso. Quando'
                                                  u' o site for buscado, essa será a frase que aparecerá à quem '
                                                  u'buscar. Melhor utilizar de 25 a 30 palavras com 160 a 180 '
                                                  u'caracteres.')
    meta_keywords = models.CharField(verbose_name=u'Meta Keywords', blank=True, null=True, max_length=100,
                                     help_text=u'Procure usar umas poucas palavras que descrevam o conteúdo do Curso. '
                                               u'Exemplo: climática, previsão climática,desenvolvimento, tempo, '
                                               u'clima. É importante que as palavras estejam no Título e nas Meta '
                                               u'Description.')

    def __unicode__(self):
        return self.nome

    @models.permalink
    def get_absolute_url(self):
        return 'curso:curso-gratis', ([self.slug])

    @property
    def video_code(self):
        return self.video.split('/')[-1]


class VideoGratis(models.Model):
    class Meta:
        verbose_name = u'Vídeo Grátis'
        verbose_name_plural = u'Vídeos Grátis'
        ordering = ['-data_ini']

    curso = models.ForeignKey(
        verbose_name='Curso', to=CursoGratis
    )
    titulo = models.CharField(
        verbose_name=u'Título', max_length=200
    )
    descricao = models.TextField(verbose_name=u'Apresentação', blank=True, null=True)
    data_ini = models.DateTimeField(verbose_name=u'Data ínicio', default=django.utils.timezone.now, null=True, blank=True,
                                    help_text=u'A partir dessa data o sistema automaticamente '
                                              u'colocará o vídeo no site')
    video = models.URLField(
        verbose_name=u'Vídeo URL'
    )
    order = models.PositiveIntegerField(verbose_name=u'Ordem')

    def __unicode__(self):
        return self.titulo

    @property
    def code(self):
        return self.video.split('/')[-1]

    @property
    def iframe(self):
        return '<iframe width="100%" height="315" src="https://www.youtube.com/embed/{0}" ' \
               'frameborder="0" allowfullscreen></iframe>'.format(self.video)

    @property
    def str_data(self):
        return pretty_date(self.data_ini)


@python_2_unicode_compatible
class CheckoutItens(models.Model):
    checkout = models.ForeignKey(
        to='pagseguro.Checkout'
    )
    curso = models.ForeignKey(
        to=Curso
    )
    qtda = models.PositiveSmallIntegerField()
    valor = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )

    def transaction(self):
        return self.checkout.transaction

    def __str__(self):
        return self.curso.nome

    @property
    def total(self):
        return self.qtda * self.valor

    def __str__(self):
        return self.curso.nome

@python_2_unicode_compatible
class SentencaAvulsa(models.Model):
    class Meta:
        verbose_name = u"Atividade Avulsa"
        verbose_name_plural = u"Atividades Avulsas"
        ordering = ['titulo']

    titulo = models.CharField(verbose_name="Título", max_length=150, help_text="Identificação")
    cod_youtube = models.CharField(verbose_name='Cód. Youtube', max_length=50, default='0',
                                   help_text="Código do vídeo no Youtube")
    esfera_especifica = models.ForeignKey(verbose_name="Esfera Específica", to=EsferaEspecifica)
    tipo_procedimento = models.ForeignKey(verbose_name="Tipo de Procedimento", to=TipoProcedimento, null=True)
    disciplina = models.ForeignKey(verbose_name="Disciplina", to=Disciplina, null=True)
    nivel = models.CharField(verbose_name="Nível", max_length=1,
                             choices=[("F", "Fácil"), ("M", "Médio"), ("D", "Difícil")])
    professor = models.ForeignKey(to='professor.Professor')
    amostra = models.TextField(verbose_name="Amostra da Sentença", blank=True, null=True)
    conteudo = models.TextField(verbose_name="Conteúdo", help_text="Conteúdo integral da proposta de sentença")
    comentario = models.TextField(verbose_name="Comentários", blank=True, null=True,
                                  help_text="Comentários do professor sobre a proposta de sentença ")
    gabarito = models.FileField(
        verbose_name='Gabarito', upload_to='gabaritos-sentenca', null=True, blank=True
    )

    def __unicode__(self):
        return self.titulo

    def __str__(self):
        return self.titulo

    @property
    def span_nivel(self):
        n = self.nivel
        if n == 'F':
            s = 'primary'
        elif n == 'M':
            s = 'warning'
        else:
            s = 'danger'
        return u'<span class="label label-{0}">{1}</span>'.format(s, self.get_nivel_display())


class SentencaOAB(models.Model):
    class Meta:
        verbose_name = "OAB 2ª Fase"
        verbose_name_plural = "OAB 2ª Fase"
        ordering = ['titulo']

    titulo = models.CharField(verbose_name="Título", max_length=150, help_text="Identificação")
    cod_youtube = models.CharField(verbose_name='Cód. Youtube', max_length=50, default='0',
                                   help_text="Código do vídeo no Youtube")
    tipo_peca = models.ForeignKey(verbose_name="Tipo de Peça Prática", to=TipoPecaPratica)
    disciplina = models.ForeignKey(verbose_name="Disciplina", to=Disciplina)
    nivel = models.CharField(verbose_name="Nível", max_length=1,
                             choices=[("F", "Fácil"), ("M", "Médio"), ("D", "Difícil")])
    professor = models.ForeignKey(to='professor.Professor')
    amostra = models.TextField(verbose_name="Amostra da Sentença", blank=True, null=True)
    conteudo = models.TextField(verbose_name="Conteúdo", help_text="Conteúdo integral da proposta de sentença")
    comentario = models.TextField(verbose_name="Comentários", blank=True, null=True,
                                  help_text="Comentários do professor sobre a proposta de sentença ")
    gabarito = models.FileField(
        verbose_name='Gabarito', upload_to='gabaritos-oab', null=True, blank=True
    )

    def __unicode__(self):
        return self.titulo

    @property
    def span_nivel(self):
        n = self.nivel
        if n == 'F':
            s = 'primary'
        elif n == 'M':
            s = 'warning'
        else:
            s = 'danger'
        return u'<span class="label label-{0}">{1}</span>'.format(s, self.get_nivel_display())


class SentencaModelo(models.Model):
    class Meta:
        verbose_name = "Sentença Modelo"
        verbose_name_plural = "Sentenças Modelo"

    sentenca_avulsa = models.ForeignKey(to=SentencaAvulsa)
    arquivo = models.FileField(
        verbose_name='Arquivo', upload_to='correcao-sentenca-modelo'
    )


class SentencaModeloOAB(models.Model):
    class Meta:
        verbose_name = "Sentença Modelo"
        verbose_name_plural = "Sentenças Modelo"

    sentenca_oab = models.ForeignKey(to=SentencaOAB)
    arquivo = models.FileField(
        verbose_name='Arquivo', upload_to='correcao-sentenca-modelo-oab'
    )


@python_2_unicode_compatible
class SentencaAvulsaAluno(models.Model):
    class Meta:
        unique_together = ['sentenca_avulsa', 'aluno']
        verbose_name = u"Atividade Avulsa do Aluno"
        verbose_name_plural = u"Atividades Avulsas dos Alunos"

    sentenca_avulsa = models.ForeignKey(
        verbose_name='Atividade Avulsa', to=SentencaAvulsa
    )
    aluno = models.ForeignKey(
        verbose_name='Aluno', to='aluno.Aluno'
    )
    resposta = models.TextField(
        verbose_name='Resposta', blank=True, default=''
    )
    correcao_individual = models.TextField(
        verbose_name=u'Correção individual', blank=True, default=''
    )
    status = models.CharField(
        verbose_name='Status', max_length=1, default='I',
        choices=[
            ('I', 'Iniciada'),
            ('A', 'Aguardando Correção'),
            ('C', 'Corrigido')
        ]
    )
    tempo = models.PositiveSmallIntegerField(
        verbose_name='Tempo', default=0
    )
    data_criacao = models.DateTimeField(
        verbose_name='Data de criação', editable=False, blank=True, auto_now_add=True
    )
    data_modificacao = models.DateTimeField(
        verbose_name='Data de alteração', editable=False, blank=True, auto_now=True
    )
    correcao = models.FileField(
        verbose_name='Correção', upload_to='correcao_sentenca', null=True, blank=True
    )
    data_conclusao = models.DateTimeField(
        verbose_name='Data de conclusão', blank=True, null=True
    )
    arquivo = models.FileField(
        verbose_name='Arquivo', upload_to='sentenca-avulsa-aluno', null=True, blank=True
    )
    data_upload = models.DateTimeField(
        verbose_name='Data Upload', blank=True, null=True
    )

    def __unicode__(self):
        return self.cod

    def __str__(self):
        return self.cod

    @property
    def cod(self):
        return u'T{0:03d}-{1}'.format(self.id, self.sentenca_avulsa)


    @property
    def time(self):
        return time.strftime('%H:%M:%S', time.gmtime(self.tempo))

    @property
    def span_status(self):
        st = {
            'I': 'success',
            'A': 'danger',
            'C': 'primary'
        }.get(self.status)
        return u'<span class="label label-{0}">{1}</span>'.format(st, self.get_status_display())

    @property
    def data_limite(self):
        try:
            ci = CheckoutItens.objects.filter(
                checkout__aluno=self.aluno,
                curso__sentenca_avulsa=self.sentenca_avulsa,
                checkout__transaction__status__in=['pago', 'disponivel']
            ).first()
            return ci.checkout.transaction.last_event_date + timedelta(days=365)
        except Exception as exc:
            return None

    @property
    def expirado(self):
        now = timezone.now()
        return now > self.data_limite


class SentencaOABAvulsaAluno(models.Model):
    class Meta:
        unique_together = ['sentenca_oab', 'aluno']
        verbose_name = "Sentença OAB do Aluno"
        verbose_name_plural = "Sentenças OAB dos Alunos"

    sentenca_oab = models.ForeignKey(
        verbose_name='OAB 2ª Fase', to=SentencaOAB
    )
    aluno = models.ForeignKey(
        verbose_name='Aluno', to='aluno.Aluno'
    )
    resposta = models.TextField(
        verbose_name='Resposta', blank=True, default=''
    )
    status = models.CharField(
        verbose_name='Status', max_length=1, default='I',
        choices=[
            ('I', 'Iniciada'),
            ('A', 'Aguardando Correção'),
            ('C', 'Corrigido')
        ]
    )
    tempo = models.PositiveSmallIntegerField(
        verbose_name='Tempo', default=0
    )
    data_criacao = models.DateTimeField(
        verbose_name='Data de criação', editable=False, blank=True, auto_now_add=True
    )
    data_modificacao = models.DateTimeField(
        verbose_name='Data de alteração', editable=False, blank=True, auto_now=True
    )
    correcao = models.FileField(
        verbose_name='Correção', upload_to='correcao_sentenca', null=True
    )

    def __unicode__(self):
        return self.cod

    @property
    def cod(self):
        try:
            return u'T{0:03d}-{1}'.format(self.id, self.sentenca_oab)
        except:
            return u'T{0:03d}'.format(self.id)

    @property
    def time(self):
        return time.strftime('%H:%M:%S', time.gmtime(self.tempo))

    @property
    def span_status(self):
        st = {
            'I': 'success',
            'A': 'danger',
            'C': 'primary'
        }.get(self.status)
        return u'<span class="label label-{0}">{1}</span>'.format(st, self.get_status_display())


def gerar_codigo():
    cod = str(uuid.uuid4())[:6].upper()
    return '%s-%s' % (cod[3:], cod[:3])


class LiberarCompraCurso(models.Model):

    codigo = models.CharField(
        verbose_name=u"Código", max_length=7,
        default=gerar_codigo(), unique=True,
        db_index=True
    )
    curso = models.ForeignKey(
        verbose_name="Curso", to=Curso,
        on_delete=models.CASCADE
    )
    aluno = models.ForeignKey(
        verbose_name="Aluno", to='aluno.Aluno',
        on_delete=models.CASCADE
    )
    data = models.DateField(
            verbose_name='Data de Válidade',
            help_text='Após essa data não será mais possivel utilizar o Código'
    )
    ativo = models.BooleanField(
        verbose_name="Ativo", default=True
    )

    class Meta:
        verbose_name = u"Liberar Compra de Curso"
        verbose_name_plural = u"Liberar Compra de Cursos"
        unique_together = ['curso', 'aluno']

    def __unicode__(self):
        return self.codigo



models.signals.post_save.connect(create_slug, sender=Categoria)
models.signals.post_save.connect(create_slug, sender=Curso)
models.signals.post_save.connect(create_slug, sender=Combo)
models.signals.post_save.connect(create_slug, sender=Livro)
models.signals.post_save.connect(create_slug, sender=Serie)
models.signals.post_save.connect(create_slug, sender=CursoGratis)
