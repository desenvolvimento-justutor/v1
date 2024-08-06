# -*- coding: utf-8 -*-
# Autor: christian
import django
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.fields import ImageField

from libs import maps
from libs.signals import create_slug


class Configuracao(models.Model):
    _animations = [
        ("slide", "Slide"),
        ("rotatein", "Rotação"),
        ("perspectivein", "Perspectiva"),
        ("scalein", "Escala"),
    ]
    _positions = [
        ("lefttop", "Canto Superior Esquerdo"),
        ("leftcenter", "Centralizado à Esquerda"),
        ("leftbottom", "Canto Inferior Esquerdo"),
        ("centertop", "Centralizado no Topo"),
        ("centercenter", "Centralizado ao Meio"),
        ("centerbottom", "Centralizado Abaixo"),
        ("righttop", "Canto Superior Direito"),
        ("rightcenter", "Centralizado à Direita"),
        ("rightbottom", "Canto Inferior Direito"),
    ]

    class Meta:
        verbose_name = "Configuração"
        verbose_name_plural = "Configurações"
        unique_together = ("ativo",)

    ativo = models.BooleanField(
        verbose_name="Ativo",
        default=False,
        help_text="Somente uma configuração estará "
        "ativa. É obrigatório que haja uma "
        "configuração ativa para o "
        "funcionamento adequado do site",
    )
    titulo = models.CharField(
        verbose_name="Título do Site",
        max_length=70,
        help_text="Crie um titulo para ser padrão do site e utilize, de preferência no começo "
        "da frase, a palavra-chave mais importante dessa página. Procure utilizar de "
        "3 a 9 palavras.",
    )
    logo = ImageField(
        verbose_name="Logotipo",
        help_text="Insira o logotipo para o cabecalho do site",
        blank=True,
        null=True,
        upload_to="images",
    )
    favicon = ImageField(
        verbose_name="Ícone",
        help_text="Ícone do site",
        blank=True,
        null=True,
        upload_to="images",
    )
    # SUBSCRIBE
    subs_ativo = models.BooleanField(
        verbose_name="Ativo",
        default=False,
        help_text="Se ativo será exibido a janela SUBSCRIBE na página " "inicial.",
    )
    subs_titulo = models.CharField(
        verbose_name="Título", max_length=150, blank=True, null=True
    )
    subs_texto = models.TextField(verbose_name="Texto", blank=True, null=True)
    subs_texto_botao = models.CharField(
        verbose_name="Texto do Botão", max_length=20, blank=True, null=True
    )
    subs_texto_sucesso = models.CharField(
        verbose_name="Texto Concluído",
        max_length=150,
        blank=True,
        null=True,
        help_text="Texto que será exibido no final, caso o usuário assine o newsletter.",
    )
    subs_texto_inferior = models.CharField(
        verbose_name="Texto Inferior",
        max_length=50,
        blank=True,
        null=True,
        help_text="Acrescenta uma linha de texto na parte inferior da janela com texto reduzido. (ex: uma observação)",
    )
    subs_animacao = models.CharField(
        verbose_name="Efeito de Animação",
        choices=_animations,
        blank=True,
        null=True,
        default="slide",
        max_length=13,
        help_text="Efeito de Animação que será executado na exibição da janela.",
    )
    subs_posicao = models.CharField(
        verbose_name="Posição da Janela",
        choices=_positions,
        blank=True,
        null=True,
        default="centercenter",
        max_length=12,
        help_text="Posição da janela em relação à página.",
    )
    subs_bgcolor = models.CharField(
        verbose_name="Cor do Fundo",
        max_length=15,
        blank=True,
        null=True,
        default="#000",
        help_text="Padrão: #000",
    )
    subs_buttonbgcolor = models.CharField(
        verbose_name="Cor do Botão",
        max_length=15,
        blank=True,
        null=True,
        default="#d71b1b",
        help_text="Padrão: #d71b1b",
    )
    subs_buttoncolor = models.CharField(
        verbose_name="Cor do Texto Botão",
        max_length=15,
        blank=True,
        null=True,
        default="#000",
        help_text="Padrão: #000",
    )
    subs_closecolor = models.CharField(
        verbose_name="Cor do Botão Fechar",
        max_length=15,
        blank=True,
        null=True,
        default="#d71b1b",
        help_text="Padrão: #d71b1b",
    )
    subs_color = models.CharField(
        verbose_name="Cor do título",
        max_length=15,
        blank=True,
        null=True,
        default="#ccc",
        help_text="Padrão: #ccc",
    )
    subs_contentcolor = models.CharField(
        verbose_name="Cor do Texto",
        max_length=15,
        blank=True,
        null=True,
        default="#000",
        help_text="Padrão: #000",
    )
    subs_imagem = ImageField(
        verbose_name="Imagem", blank=True, null=True, upload_to="images"
    )
    # CONTATO
    url_facebook = models.URLField(verbose_name="Facebook", blank=True, null=True)
    url_flicker = models.URLField(verbose_name="Flicker", blank=True, null=True)
    url_twitter = models.URLField(verbose_name="Twitter", blank=True, null=True)
    url_youtube = models.URLField(verbose_name="Youtube", blank=True, null=True)
    url_instagram = models.URLField(verbose_name="Instagram", blank=True, null=True)
    email = models.EmailField(
        verbose_name="Email Principal",
        max_length=200,
        blank=True,
        null=True,
        help_text="Email que receberá cópia dos formulários enviados pelo site.",
    )
    telefone = models.CharField(verbose_name="Telefone Comercial", max_length=15)
    # ENDEREÇO
    cep = models.CharField(verbose_name="CEP", max_length=10, blank=True, null=True)
    endereco = models.CharField(verbose_name="Endereço", max_length=100)
    numero = models.CharField(verbose_name="Número", max_length=5)
    bairro = models.CharField(verbose_name="Bairro", max_length=100)
    cidade = models.CharField(verbose_name="Cidade", max_length=100)
    uf = models.CharField(verbose_name="Estado", max_length=2)
    # SEO
    sobre_drm = models.TextField(verbose_name="Sobre DRM", blank=True, null=True)
    meta_description = models.CharField(
        verbose_name="Meta Description",
        blank=True,
        null=True,
        max_length=160,
        help_text="Resumo geral do site. Frase que descreva muito bem o site. Quando"
        " o site for buscado, essa será a frase que aparecerá à quem "
        "buscar. Melhor utilizar de 25 a 30 palavras com 160 a 180 "
        "caracteres.",
    )
    meta_keywords = models.CharField(
        verbose_name="Meta Keywords",
        blank=True,
        null=True,
        max_length=100,
        help_text="Procure usar umas poucas palavras que descrevam o conteúdo do site. "
        "Exemplo: climática, previsão climática,desenvolvimento, tempo, "
        "clima. É importante que as palavras estejam no Título e nas Meta "
        "Description.",
    )
    meta_geo_position = models.CharField(
        verbose_name="Meta Geo Position",
        blank=True,
        null=True,
        max_length=20,
        help_text="Coordenada de Localização - Utilizado geralmente o local do "
        "escritório. Ex: -13.85089,-40.0877",
    )
    meta_geo_place = models.CharField(
        verbose_name="Meta Geo Placename",
        blank=True,
        null=True,
        max_length=40,
        help_text="Localização Geográfica - Utilizado geralmente o local do "
        "escritório. Ex: Campinas, São Paulo",
    )
    meta_geo_region = models.CharField(
        verbose_name="Meta Geo Region",
        blank=True,
        null=True,
        max_length=5,
        help_text="Código da região geográfica (Sigla do Páis e do estado). Ex: "
        "BR-MG",
    )
    regulamento_premios = models.ForeignKey(
        verbose_name="Regulamento Prêmios",
        to="website.Institucional",
        blank=True,
        null=True,
        help_text="Regulamento para concorrer a prêmios",
        related_name="get_institucional",
    )
    regulamento_sentenca_avulsa = models.ForeignKey(
        verbose_name="Regulamento Atividade Avulsa",
        to="website.Institucional",
        blank=True,
        null=True,
        help_text="Regulamento para concorrer a prêmios",
        related_name="get_institucional_set",
    )
    politica = models.OneToOneField(
        verbose_name="Política de uso",
        to="website.Institucional",
        blank=True,
        null=True,
        related_name="politicas",
    )
    termos = models.OneToOneField(
        verbose_name="Termos",
        to="website.Institucional",
        blank=True,
        null=True,
        related_name="termos",
    )

    @property
    def meta_comment(self):
        return ", ".join(self.meta_keywords.split(",")[0:3])

    def __unicode__(self):
        return "%s" % self.titulo or "%s" % self.pk

    @property
    def get_institucional(self):
        return self.institucional_set.filter(ativo=True)

    @property
    def get_banner(self):
        now = django.utils.timezone.now()
        banners = self.banner_set.filter(
            Q(ativo_inicio__lte=now), Q(ativo_fim__gte=now) | Q(ativo_fim=None)
        ).order_by("order")
        return banners

    @property
    def get_noticias(self):
        now = django.utils.timezone.now()
        noticia = self.noticia_set.filter(
            Q(ativo_inicio__lte=now), Q(ativo_fim__gte=now) | Q(ativo_fim=None)
        ).order_by("-ativo_inicio")
        return noticia


class PacoteDesconto(models.Model):
    qtda = models.SmallIntegerField(verbose_name="Quantidade")
    desconto = models.DecimalField(
        verbose_name="Desconto",
        decimal_places=2,
        max_digits=5,
        help_text="Percentual do Desconto",
    )
    configuracao = models.ForeignKey(verbose_name="Configuração", to=Configuracao)

    def __str__(self):
        return "{} - {}%".format(self.qtda, self.desconto)

    class Meta:
        ordering = ["qtda"]


def _get_config_ativa():
    ativo = False
    try:
        ativo = Configuracao.objects.get(ativo=True)
    except:
        pass
    return ativo


class Endereco(models.Model):
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = verbose_name + "s"

    configuracao = models.ForeignKey(
        Configuracao, verbose_name="Endereços", related_name="endereco+"
    )
    titulo = models.CharField(verbose_name="Título", max_length=100)
    telefone = models.CharField(
        verbose_name="Telefone Comercial", max_length=15, blank=True, null=True
    )
    mapa = models.TextField(
        verbose_name="Mapa Embutido",
        blank=True,
        null=True,
        help_text="Código HTML do Google Maps.",
    )
    cep = models.CharField(verbose_name="CEP", max_length=10, blank=True, null=True)
    endereco = models.CharField(verbose_name="Endereço", max_length=100)
    bairro = models.CharField(verbose_name="Bairro", max_length=100)
    numero = models.CharField(verbose_name="Número", max_length=5)
    complemento = models.CharField(
        verbose_name="Complemento", max_length=100, blank=True, null=True
    )
    cidade = models.CharField(verbose_name="Cidade", max_length=100)
    uf = models.CharField(verbose_name="Estado", max_length=2)

    def __unicode__(self):
        return self.endereco_formatado()

    def endereco_formatado(self):
        return "%s, %s - %s" % (self.endereco, self.numero, self.bairro)

    def get_iframe_map(self):
        endereco = "{0:s}, {1:s}, {2:s} - {3:s}".format(
            self.endereco, self.numero, self.cidade, self.uf, self.cep
        )
        iframe_str = '<iframe width="100&#37" height="300" frameborder="0" style="border:0" src="%s"></iframe>'
        iframe_src = (
            "https://www.google.com/maps/embed/v1/place?key=AIzaSyA0Bn1sevI3umrF6ZR35nTIpY-iJ21PVvw&q=%s"
            % (maps.url_fix(endereco))
        )
        # iframe_destination_d = u'''
        # https://www.google.com/maps/embed/v1/directions?origin=&destination=%s&key=AIzaSyA0Bn1sevI3umrF6ZR35nTIpY-iJ21PVvw
        # ''' % (maps.url_fix(endereco))
        return iframe_str % iframe_src


class Institucional(models.Model):
    class Meta:
        verbose_name = "Institucional"
        verbose_name_plural = "Institucionais"
        ordering = ["order"]

    configuracao = models.ForeignKey(Configuracao, verbose_name="Configuração")
    nome = models.CharField(verbose_name="Título", max_length=50)
    conteudo = models.TextField(verbose_name="Conteúdo")
    ativo = models.BooleanField(verbose_name="Ativo", default=True)
    slug = models.SlugField(max_length=150, editable=False)
    # Sortable property
    order = models.PositiveIntegerField(verbose_name="Ordem")
    # SEO
    meta_description = models.CharField(
        verbose_name="Meta Description",
        blank=True,
        null=True,
        max_length=160,
        help_text="Resumo geral do site. Frase que descreva muito bem o Institucional."
        " Quando o site for buscado, essa será a frase que aparecerá à quem"
        " buscar. Melhor utilizar de 25 a 30 palavras com 160 a "
        "180 caracteres.",
    )
    meta_keywords = models.CharField(
        verbose_name="Meta Keywords",
        blank=True,
        null=True,
        max_length=100,
        help_text="Procure usar umas poucas palavras que descrevam o conteúdo da Notícia."
        " Exemplo: climática, previsão climática,desenvolvimento, tempo, "
        "clima. É importante que as palavras estejam no Título e nas Meta "
        "Description.",
    )

    @models.permalink
    def get_absolute_url(self):
        return "website:institucional", ([self.slug])

    @property
    def meta_comment(self):
        return ", ".join(self.meta_keywords.split(",")[0:3])

    def __unicode__(self):
        return self.nome

    def url(self):
        return '<a href="{0}" target="_blank">{0}</a>'.format(self.get_absolute_url())

    url.allow_tags = True


class Imagem(models.Model):
    class Meta:
        verbose_name_plural = "Imagens"

    configuracao = models.ForeignKey(
        Configuracao, verbose_name="Configuração", blank=True, null=True
    )
    imagem = ImageField(verbose_name="Imagem", upload_to="img_site/")

    # def __unicode__(self):
    #     return self.configuracao


class VideoJusTutor(models.Model):
    class Meta:
        verbose_name = "Vídeo JusTutor"
        verbose_name_plural = "Vídeos JusTutor"
        ordering = ["-data_ini"]

    titulo = models.CharField(verbose_name="Título", max_length=200)
    descricao = models.TextField(verbose_name="Apresentação", blank=True, null=True)
    data_ini = models.DateTimeField(
        verbose_name="Data ínicio",
        default=django.utils.timezone.now,
        null=True,
        blank=True,
        help_text="A partir dessa data o sistema automaticamente "
        "colocará o vídeo no site",
    )
    video = models.URLField(verbose_name="Vídeo URL")

    def __unicode__(self):
        return self.titulo

    @property
    def code(self):
        return self.video.split("/")[-1]

    @property
    def iframe(self):
        return (
            '<iframe width="100%" height="315" src="https://www.youtube.com/embed/{0}" '
            'frameborder="0" allowfullscreen></iframe>'.format(self.video)
        )


class Noticia(models.Model):
    class Meta:
        ordering = ["-ativo_inicio"]

    configuracao = models.ForeignKey(Configuracao, verbose_name="Configuração")
    nome = models.CharField(verbose_name="Título", max_length=200)
    conteudo = models.TextField(verbose_name="Conteúdo")
    ativo_inicio = models.DateTimeField(
        verbose_name="Início",
        default=django.utils.timezone.now,
        help_text="A partir dessa data o sistema automaticamente exibi a Notícia no"
        "site",
    )
    ativo_fim = models.DateTimeField(
        verbose_name="Fim",
        blank=True,
        null=True,
        help_text="A partir dessa data o sistema automaticamente remove a Notícia do "
        "site",
    )
    slug = models.SlugField(max_length=150, editable=False)
    # SEO
    meta_description = models.CharField(
        verbose_name="Meta Description",
        blank=True,
        null=True,
        max_length=160,
        help_text="Resumo geral da. Frase que descreva muito bem a notícia. Quando"
        " o site for buscado, essa será a frase que aparecerá à quem "
        "buscar. Melhor utilizar de 25 a 30 palavras com 160 a 180 "
        "caracteres.",
    )
    meta_keywords = models.CharField(
        verbose_name="Meta Keywords",
        blank=True,
        null=True,
        max_length=100,
        help_text="Procure usar umas poucas palavras que descrevam o conteúdo da "
        "Notícia. Exemplo: climática, previsão climática,desenvolvimento, "
        "tempo clima. É importante que as palavras estejam no "
        "Título e nas Meta Description.",
    )

    @models.permalink
    def get_absolute_url(self):
        return "website:noticia", ([self.slug])

    def url(self):
        return '<a href="{0}" target="_blank">{0}</a>'.format(self.get_absolute_url())

    url.allow_tags = True

    @property
    def meta_comment(self):
        return ", ".join(self.meta_keywords.split(",")[0:3])

    def __unicode__(self):
        return self.nome

    @property
    def anterior(self):
        now = timezone.now()
        return (
            Noticia.objects.filter(
                Q(ativo_inicio__lte=now),
                Q(ativo_fim__gte=now) | Q(ativo_fim=None),
                ativo_inicio__gt=self.ativo_inicio,
            )
            .order_by("ativo_inicio")
            .exclude(id=self.id)
            .first()
        )

    @property
    def proxima(self):
        now = timezone.now()
        return (
            Noticia.objects.filter(
                Q(ativo_inicio__lte=now),
                Q(ativo_fim__gte=now) | Q(ativo_fim=None),
                ativo_inicio__lt=self.ativo_inicio,
            )
            .exclude(id=self.id)
            .order_by("ativo_inicio")
            .last()
        )


class NoticiaLida(models.Model):
    class Meta:
        unique_together = ["noticia", "ip"]

    noticia = models.ForeignKey(Noticia)
    ip = models.IPAddressField()

    def __unicode__(self):
        return self.noticia.nome


def _get_urls():
    noticias = map(
        lambda x: (x.get_absolute_url(), "[N] {0}".format(x.nome)),
        Noticia.objects.all(),
    )
    institucionais = map(
        lambda x: (x.get_absolute_url(), "[I] {0}".format(x.nome)),
        Institucional.objects.all(),
    )
    return noticias + institucionais


class BannerFooter(models.Model):
    class Meta:
        verbose_name = "Banner Footer"
        verbose_name_plural = "Banners Footer"

    imagem = ImageField(
        verbose_name="Imagem",
        upload_to="banner-img",
        help_text="Escolha uma imagem com tamanho de 400x300 pixels.",
    )
    # titulo = models.CharField(verbose_name=u'Título do banner', max_length=150)
    # texto = models.TextField(verbose_name=u'Texto')
    link = models.URLField(verbose_name="Link", help_text="Insira o link do banner")
    link_v2 = models.URLField(
        verbose_name="Link V2",
        help_text="Insira o link do banner",
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(verbose_name="Ordem")

    def __unicode__(self):
        return "Banner No. %03d" % self.pk

    @property
    def banner(self):
        return "Banner No. %03d" % self.pk


class Banner(models.Model):
    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = verbose_name + "'s"
        ordering = ["order"]

    configuracao = models.ForeignKey(
        Configuracao, verbose_name="Configuração", default=1
    )
    exibir_caixa = models.BooleanField(
        verbose_name="Exibir caixa de legendas", default=False
    )
    titulo = models.CharField(
        verbose_name="Título do banner", max_length=150, blank=True, null=True
    )
    legendas = models.TextField(
        verbose_name="Legendas", help_text="Uma por linha", blank=True, null=True
    )
    order = models.PositiveIntegerField(verbose_name="Ordem")
    imagem = ImageField(
        verbose_name="Imagem",
        upload_to="banner-img",
        help_text="Escolha uma imagem com tamanho de 500x430 pixels.",
    )
    banner = ImageField(
        verbose_name="Banner",
        upload_to="banner-img",
        help_text="Escolha uma imagem com tamanho de 1585x550 pixels.",
        blank=True,
        null=True,
    )
    link = models.URLField(
        verbose_name="Link", help_text="Insira o link do banner", blank=True, null=True
    )
    link_v2 = models.URLField(
        verbose_name="Link V2",
        help_text="Insira o link do banner (V2)",
        blank=True,
        null=True,
    )
    texto_link = models.CharField(
        verbose_name="Texto do Link",
        max_length=15,
        default="Saiba+",
        help_text="Se informado o link, informe o texto que será exibido no botão",
    )
    ativo_inicio = models.DateTimeField(
        verbose_name="Início",
        default=django.utils.timezone.now,
        help_text="A partir dessa data o sistema automaticamente colocará o banner "
        "no site",
    )
    ativo_fim = models.DateTimeField(
        verbose_name="Fim",
        blank=True,
        null=True,
        help_text="A partir dessa data o sistema automaticamente irá retirar o banner do "
        "site",
    )

    # def __init__(self,  *args, **kwargs):
    #     super(Banner, self).__init__(*args, **kwargs)
    #     self._meta.get_field_by_name('link')[0]._choices = _get_urls()

    def __unicode__(self):
        res = self.titulo
        if not res:
            res = self.imagem
        return res

    @property
    def get_legendas(self):
        return self.legendas.split("\n")


class Anuncio(models.Model):
    class Meta:
        verbose_name = "Anúncio"

    configuracao = models.ForeignKey(
        verbose_name="Configuração", to=Configuracao, default=1
    )
    ativo = models.BooleanField(verbose_name="Ativo", default=True)
    titulo = models.CharField(verbose_name="Título", max_length=150)
    imagem = ImageField(
        verbose_name="Imagem",
        upload_to="anuncions",
        help_text="Escolha uma imagem com tamanho de 1874x720 pixels.",
    )
    link = models.URLField(verbose_name="Link", help_text="Insira o link do anúncio")
    pag_atividades = models.BooleanField(
        verbose_name="Pág. de Atividades", default=False
    )
    pag_curso_gratis = models.BooleanField(
        verbose_name="Pág. de Cursos Grátis", default=False
    )
    pag_cursos = models.BooleanField(verbose_name="Pág. de Cursos", default=False)
    pag_enunciados = models.BooleanField(
        verbose_name="Pág. de Enunciados", default=False
    )
    pag_resultado_busca = models.BooleanField(
        verbose_name="Pág. do Resultado da Busca", default=False
    )
    pag_conteudo = models.BooleanField(verbose_name="Pág. de Conteúdos", default=False)
    pag_videos = models.BooleanField(verbose_name="Pág. de Vídeos", default=False)
    pag_roteiro = models.BooleanField(verbose_name="Pág. de Roteiro", default=False)
    pag_noticias = models.BooleanField(verbose_name="Pág. de Notícias", default=False)
    pag_temas = models.BooleanField(verbose_name="Pág. Temas Abordados", default=False)
    pag_populares = models.BooleanField(
        verbose_name="Pág. Mais Populares", default=False
    )

    def __unicode__(self):
        return self.titulo

    def imagem_(self):
        if self.imagem:
            return '<a target="_blank" href="{1}"><img src="{0}"/></a>'.format(
                get_thumbnail(self.imagem, "80x80", crop="center", quality=95).url,
                self.imagem.url,
            )
        return

    imagem_.short_description = "Imagem"
    imagem_.allow_tags = True


class ArtigoIndice(MPTTModel):
    class Meta:
        verbose_name = "Índice"
        verbose_name_plural = "Índices"

    name = models.CharField(verbose_name="Título", max_length=50, unique=True)
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)
    parent = TreeForeignKey(
        verbose_name="Índice Superior",
        to="self",
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __unicode__(self):
        return self.name

    @property
    def total_artigos(self):
        return self.artigo_set.all().count()


class Artigo(models.Model):
    class Meta:
        verbose_name = "Texto & Artigo"
        verbose_name_plural = "Textos & Artigos"

    indice = TreeForeignKey(verbose_name="Índice", to=ArtigoIndice)
    nome = models.CharField(verbose_name="Título", max_length=150)
    conteudo = models.TextField(verbose_name="Conteúdo")
    autor = models.CharField(
        verbose_name="Autor", max_length=150, blank=True, null=True
    )
    data = models.DateField(
        verbose_name="Data cadastro", default=django.utils.timezone.now
    )

    slug = models.SlugField(max_length=150, editable=False)

    def __unicode__(self):
        return self.nome


@python_2_unicode_compatible
class WhatsAppGroup(models.Model):
    curso = models.OneToOneField(
        verbose_name="Curso", to="curso.Curso", on_delete=models.CASCADE
    )
    titulo = models.CharField(verbose_name="Título", max_length=150)
    descricao = models.TextField(verbose_name="Descrição")
    link = models.URLField(verbose_name="Link do Grupo")
    ativo = models.BooleanField(verbose_name="Ativo")

    class Meta:
        verbose_name = "Grupo do WhatsApp"
        verbose_name_plural = "Grupos do WhatsApp"

    def __str__(self):
        return self.titulo


@python_2_unicode_compatible
class WhatsAppInscritos(models.Model):
    whatsapp_group = models.ForeignKey(
        verbose_name="Grupo",
        to=WhatsAppGroup,
        on_delete=models.PROTECT,
        related_name="inscritos",
    )
    nome = models.CharField(verbose_name="Nome", max_length=150)
    email = models.EmailField(verbose_name="E-Mail")
    celular = models.EmailField(verbose_name="Celular", max_length=11)

    class Meta:
        verbose_name = "Inscrito"
        verbose_name_plural = "Inscritos"
        unique_together = ("celular", "whatsapp_group")

    def __str__(self):
        return self.nome


models.signals.post_save.connect(create_slug, sender=Artigo)
models.signals.post_save.connect(create_slug, sender=Institucional)
models.signals.post_save.connect(create_slug, sender=Noticia)
