"""justutor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

import settings

dajaxice_autodiscover()


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    url(r'^sentry-debug/$', trigger_error),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/gerarcupons/$', 'apps.cupom.views.gerarcupons'),
    url(r'^admin/import_formulario_correcao/$', 'apps.formulario_correcao.views.import_formulario_correcao'),
    url(r'^admin/gerarnotas/$', 'apps.formulario_correcao.views.gerarnotas'),
    url(r'^robots\.txt$', include('robots.urls')),
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'', include('apps.website.urls', namespace='website')),
    # APPS
    # url(r'^frontend/', include('apps.frontend.urls', namespace='frontend')),
    url(r'^aluno/', include('apps.aluno.urls', namespace='aluno')),
    url(r'^autocorrecao/', include('apps.formulario_auto_correcao.urls', namespace='autocorrecao')),
    url(r'^aluno/quizz/', include('apps.quizz.urls', namespace='quizz')),
    url(r'^professor/', include('apps.professor.urls', namespace='professor')),
    url(r'^corretor/', include('apps.corretor.urls', namespace='corretor')),
    url(r'^curso/', include('apps.curso.urls', namespace='curso')),
    url(r'^enunciado/', include('apps.enunciado.urls', namespace='enunciado')),
    url(r'^financeiro/', include('apps.financeiro.urls', namespace='financeiro')),
    url(r'^formulario_correcao/', include('apps.formulario_correcao.urls', namespace='formulario_correcao')),
    # PAGSEGURO
    url(r'^nfse/', include('apps.nfse.urls', namespace='nfse')),
    url(r'^pagseguro/', include('apps.pagseguro.urls', namespace='pagseguro')),
    url(r'^carrinho/$', 'apps.curso.views.carrinho', name='carrinho'),
    url(r'^checkout/', include('apps.checkout.urls', namespace='checkout')),
    # EDITOR
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^redactor/', include('redactor.urls')),
    # LOGIN
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^accounts/', include('allauth.urls')),
    url('^accounts/', include('registration.backends.simple.urls')),
    # SOCIAL AUTH
    # url(r'', include('social_auth.urls')),
    # BLOCG
    url(r'^comments/', include('django_comments.urls')),
    # FILER
    url(r'^filer/', include('filer.urls')),
    url(r'^', include('filer.server.urls')),
    url(r'^_nested_admin/', include('nested_admin.urls')),
]
# handler500 = handler500

if settings.DEBUG:
    # import debug_toolbar
    urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += patterns(
        '',
        # url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,
                                                                   'show_indexes': True})
    )
