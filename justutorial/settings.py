# -*- coding: utf-8 -*-

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import pusher
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

from justutorial.conf.suit import *

# import rollbar
# sentry_sdk.init(
#     dsn="https://8959ed956672451c99041dc7c611a8df@sentry.io/1873270",
#     integrations=[DjangoIntegration()],
#     environment="staging",
#     send_default_pii=True
# )

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '83^b0t#e+*+a-^cw(x99-ewj2q)@x$nmzen(@xd&&pm2=1cpu$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# ROLLBAR = {
#     'access_token': 'be5b7a3cf8c144f496ab017daf5fe625',
#     'environment': 'development' if DEBUG else 'production',
#     'root': BASE_DIR,
# }
# rollbar.init(**ROLLBAR)
ALLOWED_HOSTS = [
    'usloft6524.startdedicated.de',
    'usloft6524.startdedicated.com',
    '.justutor.com.br',
    '148.72.177.227',
    '18.205.156.171',
    '54.210.210.18'
]
if DEBUG:
    ALLOWED_HOSTS.append('*')

SITE_ID = 1
ADMINS = [
       ('Christian', 'christian.douglas.alcantara@gmail.com'),
    #    ('Justutor', 'justutorbackup@gmail.com')
]
# ----------------------------------------------------------------------------------------------------------------------
# APPLICATION DEFINITION
# ----------------------------------------------------------------------------------------------------------------------
INSTALLED_APPS = (
    'compressor',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    # Requirements
    'widget_tweaks',
    'threadedcomments',
    'django_comments',
    'corsheaders',
    # 'cacheops',
    'django_extensions',
    'suit_ckeditor',
    'ckeditor',
    'redactor',
    'dajaxice',
    'dajax',
    'nested_admin',
    # 'imperavi',
    'sorl.thumbnail',
    'filebrowser',
    'smart_selects',
    'django_select2',
    'mptt',
    # 'social_auth',
    'carton',
    # Modules
    'apps.aluno',
    'apps.enunciado',
    'apps.website',
    'apps.curso',
    'apps.cupom',
    'apps.pagseguro',
    'apps.professor',
    'apps.corretor',
    'apps.pregao',
    'apps.quizz',
    'apps.autor',
    'apps.formulario_correcao',
    'apps.formulario_auto_correcao',
    'apps.checkout',
    'apps.financeiro',
    # 'debug_toolbar',
    # 'redis_cache',
    # 'cacheops'
)

COMMENTS_APP = 'threadedcomments'
MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware'

)
HTML_MINIFY = False
KEEP_COMMENTS_ON_MINIFYING = True

ROOT_URLCONF = 'justutorial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'justutorial', 'templates'),
            os.path.join(BASE_DIR, 'apps', 'curso', 'templates'),
            os.path.join(BASE_DIR, 'apps', 'enunciado', 'templates'),
            os.path.join(BASE_DIR, 'apps', 'website', 'templates'),
            os.path.join(BASE_DIR, 'apps', 'checkout', 'templates'),
        ],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
                'django.core.context_processors.static',
                'django.core.context_processors.media',
                # apps
                'apps.website.processor.website',
                'apps.curso.processor.proc_curso',
                'apps.enunciado.processor.proc_enunciado',
                'apps.aluno.processor.proc_aluno',
                # auth login
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ]
        },
    },
]

WSGI_APPLICATION = 'justutorial.wsgi.application'

# ----------------------------------------------------------------------------------------------------------------------
# DATABASE
# ----------------------------------------------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'justutorsw',
        'USER': 'justutorsw',
        'PASSWORD': '765b85a6ca4dca39ef3a2068',
        'PORT': 5432
    }
}

# ----------------------------------------------------------------------------------------------------------------------
# INTERNATIONALIZATION
# ----------------------------------------------------------------------------------------------------------------------
LANGUAGE_CODE = 'pt-br'
# Languages we provide translations for, out of the box.
LANGUAGES = (
    ('pt-br', 'Brazilian Portuguese'),
)
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = False
# ----------------------------------------------------------------------------------------------------------------------
# STATIC FILES (CSS, JAVASCRIPT, IMAGES)
# ----------------------------------------------------------------------------------------------------------------------
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'justutorial', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'justutorial', 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
    'compressor.finders.CompressorFinder',
)
# ----------------------------------------------------------------------------------------------------------------------
# SUIT CONFIG
# ----------------------------------------------------------------------------------------------------------------------
FILEBROWSER_SUIT_TEMPLATE = True
# ----------------------------------------------------------------------------------------------------------------------
SUIT_CONFIG = {
    'ADMIN_NAME': 'JusTutorial',
    'HEADER_DATE_FORMAT': 'D. j \d\e F \d\e Y',
    'HEADER_TIME_FORMAT': 'H:i',
    'MENU': [
        'sites',
        'socialaccount',
        'django_comments',
        'threadedcomments',
        {
            'label': u'Segurança',
            'icon': 'icon-lock',
            'models': (
                'auth.user',
                'auth.group'
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': u'Textos & Artigos',
            'icon': 'icon-pencil',
            'models': (
                'website.artigoindice',
                'website.artigo'
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': u'Financeiro',
            'icon': 'icon-book',
            'models': (
                'financeiro.ConfiguracaoPacote',
                'financeiro.credito',
                'financeiro.CreditoResgate'
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': u'Livraria',
            'icon': 'icon-book',
            'models': (
                'curso.autor',
                'curso.colecao',
                'curso.livro'
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': u'Questões Objetivas',
            'icon': 'icon-question-sign',
            'models': (
                'autor.autor',
                'autor.assuntogeral',
                'autor.assuntoespecifico',
                'autor.questao',
                'autor.questaoc',
                'autor.questaom'
            )
        },
        {
            'label': u'Simulado',
            'icon': 'icon-question-sign',
            'models': (
                'autor.simulado',
                'autor.gruposimulado',
                'autor.QuestaoGrupo',
                'autor.questionarioaluno',
                'autor.RespostaQuestionarioAluno',
                'autor.DisciplinaConcurso',
                'autor.DisciplinaGrupo',
                'autor.QuestaoEscolha',
                'autor.Resultado',
                'autor.ResultadoResposta'
            )
        },
        {
            'label': u'Website',
            'icon': 'icon-globe',
            'models': (
                'website.configuracao',
                'website.institucional',
                'website.banner',
                'website.videojustutor',
                'website.noticia',
                'website.anuncio'
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': 'PagSeguro',
            'icon': 'icon-shopping-cart',
            'models': (
                'pagseguro.checkout',
                'pagseguro.transaction',
                'curso.checkoutitens'
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': u'Área do Aluno',
            'icon': 'icon-user',
            'models': (
                'aluno.aluno',
                'enunciado.resposta',
                'enunciado.respostacomentario',
                'curso.sentencaavulsaaluno',
                'curso.sentencaoabavulsaaluno',
                'curso.certificado',
                'aluno.mensagem',
                'professor.mensagem'
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': u'Cursos',
            'icon': 'icon-certificate',
            'models': (
                'curso.categoria',
                'curso.curso',
                'curso.simulado',
                'curso.combo',
                'curso.CursoCredito',
                'curso.comboaluno',
                'curso.atividade',
                'curso.tarefaatividade',
                'curso.modulo',
                'curso.destaque',
                'curso.serie',
                'curso.cursogratis',
                'curso.sentencaavulsa',
                'curso.sentencaoab',
                'curso.livro'
            ), 'permissions': 'auth.add_permission'
        },
        {
            'label': u'Formularios de correção',
            'icon': 'icon-certificate',
            'models': (
                'formulario_correcao.formulario',
                'formulario_correcao.tabela',
                'formulario_correcao.nota',
                'formulario_correcao.tabelaaluno',
                'formulario_correcao.tabelacorrecaoaluno'
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': u'Formularios de auto correção',
            'icon': 'icon-certificate',
            'models': (
                'formulario_auto_correcao.formulario',
                'formulario_auto_correcao.tabela',
                'formulario_auto_correcao.nota',
                'formulario_auto_correcao.tabelaaluno',
                'formulario_auto_correcao.tabelacorrecaoaluno',
                'formulario_auto_correcao.respostaaluno'
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': u'Questionário',
            'icon': 'icon-list-alt',
            'app': 'quizz',
            'permissions': 'auth.add_permission'
        },
        {
            'label': u'Promoções',
            'icon': 'icon-certificate',
            'models': (
                'enunciado.rankingpremiado',
                'cupom.cupom',
                'curso.liberarcompracurso'
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': 'Gerar Cupons',
            'icon': 'icon-question-sign',
            'url': '/admin/gerarcupons',
            'permissions': 'auth.add_permission'
        },
        {
            'label': u'Cadastro',
            'icon': 'icon-edit',
            'models': (
                'enunciado.esferageral',
                'enunciado.esferaespecifica',
                'enunciado.cargo',
                'enunciado.areaprofissional',
                'enunciado.orgaoentidade',
                'enunciado.tipoprocedimento',
                'enunciado.tipopecapratica',
                'enunciado.tipopecasentenca',
                'curso.tiposentencaavulsa',
                'enunciado.organizador',
                'enunciado.localidade',
                'enunciado.disciplina',
                'enunciado.concurso',
                'enunciado.tag',
                'professor.professor',
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': 'Enunciado',
            'icon': 'icon-list-alt',
            'models': (
                'enunciado.enunciadoproposta',
                'enunciado.enunciadopropostasentenca',
                'enunciado.enunciadopropostapratica',
                'enunciado.enunciadopropostadiscursiva'
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': 'Roteiros de Estudo',
            'icon': 'icon-list-alt',
            'models': (
                'enunciado.roteiroestudo',
                'enunciado.roteiroestudoitem',
                'enunciado.roteiroestudosubitem'
            ),
            'permissions': 'auth.add_permission'
        },
        {
            'label': 'Arquivos',
            'icon': 'icon-files-o',
            'app': 'filer',
            'permissions': 'auth.add_permission'
        }
    ]
}
# LOG
# ----------------------------------------------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'justutorial.log'),
            'formatter': 'verbose'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
# ----------------------------------------------------------------------------------------------------------------------
# REDACTOR
# ----------------------------------------------------------------------------------------------------------------------
REDACTOR_OPTIONS = {'lang': 'pt_br'}
REDACTOR_UPLOAD = 'uploads/'

# ----------------------------------------------------------------------------------------------------------------------
# PAGSEGURO
# ----------------------------------------------------------------------------------------------------------------------
PAGSEGURO_LOG_IN_MODEL = True
PAGSEGURO_SANDBOX = False
PAGSEGURO_FAKE = False
if PAGSEGURO_FAKE:
    PAGSEGURO_TOKEN = '209ac20b-7221-4c2c-9202-afd8a3b1f07807827b734b2998d9c3b629d621c29abd4503-617f-4a5f-83cc-71b7dfb89fb2'
    PAGSEGURO_EMAIL = 'christian.douglas.alcantara@gmail.com'
else:
    PAGSEGURO_TOKEN = '94CFB2E289C744CCAD0AD2A6383A7B81' if PAGSEGURO_SANDBOX else '94F5361CE60E41B7BCEE5AE51C730596'
    PAGSEGURO_EMAIL = 'cristiane@justutor.com.br'
PAGSEGURO_DATA = {
    'email': PAGSEGURO_EMAIL,
    'token': PAGSEGURO_TOKEN
}

CART_PRODUCT_MODEL = 'apps.curso.models.Curso'

NOME_SITE = u'JusTutor'
PROTOCOL = 'http:'
DOMINIO = 'justutor.com.br'
SITEADD = '{0}//{1}'.format(PROTOCOL, DOMINIO)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django_ses.SESBackend'
# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

# AWS_ACCESS_KEY_ID='AKIAJSR3ICBF5K56LSAQ'
# AWS_SECRET_ACCESS_KEY='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'
# SES_REGION_NAME='us-west-2'

AWS_ACCESS_KEY_ID = 'AKIAWYJNKRXAPMX47YH7'
AWS_SECRET_ACCESS_KEY = 'BEEyNaAO5QLMx/LEFL5zEOoTbXQcYfPfp9rIriCQt5MX'
SES_REGION_NAME = 'us-east-1'

DEFAULT_FROM_EMAIL = u'{0} <naoresponder@{1}>'.format(NOME_SITE, DOMINIO)
# EMAIL_HOST = 'smtp.zoho.com'
# EMAIL_HOST_USER = 'naoresponder@justutor.com.br'
# EMAIL_HOST_PASSWORD = 'NAT100nvoisaoc!'
# EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = 'AKIAWYJNKRXAMVJ6K3Z7'
EMAIL_HOST_PASSWORD = 'BMKuOIgkk29tXoWa4daATNo7K6W7VVk7V/ICVF6yAQn8'
EMAIL_SUBJECT_PREFIX = NOME_SITE
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True


# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'mail@smartweb.com.br'
# EMAIL_HOST_PASSWORD = 'Swko153575'
# EMAIL_SUBJECT_PREFIX = u'[ %s ]' % NOME_SITE
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# ----------------------------------------------------------------------------------------------------------------------
# PAGSEGURO
# ----------------------------------------------------------------------------------------------------------------------
push = pusher.Pusher(
    app_id='158278',
    key='c0d5a64b812bb1b35d3a',
    secret='fbf7f61eea7f7a891352',
    ssl=True,
    port=443
)

# push.trigger('painel_channel', 'notificar_aluno', {
#                 'message': 'notificacao.get_mensagem.msg_html',
#                 'aluno_id': 5
#             })

# NEWSLETTER
SMARTWEB_MMKT_LIST_ID = "oPeEzyP03txLXAlKIzoLFQ"
SMARTWEB_MMKT_URL = 'http://justutorial.com.br/'
SENDY_API_KEY = 'Stv8mmGM9xFhU7x62cGI'

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         },
#         "KEY_PREFIX": "example"
#     }
# }
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 20,  # Default: 300 segundos,
        'KEY_PREFIX': 'djcache',
    }
}

# ==========================
# INSTALANDO O FILER
# ==========================
INSTALLED_APPS += (
    'easy_thumbnails',
    'filer',
)
FILER_CANONICAL_URL = 'arquivos/'
FILER_ENABLE_PERMISSIONS = True

INSTALLED_APPS += (
    'robots',
)
ROBOTS_USE_SITEMAP = False

# ----------------------------------------------------------------------------------------------------------------------
# AUTHENTICATION
# ----------------------------------------------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
LOGIN_REDIRECT_URL = '/aluno/painel/'
LOGOUT_REDIRECT_URL = '/'
# ACCOUNT_ADAPTER = 'apps.aluno.adapter.AlunoAdapter'
# SOCIALACCOUNT_FORMS = {
#     'signup': 'apps.aluno.forms.AlunoForm'
# }
ACCOUNT_SIGNUP_FORM_CLASS = 'apps.aluno.forms.SignupForm'
INSTALLED_APPS += (
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook'
)
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email'],
        # 'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
        ],
        'EXCHANGE_TOKEN': True,
        # 'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.12',
    }
}
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
DEFAULT_FILE_STORAGE = 'apps.website.storage.ASCIIFileSystemStorage'
FILE_UPLOAD_PERMISSIONS = 0o777
COMPRESS_ENABLED = False
CORS_ORIGIN_ALLOW_ALL = False

CUSTOM_TOOLBAR = [
    {
        "name": "document",
        "items": [
            "Styles", "Format", "Bold", "Italic", "Underline", "Strike", "-",
            "TextColor", "BGColor", "-",
            "JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock",
        ],
    },
    {
        "name": "widgets",
        "items": [
            "Undo", "Redo", "-",
            "NumberedList", "BulletedList", "-",
            "Outdent", "Indent", "-",
            "Link", "Unlink", "-",
            "Image", "Table", "HorizontalRule", "Smiley", "SpecialChar", "-",
            "Blockquote", "-",
            "ShowBlocks", "Maximize",
        ],
    },
]

CKEDITOR_CONFIGS = {
    'default': {
        'width': '100%',
    },
    "custom-toolbar": {
        'width': '100%',
        "skin": "moono-lisa",
        "toolbar": CUSTOM_TOOLBAR,
        "toolbarGroups": None,
        "removePlugins": ",".join(["image"]),
    },
}
