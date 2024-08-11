# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import environ
import pusher

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = [".justutor.com.br", "69.164.212.28"]
if DEBUG:
    ALLOWED_HOSTS.append("localhost")

SITE_ID = 1
ADMINS = [
    ("Christian", "christian.douglas.alcantara@gmail.com"),
    ("Justutor", "desenvolvimento@justutor.com.br"),
]
# ----------------------------------------------------------------------------------------------------------------------
# APPLICATION DEFINITION
# ----------------------------------------------------------------------------------------------------------------------
INSTALLED_APPS = (
    "compressor",
    "suit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    # Requirements
    "widget_tweaks",
    "threadedcomments",
    "django_comments",
    "corsheaders",
    # 'cacheops',
    "django_extensions",
    "suit_ckeditor",
    "ckeditor",
    "redactor",
    "dajaxice",
    "dajax",
    "nested_admin",
    # 'imperavi',
    "sorl.thumbnail",
    "filebrowser",
    "smart_selects",
    "django_select2",
    "mptt",
    # 'social_auth',
    "carton",
    # Modules
    "apps.aluno",
    "apps.enunciado",
    "apps.website",
    "apps.curso",
    "apps.cupom",
    "apps.pagseguro",
    "apps.professor",
    "apps.corretor",
    "apps.pregao",
    "apps.quizz",
    "apps.autor",
    "apps.formulario_correcao",
    "apps.formulario_auto_correcao",
    "apps.checkout",
    "apps.financeiro",
    "apps.nfse",
    "apps.pix",
    # 'debug_toolbar',
    # 'redis_cache',
    # 'cacheops'
)

COMMENTS_APP = "threadedcomments"
MIDDLEWARE_CLASSES = (
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # 'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware'
)
HTML_MINIFY = False
KEEP_COMMENTS_ON_MINIFYING = True

ROOT_URLCONF = "justutorial.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "justutorial", "templates"),
            os.path.join(BASE_DIR, "apps", "curso", "templates"),
            os.path.join(BASE_DIR, "apps", "enunciado", "templates"),
            os.path.join(BASE_DIR, "apps", "website", "templates"),
            os.path.join(BASE_DIR, "apps", "checkout", "templates"),
        ],
        # 'APP_DIRS': True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.core.context_processors.request",
                "django.core.context_processors.static",
                "django.core.context_processors.media",
                # apps
                "apps.website.processor.website",
                "apps.curso.processor.proc_curso",
                "apps.enunciado.processor.proc_enunciado",
                "apps.aluno.processor.proc_aluno",
                # auth login
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                "django.template.loaders.eggs.Loader",
            ],
        },
    },
]

WSGI_APPLICATION = "justutorial.wsgi.application"

# ----------------------------------------------------------------------------------------------------------------------
# DATABASE
# ----------------------------------------------------------------------------------------------------------------------
DATABASE_URL = env.db("DATABASE_URL")
DATABASES = {"default": DATABASE_URL}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# ----------------------------------------------------------------------------------------------------------------------
# INTERNATIONALIZATION
# ----------------------------------------------------------------------------------------------------------------------
LANGUAGE_CODE = "pt-br"
# Languages we provide translations for, out of the box.
LANGUAGES = (("pt-br", "Brazilian Portuguese"),)
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_L10N = True
USE_TZ = False
# ----------------------------------------------------------------------------------------------------------------------
# STATIC FILES (CSS, JAVASCRIPT, IMAGES)
# ----------------------------------------------------------------------------------------------------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "justutorial", "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "justutorial", "media")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "dajaxice.finders.DajaxiceFinder",
    "compressor.finders.CompressorFinder",
)
# ----------------------------------------------------------------------------------------------------------------------
# SUIT CONFIG
# ----------------------------------------------------------------------------------------------------------------------
FILEBROWSER_SUIT_TEMPLATE = True
# ----------------------------------------------------------------------------------------------------------------------
SUIT_CONFIG = {
    "ADMIN_NAME": "JusTutorial",
    "HEADER_DATE_FORMAT": "D. j \d\e F \d\e Y",
    "HEADER_TIME_FORMAT": "H:i",
    "MENU": [
        "sites",
        "socialaccount",
        "django_comments",
        "threadedcomments",
        {
            "label": "Segurança",
            "icon": "icon-lock",
            "models": ("auth.user", "auth.group"),
            "permissions": "auth.add_permission",
        },
        {
            "label": "WhatsApp",
            "icon": "icon-star",
            "models": ("website.WhatsAppGroup", "website.WhatsAppInscritos"),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Textos & Artigos",
            "icon": "icon-pencil",
            "models": ("website.artigoindice", "website.artigo"),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Financeiro",
            "icon": "icon-book",
            "models": (
                "financeiro.ConfiguracaoPacote",
                "financeiro.credito",
                "financeiro.CreditoResgate",
            ),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Livraria",
            "icon": "icon-book",
            "models": ("curso.autor", "curso.colecao", "curso.livro"),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Questões Objetivas",
            "icon": "icon-question-sign",
            "models": (
                "autor.autor",
                "autor.assuntogeral",
                "autor.assuntoespecifico",
                "autor.questao",
                "autor.questaoc",
                "autor.questaom",
            ),
        },
        {
            "label": "Simulado",
            "icon": "icon-question-sign",
            "models": (
                "autor.simulado",
                "autor.gruposimulado",
                "autor.QuestaoGrupo",
                "autor.questionarioaluno",
                "autor.RespostaQuestionarioAluno",
                "autor.DisciplinaConcurso",
                "autor.DisciplinaGrupo",
                "autor.QuestaoEscolha",
                "autor.Resultado",
                "autor.ResultadoResposta",
            ),
        },
        {
            "label": "Website",
            "icon": "icon-globe",
            "models": (
                "website.configuracao",
                "website.institucional",
                "website.banner",
                "website.bannerfooter",
                "website.videojustutor",
                "website.noticia",
                "website.anuncio",
                "website.gptmmodels",
            ),
            "permissions": "auth.add_permission",
        },
        {
            "label": "PagSeguro",
            "icon": "icon-shopping-cart",
            "models": (
                "pagseguro.checkout",
                "pagseguro.transaction",
                "curso.checkoutitens",
                "pix.cobranca",
            ),
            "permissions": "auth.add_permission",
        },
        {
            "label": "NFSe",
            "icon": "icon-shopping-cart",
            "models": ("nfse.NSFe",),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Área do Aluno",
            "icon": "icon-user",
            "models": (
                "aluno.aluno",
                "enunciado.resposta",
                "enunciado.respostacomentario",
                "curso.sentencaavulsaaluno",
                "curso.sentencaoabavulsaaluno",
                "curso.certificado",
                "aluno.mensagem",
                "professor.mensagem",
            ),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Cursos",
            "icon": "icon-certificate",
            "models": (
                "curso.categoria",
                "curso.curso",
                "curso.simulado",
                "curso.combo",
                "curso.CursoCredito",
                "curso.comboaluno",
                "curso.atividade",
                "curso.tarefaatividade",
                "curso.modulo",
                "curso.destaque",
                "curso.serie",
                "curso.cursogratis",
                "curso.sentencaavulsa",
                "curso.sentencaoab",
                "curso.livro",
            ),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Formularios de correção",
            "icon": "icon-certificate",
            "models": (
                "formulario_correcao.formulario",
                "formulario_correcao.tabela",
                "formulario_correcao.nota",
                "formulario_correcao.tabelaaluno",
                "formulario_correcao.tabelacorrecaoaluno",
            ),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Formularios de auto correção",
            "icon": "icon-certificate",
            "models": (
                "formulario_auto_correcao.formulario",
                "formulario_auto_correcao.tabela",
                "formulario_auto_correcao.nota",
                "formulario_auto_correcao.tabelaaluno",
                "formulario_auto_correcao.tabelacorrecaoaluno",
                "formulario_auto_correcao.respostaaluno",
            ),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Questionário",
            "icon": "icon-list-alt",
            "app": "quizz",
            "permissions": "auth.add_permission",
        },
        {
            "label": "Promoções",
            "icon": "icon-certificate",
            "models": (
                "enunciado.rankingpremiado",
                "cupom.cupom",
                "curso.liberarcompracurso",
                "curso.cortesia",
            ),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Gerar Cupons",
            "icon": "icon-question-sign",
            "url": "/admin/gerarcupons",
            "permissions": "auth.add_permission",
        },
        {
            "label": "Importar Notas",
            "icon": "icon-question-sign",
            "url": "/admin/gerarnotas",
            "permissions": "auth.add_permission",
        },
        {
            "label": "Importar Formulário Correção",
            "icon": "icon-question-sign",
            "url": "/admin/import_formulario_correcao",
            "permissions": "auth.add_permission",
        },
        {
            "label": "Cadastro",
            "icon": "icon-edit",
            "models": (
                "enunciado.esferageral",
                "enunciado.esferaespecifica",
                "enunciado.cargo",
                "enunciado.areaprofissional",
                "enunciado.orgaoentidade",
                "enunciado.tipoprocedimento",
                "enunciado.tipopecapratica",
                "enunciado.tipopecasentenca",
                "curso.tiposentencaavulsa",
                "enunciado.organizador",
                "enunciado.localidade",
                "enunciado.disciplina",
                "enunciado.concurso",
                "enunciado.tag",
                "professor.professor",
            ),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Enunciado",
            "icon": "icon-list-alt",
            "models": (
                "enunciado.enunciadoproposta",
                "enunciado.enunciadopropostasentenca",
                "enunciado.enunciadopropostapratica",
                "enunciado.enunciadopropostadiscursiva",
            ),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Roteiros de Estudo",
            "icon": "icon-list-alt",
            "models": (
                "enunciado.roteiroestudo",
                "enunciado.roteiroestudoitem",
                "enunciado.roteiroestudosubitem",
            ),
            "permissions": "auth.add_permission",
        },
        {
            "label": "Arquivos",
            "icon": "icon-files-o",
            "app": "filer",
            "permissions": "auth.add_permission",
        },
    ],
}
# LOG
# ----------------------------------------------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "justutorial.log"),
            "formatter": "verbose",
        },
        "file_nfse": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "nfse.log"),
            "formatter": "verbose",
        },
        "file_pags": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "pagseguro.log"),
            "formatter": "verbose",
        },
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "nfse": {
            "handlers": ["console", "file_nfse"],
            "level": "DEBUG",
            "propagate": True,
        },
        "pags": {
            "handlers": ["console", "file_pags"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
# ----------------------------------------------------------------------------------------------------------------------
# REDACTOR
# ----------------------------------------------------------------------------------------------------------------------
REDACTOR_OPTIONS = {"lang": "pt_br"}
REDACTOR_UPLOAD = "uploads/"

# ----------------------------------------------------------------------------------------------------------------------
# PAGSEGURO
# ----------------------------------------------------------------------------------------------------------------------
PAGSEGURO_LOG_IN_MODEL = True
PAGSEGURO_SANDBOX = env.bool("PAGSEGURO_SANDBOX")
PAGSEGURO_TOKEN_SANDBOX = env("PAGSEGURO_TOKEN_SANDBOX")
PAGSEGURO_TOKEN = env("PAGSEGURO_TOKEN")
if PAGSEGURO_SANDBOX:
    PAGSEGURO_TOKEN = PAGSEGURO_TOKEN_SANDBOX

PAGSEGURO_EMAIL = env("PAGSEGURO_EMAIL")
PAGSEGURO_DATA = {"email": PAGSEGURO_EMAIL, "token": PAGSEGURO_TOKEN}

CART_PRODUCT_MODEL = "apps.curso.models.Curso"

NOME_SITE = "JusTutor"
PROTOCOL = "http:"
DOMINIO = "justutor.com.br"
SITEADD = "{0}//{1}".format(PROTOCOL, DOMINIO)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
SES_REGION_NAME = env("SES_REGION_NAME")

DEFAULT_FROM_EMAIL = "{0} <naoresponder@{1}>".format(NOME_SITE, DOMINIO)
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_SUBJECT_PREFIX = NOME_SITE
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# ----------------------------------------------------------------------------------------------------------------------
# PAGSEGURO
# ----------------------------------------------------------------------------------------------------------------------
push = pusher.Pusher(
    app_id="158278",
    key="c0d5a64b812bb1b35d3a",
    secret="fbf7f61eea7f7a891352",
    ssl=True,
    port=443,
)

# NEWSLETTER
SMARTWEB_MMKT_LIST_ID = "dVj0tVml87zSUbLY9tlDZg"
SMARTWEB_MMKT_URL = "http://justutorial.com.br/"
SENDY_API_KEY = "dImKU64JK1KSEvu1p83X"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
        "TIMEOUT": 20,  # Default: 300 segundos,
        "KEY_PREFIX": "djcache",
    }
}

# ==========================
# INSTALANDO O FILER
# ==========================
INSTALLED_APPS += (
    "easy_thumbnails",
    "filer",
)
FILER_CANONICAL_URL = "arquivos/"
FILER_ENABLE_PERMISSIONS = True

INSTALLED_APPS += ("robots",)
ROBOTS_USE_SITEMAP = False

# ----------------------------------------------------------------------------------------------------------------------
# AUTHENTICATION
# ----------------------------------------------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
LOGIN_REDIRECT_URL = "/aluno/painel/"
LOGOUT_REDIRECT_URL = "/"
# ACCOUNT_ADAPTER = 'apps.aluno.adapter.AlunoAdapter'
# SOCIALACCOUNT_FORMS = {
#     'signup': 'apps.aluno.forms.AlunoForm'
# }
ACCOUNT_SIGNUP_FORM_CLASS = "apps.aluno.forms.SignupForm"
INSTALLED_APPS += (
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
)
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    "facebook": {
        "METHOD": "oauth2",
        "SCOPE": ["email"],
        # 'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        "INIT_PARAMS": {"cookie": True},
        "FIELDS": [
            "id",
            "email",
            "name",
            "first_name",
            "last_name",
        ],
        "EXCHANGE_TOKEN": True,
        # 'LOCALE_FUNC': 'path.to.callable',
        "VERIFIED_EMAIL": False,
        "VERSION": "v2.12",
    }
}
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
DEFAULT_FILE_STORAGE = "apps.website.storage.ASCIIFileSystemStorage"
FILE_UPLOAD_PERMISSIONS = 0o777
COMPRESS_ENABLED = False
CORS_ORIGIN_ALLOW_ALL = False

CUSTOM_TOOLBAR = [
    {
        "name": "document",
        "items": [
            "Styles",
            "Format",
            "Bold",
            "Italic",
            "Underline",
            "Strike",
            "-",
            "TextColor",
            "BGColor",
            "-",
            "JustifyLeft",
            "JustifyCenter",
            "JustifyRight",
            "JustifyBlock",
        ],
    },
    {
        "name": "widgets",
        "items": [
            "Undo",
            "Redo",
            "-",
            "NumberedList",
            "BulletedList",
            "-",
            "Outdent",
            "Indent",
            "-",
            "Link",
            "Unlink",
            "-",
            "Image",
            "Table",
            "HorizontalRule",
            "Smiley",
            "SpecialChar",
            "-",
            "Blockquote",
            "-",
            "ShowBlocks",
            "Maximize",
        ],
    },
]

CKEDITOR_CONFIGS = {
    "default": {
        "width": "100%",
    },
    "custom-toolbar": {
        "width": "100%",
        "skin": "moono-lisa",
        "toolbar": CUSTOM_TOOLBAR,
        "toolbarGroups": None,
        "removePlugins": ",".join(["image"]),
    },
}
