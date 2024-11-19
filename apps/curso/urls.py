# -*- coding: utf-8 -*-
# Autor: christian
from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    'apps.curso.views',
    url(r'^categoria/(?P<slug>[-\w]+)/$', views.categoria, name='categoria'),
    url(r'^curso/(?P<slug>[-\w]+)/$', views.curso, name='curso'),
    url(r'^pre-inscricao/$', views.pre_inscricao, name='pre-inscricao'),
    url(r'^montar-pacote/$', views.montar_pacote, name='montar-pacote'),
    url(r'^relatorio/$', views.relatorio, name='relatorio'),
    url(r'^sentenca/(?P<slug>[-\w]+)/$', views.curso_sentenca, name='curso-sentenca'),  # Curso de sentença
    url(r'^simulado/(?P<slug>[-\w]+)/$', views.curso_sentenca, name='curso-simulado'),  # Curso de sentença
    url(r'^simulados/$', views.CursoSimuladoListView.as_view(), name='simulado-list'),  # Curso de sentença
    url(r'^oab/(?P<slug>[-\w]+)/$', views.curso_sentenca, name='curso-oab'),  # OAB 2 fase
    url(r'^serie/(?P<slug>[-\w]+)/$', views.serie, name='serie'),
    url(r'^curso-gratis/(?P<slug>[-\w]+)/$', views.curso_gratis, name='curso-gratis'),
    # url(r'', 'cursos', name='cursos'),
    url(r'^carrinho/$', views.carrinho, name='carrinho'),
    url(r'^carrinho-pagamento/$', views.carrinho_pagamento, name='carrinho-pagamento'),
    url(r'^get-payment-methods/$', views.get_payment_methods, name='get-payment-methods'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^trans/$', 'trans', name='trans'),
    url(r'^get-tarefa-json/$', views.get_tarefa_json, name='get-tarefa-json'),
    url(r'^get-alunos-curso-json/$', views.get_alunos_curso_json, name='get-alunos-curso-json'),
    url(r'^get-amostra-json/$', views.get_amostra_json, name='get-amostra-json'),
    url(r'^post-resposta/(?P<pk>[0-9]+)/$', views.post_resposta, name='post-resposta'),

    url(r'^post-correcao/(?P<pk>[0-9]+)/$', views.post_correcao, name='post-correcao'),

    url(r'^atividade/responder/(?P<pk>[0-9]+)/$', views.atividade_responder, name='atividade-responder'),

    url(r'^atividade/imprimir/(?P<pk>[0-9]+)/$', views.imprimir, name='atividade-imprimir'),

    url(r'^baixar/correcao/(?P<pk>[0-9]+)/$', views.baixar_correcao, name='baixar-correcao'),

    url(r'^sentenca/responder/(?P<pk>[0-9]+)/$', views.sentenca_responder, name='sentenca-responder'),
    url(r'^sentenca/imprimir/(?P<pk>[0-9]+)/$', views.sentenca_imprimir, name='sentenca-imprimir'),
    url(r'^post-sentenca/(?P<pk>[0-9]+)/$', views.post_sentenca, name='post-sentenca'),

    url(r'^pecas-oab/responder/(?P<pk>[0-9]+)/$', views.sentenca_oab_responder, name='sentenca-oab-responder'),
    url(r'^post-sentenca-oab/(?P<pk>[0-9]+)/$', views.post_sentenca_oab, name='post-sentenca-oarab'),

    url(r'^download/tarefa/(?P<pk>[0-9]+)/$', views.download_tarefa, name='download-tarefa'),
    url(r'^enviar/correcao/$', views.enviar_correcao, name='enviar-correcao'),
    url(r'^enviar/resposta/padrao/$', views.enviar_resposta_padrao, name='enviar-resposta-padrao'),
    url(r'^ajax-search-simulado$', views.ajax_search_simulado, name='ajax-search-simulado'),
    url(r'^ajax-gerar-cortesia', views.ajax_gerar_cortesia, name='ajax-gerar-cortesia'),
    url(r'^ajax-validar-cortesia', views.ajax_validar_cortesia, name='ajax-validar-cortesia'),
    url(r'^ajax-desistir-tarefa', views.ajax_desistir_tarefa, name='ajax-desistir-tarefa'),
    url(r"^vdo_modal/(?P<vdo_id>[:\w]+)/$", views.vdo_view, name="vdo_view"),

)
